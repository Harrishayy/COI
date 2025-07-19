#!/usr/bin/env python3
"""
Data loading and preprocessing for the StudyChat dataset.
"""

import pandas as pd
from pathlib import Path
from typing import Optional
from datasets import load_dataset
from ..utils.logger import setup_logger

class StudyChatLoader:
    """Load and preprocess StudyChat dataset."""
    
    def __init__(self, config):
        """Initialize loader with configuration."""
        self.config = config
        self.logger = setup_logger(__name__)
    
    def load(self, subset_size: Optional[int] = None) -> pd.DataFrame:
        """
        Load StudyChat dataset and preprocess.
        
        Args:
            subset_size: Number of messages to load (None for full dataset)
            
        Returns:
            DataFrame with processed messages
        """
        self.logger.info("Loading StudyChat dataset...")
        
        # Load dataset from HuggingFace
        try:
            dataset = load_dataset("studychat", split="train")
            self.logger.info(f"Loaded {len(dataset)} messages from StudyChat")
        except Exception as e:
            self.logger.error(f"Failed to load StudyChat dataset: {e}")
            # Fallback to existing processed data if available
            processed_path = Path(self.config.data_dir) / "processed" / "messages.parquet"
            if processed_path.exists():
                self.logger.info("Using existing processed data")
                return pd.read_parquet(processed_path)
            else:
                raise e
        
        # Convert to DataFrame
        df = pd.DataFrame(dataset)
        
        # Apply subset if specified
        if subset_size:
            df = df.head(subset_size)
            self.logger.info(f"Using subset of {len(df)} messages")
        
        # Basic preprocessing
        df = self._preprocess(df)
        
        # Save processed data
        output_path = Path(self.config.data_dir) / "processed" / "messages.parquet"
        output_path.parent.mkdir(parents=True, exist_ok=True)
        df.to_parquet(output_path)
        
        self.logger.info(f"Saved {len(df)} processed messages to {output_path}")
        return df
    
    def _preprocess(self, df: pd.DataFrame) -> pd.DataFrame:
        """Preprocess the dataset."""
        # Ensure required columns exist
        required_columns = ['text', 'speaker_type', 'chatId']
        
        # Map dataset columns to expected format
        column_mapping = {
            'message': 'text',
            'role': 'speaker_type',
            'thread_id': 'chatId'
        }
        
        # Rename columns if needed
        for old_col, new_col in column_mapping.items():
            if old_col in df.columns and new_col not in df.columns:
                df = df.rename(columns={old_col: new_col})
        
        # Add missing columns with defaults
        if 'text' not in df.columns:
            df['text'] = df.get('message', '')
        if 'speaker_type' not in df.columns:
            df['speaker_type'] = df.get('role', 'user')
        if 'chatId' not in df.columns:
            df['chatId'] = df.get('thread_id', 'default')
        
        # Add turn index
        df['turn_index'] = range(len(df))
        
        # Add dataset identifier
        df['dataset'] = 'studychat'
        
        # Ensure text is string
        df['text'] = df['text'].astype(str)
        
        return df 