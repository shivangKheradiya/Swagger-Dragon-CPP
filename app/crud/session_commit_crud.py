from uuid import UUID
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.core.enums import OperationType
from app.registry import (
    LIVE_TABLE_REGISTRY,
    HISTORY_TABLE_REGISTRY,
    SESSION_OVERLAY_REGISTRY,
)
from app.models.session_history import SessionHistoryBase


# ---------------------------------------------------------
# COMMIT SESSION
# ---------------------------------------------------------
def commit_session(
    db: Session,
    table_code: str,
    session_uuid: UUID,
):
    """
    Commit all staged changes for a session.

    DB RESPONSIBILITIES ONLY:
    1. Apply session overlay rows to live table
    2. Write history rows
    3. Clear session overlay
    4. Mark session inactive

    DOES NOT:
    - Create a new session
    - Assume tool / UI behavior
    """

    # -----------------------------------------------------
    # Resolve models
    # -----------------------------------------------------
    try:
        OverlayModel = SESSION_OVERLAY_REGISTRY[table_code]
        LiveModel = LIVE_TABLE_REGISTRY[table_code]
        HistoryModel = HISTORY_TABLE_REGISTRY[table_code]
    except KeyError:
        raise HTTPException(status_code=400, detail="Invalid table code")

    # -----------------------------------------------------
    # Validate session
    # -----------------------------------------------------
    session = (
        db.query(SessionHistoryBase)
        .filter(
            SessionHistoryBase.SessionUUID == session_uuid,
            SessionHistoryBase.IsActive == True,
        )
        .first()
    )

    if not session:
        raise HTTPException(
            status_code=400,
            detail="Session not found or already inactive",
        )

    # -----------------------------------------------------
    # Fetch overlay rows for this session
    # -----------------------------------------------------
    overlays = (
        db.query(OverlayModel)
        .filter(OverlayModel.SessionUUID == session_uuid)
        .all()
    )

    if not overlays:
        raise HTTPException(
            status_code=400,
            detail="No staged changes to commit",
        )

    # -----------------------------------------------------
    # Apply changes
    # -----------------------------------------------------
    for overlay in overlays:

        if overlay.OperationType == OperationType.CREATE:
            # INSERT new live attribute
            live = LiveModel(
                uuid=overlay.uuid,
                node_uuid=overlay.node_uuid,
                attribute_id=overlay.attribute_id,
                value=overlay.NewValue,
            )
            db.add(live)

        elif overlay.OperationType == OperationType.UPDATE:
            live = (
                db.query(LiveModel)
                .filter(LiveModel.uuid == overlay.uuid)
                .first()
            )
            if not live:
                raise HTTPException(
                    status_code=409,
                    detail=f"Live attribute not found: {overlay.uuid}",
                )
            live.value = overlay.NewValue

        elif overlay.OperationType == OperationType.DELETE:
            live = (
                db.query(LiveModel)
                .filter(LiveModel.uuid == overlay.uuid)
                .first()
            )
            if not live:
                raise HTTPException(
                    status_code=409,
                    detail=f"Live attribute not found: {overlay.uuid}",
                )
            db.delete(live)

        else:
            raise HTTPException(
                status_code=400,
                detail=f"Unknown OperationType: {overlay.OperationType}",
            )

        # -------------------------------------------------
        # Write history (direct copy, no transforms)
        # -------------------------------------------------
        history = HistoryModel(
            uuid=overlay.uuid,
            OperationType=overlay.OperationType,
            SessionUUID=session_uuid,
            OldValue=overlay.OldValue,
            NewValue=overlay.NewValue,
        )
        db.add(history)

    # -----------------------------------------------------
    # Clear overlay rows
    # -----------------------------------------------------
    (
        db.query(OverlayModel)
        .filter(OverlayModel.SessionUUID == session_uuid)
        .delete(synchronize_session=False)
    )

    # -----------------------------------------------------
    # Mark session inactive
    # -----------------------------------------------------
    session.IsActive = False

    db.commit()

    return {
        "status": "committed",
        "session_uuid": session_uuid,
    }