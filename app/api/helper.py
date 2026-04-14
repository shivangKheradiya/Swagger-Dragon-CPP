from app.registry import LIVE_TABLE_REGISTRY
from fastapi import HTTPException

# ---------------------------------------------------------
# Helper: validate domain/table code
# ---------------------------------------------------------
def validate_table(table: str):
    if table not in LIVE_TABLE_REGISTRY:
        raise HTTPException(status_code=400, detail=f"Invalid table code: {table}")