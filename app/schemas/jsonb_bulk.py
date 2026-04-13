from typing import List, Dict, Optional, Literal
from uuid import UUID
from pydantic import BaseModel, Field


# ---------------------------------------------------------
# Individual operation payloads
# ---------------------------------------------------------

class BulkCreateItem(BaseModel):
    node_uuid: UUID
    attribute_id: int
    value: object


class BulkUpdateItem(BaseModel):
    uuid: UUID
    value: object


class BulkDeleteItem(BaseModel):
    uuid: UUID


# ---------------------------------------------------------
# Operation groups (ordered by phase)
# ---------------------------------------------------------

class BulkOperations(BaseModel):
    create: List[BulkCreateItem] = Field(default_factory=list)
    update: List[BulkUpdateItem] = Field(default_factory=list)
    delete: List[BulkDeleteItem] = Field(default_factory=list)


# ---------------------------------------------------------
# Bulk request
# ---------------------------------------------------------

class JSONBBulkRequest(BaseModel):
    session_uuid: UUID
    operations: BulkOperations


# ---------------------------------------------------------
# Failure reporting
# ---------------------------------------------------------

class BulkFailure(BaseModel):
    index: int
    reason: str


class BulkOperationSummary(BaseModel):
    total: int
    success: int
    failed: int


class JSONBBulkResponse(BaseModel):
    status: Literal["success", "partial_success", "failed"]
    summary: Dict[str, BulkOperationSummary]
    failures: Dict[str, List[BulkFailure]]