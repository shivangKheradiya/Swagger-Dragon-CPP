from sqlalchemy import Column, String, SmallInteger, DateTime
from sqlalchemy.dialects.postgresql import JSONB
from datetime import datetime
from app.models.base import Base

class TreeNodeAttributeHistory(Base):
    __abstract__ = True

    TNHAUUID = Column(String, primary_key=True)
    TNAUUID = Column(String, nullable=False)

    OperationType = Column(SmallInteger, nullable=False)
    ChangedAt = Column(DateTime, default=datetime.utcnow)

    ValueType = Column(SmallInteger, nullable=False)
    OldValue = Column(JSONB)
    NewValue = Column(JSONB)

class TreeNodeAttributesDesignHistory(TreeNodeAttributeHistory):
    __tablename__ = "TreeNodeAttributes_Design_History"