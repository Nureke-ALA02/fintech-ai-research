import os
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def setup_publication_style():
    """Настройка публикационной темы и стилей рендеринга."""
    # Правило 3: Публикационная тема + читаемый размер шрифта
    sns.set_theme(style="whitegrid", font_scale=1.2)
    plt.rcParams.update({
        "font.family": "sans-serif",
        "font.sans-serif": ["Arial", "DejaVu Sans", "Helvetica"],
        "axes.edgecolor": "#cccccc",
        "axes.linewidth": 0.8,
        "grid.linestyle": "--",
        "grid.alpha": 0.6,
        "figure.dpi": 300,
        "savefig.dpi": 300,
        "savefig.bbox": "tight"
    })


def plot_benchmark_results(jsonl_filepath='outputs/tables/benchmark_run.jsonl',
                           output_image_path='outputs/figures/benchmark_latency.png'):
    """
    Построение графика производительности с соблюдением 3 правил научной визуализации.
    """
    if not os.path.exists(jsonl_filepath):
        # Если основного файла нет, проверяем альтернативное имя
        jsonl_filepath = 'outputs/tables/benchmark_metrics.jsonl'
        if not os.path.exists(jsonl_filepath):
            print(f"[ERROR] Файл с логами {jsonl_filepath} не найден.")
            return

    # Загрузка данных
    data = []
    with open(jsonl_filepath, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                data.append(json.loads(line.strip()))
    
    df = pd.DataFrame(data)
    df_valid = df[df.get('success', True) == True].copy()

    # Применяем стили
    setup_publication_style()
    fig, ax = plt.subplots(figsize=(9, 5.5))

    # Правило 3: Colorblind-safe палитра + комбинирование цвета, маркеров и штриховки
    palette = sns.color_palette("colorblind")
    primary_color = palette[0]
    secondary_color = palette[3]

    iterations = df_valid['iteration'].values
    durations = df_valid['duration_ms'].values

    # Правило 2: Отображение медианы (p50) и скользящего разброса
    # Для временных рядов/итераций строим медиану и скользящие квантили (p25-p75)
    window = 5
    df_valid['p50_rolling'] = df_valid['duration_ms'].rolling(window, min_periods=1).median()
    df_valid['p25_rolling'] = df_valid['duration_ms'].rolling(window, min_periods=1).quantile(0.25)
    df_valid['p75_rolling'] = df_valid['duration_ms'].rolling(window, min_periods=1).quantile(0.75)

    # Затененная область перцентилей (p25–p75) для асимметричных IT-выбросов
    ax.fill_between(
        df_valid['iteration'],
        df_valid['p25_rolling'],
        df_valid['p75_rolling'],
        color=primary_color,
        alpha=0.25,
        label='IQR (p25–p75 Range)'
    )

    # Основная линия с маркерами и штриховкой для ЧБ-печати
    ax.plot(
        df_valid['iteration'],
        df_valid['p50_rolling'],
        color=primary_color,
        linestyle='-',
        linewidth=2,
        marker='o',
        markersize=4,
        markevery=5,  # Маркеры каждые 5 итераций, чтобы не перегружать график
        label='Median Latency (p50)'
    )

    # Отрисовка сглаженного 95-го перцентиля (Tail Latency)
    df_valid['p95_rolling'] = df_valid['duration_ms'].rolling(window, min_periods=1).quantile(0.95)
    ax.plot(
        df_valid['iteration'],
        df_valid['p95_rolling'],
        color=secondary_color,
        linestyle='--',
        linewidth=1.8,
        marker='s',
        markersize=4,
        markevery=5,
        label='Tail Latency (p95)'
    )

    # Правило 1: Оси, подписи с физическими единицами и масштабирование
    ax.set_xlabel("Benchmark Iteration Index [n]", fontsize=12, fontweight='bold', labelpad=8)
    ax.set_ylabel("Execution Latency [ms]", fontsize=12, fontweight='bold', labelpad=8)
    ax.set_title("Execution Latency Dynamics & Tail Variability", fontsize=14, pad=12)

    # Правило 1: Логарифмическая шкала при сильном разбросе ИЛИ строгое начало с 0
    max_lat = durations.max()
    min_lat = durations.min()
    if max_lat / (min_lat + 1e-9) > 100:
        ax.set_yscale('log')
        ax.set_ylabel("Execution Latency [ms] (Log Scale)", fontsize=12, fontweight='bold')
    else:
        ax.set_ylim(bottom=0)  # Строгое начало с 0 для честного отображения

    # Настройка легенды и сетки
    ax.legend(loc='upper right', frameon=True, facecolor='white', framealpha=0.9)
    plt.tight_layout()

    # Сохранение в высоком разрешении
    os.makedirs(os.path.dirname(output_image_path), exist_ok=True)
    plt.savefig(output_image_path, dpi=300, format='png')
    plt.close()

    print(f"[SUCCESS] Публикационный график успешно сохранен в: {output_image_path}")


if __name__ == "__main__":
    plot_benchmark_results()