import json
import os
import numpy as np
import pandas as pd

def load_and_clean_logs(filepath='outputs/tables/benchmark_metrics.jsonl'):
    """
    Загрузка, валидация и неразрушающая очистка логов бенчмарка.
    """
    data = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    data.append(json.loads(line.strip()))
    except FileNotFoundError:
        print(f"[ERROR] Файл {filepath} не найден. Проверьте путь к логам.")
        return None

    df = pd.DataFrame(data)
    print(f"[INFO] Загружено сырых записей: {len(df)}")

    if 'phase' in df.columns:
        df = df[df['phase'] == 'benchmark'].copy()

    if 'success' in df.columns:
        total_runs = len(df)
        error_count = len(df[df['success'] == False])
        error_rate = (error_count / total_runs) * 100 if total_runs > 0 else 0.0
        
        print(f"--- [GUARDRAIL METRIC] ---")
        print(f"Общее число итераций : {total_runs}")
        print(f"Количество сбоев     : {error_count}")
        print(f"Уровень ошибок (Error): {error_rate:.2f}%")
        
        if error_rate > 1.0:
            print("[WARNING] Внимание: Уровень ошибок превышает 1%!")
        print("----------------------------")

    df_valid = df[df.get('success', True) == True].copy()
    
    if 'duration_ms' in df_valid.columns:
        Q1 = df_valid['duration_ms'].quantile(0.25)
        Q3 = df_valid['duration_ms'].quantile(0.75)
        IQR = Q3 - Q1
        
        lower_bound = Q1 - 3.0 * IQR
        upper_bound = Q3 + 3.0 * IQR
        
        df_valid['is_outlier'] = (df_valid['duration_ms'] < lower_bound) | (df_valid['duration_ms'] > upper_bound)
        outliers_count = df_valid['is_outlier'].sum()
        print(f"[OUTLIERS] Найдено аппаратных выбросов/спайков (3*IQR): {outliers_count} из {len(df_valid)}")

    return df_valid


def compute_scientific_aggregates(df_cleaned):
    """
    Расчет центральных тенденций, перцентилей и бутстреп-доверительных интервалов.
    """
    if df_cleaned is None or df_cleaned.empty:
        print("[ERROR] Передан пустой датасет.")
        return None

    durations = df_cleaned['duration_ms'].values

    mean_val = np.mean(durations)
    std_val = np.std(durations, ddof=1)
    p50 = np.percentile(durations, 50)
    p95 = np.percentile(durations, 95)
    p99 = np.percentile(durations, 99)

    n_bootstraps = 1000
    boot_means = []
    boot_p50 = []
    
    np.random.seed(42)
    for _ in range(n_bootstraps):
        sample = np.random.choice(durations, size=len(durations), replace=True)
        boot_means.append(np.mean(sample))
        boot_p50.append(np.percentile(sample, 50))
        
    ci_mean_lower, ci_mean_upper = np.percentile(boot_means, [2.5, 97.5])
    ci_p50_lower, ci_p50_upper = np.percentile(boot_p50, [2.5, 97.5])

    summary_data = {
        "metric": ["latency_ms"],
        "count": [len(durations)],
        "mean": [round(mean_val, 4)],
        "mean_ci95_lower": [round(ci_mean_lower, 4)],
        "mean_ci95_upper": [round(ci_mean_upper, 4)],
        "std": [round(std_val, 4)],
        "p50_median": [round(p50, 4)],
        "p50_ci95_lower": [round(ci_p50_lower, 4)],
        "p50_ci95_upper": [round(ci_p50_upper, 4)],
        "p95": [round(p95, 4)],
        "p99": [round(p99, 4)]
    }
    
    df_summary = pd.DataFrame(summary_data)

    print("\n" + "=" * 50)
    print("      РЕЗУЛЬТАТЫ СТАТИСТИЧЕСКОГО АГРЕГИРОВАНИЯ")
    print("=" * 50)
    for col in df_summary.columns:
        print(f"{col.ljust(18)}: {df_summary[col].values[0]}")
    print("=" * 50)

    output_dir = 'outputs/tables'
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, 'metrics_summary.csv')
    
    df_summary.to_csv(output_path, index=False, encoding='utf-8')
    print(f"[EXPORT] Агрегированные данные успешно сохранены в: {output_path}")

    return df_summary


if __name__ == "__main__":
    df_cleaned = load_and_clean_logs()
    if df_cleaned is not None and not df_cleaned.empty:
        print("\nПервые 3 строки очищенного датасета:")
        print(df_cleaned.head(3))
        
        # Автоматический запуск расчета и экспорта в CSV
        compute_scientific_aggregates(df_cleaned)