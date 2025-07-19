import pandas as pd
from tqdm.auto import tqdm
from config import PROC_DIR
from llm_client import setup_openai, classify_message


def classify_with_context(df, context_turns=1):
    """
    Re-classify using previous N turns as additional context.
    
    Args:
        df: DataFrame with messages
        context_turns: Number of previous turns to include as context
        
    Returns:
        DataFrame with context-based classifications
    """
    setup_openai()
    
    rows = []
    for _, row in tqdm(df.iterrows(), total=len(df), desc=f"Context classify (N={context_turns})"):
        thread = df[df.thread_id == row.thread_id].sort_values("turn_index")
        prev = thread[thread.turn_index < row.turn_index].tail(context_turns)["text"].tolist()
        
        # Join context with current message
        joined = ("\n".join(prev + [row.text])) if prev else row.text
        
        res = classify_message(joined)
        rows.append({
            **row.to_dict(),
            "ctx_stage": res.get("stage"),
            "ctx_label": res.get("label"),
            "ctx_confidence": res.get("confidence"),
            "ctx_rationale": res.get("rationale")
        })
    
    return pd.DataFrame(rows)


def main():
    """Run context-based reclassification (pilot version)."""
    final_labels_path = PROC_DIR / "studychat_auto_final.parquet"
    
    if not final_labels_path.exists():
        print("Final labels not found. Run postprocess.py first.")
        return
    
    auto_final = pd.read_parquet(final_labels_path)
    
    # For pilot, use only first 300 messages to control cost
    pilot_df = auto_final.head(300)
    print(f"Running context-based classification on {len(pilot_df)} messages...")
    
    # Run with 1-turn context
    ctx_df = classify_with_context(pilot_df, context_turns=1)
    
    # Save results
    ctx_path = PROC_DIR / "studychat_context_variant.parquet"
    ctx_df.to_parquet(ctx_path, index=False)
    print(f"Saved context variant results -> {ctx_path}")
    
    # Compare results
    print(f"\nComparison (original vs context):")
    print(f"Original stage distribution: {pilot_df['final_stage'].value_counts().sort_index().to_dict()}")
    print(f"Context stage distribution: {ctx_df['ctx_stage'].value_counts().sort_index().to_dict()}")
    
    # Agreement analysis
    agreement = (pilot_df['final_stage'] == ctx_df['ctx_stage']).mean()
    print(f"Agreement rate: {agreement:.3f}")
    
    # Confidence comparison
    if 'raw_confidence' in pilot_df.columns and 'ctx_confidence' in ctx_df.columns:
        orig_conf = pilot_df['raw_confidence'].mean()
        ctx_conf = ctx_df['ctx_confidence'].mean()
        print(f"Average confidence - Original: {orig_conf:.1f}, Context: {ctx_conf:.1f}")
    
    return ctx_df


if __name__ == "__main__":
    main() 