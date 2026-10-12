# Flask vs FastAPI: Latency Benchmark of Python Web Frameworks under Concurrent Load

![License: MIT](https://img.shields.io/badge/license-MIT-green)
![Status](https://img.shields.io/badge/status-in%20progress-yellow)

**Authors:** <Author 1>, <Author 2> (Narxoz University, Digital Management and Design)

## Overview
This repository contains a reproducible benchmark that compares a synchronous WSGI framework (Flask + gunicorn)
with an ASGI framework (FastAPI + uvicorn) under increasing concurrent load.

**Research Question.** Does FastAPI achieve lower p95 latency than Flask for an identical CPU-bound
REST endpoint when concurrency grows from 1 to 50 clients?

**Hypotheses.** H0: no difference in median p95 latency between the frameworks.
H1: FastAPI's p95 latency is lower than Flask's at concurrency >= 10.

## Repository Structure
```
.
├── configs/config.yaml     # all experiment parameters
├── data/sample/            # 10-row sample of request parameters (full data: Week 7)
├── docs/methodology_card.md # Methodology Passport Card
├── docs/related_work.md    # Related Work and Research Gap
├── notebooks/              # analysis notebooks (Week 7+)
├── results/                # generated outputs (git-ignored)
├── scripts/run.sh          # shell entry point
├── src/
│   ├── benchmark.py        # benchmark runner
│   ├── workload.py         # identical workload for both frameworks
│   └── apps/               # flask_app.py, fastapi_app.py
├── Dockerfile
├── requirements.txt        # exact version pins
├── LICENSE
└── README.md
```

## System Requirements
- Any OS with Docker >= 24 (or Python 3.12 on Linux/macOS)
- CPU: 4+ cores recommended; RAM: 4 GB; no GPU required

## Quickstart (3 commands)
```bash
git clone https://github.com/<username>/<repo>.git && cd <repo>
docker build -t web-bench .
docker run --rm -v "$(pwd)/results:/app/results" web-bench
```
Output: `results/raw_latencies.csv` and `results/summary.csv`, plus a console log with the guardrail check.

Without Docker (Linux/macOS): `python -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt && bash scripts/run.sh`

## Planned Benchmarks
| ID | Framework | Concurrency | Repetitions | Primary metric | Status |
|----|-----------|-------------|-------------|----------------|--------|
| B1 | Flask (gunicorn) | 1, 10, 50 | 3 (sample) -> 10 (Week 7) | p95 latency (ms) | skeleton tested |
| B2 | FastAPI (uvicorn) | 1, 10, 50 | 3 (sample) -> 10 (Week 7) | p95 latency (ms) | skeleton tested |

## Expected Results (placeholder)
| Framework | Concurrency | p50 (ms) | p95 (ms) | p99 (ms) | Throughput (RPS) | Error rate |
|-----------|-------------|----------|----------|----------|------------------|-----------|
| Flask | 10 | TBD | TBD | TBD | TBD | TBD |
| FastAPI | 10 | TBD | TBD | TBD | TBD | TBD |

## Citation
```bibtex
@misc{flask_fastapi_bench_2026,
  title  = {Flask vs FastAPI: Latency Benchmark under Concurrent Load},
  author = {<Author 1> and <Author 2>},
  year   = {2026},
  url    = {https://github.com/<username>/<repo>}
}
```

## License
MIT — see [LICENSE](LICENSE).
