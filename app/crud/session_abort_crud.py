from uuid import UUID
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.registry import SESSION_OVERLAY_REGISTRY
from app.models.session_history import SessionHistoryBase


def abort_session(
    db: Session,
    session_uuid: UUID,
):
    """
    Abort a session.

    EFFECTS:
    - Deletes all session overlay rows
    - Marks session inactive
    - Does NOT touch live data
    - Does NOT write history
    """

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
    # Clear overlay rows (ALL domains)
    # -----------------------------------------------------
    for OverlayModel in SESSION_OVERLAY_REGISTRY.values():
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
        "status": "aborted",
        "session_uuid": session_uuid,
    }