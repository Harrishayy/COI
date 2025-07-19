import pandas as pd
from config import PROC_DIR, LABELS_DIR, CONF_THRESHOLD, SEED


def sample_low_confidence(df, n=200):
    """
    Sample messages with low confidence for manual review.
    
    Args:
        df: DataFrame with classification results
        n: Number of samples to return
        
    Returns:
        DataFrame with low-confidence samples
    """
    low = df[df["raw_confidence"].fillna(0) < CONF_THRESHOLD]
    
    if len(low) == 0:
        print("No low-confidence messages found.")
        return pd.DataFrame()
    
    sample = low.sample(min(n, len(low)), random_state=SEED)
    return sample


def main():
    """Generate active learning sample for manual review."""
    final_labels_path = PROC_DIR / "studychat_auto_final.parquet"
    
    if not final_labels_path.exists():
        print("Final labels not found. Run postprocess.py first.")
        return
    
    auto_final = pd.read_parquet(final_labels_path)
    print(f"Analyzing confidence for {len(auto_final)} messages...")
    
    # Generate low-confidence sample
    sample = sample_low_confidence(auto_final, n=200)
    
    if len(sample) == 0:
        print("No low-confidence messages to sample.")
        return
    
    # Save sample
    path = LABELS_DIR / "active_learning_sample.csv"
    sample.to_csv(path, index=False)
    print(f"Exported active learning sample -> {path}")
    print(f"Sample size: {len(sample)}")
    
    # Confidence statistics
    print(f"\nConfidence Statistics:")
    print(f"  Threshold: {CONF_THRESHOLD}")
    print(f"  Low-confidence messages: {len(auto_final[auto_final['raw_confidence'].fillna(0) < CONF_THRESHOLD])}")
    print(f"  Average confidence: {auto_final['raw_confidence'].mean():.1f}")
    print(f"  Min confidence: {auto_final['raw_confidence'].min():.1f}")
    print(f"  Max confidence: {auto_final['raw_confidence'].max():.1f}")
    
    # Stage distribution in sample
    if len(sample) > 0:
        stage_dist = sample["final_stage"].value_counts().sort_index()
        print(f"\nStage distribution in sample: {stage_dist.to_dict()}")
    
    return sample


if __name__ == "__main__":
    main() 