from sqlalchemy import Column, String, Integer, Boolean, ForeignKey
from .database import Base


class TreeNodes(Base):
    __tablename__ = "TreeNodes"

    UUID = Column(String, primary_key=True)
    Parent = Column(String, nullable=True)
    IsDeleted = Column(Boolean, default=False)


class TreeNodeAttributes(Base):
    __tablename__ = "TreeNodeAttributes"

    UUID = Column(String, primary_key=True)
    TreeNodeUUID = Column(String, ForeignKey("TreeNodes.UUID"))
    ElementTypeAttributeID = Column(Integer)
    Value = Column(String, nullable=True)
    ChangedFrom = Column(String, nullable=True)
    IsDeleted = Column(Boolean, default=False)


class ElementTypes(Base):
    __tablename__ = "ElementTypes"

    IDNo = Column(Integer, primary_key=True, autoincrement=True)
    Name = Column(String, nullable=True)


class ElementTypeAttributes(Base):
    __tablename__ = "ElementTypeAttributes"

    IDNo = Column(Integer, primary_key=True, autoincrement=True)
    ElementTypeID = Column(Integer, ForeignKey("ElementTypes.IDNo"))
    Name = Column(String)
    DataType = Column(String)
    DefaultValue = Column(String)