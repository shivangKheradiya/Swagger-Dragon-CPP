import uuid
from sqlalchemy import (
    Column,
    Integer,
    DateTime,
    func
)
from sqlalchemy.dialects.postgresql import UUID, JSONB
from app.models.base import Base


class SessionJSONBBase(Base):
    """
    Session-scoped working copy / overlay.

    ✅ Represents attribute changes within an active session
    ✅ Can be used for preview, undo, approval flows
    ❌ NOT permanent history
    """

    __abstract__ = True

    # Session overlay record
    TNHAUUID = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # CHANGED: NOT unique (multiple changes allowed)
    TNAUUID = Column(UUID(as_uuid=True), nullable=False, index=True)

    OperationType = Column(Integer, nullable=False)

    # ✅ FIXED: defined ONCE (duplicate removed)
    SessionUUID = Column(UUID(as_uuid=True), nullable=False, index=True)

    ChangedAt = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )

    OldValue = Column(JSONB, nullable=True)
    NewValue = Column(JSONB, nullable=True)