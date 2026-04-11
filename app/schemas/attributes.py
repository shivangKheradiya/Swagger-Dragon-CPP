from pydantic import BaseModel
from typing import Any

class AttributeCreate(BaseModel):
    tree_node_uuid: str
    element_type_attribute_id: int
    value_type: int
    value: Any