import re
import pandas as pd
from config import PROC_DIR
from codebook import CODEBOOK_MIN


def apply_rules(df: pd.DataFrame) -> pd.DataFrame:
    """
    Apply rule-based post-processing to raw classifications.
    
    Args:
        df: DataFrame with raw classification results
        
    Returns:
        DataFrame with final stage and label columns
    """
    # Rule patterns
    CLOSURE_PAT = re.compile(r"\b(it works now|fixed|resolved|final answer|all tests pass|passes now)\b", re.I)
    GREETING_PAT = re.compile(r"^(hi|hello|thanks|thank you)\b", re.I)
    
    final_stage = []
    for _, r in df.iterrows():
        stage = r.raw_stage
        text = r.text
        
        # Rule 1: If stage 2 or 3 contains closure language, promote to stage 4
        if stage in (2, 3) and CLOSURE_PAT.search(text):
            stage = 4
        
        # Rule 2: If stage 1 is just a greeting, demote to stage 2
        if stage == 1 and GREETING_PAT.search(text) and len(text.split()) <= 4:
            stage = 2
        
        final_stage.append(stage)
    
    out = df.copy()
    out["final_stage"] = final_stage
    out["final_label"] = out["final_stage"].map(
        lambda s: CODEBOOK_MIN.get(int(s), {}).get("name", "UNKNOWN") if s else None
    )
    
    return out


def main():
    """Apply post-processing rules to raw classifications."""
    final_labels_path = PROC_DIR / "studychat_auto_final.parquet"
    
    if final_labels_path.exists():
        auto_final = pd.read_parquet(final_labels_path)
        print("Loaded final labels:", len(auto_final))
    else:
        # Load raw labels
        raw_labels_path = PROC_DIR / "studychat_auto_raw.parquet"
        if not raw_labels_path.exists():
            print("Raw labels not found. Run auto_label.py first.")
            return
        
        auto_raw = pd.read_parquet(raw_labels_path)
        print("Applying post-processing rules...")
        
        auto_final = apply_rules(auto_raw)
        auto_final.to_parquet(final_labels_path, index=False)
        print("Saved final labels ->", final_labels_path)
    
    # Print summary of changes
    if 'raw_stage' in auto_final.columns and 'final_stage' in auto_final.columns:
        changes = (auto_final['raw_stage'] != auto_final['final_stage']).sum()
        total = len(auto_final)
        print(f"\nPost-processing Summary:")
        print(f"Total messages: {total}")
        print(f"Messages changed by rules: {changes} ({changes/total*100:.1f}%)")
        
        if changes > 0:
            print("\nStage changes:")
            for _, row in auto_final[auto_final['raw_stage'] != auto_final['final_stage']].head(5).iterrows():
                print(f"  {row['raw_stage']} -> {row['final_stage']}: {row['text'][:50]}...")
    
    return auto_final


if __name__ == "__main__":
    main() 