from typing import List, Literal, Any, Optional
from uuid import UUID
from pydantic import BaseModel, Field

LogicType = Literal["AND", "OR"]
OperatorType = Literal[
    "eq", "ne",
    "gt", "gte", "lt", "lte",
    "like", "ilike",
    "in"
]

class SearchCondition(BaseModel):
    field: str = Field(..., description="Column name")
    operator: OperatorType
    value: Any

class SearchGroup(BaseModel):
    logic: LogicType
    conditions: List[SearchCondition]

class SearchRequest(BaseModel):
    table: str = Field(..., description="DESI / CATA / DICT / ...")

    scope: Literal["live", "overlay", "merged"] = "live"
    session_uuid: Optional[UUID] = None

    where: List[SearchGroup]

    limit: int = 100
    offset: int = 0
