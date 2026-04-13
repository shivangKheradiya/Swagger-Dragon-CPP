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
    table_name: str,
    session_uuid: UUID,
):
    """
    Commit all staged changes for a session.

    Steps (atomic):
    1. Apply overlay changes to live table
    2. Write history rows
    3. Mark session inactive
    4. Delete overlay rows
    5. Create a new active session
    """

    try:
        OverlayModel = SESSION_OVERLAY_REGISTRY[table_name]
        LiveModel = LIVE_TABLE_REGISTRY[table_name]
        HistoryModel = HISTORY_TABLE_REGISTRY[table_name]
    except KeyError:
        raise HTTPException(status_code=400, detail="Invalid table name")

    # -----------------------------------------------------
    # Validate session existence and status
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
    # Fetch all overlay rows
    # -----------------------------------------------------
    overlays = (
        db.query(OverlayModel)
        .filter(OverlayModel.SessionUUID == session_uuid)
        .order_by(OverlayModel.ChangedAt)
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
            # CREATE live row
            live = LiveModel(
                node_uuid=overlay.NewValue["node_uuid"],
                attribute_id=overlay.NewValue["attribute_id"],
                value=overlay.NewValue["value"],
            )
            db.add(live)
            db.flush()  # get UUID

            # WRITE history
            db.add(
                HistoryModel(
                    TNAUUID=live.uuid,
                    OperationType=OperationType.CREATE,
                    OldValue=None,
                    NewValue=live.value,
                )
            )

        elif overlay.OperationType == OperationType.UPDATE:
            live = (
                db.query(LiveModel)
                .filter(LiveModel.uuid == overlay.TNAUUID)
                .first()
            )
            if not live:
                raise HTTPException(
                    status_code=409,
                    detail=f"Live record not found for UPDATE: {overlay.TNAUUID}",
                )

            old_value = live.value
            live.value = overlay.NewValue

            db.add(
                HistoryModel(
                    TNAUUID=live.uuid,
                    OperationType=OperationType.UPDATE,
                    OldValue=old_value,
                    NewValue=live.value,
                )
            )

        elif overlay.OperationType == OperationType.DELETE:
            live = (
                db.query(LiveModel)
                .filter(LiveModel.uuid == overlay.TNAUUID)
                .first()
            )
            if not live:
                raise HTTPException(
                    status_code=409,
                    detail=f"Live record not found for DELETE: {overlay.TNAUUID}",
                )

            db.add(
                HistoryModel(
                    TNAUUID=live.uuid,
                    OperationType=OperationType.DELETE,
                    OldValue=live.value,
                    NewValue=None,
                )
            )
            db.delete(live)

    # -----------------------------------------------------
    # Close session
    # -----------------------------------------------------
    session.IsActive = False

    # -----------------------------------------------------
    # Clear overlay rows
    # -----------------------------------------------------
    (
        db.query(OverlayModel)
        .filter(OverlayModel.SessionUUID == session_uuid)
        .delete(synchronize_session=False)
    )

    # -----------------------------------------------------
    # Create new active session
    # -----------------------------------------------------
    new_session = SessionHistoryBase(
        UserName=session.UserName,
        HostName=session.HostName,
        IsActive=True,
    )

    db.add(new_session)
    db.commit()

    return {
        "status": "committed",
        "old_session_uuid": session_uuid,
        "new_session_uuid": new_session.SessionUUID,
    }