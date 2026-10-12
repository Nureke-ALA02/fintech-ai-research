"""Identical deterministic CPU workload shared by both frameworks (controlled variable)."""
import hashlib


def run_workload(payload_size: int, iterations: int) -> dict:
    data = b"x" * payload_size
    digest = data
    for _ in range(iterations):
        digest = hashlib.sha256(digest).digest()
    return {"digest": digest.hex()[:16]}
