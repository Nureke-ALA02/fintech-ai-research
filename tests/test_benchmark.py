import os
from src.benchmark_runner import run_benchmark


def test_benchmark_runner_integration(monkeypatch):
    """
    Интеграционный тест для проверки работы измерительного стенда:
    - Проверяет успешное выполнение пайплайна бенчмарка.
    - Проверяет генерацию и наличие файла с логами .jsonl.
    - Проверяет структуру сохраненных данных.
    """
    # Запускаем бенчмарк
    run_benchmark()

    # Путь к сгенерированному файлу логов
    jsonl_path = 'outputs/tables/benchmark_run.jsonl'
    
    # 1. Проверяем, что файл был создан
    assert os.path.exists(jsonl_path), "Файл логов бенчмарка не был создан."

    # 2. Проверяем, что файл не пустой и содержит строки
    with open(jsonl_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    assert len(lines) > 0, "Файл логов пуст."

    import json
    # 3. Проверяем валидность первой записи JSONL
    first_record = json.loads(lines[0])
    assert "duration_ms" in first_record
    assert "success" in first_record
    assert first_record["success"] is True