import uuid
from datetime import datetime

OP_CREATE = 1
OP_UPDATE = 2
OP_DELETE = 3

def write_history(db, history_model, attr, op, old_val, new_val):
    record = history_model(
        TNHAUUID=str(uuid.uuid4()),
        TNAUUID=attr.UUID,
        OperationType=op,
        ChangedAt=datetime.utcnow(),
        ValueType=attr.ValueType,
        OldValue=old_val,
        NewValue=new_val
    )
    db.add(record)