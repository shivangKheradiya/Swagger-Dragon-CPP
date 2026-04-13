from uuid import UUID
from datetime import datetime

def make_json_safe(obj):
    """
    Recursively convert Python-only types into JSON-safe values.
    """
    if isinstance(obj, dict):
        return {k: make_json_safe(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [make_json_safe(v) for v in obj]
    if isinstance(obj, UUID):
        return str(obj)
    if isinstance(obj, datetime):
        return obj.isoformat()
    return obj
