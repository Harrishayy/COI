import pandas as pd
from config import LABELS_DIR, GOLD_SAMPLE_MESSAGES, SEED, PROC_DIR


def create_gold_sample():
    """Create a stratified sample for manual annotation."""
    gold_sample_file = LABELS_DIR / "gold_sample_for_labeling.csv"
    
    if gold_sample_file.exists():
        print("Gold sample already exists:", gold_sample_file)
        return gold_sample_file
    
    # Load messages
    messages_path = PROC_DIR / "messages.parquet"
    if not messages_path.exists():
        print("Messages not found. Run studychat_load.py first.")
        return None
    
    df = pd.read_parquet(messages_path)
    
    # Simple stratification by position in thread (early / mid / late)
    tmp = df.copy()
    tmp["pos_bucket"] = pd.cut(tmp["turn_index"],
                               bins=[-1, 2, 6, 1e9],
                               labels=["early", "mid", "late"])
    
    per_bucket = GOLD_SAMPLE_MESSAGES // 3
    sample = (tmp.groupby("pos_bucket", group_keys=False)
              .apply(lambda g: g.sample(min(len(g), per_bucket), random_state=SEED)))
    
    sample = sample.sample(frac=1, random_state=SEED).reset_index(drop=True)
    sample["label_rater1"] = ""
    sample["label_rater2"] = ""
    
    sample.to_csv(gold_sample_file, index=False)
    print("Exported gold sample ->", gold_sample_file)
    print(f"Sample size: {len(sample)}")
    print(f"Position distribution: {sample['pos_bucket'].value_counts().to_dict()}")
    
    return gold_sample_file


def main():
    """Generate gold sample for manual annotation."""
    create_gold_sample()


if __name__ == "__main__":
    main() 