#!/usr/bin/env python3
"""
Main pipeline for StudyChat Cognitive Presence Analysis.

This module provides a unified interface for running the complete cognitive presence
analysis pipeline, from data loading through classification to final analysis.
"""

import logging
import os
import sys
from pathlib import Path
from typing import Optional, Dict, Any
from dataclasses import dataclass

# Add current directory to path for existing scripts
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from .utils.config import Config
    from .utils.logger import setup_logger
except ImportError:
    # Fallback for direct execution
    from utils.config import Config
    from utils.logger import setup_logger

@dataclass
class PipelineResults:
    """Results from the cognitive presence pipeline."""
    cpi: float
    sws: float
    pc: float
    ra: float
    stage_distribution: Dict[int, int]
    confidence_stats: Dict[str, float]
    thread_count: int
    message_count: int
    processing_time: float

class CognitivePresencePipeline:
    """
    Main pipeline for cognitive presence analysis.
    
    This class orchestrates the complete workflow:
    1. Data loading and preprocessing
    2. LLM-based classification
    3. Post-processing and validation
    4. Metrics computation
    5. Analysis and visualization
    """
    
    def __init__(self, config: Optional[Config] = None):
        """
        Initialize the pipeline.
        
        Args:
            config: Configuration object. If None, uses default config.
        """
        self.config = config or Config()
        self.logger = setup_logger(__name__)
        
        # Ensure output directories exist
        self._create_directories()
    
    def _create_directories(self):
        """Create necessary output directories."""
        directories = [
            "data/processed",
            "results",
            "analysis",
            "figures",
            "logs"
        ]
        
        for directory in directories:
            Path(directory).mkdir(parents=True, exist_ok=True)
    
    def run(self, subset_size: Optional[int] = None) -> PipelineResults:
        """
        Run the complete cognitive presence analysis pipeline.
        
        Args:
            subset_size: Number of messages to process. If None, uses config default.
            
        Returns:
            PipelineResults object containing all results.
        """
        import time
        start_time = time.time()
        
        self.logger.info("Starting cognitive presence analysis pipeline")
        
        try:
            # Stage 1: Data Loading
            self.logger.info("Stage 1: Loading and preprocessing data")
            messages = self.run_stage('load', subset_size=subset_size)
            
            # Stage 2: Classification
            self.logger.info("Stage 2: Classifying messages with LLM")
            raw_classifications = self.run_stage('classify', messages=messages)
            
            # Stage 3: Post-processing
            self.logger.info("Stage 3: Post-processing classifications")
            final_classifications = self.run_stage('postprocess', raw_classifications=raw_classifications)
            
            # Stage 4: Metrics Computation
            self.logger.info("Stage 4: Computing CP-Bench metrics")
            thread_metrics = self.run_stage('metrics', classifications=final_classifications)
            
            # Stage 5: Bootstrap Analysis
            self.logger.info("Stage 5: Computing bootstrap confidence intervals")
            aggregate_metrics = self.run_stage('bootstrap', thread_metrics=thread_metrics)
            
            # Stage 6: Bias Analysis
            self.logger.info("Stage 6: Analyzing role-based bias")
            bias_results = self.run_stage('bias', classifications=final_classifications)
            
            # Stage 7: Visualization
            self.logger.info("Stage 7: Generating visualizations and analysis")
            self.run_stage('visualize', classifications=final_classifications, 
                          thread_metrics=thread_metrics, aggregate_metrics=aggregate_metrics,
                          bias_results=bias_results)
            
            # Stage 8: Save Artifacts
            self.logger.info("Stage 8: Saving reproducibility artifacts")
            self._save_artifacts()
            
            processing_time = time.time() - start_time
            
            # Compile results
            results = PipelineResults(
                cpi=aggregate_metrics['cpi']['mean'],
                sws=aggregate_metrics['sws']['mean'],
                pc=aggregate_metrics['pc']['mean'],
                ra=aggregate_metrics['ra']['mean'],
                stage_distribution=final_classifications['final_stage'].value_counts().to_dict(),
                confidence_stats={
                    'mean': final_classifications['raw_confidence'].mean(),
                    'std': final_classifications['raw_confidence'].std(),
                    'min': final_classifications['raw_confidence'].min(),
                    'max': final_classifications['raw_confidence'].max()
                },
                thread_count=len(thread_metrics),
                message_count=len(final_classifications),
                processing_time=processing_time
            )
            
            self.logger.info(f"Pipeline completed successfully in {processing_time:.2f}s")
            self.logger.info(f"Processed {results.message_count} messages across {results.thread_count} threads")
            self.logger.info(f"CPI: {results.cpi:.3f}, SWS: {results.sws:.3f}, PC: {results.pc:.3f}, RA: {results.ra:.3f}")
            
            return results
            
        except Exception as e:
            self.logger.error(f"Pipeline failed: {str(e)}")
            raise
    
    def run_stage(self, stage: str, **kwargs) -> Any:
        """
        Run a specific pipeline stage.
        
        Args:
            stage: Stage name ('load', 'classify', 'postprocess', 'metrics', 'bootstrap', 'bias', 'visualize')
            **kwargs: Stage-specific arguments
            
        Returns:
            Stage-specific results
        """
        stages = {
            'load': self._run_load,
            'classify': self._run_classify,
            'postprocess': self._run_postprocess,
            'metrics': self._run_metrics,
            'bootstrap': self._run_bootstrap,
            'bias': self._run_bias,
            'visualize': self._run_visualize
        }
        
        if stage not in stages:
            raise ValueError(f"Unknown stage: {stage}. Available stages: {list(stages.keys())}")
        
        return stages[stage](**kwargs)
    
    def _run_load(self, subset_size: Optional[int] = None):
        """Run data loading stage using existing script."""
        import subprocess
        import os
        import pathlib
        
        # Set environment variable to override PILOT_LIMIT
        env = os.environ.copy()
        if subset_size:
            env['PILOT_LIMIT'] = str(subset_size)
            # Force fresh load by removing all cached files
            cached_files = [
                pathlib.Path("data/processed/messages.parquet"),
                pathlib.Path("data/processed/studychat_auto_raw.parquet"),
                pathlib.Path("data/processed/studychat_auto_final.parquet")
            ]
            for cached_file in cached_files:
                if cached_file.exists():
                    cached_file.unlink()
        
        # Run the existing data loading script with modified environment
        cmd = ["python3", "studychat_load.py"]
        result = subprocess.run(cmd, capture_output=True, text=True, env=env)
        
        if result.returncode != 0:
            raise RuntimeError(f"Data loading failed: {result.stderr}")
        
        # Load the processed data
        import pandas as pd
        messages = pd.read_parquet("data/processed/messages.parquet")
        return messages
    
    def _run_classify(self, messages):
        """Run classification stage using existing script."""
        import subprocess
        
        # Run the existing classification script
        cmd = ["python3", "auto_label.py"]
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode != 0:
            raise RuntimeError(f"Classification failed: {result.stderr}")
        
        # Load the raw classifications
        import pandas as pd
        raw_classifications = pd.read_parquet("data/processed/studychat_auto_raw.parquet")
        return raw_classifications
    
    def _run_postprocess(self, raw_classifications):
        """Run post-processing stage using existing script."""
        import subprocess
        
        # Run the existing post-processing script
        cmd = ["python3", "postprocess.py"]
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode != 0:
            raise RuntimeError(f"Post-processing failed: {result.stderr}")
        
        # Load the final classifications
        import pandas as pd
        final_classifications = pd.read_parquet("data/processed/studychat_auto_final.parquet")
        return final_classifications
    
    def _run_metrics(self, classifications):
        """Run metrics computation stage using existing script."""
        import subprocess
        
        # Run the existing metrics script
        cmd = ["python3", "compute_metrics.py"]
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode != 0:
            raise RuntimeError(f"Metrics computation failed: {result.stderr}")
        
        # Load the thread metrics
        import pandas as pd
        thread_metrics = pd.read_csv("results/thread_metrics_studychat.csv")
        return thread_metrics
    
    def _run_bootstrap(self, thread_metrics):
        """Run bootstrap analysis stage using existing script."""
        import subprocess
        
        # Run the existing bootstrap script
        cmd = ["python3", "bootstrap_ci.py"]
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode != 0:
            raise RuntimeError(f"Bootstrap analysis failed: {result.stderr}")
        
        # Load the aggregate metrics
        import pandas as pd
        aggregate_metrics = pd.read_csv("results/aggregate_metrics_studychat.csv")
        
        # Convert to expected format
        metrics_dict = {}
        for _, row in aggregate_metrics.iterrows():
            metrics_dict[row['metric']] = {
                'mean': row['mean'],
                'ci_low': row['ci_low'],
                'ci_high': row['ci_high']
            }
        
        return metrics_dict
    
    def _run_bias(self, classifications):
        """Run bias analysis stage using existing script."""
        import subprocess
        
        # Run the existing bias analysis script
        cmd = ["python3", "bias_checks.py"]
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode != 0:
            raise RuntimeError(f"Bias analysis failed: {result.stderr}")
        
        # Load the bias results
        import pandas as pd
        bias_results = pd.read_csv("results/role_stage_distribution.csv")
        return bias_results
    
    def _run_visualize(self, classifications, thread_metrics, aggregate_metrics, bias_results):
        """Run visualization stage using existing script."""
        import subprocess
        
        # Run the existing visualization script
        cmd = ["python3", "visuals.py"]
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode != 0:
            raise RuntimeError(f"Visualization failed: {result.stderr}")
        
        return True
    
    def _save_artifacts(self):
        """Save reproducibility artifacts."""
        import subprocess
        
        # Run the existing artifacts script
        cmd = ["python3", "save_artifacts.py"]
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode != 0:
            self.logger.warning(f"Artifact saving failed: {result.stderr}")
        else:
            self.logger.info("Saved reproducibility artifacts")
    
    def get_status(self) -> Dict[str, Any]:
        """
        Get current pipeline status and configuration.
        
        Returns:
            Dictionary with pipeline status information
        """
        return {
            'config': {
                'model_name': self.config.model_name,
                'pilot_limit': self.config.pilot_limit,
                'temperature': self.config.temperature
            },
            'directories': {
                'data': Path('data/processed').exists(),
                'results': Path('results').exists(),
                'analysis': Path('analysis').exists(),
                'figures': Path('figures').exists()
            },
            'files': {
                'messages': Path('data/processed/messages.parquet').exists(),
                'raw_classifications': Path('data/processed/studychat_auto_raw.parquet').exists(),
                'final_classifications': Path('data/processed/studychat_auto_final.parquet').exists()
            }
        } 