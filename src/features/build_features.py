import pandas as pd


def build_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Applies feature engineering transformations to the dataset:
    - Creates categorical binary flags for high AI usage.
    - Computes a combined Performance-Efficiency Index.
    """
    df_feat = df.copy()

    # Binary flag for heavy AI users (frequency >= 4)
    df_feat['is_heavy_ai_user'] = (df_feat['ai_frequency'] >= 4).astype(int)

    # Combined composite performance-efficiency index
    df_feat['perf_efficiency_index'] = (
        df_feat['perceived_productivity'] + df_feat['perceived_efficiency']
    ) / 2.0

    return df_feat


if __name__ == '__main__':
    from src.data.data_loader import load_and_preprocess_data
    df = load_and_preprocess_data()
    df_features = build_features(df)
    print("[SUCCESS] Features successfully engineered.")
    print(df_features[['employee_id', 'is_heavy_ai_user', 'perf_efficiency_index']].head())