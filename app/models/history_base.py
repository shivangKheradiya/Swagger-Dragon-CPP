import uuid
from sqlalchemy import Column, Integer, DateTime
from sqlalchemy.dialects.postgresql import UUID, JSONB
from .base import Base

class JSONBHistoryBase(Base):
    """
    History table for attribute value changes.
    One row per CREATE / UPDATE / DELETE.
    """

    __abstract__ = True

    HistoryUUID = Column( UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    # Reference to live row (TreeDESI.uuid)
    uuid = Column( UUID(as_uuid=True), nullable=False, index=True )
    # 1 = CREATE, 2 = UPDATE, 3 = DELETE
    OperationType = Column( Integer, nullable=False )
    OldValue = Column( JSONB, nullable=True )
    NewValue = Column( JSONB, nullable=True )
    
    SessionUUID = Column(
        UUID(as_uuid=True),
        nullable=False,
        index=True
    )
