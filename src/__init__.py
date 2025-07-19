"""
StudyChat Cognitive Presence Analysis Pipeline

A comprehensive pipeline for analyzing cognitive presence in educational conversations
using LLM-based classification and CP-Bench metrics.
"""

from .pipeline import CognitivePresencePipeline, PipelineResults
from .utils.config import Config, DEFAULT_CONFIG, PRODUCTION_CONFIG, DEVELOPMENT_CONFIG

__version__ = "1.0.0"
__author__ = "StudyChat Cognitive Presence Team"

__all__ = [
    "CognitivePresencePipeline",
    "PipelineResults", 
    "Config",
    "DEFAULT_CONFIG",
    "PRODUCTION_CONFIG",
    "DEVELOPMENT_CONFIG"
] 