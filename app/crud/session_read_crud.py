from uuid import UUID
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.registry import SESSION_OVERLAY_REGISTRY


# ---------------------------------------------------------
# READ ALL STAGED CHANGES FOR A SESSION
# ---------------------------------------------------------
def read_session_overlay(
    db: Session,
    table_code: str,
    session_uuid: UUID,
):
    """
    Return all staged changes for a session (overlay only).
    """
    try:
        OverlayModel = SESSION_OVERLAY_REGISTRY[table_code]
    except KeyError:
        raise HTTPException(status_code=400, detail="Invalid table code")

    return (
        db.query(OverlayModel)
        .filter(OverlayModel.SessionUUID == session_uuid)
        .all()
    )


# ---------------------------------------------------------
# READ ONE STAGED ATTRIBUTE
# ---------------------------------------------------------
def read_session_overlay_one(
    db: Session,
    table_code: str,
    session_uuid: UUID,
    attribute_uuid: UUID,
):
    """
    Return a single staged change for an attribute in a session.
    """
    try:
        OverlayModel = SESSION_OVERLAY_REGISTRY[table_code]
    except KeyError:
        raise HTTPException(status_code=400, detail="Invalid table code")

    obj = (
        db.query(OverlayModel)
        .filter(
            OverlayModel.SessionUUID == session_uuid,
            OverlayModel.uuid == attribute_uuid,
        )
        .first()
    )

    if not obj:
        raise HTTPException(status_code=404, detail="No staged change found")

    return obj