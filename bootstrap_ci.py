import pandas as pd
import numpy as np
from config import RESULTS_DIR, SEED


def bootstrap_mean(arr, B=1000, seed=SEED):
    """
    Compute bootstrap confidence intervals for mean.
    
    Args:
        arr: Array of values
        B: Number of bootstrap samples
        seed: Random seed
        
    Returns:
        Tuple of (mean, lower_ci, upper_ci)
    """
    rng = np.random.default_rng(seed)
    n = len(arr)
    
    if n == 0:
        return (np.nan, np.nan, np.nan)
    
    means = []
    for _ in range(B):
        sample = rng.choice(arr, size=n, replace=True)
        means.append(sample.mean())
    
    lo, hi = np.percentile(means, [2.5, 97.5])
    return arr.mean(), lo, hi


def main():
    """Compute bootstrap confidence intervals for aggregate metrics."""
    thread_metrics_path = RESULTS_DIR / "thread_metrics_studychat.csv"
    
    if not thread_metrics_path.exists():
        print("Thread metrics not found. Run compute_metrics.py first.")
        return
    
    thread_metrics = pd.read_csv(thread_metrics_path)
    print(f"Computing bootstrap CIs for {len(thread_metrics)} threads...")
    
    # Compute bootstrap CIs for each metric
    agg_rows = []
    for metric in ["sws", "pc", "ra", "cpi"]:
        mean_, lo, hi = bootstrap_mean(thread_metrics[metric].values)
        agg_rows.append({
            "metric": metric,
            "mean": mean_,
            "ci_low": lo,
            "ci_high": hi,
            "threads": len(thread_metrics)
        })
    
    agg_df = pd.DataFrame(agg_rows)
    
    # Save results
    agg_path = RESULTS_DIR / "aggregate_metrics_studychat.csv"
    agg_df.to_csv(agg_path, index=False)
    print(f"Saved aggregate metrics -> {agg_path}")
    
    # Print results
    print(f"\nBootstrap Confidence Intervals (95%):")
    print(f"{'Metric':<8} {'Mean':<8} {'CI_Low':<8} {'CI_High':<8}")
    print("-" * 40)
    for _, row in agg_df.iterrows():
        print(f"{row['metric']:<8} {row['mean']:<8.3f} {row['ci_low']:<8.3f} {row['ci_high']:<8.3f}")
    
    # Additional statistics
    print(f"\nAdditional Statistics:")
    for metric in ["sws", "pc", "ra", "cpi"]:
        values = thread_metrics[metric]
        print(f"{metric.upper()}:")
        print(f"  Std Dev: {values.std():.3f}")
        print(f"  Median:  {values.median():.3f}")
        print(f"  Range:   [{values.min():.3f}, {values.max():.3f}]")
    
    return agg_df


if __name__ == "__main__":
    main() 