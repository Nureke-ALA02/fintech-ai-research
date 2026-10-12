"""FastAPI (ASGI) implementation of the benchmark workload.
Sync `def` endpoint is used on purpose: the workload is CPU-bound, same as in Flask.
"""
from fastapi import FastAPI
from pydantic import BaseModel
from src.workload import run_workload

app = FastAPI()


class Item(BaseModel):
    id: int
    payload_size: int
    iterations: int


@app.post("/process")
def process(item: Item):
    return run_workload(item.payload_size, item.iterations)


@app.get("/health")
def health():
    return {"status": "ok"}
