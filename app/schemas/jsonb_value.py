from typing import Any, Optional
from pydantic import BaseModel, field_validator

from ..attributes.definitions import ATTRIBUTE_DEFINITION, AttributeType


class JSONBCreate(BaseModel):
    node_uuid: str
    attribute_id: int
    value: Optional[Any]  # allows JSON null

    @field_validator("value")
    @classmethod
    def validate_value(cls, v, info):
        """
        Safely validate value based on attribute_id and table context.
        """
        context = info.context or {}
        table_name = context.get("table")

        # ✅ First validation pass (FastAPI) → skip typed validation
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
            raise ValueError("Expected string value")

        if attr_type == AttributeType.integer and not isinstance(v, int):
            raise ValueError("Expected integer value")

        if attr_type == AttributeType.boolean and not isinstance(v, bool):
            raise ValueError("Expected boolean value")

        if attr_type == AttributeType.object and not isinstance(v, dict):
            raise ValueError("Expected object value")

        if attr_type == AttributeType.array and not isinstance(v, list):
            raise ValueError("Expected array value")

        return v