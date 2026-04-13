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
    table_name: str,
    payload,
):
    """
    Stage a CREATE operation in session overlay.
    """
    try:
        OverlayModel = SESSION_OVERLAY_REGISTRY[table_name]
    except KeyError:
        raise HTTPException(status_code=400, detail="Invalid table name")

    overlay = OverlayModel(
        TNAUUID=None,  # No live UUID yet (will be created at commit)
        OperationType=OperationType.CREATE,
        SessionUUID=payload.session_uuid,
        OldValue=None,
        NewValue={
            "node_uuid": payload.node_uuid,
            "attribute_id": payload.attribute_id,
            "value": payload.value,
        },
    )

    db.add(overlay)
    db.commit()

    return {
        "status": "staged",
        "operation": "CREATE",
        "session_uuid": payload.session_uuid,
    }


# ---------------------------------------------------------
# UPDATE (SESSION OVERLAY)
# ---------------------------------------------------------
def push_update(
    db: Session,
    table_name: str,
    uuid: UUID,
    payload,
):
    """
    Stage an UPDATE operation in session overlay.
    """
    try:
        OverlayModel = SESSION_OVERLAY_REGISTRY[table_name]
        LiveModel = LIVE_TABLE_REGISTRY[table_name]
    except KeyError:
        raise HTTPException(status_code=400, detail="Invalid table name")

    # ✅ Validate live record exists
    live = db.query(LiveModel).filter(LiveModel.uuid == uuid).first()
    if not live:
        raise HTTPException(status_code=404, detail="Record not found")

    overlay = OverlayModel(
        TNAUUID=uuid,
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
        "uuid": uuid,
        "session_uuid": payload.session_uuid,
    }


# ---------------------------------------------------------
# DELETE (SESSION OVERLAY)
# ---------------------------------------------------------
def push_delete(
    db: Session,
    table_name: str,
    uuid: UUID,
    session_uuid: UUID,
):
    """
    Stage a DELETE operation in session overlay.
    """
    try:
        OverlayModel = SESSION_OVERLAY_REGISTRY[table_name]
        LiveModel = LIVE_TABLE_REGISTRY[table_name]
    except KeyError:
        raise HTTPException(status_code=400, detail="Invalid table name")

    live = db.query(LiveModel).filter(LiveModel.uuid == uuid).first()
    if not live:
        raise HTTPException(status_code=404, detail="Record not found")

    overlay = OverlayModel(
        TNAUUID=uuid,
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
        "uuid": uuid,
        "session_uuid": session_uuid,
    }