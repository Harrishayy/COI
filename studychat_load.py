import pandas as pd
from datasets import load_dataset
from config import PROC_DIR
import os

# Get PILOT_LIMIT from environment or use default
PILOT_LIMIT = int(os.environ.get('PILOT_LIMIT', 50))


def load_studychat() -> pd.DataFrame:
    """Load StudyChat dataset and convert to DataFrame format."""
    ds = load_dataset("wmcnicho/StudyChat")
    rows = []
    for split in ds.keys():
        for convo in ds[split]:
            # Use chatId as thread_id, or generate one if not available
            convo_id = convo.get("chatId") or convo.get("id") or f"convo_{len(rows)}"
            
            # Process messages
            for idx, m in enumerate(convo["messages"]):
                rows.append({
                    "dataset": "studychat",
                    "thread_id": convo_id,
                    "turn_index": idx,
                    "speaker_type": m.get("role", "unknown"),
                    "text": (m.get("content") or "").strip()
                })
    
    df = pd.DataFrame(rows)
    df.sort_values(["thread_id", "turn_index"], inplace=True)
    return df


def main():
    """Load and save StudyChat messages to parquet."""
    messages_path = PROC_DIR / "messages.parquet"
    
    if messages_path.exists():
        df = pd.read_parquet(messages_path)
        print("Loaded cached messages:", len(df))
    else:
        print("Loading StudyChat dataset...")
        df = load_studychat()
        if PILOT_LIMIT:
            df = df.head(PILOT_LIMIT)
            print(f"Using pilot subset: {PILOT_LIMIT} messages")
        df.to_parquet(messages_path, index=False)
        print("Loaded & saved messages:", len(df), "->", messages_path)
    
    print(f"Dataset shape: {df.shape}")
    print(f"Unique threads: {df['thread_id'].nunique()}")
    print(f"Speaker types: {df['speaker_type'].value_counts().to_dict()}")
    
    return df


if __name__ == "__main__":
    main() 