import uuid
from sqlalchemy import Column, Integer, Index
from sqlalchemy.dialects.postgresql import UUID, JSONB
from app.models.base import Base


class SessionJSONBBase(Base):
    """
    Session-scoped working copy / overlay.

    ✅ Draft state for attribute changes
    ✅ State-shaped (same shape as live table)
    ✅ Optimized for fast commit into live + history
    ✅ NOT permanent history
    """

    __abstract__ = True

    # Attribute UUID:
    # - CREATE  → newly generated
    # - UPDATE  → from live table
    # - DELETE  → from live table
    uuid = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    # Parent node of the attribute
    node_uuid = Column(
        UUID(as_uuid=True),
        nullable=False,
        index=True
    )

    # Attribute definition
    attribute_id = Column(
        Integer,
        nullable=False,
        index=True
    )

    # Operation semantics
    # 1 = CREATE, 2 = UPDATE, 3 = DELETE
    OperationType = Column(
        Integer,
        nullable=False
    )

    # Owning session
    SessionUUID = Column(
        UUID(as_uuid=True),
        nullable=False,
        index=True
    )

    # Value snapshots (same meaning as history table)
    OldValue = Column(JSONB, nullable=True)
    NewValue = Column(JSONB, nullable=True)