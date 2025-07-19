import pandas as pd
from config import PROC_DIR, RESULTS_DIR


def analyze_role_stage_distribution(df):
    """Analyze distribution of stages by speaker role."""
    role_stage = (df.groupby("speaker_type")["final_stage"]
                  .value_counts(normalize=True)
                  .mul(100)
                  .rename("pct")
                  .reset_index()
                  .sort_values(["speaker_type", "final_stage"]))
    
    return role_stage


def main():
    """Analyze potential biases in role × stage distribution."""
    final_labels_path = PROC_DIR / "studychat_auto_final.parquet"
    
    if not final_labels_path.exists():
        print("Final labels not found. Run postprocess.py first.")
        return
    
    auto_final = pd.read_parquet(final_labels_path)
    print(f"Analyzing role × stage distribution for {len(auto_final)} messages...")
    
    # Analyze role-stage distribution
    role_stage = analyze_role_stage_distribution(auto_final)
    
    # Save results
    role_stage_path = RESULTS_DIR / "role_stage_distribution.csv"
    role_stage.to_csv(role_stage_path, index=False)
    print(f"Saved role-stage distribution -> {role_stage_path}")
    
    # Print summary
    print(f"\nRole × Stage Distribution:")
    print(role_stage.to_string(index=False))
    
    # Check for potential biases
    print(f"\nBias Analysis:")
    
    # Overall stage distribution
    overall_stages = auto_final["final_stage"].value_counts(normalize=True).sort_index()
    print(f"Overall stage distribution: {overall_stages.to_dict()}")
    
    # Per-role analysis
    for role in auto_final["speaker_type"].unique():
        role_data = auto_final[auto_final["speaker_type"] == role]
        if len(role_data) > 0:
            role_stages = role_data["final_stage"].value_counts(normalize=True).sort_index()
            print(f"\n{role} (n={len(role_data)}): {role_stages.to_dict()}")
    
    # Statistical test for independence (chi-square)
    try:
        from scipy.stats import chi2_contingency
        contingency = pd.crosstab(auto_final["speaker_type"], auto_final["final_stage"])
        chi2, p_value, dof, expected = chi2_contingency(contingency)
        print(f"\nChi-square test for independence:")
        print(f"  Chi2 = {chi2:.3f}")
        print(f"  p-value = {p_value:.3f}")
        print(f"  Degrees of freedom = {dof}")
        
        if p_value < 0.05:
            print("  → Significant association between role and stage (potential bias)")
        else:
            print("  → No significant association detected")
            
    except ImportError:
        print("scipy not available for chi-square test")
    
    return role_stage


if __name__ == "__main__":
    main() 