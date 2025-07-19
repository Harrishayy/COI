#!/usr/bin/env python3
"""
Configuration management for the cognitive presence pipeline.

This module provides a centralized configuration system that handles all
settings for the pipeline, including model parameters, file paths,
and analysis parameters.
"""

import os
import json
from pathlib import Path
from typing import Dict, Any, Optional
from dataclasses import dataclass, field

@dataclass
class Config:
    """
    Configuration for the cognitive presence pipeline.
    
    This class centralizes all configuration parameters and provides
    methods for loading from files and environment variables.
    """
    
    # Model Configuration
    model_name: str = "gpt-4"
    temperature: float = 0.1
    max_tokens: int = 100
    request_timeout: int = 30
    max_retries: int = 3
    retry_delay: float = 1.0
    
    # Data Configuration
    dataset_name: str = "studychat"
    pilot_limit: Optional[int] = 50
    batch_size: int = 10
    
    # CP-Bench Weights
    alpha: float = 0.5  # SWS weight
    beta: float = 0.3   # PC weight
    gamma: float = 0.2  # RA weight
    
    # Classification Configuration
    confidence_threshold: float = 0.7
    include_rationale: bool = True
    
    # Bootstrap Configuration
    bootstrap_samples: int = 1000
    confidence_level: float = 0.95
    
    # File Paths
    data_dir: str = "data"
    results_dir: str = "results"
    analysis_dir: str = "analysis"
    figures_dir: str = "figures"
    logs_dir: str = "logs"
    
    # Logging Configuration
    log_level: str = "INFO"
    log_format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # Random Seed
    random_seed: int = 42
    
    # Prompt Template
    prompt_template: str = field(default_factory=lambda: """You are a cognitive presence classifier. Classify the following message into one of four cognitive presence stages:

STAGES:
1. Triggering: Problem identification, questions, confusion, uncertainty
2. Exploration: Information seeking, brainstorming, divergent thinking, exchange of information
3. Integration: Synthesizing ideas, connecting concepts, convergent thinking, creating solutions
4. Resolution: Applying solutions, testing, confirming results, closure

CLASSIFICATION RULES:
- Classify based on the cognitive activity shown in the message
- Consider the speaker's role (user/assistant/system)
- System messages are typically Stage 1 or 4
- User questions are typically Stage 1
- Assistant explanations are typically Stage 2 or 3

MESSAGE: "{text}"
SPEAKER: {speaker_type}

Respond with JSON only:
{{
    "stage": <1-4>,
    "confidence": <0-100>,
    "rationale": "<brief explanation>"
}}""")
    
    # Codebook
    codebook: Dict[str, Any] = field(default_factory=lambda: {
        "stages": {
            "1": {
                "name": "Triggering",
                "description": "Problem identification, questions, confusion, uncertainty",
                "keywords": ["question", "problem", "confused", "uncertain", "help", "how", "what", "why"]
            },
            "2": {
                "name": "Exploration",
                "description": "Information seeking, brainstorming, divergent thinking, exchange of information",
                "keywords": ["explore", "brainstorm", "think", "consider", "maybe", "could", "might", "information"]
            },
            "3": {
                "name": "Integration",
                "description": "Synthesizing ideas, connecting concepts, convergent thinking, creating solutions",
                "keywords": ["synthesize", "connect", "combine", "therefore", "thus", "solution", "conclusion"]
            },
            "4": {
                "name": "Resolution",
                "description": "Applying solutions, testing, confirming results, closure",
                "keywords": ["apply", "test", "confirm", "works", "solved", "complete", "finished", "done"]
            }
        }
    })
    
    def __post_init__(self):
        """Post-initialization setup."""
        # Set random seed
        import random
        import numpy as np
        random.seed(self.random_seed)
        np.random.seed(self.random_seed)
        
        # Validate weights sum to 1
        weight_sum = self.alpha + self.beta + self.gamma
        if abs(weight_sum - 1.0) > 1e-6:
            raise ValueError(f"CP-Bench weights must sum to 1.0, got {weight_sum}")
    
    @classmethod
    def from_file(cls, filepath: str) -> "Config":
        """
        Load configuration from a JSON file.
        
        Args:
            filepath: Path to JSON configuration file
            
        Returns:
            Config object with loaded settings
        """
        with open(filepath, 'r') as f:
            config_dict = json.load(f)
        
        return cls(**config_dict)
    
    @classmethod
    def from_env(cls) -> "Config":
        """
        Load configuration from environment variables.
        
        Returns:
            Config object with environment-based settings
        """
        config = cls()
        
        # Model settings
        if os.getenv('MODEL_NAME'):
            config.model_name = os.getenv('MODEL_NAME')
        if os.getenv('TEMPERATURE'):
            config.temperature = float(os.getenv('TEMPERATURE'))
        if os.getenv('MAX_TOKENS'):
            config.max_tokens = int(os.getenv('MAX_TOKENS'))
        
        # Data settings
        if os.getenv('PILOT_LIMIT'):
            config.pilot_limit = int(os.getenv('PILOT_LIMIT'))
        if os.getenv('BATCH_SIZE'):
            config.batch_size = int(os.getenv('BATCH_SIZE'))
        
        # CP-Bench weights
        if os.getenv('ALPHA'):
            config.alpha = float(os.getenv('ALPHA'))
        if os.getenv('BETA'):
            config.beta = float(os.getenv('BETA'))
        if os.getenv('GAMMA'):
            config.gamma = float(os.getenv('GAMMA'))
        
        # Other settings
        if os.getenv('CONFIDENCE_THRESHOLD'):
            config.confidence_threshold = float(os.getenv('CONFIDENCE_THRESHOLD'))
        if os.getenv('LOG_LEVEL'):
            config.log_level = os.getenv('LOG_LEVEL')
        if os.getenv('RANDOM_SEED'):
            config.random_seed = int(os.getenv('RANDOM_SEED'))
        
        return config
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert configuration to dictionary.
        
        Returns:
            Dictionary representation of configuration
        """
        return {
            'model_name': self.model_name,
            'temperature': self.temperature,
            'max_tokens': self.max_tokens,
            'request_timeout': self.request_timeout,
            'max_retries': self.max_retries,
            'retry_delay': self.retry_delay,
            'dataset_name': self.dataset_name,
            'pilot_limit': self.pilot_limit,
            'batch_size': self.batch_size,
            'alpha': self.alpha,
            'beta': self.beta,
            'gamma': self.gamma,
            'confidence_threshold': self.confidence_threshold,
            'include_rationale': self.include_rationale,
            'bootstrap_samples': self.bootstrap_samples,
            'confidence_level': self.confidence_level,
            'data_dir': self.data_dir,
            'results_dir': self.results_dir,
            'analysis_dir': self.analysis_dir,
            'figures_dir': self.figures_dir,
            'logs_dir': self.logs_dir,
            'log_level': self.log_level,
            'log_format': self.log_format,
            'random_seed': self.random_seed
        }
    
    def save(self, filepath: str):
        """
        Save configuration to a JSON file.
        
        Args:
            filepath: Path to save configuration file
        """
        with open(filepath, 'w') as f:
            json.dump(self.to_dict(), f, indent=2)
    
    def get_file_paths(self) -> Dict[str, Path]:
        """
        Get all file paths used by the pipeline.
        
        Returns:
            Dictionary mapping path names to Path objects
        """
        return {
            'messages': Path(self.data_dir) / 'processed' / 'messages.parquet',
            'raw_classifications': Path(self.data_dir) / 'processed' / 'studychat_auto_raw.parquet',
            'final_classifications': Path(self.data_dir) / 'processed' / 'studychat_auto_final.parquet',
            'thread_metrics': Path(self.results_dir) / 'thread_metrics_studychat.csv',
            'aggregate_metrics': Path(self.results_dir) / 'aggregate_metrics_studychat.csv',
            'role_stage_distribution': Path(self.results_dir) / 'role_stage_distribution.csv',
            'overview_dashboard': Path(self.analysis_dir) / 'overview_dashboard.png',
            'detailed_analysis': Path(self.analysis_dir) / 'detailed_analysis.png',
            'results_explanation': Path(self.analysis_dir) / 'results_explanation.md'
        }
    
    def validate(self) -> bool:
        """
        Validate configuration settings.
        
        Returns:
            True if configuration is valid, raises ValueError otherwise
        """
        # Check model name
        valid_models = ['gpt-4', 'gpt-3.5-turbo', 'gpt-4-turbo']
        if self.model_name not in valid_models:
            raise ValueError(f"Invalid model name: {self.model_name}. Valid options: {valid_models}")
        
        # Check temperature
        if not 0 <= self.temperature <= 2:
            raise ValueError(f"Temperature must be between 0 and 2, got {self.temperature}")
        
        # Check max tokens
        if self.max_tokens <= 0:
            raise ValueError(f"Max tokens must be positive, got {self.max_tokens}")
        
        # Check weights
        if not 0 <= self.alpha <= 1:
            raise ValueError(f"Alpha must be between 0 and 1, got {self.alpha}")
        if not 0 <= self.beta <= 1:
            raise ValueError(f"Beta must be between 0 and 1, got {self.beta}")
        if not 0 <= self.gamma <= 1:
            raise ValueError(f"Gamma must be between 0 and 1, got {self.gamma}")
        
        # Check confidence threshold
        if not 0 <= self.confidence_threshold <= 1:
            raise ValueError(f"Confidence threshold must be between 0 and 1, got {self.confidence_threshold}")
        
        # Check bootstrap settings
        if self.bootstrap_samples <= 0:
            raise ValueError(f"Bootstrap samples must be positive, got {self.bootstrap_samples}")
        if not 0 < self.confidence_level < 1:
            raise ValueError(f"Confidence level must be between 0 and 1, got {self.confidence_level}")
        
        return True

# Default configurations
DEFAULT_CONFIG = Config()

PRODUCTION_CONFIG = Config(
    model_name="gpt-4",
    temperature=0.1,
    max_tokens=100,
    pilot_limit=None,  # Full dataset
    batch_size=20,
    log_level="INFO"
)

DEVELOPMENT_CONFIG = Config(
    model_name="gpt-4",
    temperature=0.1,
    max_tokens=100,
    pilot_limit=50,  # Small subset for testing
    batch_size=5,
    log_level="DEBUG"
) 