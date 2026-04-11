from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db import get_db
from app.schemas.attributes import AttributeCreate
from app.services.attribute_service import create_attribute
from app.models.attributes import TreeNodeAttributesDesign
from app.models.history import TreeNodeAttributesDesignHistory

router = APIRouter(prefix="/design/attributes", tags=["Design Attributes"])

@router.post("/")
def create(payload: AttributeCreate, db: Session = Depends(get_db)):
    attr = create_attribute(
        db,
        TreeNodeAttributesDesign,
        TreeNodeAttributesDesignHistory,
        payload
    )
    db.commit()
    return attr
