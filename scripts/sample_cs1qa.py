import json
import random
from pathlib import Path
from typing import List, Dict, Any
import numpy as np
import pandas as pd
from scipy.stats import norm

from config import PROC_DIR, SEED

random.seed(SEED)
np.random.seed(SEED)

SRC_JSON = Path("filtered_dataset_uniform.json")  # original nested file
DST_JSON = Path("filtered_dataset_uniform_sample.json")  # smaller subset json (same schema)

# -----------------------------
# Helper functions
# -----------------------------

def _load_conversations() -> List[Dict[str, Any]]:
    """Read the full CS1QA JSON and return the list of conversation dicts."""
    with SRC_JSON.open() as f:
        data = json.load(f)
    # Guard against alternate top-level keys
    if isinstance(data, dict) and "conversations" in data:
        return data["conversations"]
    if isinstance(data, list):
        return data  # already a list of convos
    raise ValueError("Unexpected JSON structure in CS1QA file")


def _compute_sampling_weights(lengths: np.ndarray) -> np.ndarray:
    """Generate weights proportional to a normal pdf fitted to the observed mean/std.
    This biases sampling toward the centre of the observed length distribution,
    trimming extreme long/short conversations while still keeping shape."""
    mu = lengths.mean()
    sigma = lengths.std(ddof=0) or 1.0  # avoid div-by-zero if all equal
    pdf = norm.pdf(lengths, loc=mu, scale=sigma)
    if pdf.sum() == 0:
        return np.ones_like(pdf, dtype=float) / len(pdf)
    return pdf / pdf.sum()


def sample_cs1qa(max_conversations: int = 300) -> List[Dict[str, Any]]:
    """Return a subset of conversations whose length distribution approximates normal.

    Args:
        max_conversations: maximum number of conversations to keep.
    """
    conversations = _load_conversations()
    lengths = np.array([len(c["discourse"]) for c in conversations])

    weights = _compute_sampling_weights(lengths)

    # Draw without replacement using the computed weights
    idx = np.arange(len(conversations))
    chosen_idx = np.random.choice(idx, size=min(max_conversations, len(conversations)), replace=False, p=weights)

    subset = [conversations[i] for i in sorted(chosen_idx)]
    return subset


def export_subset(subset: List[Dict[str, Any]]):
    """Save subset as JSON and create a matching parquet with flat message rows."""
    # Save JSON --------------------------------------------------------
    with DST_JSON.open("w") as f:
        json.dump({"conversations": subset}, f, ensure_ascii=False, indent=2)
    print(f"💾 Saved reduced JSON → {DST_JSON}")

    # Flatten to DataFrame (same columns as StudyChat loader) ---------
    rows = []
    for convo in subset:
        cid = convo["conversation_id"]
        for msg in convo["discourse"]:
            rows.append({
                "dataset": "cs1qa",
                "thread_id": cid,
                "turn_index": msg["sequence_number"],
                "speaker_type": msg["speaker_role"],
                "text": msg["content"].strip()
            })
    df = pd.DataFrame(rows).sort_values(["thread_id", "turn_index"])
    out_parquet = PROC_DIR / "cs1qa_messages_sample.parquet"
    out_parquet.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(out_parquet, index=False)
    print(f"✅ Saved flattened sample → {out_parquet}  ({len(df)} messages)")


if __name__ == "__main__":
    subset = sample_cs1qa(max_conversations=300)
    export_subset(subset) 