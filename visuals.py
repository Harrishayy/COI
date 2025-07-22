import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from config import PROC_DIR, FIG_DIR


def plot_stage_distribution(df):
    """Plot stage distribution histogram."""
    pct = df["final_stage"].value_counts(normalize=True).sort_index().mul(100)
    
    plt.figure(figsize=(6, 4))
    plt.bar(pct.index.astype(str), pct.values)
    plt.xlabel("Stage")
    plt.ylabel("% of messages")
    plt.title("Cognitive Presence Stage Distribution (StudyChat)")
    plt.tight_layout()
    
    out = FIG_DIR / "stage_distribution_studychat.png"
    plt.savefig(out, dpi=150)
    print("Saved:", out)
    plt.close()


def transition_matrix(df):
    """Compute stage transition probability matrix."""
    tm = np.zeros((4, 4))
    
    for tid, g in df.groupby("thread_id"):
        stages = g.sort_values("turn_index")["final_stage"].tolist()
        for a, b in zip(stages, stages[1:]):
            if a is not None and b is not None:
                tm[a-1, b-1] += 1
    
    row_sums = tm.sum(axis=1, keepdims=True)
    probs = np.divide(tm, row_sums, out=np.zeros_like(tm), where=row_sums>0)
    return probs


def plot_transition_matrix(df):
    """Plot stage transition probability matrix."""
    probs = transition_matrix(df)
    
    plt.figure(figsize=(4, 4))
    plt.imshow(probs, cmap="Blues")
    
    for i in range(4):
        for j in range(4):
            plt.text(j, i, f"{probs[i,j]:.2f}", ha="center", va="center", color="black")
    
    plt.colorbar(label="P(next stage)")
    plt.xticks(range(4), [1, 2, 3, 4])
    plt.yticks(range(4), [1, 2, 3, 4])
    plt.title("Stage Transition Matrix (StudyChat)")
    plt.tight_layout()
    
    out = FIG_DIR / "stage_transitions_studychat.png"
    plt.savefig(out, dpi=150)
    print("Saved:", out)
    plt.close()


def resolution_curve(df):
    """Plot resolution attainment curve."""
    # For threads containing Stage 4, record first index where it appears
    lengths, first_pos = [], []
    
    for tid, g in df.groupby("thread_id"):
        stages = g.sort_values("turn_index")["final_stage"].tolist()
        if 4 in stages:
            lengths.append(len(stages))
            first_pos.append(stages.index(4) + 1)  # 1-based
    
    if not lengths:
        print("No Resolution occurrences.")
        return
    
    curve_df = pd.DataFrame({"thread_len": lengths, "first_res_idx": first_pos})
    max_len = curve_df["thread_len"].max()
    
    xs = list(range(1, max_len + 1))
    ys = [(curve_df["first_res_idx"] <= x).mean() for x in xs]
    
    plt.figure(figsize=(6, 4))
    plt.plot(xs, ys, marker="o")
    plt.xlabel("Thread length (messages)")
    plt.ylabel("Cumulative P(Resolution attained)")
    plt.title("Resolution Attainment Curve (StudyChat)")
    plt.grid(alpha=0.3)
    plt.tight_layout()
    
    out = FIG_DIR / "resolution_curve_studychat.png"
    plt.savefig(out, dpi=150)
    print("Saved:", out)
    plt.close()


def main():
    """Generate all visualizations."""
    final_labels_path = PROC_DIR / "studychat_auto_final.parquet"
    
    if not final_labels_path.exists():
        print("Final labels not found. Run postprocess.py first.")
        return
    
    auto_final = pd.read_parquet(final_labels_path)
    print(f"Generating visualizations for {len(auto_final)} messages...")
    
    # Generate all plots
    plot_stage_distribution(auto_final)
    plot_transition_matrix(auto_final)
    resolution_curve(auto_final)
    
    print("All visualizations completed!")
    return True


if __name__ == "__main__":
    main() 