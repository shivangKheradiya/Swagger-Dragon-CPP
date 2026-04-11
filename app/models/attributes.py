from sqlalchemy import (
    Column, String, Integer, BigInteger,
    Boolean, Float, DateTime, SmallInteger
)
from sqlalchemy.dialects.postgresql import JSONB
from app.models.base import Base

class TreeNodeAttribute(Base):
    __abstract__ = True

    UUID = Column(String, primary_key=True)
    TreeNodeUUID = Column(String, index=True, nullable=False)
    ElementTypeAttributeID = Column(Integer, nullable=False)

    ValueType = Column(SmallInteger, nullable=False)

    ValueString = Column(String)
    ValueInt = Column(BigInteger)
    ValueFloat = Column(Float)
    ValueBool = Column(Boolean)
    ValueDateTime = Column(DateTime)
    ValueUUID = Column(String)
    ValueJSON = Column(JSONB)

class TreeNodeAttributesDesign(TreeNodeAttribute):
    __tablename__ = "TreeNodeAttributes_Design"
