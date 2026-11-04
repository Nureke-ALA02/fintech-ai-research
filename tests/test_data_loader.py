import pandas as pd
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