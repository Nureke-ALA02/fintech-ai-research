import os
import numpy as np
import pandas as pd


def generate_synthetic_data(n_samples: int = 100, seed: int = 42) -> pd.DataFrame:
    """Generates synthetic survey and performance telemetry data."""
    np.random.seed(seed)

    ai_frequency = np.random.choice([1, 2, 3, 4, 5], size=n_samples, p=[0.1, 0.15, 0.25, 0.3, 0.2])
    developer_seniority = np.random.choice(['Junior', 'Middle', 'Senior'], size=n_samples, p=[0.3, 0.4, 0.3])

    perceived_productivity = np.clip(
        1.5 + 0.6 * ai_frequency + np.random.normal(0, 0.5, n_samples), 1, 5
    )
    perceived_efficiency = np.clip(
        1.2 + 0.65 * ai_frequency + np.random.normal(0, 0.4, n_samples), 1, 5
    )
    task_completion_time = np.clip(
        150 - 15 * ai_frequency + np.random.normal(0, 15, n_samples), 30, 200
    )

    df = pd.DataFrame({
        'employee_id': [f'EMP_{i:03d}' for i in range(1, n_samples + 1)],
        'seniority': developer_seniority,
        'ai_frequency': ai_frequency,
        'perceived_productivity': np.round(perceived_productivity, 2),
        'perceived_efficiency': np.round(perceived_efficiency, 2),
        'task_completion_time_min': np.round(task_completion_time, 1)
    })

    return df


def load_and_preprocess_data(raw_data_path: str = 'data/raw/survey_responses.csv') -> pd.DataFrame:
    """Loads raw data or generates synthetic dataset if missing."""
    if os.path.exists(raw_data_path):
        df = pd.read_csv(raw_data_path)
    else:
        df = generate_synthetic_data(n_samples=100)

    df = df.dropna()
    os.makedirs('data/processed', exist_ok=True)
    df.to_csv('data/processed/cleaned_dataset.csv', index=False)
    print(f"[SUCCESS] Dataset processed and saved. Rows: {len(df)}")
    return df