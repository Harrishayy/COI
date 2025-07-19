import pandas as pd
from tqdm.auto import tqdm
from config import PROC_DIR
from llm_client import setup_openai, classify_message


def batch_classify(df: pd.DataFrame) -> pd.DataFrame:
    """
    Classify all messages in the dataset.
    
    Args:
        df: DataFrame with messages to classify
        
    Returns:
        DataFrame with original data + classification results
    """
    setup_openai()
    
    rows = []
    for idx, row in tqdm(df.iterrows(), total=len(df), desc="Classifying"):
        try:
            res = classify_message(row.text)
            rows.append({
                **row.to_dict(),
                "raw_stage": res.get("stage"),
                "raw_label": res.get("label"),
                "raw_confidence": res.get("confidence"),
                "raw_rationale": res.get("rationale")
            })
        except Exception as e:
            print(f"Error classifying message {idx}: {e}")
            print(f"Text: {row.text[:100]}...")
            rows.append({
                **row.to_dict(),
                "raw_stage": None,
                "raw_label": None,
                "raw_confidence": 0,
                "raw_rationale": f"Error: {str(e)}"
            })
    
    return pd.DataFrame(rows)


def main():
    """Run batch classification on StudyChat messages."""
    raw_labels_path = PROC_DIR / "studychat_auto_raw.parquet"
    
    if raw_labels_path.exists():
        auto_raw = pd.read_parquet(raw_labels_path)
        print("Loaded existing raw labels:", len(auto_raw))
    else:
        # Load messages
        messages_path = PROC_DIR / "messages.parquet"
        if not messages_path.exists():
            print("Messages not found. Run studychat_load.py first.")
            return
        
        df = pd.read_parquet(messages_path)
        print(f"Classifying {len(df)} messages...")
        
        auto_raw = batch_classify(df)
        auto_raw.to_parquet(raw_labels_path, index=False)
        print("Saved raw labels ->", raw_labels_path)
    
    # Print summary statistics
    print(f"\nClassification Summary:")
    print(f"Total messages: {len(auto_raw)}")
    print(f"Successful classifications: {auto_raw['raw_stage'].notna().sum()}")
    print(f"Failed classifications: {auto_raw['raw_stage'].isna().sum()}")
    
    if auto_raw['raw_stage'].notna().sum() > 0:
        stage_counts = auto_raw['raw_stage'].value_counts().sort_index()
        print(f"Stage distribution: {stage_counts.to_dict()}")
        
        avg_confidence = auto_raw['raw_confidence'].mean()
        print(f"Average confidence: {avg_confidence:.1f}")
    
    return auto_raw


if __name__ == "__main__":
    main() 