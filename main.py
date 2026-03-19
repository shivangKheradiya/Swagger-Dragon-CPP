from fastapi import FastAPI
from typing import List, Optional

app = FastAPI()

# 1. String API
@app.get("/string")
def get_string(name: str):
    return {"received_string": name}

# 2. Integer API
@app.get("/integer")
def get_integer(value: int):
    return {"received_integer": value}

# 3. Boolean API
@app.get("/boolean")
def get_boolean(flag: bool):
    return {"received_boolean": flag}

# 4. Array API (list of strings or ints)
@app.get("/array")
def get_array(items: List[str]):
    return {"received_array": items}

# Optional: Mixed example
@app.get("/mixed")
def get_mixed(name: str, age: int, active: bool, tags: Optional[List[str]] = None):
    return {
        "name": name,
        "age": age,
        "active": active,
        "tags": tags or []
    }