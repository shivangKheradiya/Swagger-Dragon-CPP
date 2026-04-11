import uuid
from sqlalchemy import Column, Integer
from sqlalchemy.dialects.postgresql import UUID, JSONB
from .base import Base

class JSONBBase(Base):
    __abstract__ = True

    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    node_uuid = Column(UUID(as_uuid=True), nullable=False)
    attribute_id = Column(Integer, nullable=False)
    value = Column(JSONB, nullable=False)  # JSON null allowed