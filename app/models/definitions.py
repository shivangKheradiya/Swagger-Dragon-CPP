from sqlalchemy import Column, Integer, String
from app.models.base import Base

class ElementTypeAttributesDesign(Base):
    __tablename__ = "ElementTypeAttributes_Design"

    ID = Column(Integer, primary_key=True)
    Name = Column(String, nullable=False)
    DataType = Column(String, nullable=False)
