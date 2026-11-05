import json
import os
import platform
import time
from datetime import datetime, timezone
import numpy as np

from src.data.data_loader import generate_synthetic_data, load_and_preprocess_data
from src.features.build_features import build_features


def target_pipeline_execution():
    """Целевая функция пайплайна: генерация данных и построение признаков."""
    df = generate_synthetic_data(n_samples=100)
    df_feat = build_features(df)
    return len(df_feat)


def run_benchmark():
    warmup_iterations = 10
    total_iterations = 100
    metrics_log = []

    print("[INFO] Запуск фазы прогрева и бенчмаркинга...")

    for i in range(total_iterations + warmup_iterations):
        success = True
        error_msg = None
        
        # Строгая изоляция замера (I/O вне таймера)
        start_time = time.perf_counter()
        try:
            target_pipeline_execution()
        except Exception as e:
            success = False
            error_msg = str(e)
        duration = time.perf_counter() - start_time

        # Отбрасываем фазу прогрева (Warm-up Bias mitigation)
        if i >= warmup_iterations:
            record = {
                "timestamp_utc": datetime.now(timezone.utc).isoformat(),
                "iteration": i - warmup_iterations,
                "duration_ms": round(duration * 1000, 4),
                "success": success,
                "error": error_msg,
                "env_python": platform.python_version(),
                "os": platform.platform()
            }
            metrics_log.append(record)

    # Пакетная запись сырых данных в JSONL (сохраняем изоляцию I/O)
    os.makedirs('outputs/tables', exist_ok=True)
    jsonl_path = 'outputs/tables/benchmark_run.jsonl'
    
    with open(jsonl_path, 'w', encoding='utf-8') as f:
        for record in metrics_log:
            f.write(json.dumps(record) + '\n')

    # Расчет метрик центральной тенденции и перцентилей
    successful_durations = [r["duration_ms"] for r in metrics_log if r["success"]]
    
    if not successful_durations:
        print("[ERROR] Все итерации бенчмарка завершились с ошибкой.")
        return

    p50 = np.percentile(successful_durations, 50)
    p95 = np.percentile(successful_durations, 95)
    p99 = np.percentile(successful_durations, 99)
    mean_val = np.mean(successful_durations)

    print("\n" + "="*50)
    print("       РЕЗУЛЬТАТЫ ИЗМЕРИТЕЛЬНОГО СТЕНДА")
    print("="*50)
    print(f" Успешных прогонов : {len(successful_durations)} / {total_iterations}")
    print(f" Среднее (Mean)    : {mean_val:.2f} ms")
    print(f" Медиана (p50)     : {p50:.2f} ms")
    print(f" Перцентиль (p95)  : {p95:.2f} ms")
    print(f" Перцентиль (p99)  : {p99:.2f} ms")
    print(f" Логи сохранены в  : {jsonl_path}")
    print("="*50)


if __name__ == "__main__":
    run_benchmark()