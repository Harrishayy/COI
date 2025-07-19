import pandas as pd
import numpy as np
from sklearn.metrics import cohen_kappa_score
from collections import Counter
from config import LABELS_DIR
from codebook import CODEBOOK_MIN


def evaluate_humans():
    """Evaluate human-human reliability on completed gold sample."""
    completed = LABELS_DIR / "gold_sample_for_labeling_completed.csv"
    
    if not completed.exists():
        print("Completed gold file not found; skip for now.")
        print("Expected file:", completed)
        return None
    
    g = pd.read_csv(completed)
    name_to_int = {v["name"].lower(): k for k, v in CODEBOOK_MIN.items()}
    
    def norm(x):
        x = str(x).strip().lower()
        if x.isdigit():
            return int(x)
        return name_to_int.get(x, np.nan)
    
    g["r1"] = g["label_rater1"].map(norm)
    g["r2"] = g["label_rater2"].map(norm)
    
    mask = g["r1"].notna() & g["r2"].notna()
    
    if mask.sum() == 0:
        print("No overlapping labels yet.")
        return None
    
    kappa = cohen_kappa_score(g.loc[mask, "r1"], g.loc[mask, "r2"])
    print(f"Human-Human Cohen kappa: {kappa:.3f} (n={mask.sum()})")
    print("Counts r1:", Counter(g.loc[mask, "r1"]))
    print("Counts r2:", Counter(g.loc[mask, "r2"]))
    
    # Agreement matrix
    agreement_matrix = pd.crosstab(g.loc[mask, "r1"], g.loc[mask, "r2"], 
                                  rownames=['Rater 1'], colnames=['Rater 2'])
    print("\nAgreement matrix:")
    print(agreement_matrix)
    
    return g


def main():
    """Evaluate human reliability."""
    evaluate_humans()


if __name__ == "__main__":
    main() 