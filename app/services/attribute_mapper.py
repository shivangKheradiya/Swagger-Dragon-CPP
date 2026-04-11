from app.core.enums import ValueType

def apply_value(attribute, value_type: ValueType, value):
    attribute.ValueType = value_type

    if value_type == ValueType.STRING:
        attribute.ValueString = value
    elif value_type == ValueType.INTEGER:
        attribute.ValueInt = value
    elif value_type == ValueType.FLOAT:
        attribute.ValueFloat = value
    elif value_type == ValueType.BOOLEAN:
        attribute.ValueBool = value
    elif value_type == ValueType.DATETIME:
        attribute.ValueDateTime = value
    elif value_type == ValueType.UUID:
        attribute.ValueUUID = value
    elif value_type == ValueType.JSON:
        attribute.ValueJSON = value
    else:
        raise ValueError("Unsupported ValueType")