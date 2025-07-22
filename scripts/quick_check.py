#!/usr/bin/env python3
"""
Quick test script to classify 10 messages from each dataset using gpt-4o-mini.
"""

import os
import pandas as pd
import openai
import ast
import json
from pathlib import Path
from codebook import ONE_SHOT_PROMPT

# Set up OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")
MODEL = "o4-mini"

def classify_message(text: str):
    """Classify a single message using gpt-4o-mini."""
    try:
        prompt = ONE_SHOT_PROMPT.format(text=text)
        resp = openai.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": prompt}]
        )
        content = resp.choices[0].message.content
        
        # Extract JSON from response
        import re
        m = re.search(r"\{.*\}", content, re.S)
        if m:
            data = json.loads(m.group(0))
            return data.get("stage"), data.get("label"), data.get("confidence", 0)
        else:
            return None, None, 0
    except Exception as e:
        print(f"Error classifying: {e}")
        return None, None, 0

def test_dataset(path: str, dataset_name: str, n=10):
    """Test classification on a dataset."""
    print(f"\n{'='*60}")
    print(f"Testing {dataset_name} - {n} messages")
    print(f"{'='*60}")
    
    if not Path(path).exists():
        print(f"❌ File not found: {path}")
        return
    
    df = pd.read_parquet(path).head(n)
    print(f"📊 Dataset shape: {df.shape}")
    print(f"👥 Speaker types: {df['speaker_type'].value_counts().to_dict()}")
    
    results = []
    total_tokens = 0
    
    for idx, row in df.iterrows():
        text = row['text'][:200] + "..." if len(row['text']) > 200 else row['text']
        print(f"\n--- Message {idx+1} ---")
        print(f"Speaker: {row['speaker_type']}")
        print(f"Text: {text}")
        
        stage, label, confidence = classify_message(row['text'])
        
        print(f"Classification: Stage {stage} ({label}) - Confidence: {confidence}%")
        
        results.append({
            'thread_id': row['thread_id'],
            'turn_index': row['turn_index'],
            'speaker_type': row['speaker_type'],
            'stage': stage,
            'label': label,
            'confidence': confidence,
            'text_preview': text
        })
    
    # Summary
    results_df = pd.DataFrame(results)
    print(f"\n📈 Summary for {dataset_name}:")
    print(f"Stage distribution: {results_df['stage'].value_counts().sort_index().to_dict()}")
    print(f"Average confidence: {results_df['confidence'].mean():.1f}%")
    print(f"Success rate: {(results_df['stage'].notna().sum() / len(results_df)) * 100:.1f}%")
    
    return results_df

def main():
    """Run tests on both datasets."""
    print("🚀 Quick Classification Test with gpt-4o-mini")
    print("=" * 60)
    
    # Test StudyChat
    studychat_path = "data/processed/messages.parquet"
    studychat_results = test_dataset(studychat_path, "StudyChat", 10)
    
    # Test CS1QA (if sample exists)
    cs1qa_path = "data/processed/cs1qa_messages_sample.parquet"
    cs1qa_results = test_dataset(cs1qa_path, "CS1QA", 10)
    
    # Comparison
    if studychat_results is not None and cs1qa_results is not None:
        print(f"\n{'='*60}")
        print("COMPARISON SUMMARY")
        print(f"{'='*60}")
        
        print(f"\nStudyChat vs CS1QA:")
        print(f"Average confidence: {studychat_results['confidence'].mean():.1f}% vs {cs1qa_results['confidence'].mean():.1f}%")
        print(f"Success rate: {(studychat_results['stage'].notna().sum() / len(studychat_results)) * 100:.1f}% vs {(cs1qa_results['stage'].notna().sum() / len(cs1qa_results)) * 100:.1f}%")
        
        print(f"\nStage distribution comparison:")
        sc_stages = studychat_results['stage'].value_counts().sort_index()
        cs1_stages = cs1qa_results['stage'].value_counts().sort_index()
        print(f"StudyChat: {sc_stages.to_dict()}")
        print(f"CS1QA: {cs1_stages.to_dict()}")

if __name__ == "__main__":
    main() 