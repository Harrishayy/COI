import pandas as pd
import numpy as np
from collections import Counter
from config import PROC_DIR, RESULTS_DIR, ALPHA, BETA, GAMMA, STAGE_WEIGHTS


def compute_thread_metrics(df: pd.DataFrame) -> pd.DataFrame:
    """
    Compute CP-Bench metrics for each thread.
    
    Args:
        df: DataFrame with final stage classifications
        
    Returns:
        DataFrame with thread-level metrics
    """
    rows = []
    
    for thread_id, g in df.groupby("thread_id"):
        g = g.sort_values("turn_index")
        stages = g["final_stage"].dropna().astype(int).tolist()
        
        if not stages:
            continue
        
        N = len(stages)
        counts = Counter(stages)
        
        # Stage Weighted Score (SWS)
        sws = sum(STAGE_WEIGHTS[s] * c for s, c in counts.items()) / (4 * N)
        
        # Progressive Coherence (PC)
        forward, transitions = 0, 0
        for a, b in zip(stages, stages[1:]):
            if a != b:
                transitions += 1
                if b == a + 1:
                    forward += 1
        
        pc = forward / transitions if transitions > 0 else 0
        
        # Resolution Attainment (RA)
        ra = 1 if 4 in counts else 0
        
        # Cognitive Presence Index (CPI)
        cpi = ALPHA * sws + BETA * pc + GAMMA * ra
        
        rows.append({
            "thread_id": thread_id,
            "messages": N,
            "sws": sws,
            "pc": pc,
            "ra": ra,
            "cpi": cpi
        })
    
    return pd.DataFrame(rows)


def main():
    """Compute thread-level CP-Bench metrics."""
    final_labels_path = PROC_DIR / "studychat_auto_final.parquet"
    
    if not final_labels_path.exists():
        print("Final labels not found. Run postprocess.py first.")
        return
    
    auto_final = pd.read_parquet(final_labels_path)
    print(f"Computing metrics for {auto_final['thread_id'].nunique()} threads...")
    
    thread_metrics = compute_thread_metrics(auto_final)
    
    # Save results
    thread_metrics_path = RESULTS_DIR / "thread_metrics_studychat.csv"
    thread_metrics.to_csv(thread_metrics_path, index=False)
    print(f"Saved thread metrics -> {thread_metrics_path}")
    
    # Print summary statistics
    print(f"\nCP-Bench Metrics Summary:")
    print(f"Total threads: {len(thread_metrics)}")
    print(f"Average messages per thread: {thread_metrics['messages'].mean():.1f}")
    print(f"Stage Weighted Score (SWS): {thread_metrics['sws'].mean():.3f}")
    print(f"Progressive Coherence (PC): {thread_metrics['pc'].mean():.3f}")
    print(f"Resolution Attainment (RA): {thread_metrics['ra'].mean():.3f}")
    print(f"Cognitive Presence Index (CPI): {thread_metrics['cpi'].mean():.3f}")
    
    # Distribution of CPI
    print(f"\nCPI Distribution:")
    print(f"  Min: {thread_metrics['cpi'].min():.3f}")
    print(f"  Median: {thread_metrics['cpi'].median():.3f}")
    print(f"  Max: {thread_metrics['cpi'].max():.3f}")
    
    # Resolution attainment rate
    resolution_rate = thread_metrics['ra'].mean()
    print(f"\nResolution Attainment Rate: {resolution_rate:.1%}")
    
    return thread_metrics


if __name__ == "__main__":
    main() 