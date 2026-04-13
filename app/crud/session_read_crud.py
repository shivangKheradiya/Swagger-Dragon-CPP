from uuid import UUID
from sqlalchemy.orm import Session

from app.registry import LIVE_TABLE_REGISTRY, SESSION_OVERLAY_REGISTRY
from app.core.enums import OperationType


def read_all_with_overlay(
    db: Session,
    table_name: str,
    session_uuid: UUID,
):
    """
    Read all records merged with session overlay.
    Overlay rows override live state.
    """

    LiveModel = LIVE_TABLE_REGISTRY[table_name]
    OverlayModel = SESSION_OVERLAY_REGISTRY[table_name]

    # Fetch live rows
    live_rows = {
        row.uuid: row
        for row in db.query(LiveModel).all()
    }

    # Fetch overlay rows for session
    overlays = (
        db.query(OverlayModel)
        .filter(OverlayModel.SessionUUID == session_uuid)
        .order_by(OverlayModel.ChangedAt)
        .all()
    )

    # Apply overlays
    for overlay in overlays:
        if overlay.OperationType == OperationType.CREATE:
            # Virtual row (not yet in DB)
            live_rows[overlay.TNHAUUID] = overlay.NewValue

        elif overlay.OperationType == OperationType.UPDATE:
            if overlay.TNAUUID in live_rows:
                live_rows[overlay.TNAUUID].value = overlay.NewValue

        elif overlay.OperationType == OperationType.DELETE:
            live_rows.pop(overlay.TNAUUID, None)

    return list(live_rows.values())


def read_one_with_overlay(
    db: Session,
    table_name: str,
    uuid: UUID,
    session_uuid: UUID,
):
    """
    Read one record merged with session overlay.
    """

    LiveModel = LIVE_TABLE_REGISTRY[table_name]
    OverlayModel = SESSION_OVERLAY_REGISTRY[table_name]

    # Check overlay first (latest change wins)
    overlay = (
        db.query(OverlayModel)
        .filter(
            OverlayModel.SessionUUID == session_uuid,
            OverlayModel.TNAUUID == uuid,
        )
        .order_by(OverlayModel.ChangedAt.desc())
        .first()
    )

    if overlay:
        if overlay.OperationType == OperationType.DELETE:
            return None
        if overlay.OperationType in (
            OperationType.CREATE,
            OperationType.UPDATE,
        ):
            return overlay.NewValue

    # Fallback to live
    return (
        db.query(LiveModel)
        .filter(LiveModel.uuid == uuid)
        .first()
    )
