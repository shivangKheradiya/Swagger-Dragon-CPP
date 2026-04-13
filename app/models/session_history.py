import uuid
from sqlalchemy import (
    Column,
    String,
    Boolean,
    DateTime,
    func
)
from sqlalchemy.dialects.postgresql import UUID
from app.models.base import Base


class SessionHistoryBase(Base):
    """
    Session metadata table.

    ✅ Represents a user's logical working session.
    ✅ Joined by SessionUUID from history tables.
    """
    __tablename__ = "session_history" 
    
    SessionUUID = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    # CHANGED: JSONB → String (simpler & indexable)
    UserName = Column(String, nullable=True)
    HostName = Column(String, nullable=True)

    # CHANGED: JSONB → proper timestamp
    DateTime = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )

    IsActive = Column(Boolean, default=True, nullable=False)
