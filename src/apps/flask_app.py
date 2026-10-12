"""Flask (WSGI) implementation of the benchmark workload."""
from flask import Flask, jsonify, request
from src.workload import run_workload

app = Flask(__name__)


@app.post("/process")
def process():
    body = request.get_json()
    return jsonify(run_workload(body["payload_size"], body["iterations"]))


@app.get("/health")
def health():
    return jsonify(status="ok")
