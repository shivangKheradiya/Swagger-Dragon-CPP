from fastapi import FastAPI, HTTPException
from .database import create_table
from . import crud

app = FastAPI()


@app.on_event("startup")
def init_db():
    create_table()


@app.post("/items")
def create_item(payload: dict):
    return crud.create_item(payload)


@app.get("/items")
def get_items():
    return crud.read_items()


@app.get("/items/{item_id}")
def get_item(item_id: int):
    result = crud.read_item(item_id)
    if not result:
        raise HTTPException(status_code=404, detail="Item not found")
    return result


@app.put("/items/{item_id}")
def update_item(item_id: int, payload: dict):
    return crud.update_item(item_id, payload)


@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    return crud.delete_item(item_id)