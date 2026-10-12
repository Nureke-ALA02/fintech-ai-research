#!/usr/bin/env bash
set -euo pipefail
python -m src.benchmark --config "${1:-configs/config.yaml}"
