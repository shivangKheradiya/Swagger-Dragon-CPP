import uuid
from app.services.attribute_mapper import apply_value
from app.services.history_service import write_history, OP_CREATE

def create_attribute(db, model, history_model, payload):
    attr = model(
        UUID=str(uuid.uuid4()),
        TreeNodeUUID=payload.tree_node_uuid,
        ElementTypeAttributeID=payload.element_type_attribute_id
    )

    apply_value(attr, payload.value_type, payload.value)

    db.add(attr)

    snapshot = {
        "ValueType": payload.value_type,
        "Value": payload.value
    }

    write_history(db, history_model, attr, OP_CREATE, None, snapshot)
    return attr