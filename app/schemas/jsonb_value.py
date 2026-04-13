from typing import Any
from uuid import UUID

from pydantic import BaseModel, field_validator

from ..attributes.definitions import ATTRIBUTE_DEFINITION, AttributeType


class JSONBCreate(BaseModel):
    """
    Request schema for JSONB attribute operations.

    IMPORTANT:
    - session_uuid is REQUIRED
    - value is REQUIRED but may be JSON null (None)
    """

    session_uuid: UUID               # ✅ NEW (MANDATORY)
    node_uuid: UUID
    attribute_id: int
    value: Any                       # ✅ REQUIRED; JSON null allowed

    @field_validator("value")
    @classmethod
    def validate_value(cls, v, info):
        """
        Safely validate value based on attribute_id and table context.

        Validation rules:
        - JSON null is always allowed
        - Attribute rules apply only if definition exists
        - Validation is advisory, not coercive
        """

        context = info.context or {}
        table_name = context.get("table")

        # ✅ FastAPI first-pass validation → skip deep validation
        if not table_name:
            return v

        table_rules = ATTRIBUTE_DEFINITION.get(table_name)
        if not table_rules:
            return v

        attribute_id = info.data.get("attribute_id")
        attr_type = table_rules.get(attribute_id)

        if not attr_type:
            raise ValueError(f"Unknown attribute_id: {attribute_id}")

        # ✅ JSON null is ALWAYS allowed
        if v is None:
            return v

        if attr_type == AttributeType.string and not isinstance(v, str):
            raise ValueError("Expected string JSON value")

        if attr_type == AttributeType.integer and not isinstance(v, int):
            raise ValueError("Expected integer JSON value")

        if attr_type == AttributeType.boolean and not isinstance(v, bool):
            raise ValueError("Expected boolean JSON value")

        if attr_type == AttributeType.object and not isinstance(v, dict):
            raise ValueError("Expected JSON object")

        if attr_type == AttributeType.array and not isinstance(v, list):
            raise ValueError("Expected JSON array")

        return v