import uuid
from uuid import UUID
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.core.enums import OperationType
from app.registry import SESSION_OVERLAY_REGISTRY, LIVE_TABLE_REGISTRY


# ---------------------------------------------------------
# CREATE (SESSION OVERLAY)
# ---------------------------------------------------------
def push_create(
    db: Session,
    table_code: str,
    payload,
):
    """
    Stage a CREATE operation in the session overlay.

    - Generates a new attribute UUID
    - Stores proposed state only
    """
    try:
        OverlayModel = SESSION_OVERLAY_REGISTRY[table_code]
    except KeyError:
        raise HTTPException(status_code=400, detail="Invalid table code")

    new_uuid = uuid.uuid4()

    overlay = OverlayModel(
        uuid=new_uuid,
        node_uuid=payload.node_uuid,
        attribute_id=payload.attribute_id,
        OperationType=OperationType.CREATE,
        SessionUUID=payload.session_uuid,
        OldValue=None,
        NewValue=payload.value,
    )

    db.add(overlay)
    db.commit()

    return {
        "status": "staged",
        "operation": "CREATE",
        "uuid": new_uuid,
        "session_uuid": payload.session_uuid,
    }


# ---------------------------------------------------------
# UPDATE (SESSION OVERLAY)
# ---------------------------------------------------------
def push_update(
    db: Session,
    table_code: str,
    attribute_uuid: UUID,
    payload,
):
    """
    Stage an UPDATE operation.

    - Overwrites existing overlay row if present
    - Or creates a new overlay row from live table
    """
    try:
        OverlayModel = SESSION_OVERLAY_REGISTRY[table_code]
        LiveModel = LIVE_TABLE_REGISTRY[table_code]
    except KeyError:
        raise HTTPException(status_code=400, detail="Invalid table code")

    # Fetch live attribute
    live = db.query(LiveModel).filter(LiveModel.uuid == attribute_uuid).first()
    if not live:
        raise HTTPException(status_code=404, detail="Live attribute not found")

    # Check if overlay already exists in this session
    overlay = (
        db.query(OverlayModel)
        .filter(
            OverlayModel.SessionUUID == payload.session_uuid,
            OverlayModel.uuid == attribute_uuid,
        )
        .first()
    )

    if overlay:
        # Overwrite staged value
        overlay.NewValue = payload.value
        overlay.OperationType = OperationType.UPDATE
    else:
        # Create overlay from live state
        overlay = OverlayModel(
            uuid=attribute_uuid,
            node_uuid=live.node_uuid,
            attribute_id=live.attribute_id,
            OperationType=OperationType.UPDATE,
            SessionUUID=payload.session_uuid,
            OldValue=live.value,
            NewValue=payload.value,
        )
        db.add(overlay)

    db.commit()

    return {
        "status": "staged",
        "operation": "UPDATE",
        "uuid": attribute_uuid,
        "session_uuid": payload.session_uuid,
    }


# ---------------------------------------------------------
# DELETE (SESSION OVERLAY)
# ---------------------------------------------------------
def push_delete(
    db: Session,
    table_code: str,
    attribute_uuid: UUID,
    session_uuid: UUID,
):
    """
    Stage a DELETE operation.

    - Removes any existing CREATE overlay
    - Or stages DELETE for a live attribute
    """
    try:
        OverlayModel = SESSION_OVERLAY_REGISTRY[table_code]
        LiveModel = LIVE_TABLE_REGISTRY[table_code]
    except KeyError:
        raise HTTPException(status_code=400, detail="Invalid table code")

    # Check if overlay already exists
    overlay = (
        db.query(OverlayModel)
        .filter(
            OverlayModel.SessionUUID == session_uuid,
            OverlayModel.uuid == attribute_uuid,
        )
        .first()
    )

    # If attribute was created in this session → just drop it
    if overlay and overlay.OperationType == OperationType.CREATE:
        db.delete(overlay)
        db.commit()
        return {
            "status": "discarded",
            "operation": "CREATE_REMOVED",
            "uuid": attribute_uuid,
            "session_uuid": session_uuid,
        }

    # Otherwise fetch live row
    live = db.query(LiveModel).filter(LiveModel.uuid == attribute_uuid).first()
    if not live:
        raise HTTPException(status_code=404, detail="Live attribute not found")

    if overlay:
        overlay.OperationType = OperationType.DELETE
        overlay.OldValue = live.value
        overlay.NewValue = None
    else:
        overlay = OverlayModel(
            uuid=attribute_uuid,
            node_uuid=live.node_uuid,
            attribute_id=live.attribute_id,
            OperationType=OperationType.DELETE,
            SessionUUID=session_uuid,
            OldValue=live.value,
            NewValue=None,
        )
        db.add(overlay)

    db.commit()

    return {
        "status": "staged",
        "operation": "DELETE",
        "uuid": attribute_uuid,
        "session_uuid": session_uuid,
    }