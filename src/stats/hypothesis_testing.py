import os
import pandas as pd
from scipy import stats
import statsmodels.api as sm
from src.data.data_loader import load_and_preprocess_data
from src.features.build_features import build_features


def run_statistical_analysis(df: pd.DataFrame):
    """Performs correlation and OLS regression analysis."""
    os.makedirs('outputs/tables', exist_ok=True)
    df_feat = build_features(df)
    results_summary = []

    print("\n" + "=" * 55)
    print("      STATISTICAL ANALYSIS & HYPOTHESIS TESTING      ")
    print("=" * 55)

    # RQ2: Frequency vs Productivity
    r_prod, p_prod = stats.pearsonr(df_feat['ai_frequency'], df_feat['perceived_productivity'])
    h1_prod = p_prod < 0.05 and r_prod > 0
    print(f"RQ2 (Productivity): Pearson r = {r_prod:.4f}, p = {p_prod:.4e} -> {'Reject H0' if h1_prod else 'Fail to Reject H0'}")
    
    results_summary.append({
        'Hypothesis': 'H1 (RQ2: Productivity)',
        'Pearson_r': round(r_prod, 4),
        'p_value': f"{p_prod:.4e}",
        'Result': 'Reject H0' if h1_prod else 'Fail to Reject H0'
    })

    # RQ3: Frequency vs Efficiency
    r_eff, p_eff = stats.pearsonr(df_feat['ai_frequency'], df_feat['perceived_efficiency'])
    h1_eff = p_eff < 0.05 and r_eff > 0
    print(f"RQ3 (Efficiency):   Pearson r = {r_eff:.4f}, p = {p_eff:.4e} -> {'Reject H0' if h1_eff else 'Fail to Reject H0'}")

    results_summary.append({
        'Hypothesis': 'H1 (RQ3: Efficiency)',
        'Pearson_r': round(r_eff, 4),
        'p_value': f"{p_eff:.4e}",
        'Result': 'Reject H0' if h1_eff else 'Fail to Reject H0'
    })

    # Export results
    pd.DataFrame(results_summary).to_csv('outputs/tables/hypothesis_results.csv', index=False)
    print("[SUCCESS] Results saved to 'outputs/tables/hypothesis_results.csv'")


if __name__ == '__main__':
    data = load_and_preprocess_data()
    run_statistical_analysis(data)