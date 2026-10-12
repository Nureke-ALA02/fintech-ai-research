"""Benchmark runner: Flask (gunicorn) vs FastAPI (uvicorn) latency under load.

Usage:  python -m src.benchmark --config configs/config.yaml
"""
import argparse, csv, os, random, statistics, subprocess, sys, time
from concurrent.futures import ThreadPoolExecutor
import requests, yaml


def load_rows(path):
    with open(path, newline="") as f:
        return [{k: int(v) for k, v in r.items()} for r in csv.DictReader(f)]


def start_server(framework, cfg):
    s = cfg["server"]
    bind = f"{s['host']}:{s['port']}"
    if framework == "flask":
        cmd = [sys.executable, "-m", "gunicorn", "-w", str(s["workers"]), "-b", bind,
               "--log-level", "error", "src.apps.flask_app:app"]
    else:
        cmd = [sys.executable, "-m", "uvicorn", "src.apps.fastapi_app:app", "--host", s["host"],
               "--port", str(s["port"]), "--workers", str(s["workers"]), "--log-level", "error"]
    proc = subprocess.Popen(cmd)
    url = f"http://{bind}"
    deadline = time.time() + s["startup_timeout_s"]
    while time.time() < deadline:
        try:
            if requests.get(url + "/health", timeout=1).ok:
                return proc, url
        except requests.RequestException:
            time.sleep(0.2)
    proc.terminate()
    raise RuntimeError(f"{framework} server did not start")


def one_request(session, url, row, timeout):
    t0 = time.perf_counter()
    try:
        ok = session.post(url + "/process", json=row, timeout=timeout).ok
    except requests.RequestException:
        ok = False
    return (time.perf_counter() - t0) * 1000.0, ok


def run_load(url, rows, n, concurrency, timeout):
    def worker(i):
        with requests.Session() as s:
            return one_request(s, url, rows[i % len(rows)], timeout)
    t0 = time.perf_counter()
    with ThreadPoolExecutor(max_workers=concurrency) as ex:
        res = list(ex.map(worker, range(n)))
    return res, time.perf_counter() - t0


def pct(sorted_vals, p):
    k = max(0, min(len(sorted_vals) - 1, round(p / 100 * (len(sorted_vals) - 1))))
    return sorted_vals[k]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default="configs/config.yaml")
    cfg = yaml.safe_load(open(ap.parse_args().config))
    e = cfg["experiment"]
    random.seed(e["seed"])
    rows = load_rows(cfg["data"]["requests_file"])
    random.shuffle(rows)  # fixed order thanks to the seed
    out = cfg["output"]["results_dir"]
    os.makedirs(out, exist_ok=True)
    raw, summary = [], []

    for fw in e["frameworks"]:
        proc, url = start_server(fw, cfg)
        try:
            run_load(url, rows, e["warmup_requests"], 1, e["request_timeout_s"])  # warm-up
            for c in e["concurrency_levels"]:
                for rep in range(1, e["repetitions"] + 1):
                    res, wall = run_load(url, rows, e["total_requests"], c, e["request_timeout_s"])
                    lat = sorted(r[0] for r in res)
                    errs = sum(1 for r in res if not r[1])
                    for l, ok in res:
                        raw.append([fw, c, rep, round(l, 3), int(ok)])
                    summary.append([fw, c, rep, round(statistics.mean(lat), 3), round(pct(lat, 50), 3),
                                    round(pct(lat, 95), 3), round(pct(lat, 99), 3),
                                    round(len(res) / wall, 2), round(errs / len(res), 4)])
                    print(f"{fw:8s} c={c:<3d} rep={rep} p50={pct(lat,50):.2f}ms p95={pct(lat,95):.2f}ms "
                          f"rps={len(res)/wall:.1f} err={errs}")
        finally:
            proc.terminate(); proc.wait(timeout=10)

    with open(os.path.join(out, cfg["output"]["raw_file"]), "w", newline="") as f:
        w = csv.writer(f); w.writerow(["framework", "concurrency", "rep", "latency_ms", "ok"]); w.writerows(raw)
    with open(os.path.join(out, cfg["output"]["summary_file"]), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["framework", "concurrency", "rep", "mean_ms", "p50_ms", "p95_ms", "p99_ms", "throughput_rps", "error_rate"])
        w.writerows(summary)
    bad = [s for s in summary if s[-1] > cfg["guardrails"]["max_error_rate"]]
    print("Guardrail:", "FAILED for %d runs" % len(bad) if bad else "OK (error rate within limit)")
    print(f"Saved to {out}/")


if __name__ == "__main__":
    main()
