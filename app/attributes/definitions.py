from enum import Enum

class AttributeType(str, Enum):
    string = "string"
    integer = "integer"
    boolean = "boolean"
    object = "object"
    array = "array"
    any = "any"

ATTRIBUTE_DEFINITION = {
    "tree_desi": {
        1: AttributeType.string,
        2: AttributeType.integer,
        3: AttributeType.boolean,
    },
    "asset_desi": {
        10: AttributeType.string,
        11: AttributeType.object,
    },
}