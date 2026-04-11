from pydantic import BaseModel
from typing import Any
from datetime import datetime

class AttributeHistoryOut(BaseModel):
    operation_type: int
    changed_at: datetime
    old_value: Any
    new_value: Any