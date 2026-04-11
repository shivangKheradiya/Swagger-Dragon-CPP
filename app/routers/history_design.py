from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db import get_db
from app.models.history import TreeNodeAttributesDesignHistory

router = APIRouter(prefix="/design/history", tags=["Design History"])

@router.get("/{attribute_uuid}")
def history(attribute_uuid: str, db: Session = Depends(get_db)):
    return (
        db.query(TreeNodeAttributesDesignHistory)
        .filter_by(TNAUUID=attribute_uuid)
        .order_by(TreeNodeAttributesDesignHistory.ChangedAt)
        .all()
    )