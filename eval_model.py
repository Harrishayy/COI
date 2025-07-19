import pandas as pd
import numpy as np
from sklearn.metrics import classification_report, confusion_matrix, cohen_kappa_score
from config import LABELS_DIR, PROC_DIR
from codebook import CODEBOOK_MIN


def evaluate_model():
    """Evaluate model performance against gold standard."""
    gold_path = LABELS_DIR / "gold_adjudicated.csv"
    
    if not gold_path.exists():
        print("Gold adjudicated file not found; skip.")
        print("Expected file:", gold_path)
        return None
    
    # Load gold standard
    gold = pd.read_csv(gold_path)
    print(f"Loaded gold standard: {len(gold)} samples")
    
    # Load model predictions
    final_labels_path = PROC_DIR / "studychat_auto_final.parquet"
    if not final_labels_path.exists():
        print("Final labels not found. Run postprocess.py first.")
        return None
    
    auto_final = pd.read_parquet(final_labels_path)
    
    # Map stage names to integers
    name_map = {v["name"].lower(): k for k, v in CODEBOOK_MIN.items()}
    
    def to_stage(x):
        x = str(x).strip().lower()
        if x.isdigit():
            return int(x)
        return name_map.get(x, np.nan)
    
    # Process gold standard
    if "gold_stage" in gold.columns:
        gold["gs"] = gold["gold_stage"].map(to_stage)
    elif "gold_label" in gold.columns:
        gold["gs"] = gold["gold_label"].map(to_stage)
    else:
        raise ValueError("gold_adjudicated.csv must have gold_stage or gold_label column.")
    
    # Merge with model predictions
    merged = gold.merge(auto_final,
                        on=["thread_id", "turn_index", "text"],
                        how="left")
    
    mask = merged["gs"].notna() & merged["final_stage"].notna()
    
    if mask.sum() == 0:
        print("No overlapping predictions found.")
        return None
    
    y_true = merged.loc[mask, "gs"]
    y_pred = merged.loc[mask, "final_stage"]
    
    print(f"Evaluation samples: {mask.sum()}")
    print("\nClassification Report:")
    print(classification_report(y_true, y_pred, digits=3))
    
    kappa = cohen_kappa_score(y_true, y_pred)
    print(f"Cohen's kappa (model vs gold): {kappa:.3f}")
    
    cm = confusion_matrix(y_true, y_pred, labels=[1, 2, 3, 4])
    print("\nConfusion Matrix:")
    print(cm)
    
    # Per-stage accuracy
    stage_acc = {}
    for stage in [1, 2, 3, 4]:
        stage_mask = y_true == stage
        if stage_mask.sum() > 0:
            acc = (y_true[stage_mask] == y_pred[stage_mask]).mean()
            stage_acc[stage] = acc
            print(f"Stage {stage} accuracy: {acc:.3f} (n={stage_mask.sum()})")
    
    return merged, cm


def main():
    """Evaluate model against gold standard."""
    evaluate_model()


if __name__ == "__main__":
    main() 