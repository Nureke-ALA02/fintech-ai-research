import json
import os
import platform
import time
from datetime import datetime
import numpy as np
import pandas as pd
import pytest
from scipy import stats

from src.data.data_loader import generate_synthetic_data, load_and_preprocess_data
from src.features.build_features import build_features


def test_synthetic_data():
    df = generate_synthetic_data(n_samples=30)
    assert len(df) == 30
    assert 'ai_frequency' in df.columns


def test_feature_engineering():
    df = generate_synthetic_data(n_samples=10)
    df_feat = build_features(df)
    assert 'is_heavy_ai_user' in df_feat.columns
    assert 'perf_efficiency_index' in df_feat.columns


def test_data_loader():
    df = load_and_preprocess_data()
    assert not df.empty
    assert df.isnull().sum().sum() == 0


def test_benchmark_pipeline_performance():
    """
    Бенчмарк-тест пайплайна генерации и обработки данных:
    - Изоляция I/O от замеров времени
    - Фаза прогрева (Warm-up)
    - Обработка ошибок и фиксация статусов
    - Сохранение сырых логов в JSONL с микросекундными метками
    - Расчет перцентилей (p50, p95, p99)
    """
    warmup_iterations = 10
    total_iterations = 100
    metrics_log = []

    # Целевая функция, производительность которой мы измеряем
    def target_pipeline_execution():
        df = generate_synthetic_data(n_samples=100)
        df_feat = build_features(df)
        return len(df_feat)

    # Цикл бенчмаркинга с фазой прогрева
    for i in range(total_iterations + warmup_iterations):
        success = True
        error_msg = None
        
        # Точный замер времени выполнения (изолирован от I/O)
        start_time = time.perf_counter()
        try:
            target_pipeline_execution()
        except Exception as e:
            success = False
            error_msg = str(e)
        duration = time.perf_counter() - start_time

        # Отбрасываем результаты фазы прогрева (Warm-up Bias mitigation)
        if i >= warmup_iterations:
            record = {
                "timestamp_utc": datetime.utcnow().isoformat(),
                "iteration": i - warmup_iterations,
                "duration_ns": int(duration * 1e9),
                "duration_ms": round(duration * 1000, 4),
                "success": success,
                "error": error_msg,
                "env_python": platform.python_version()
            }
            metrics_log.append(record)

    # Пакетный I/O: запись сырых логов в JSONL в конце теста
    os.makedirs('outputs/tables', exist_ok=True)
    jsonl_path = 'outputs/tables/benchmark_metrics.jsonl'
    with open(jsonl_path, 'w', encoding='utf-8') as f:
        for record in metrics_log:
            f.write(json.dumps(record) + '\n')

    # Извлекаем успешные замеры для расчета перцентилей
    successful_durations = [r["duration_ms"] for r in metrics_log if r["success"]]
    
    assert len(successful_durations) > 0, "Все итерации бенчмарка завершились с ошибкой."

    # Расчет центральных тенденций и перцентилей
    p50 = np.percentile(successful_durations, 50)
    p95 = np.percentile(successful_durations, 95)
    p99 = np.percentile(successful_durations, 99)

    print(f"\n[BENCHMARK RESULTS] p50: {p50:.2f}ms | p95: {p95:.2f}ms | p99: {p99:.2f}ms")

    # Утверждения для тестов (проверяем стабильность пайплайна)
    assert p99 < 500.0, "Превышен допустимый порог задержки p99."