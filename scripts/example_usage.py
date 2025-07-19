#!/usr/bin/env python3
"""
Example usage of the StudyChat Cognitive Presence Pipeline.

This script demonstrates different ways to use the pipeline for analysis.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from pipeline import CognitivePresencePipeline
from utils.config import Config, DEVELOPMENT_CONFIG, PRODUCTION_CONFIG

def example_basic_usage():
    """Example 1: Basic usage with default configuration."""
    print("=" * 60)
    print("EXAMPLE 1: Basic Usage")
    print("=" * 60)
    
    # Initialize pipeline with default config
    pipeline = CognitivePresencePipeline()
    
    # Run on small subset
    results = pipeline.run(subset_size=50)
    
    print(f"Processed {results.message_count} messages")
    print(f"CPI: {results.cpi:.3f}")
    print(f"Stage distribution: {results.stage_distribution}")

def example_custom_config():
    """Example 2: Custom configuration."""
    print("\n" + "=" * 60)
    print("EXAMPLE 2: Custom Configuration")
    print("=" * 60)
    
    # Create custom configuration
    config = Config(
        model_name="gpt-4",
        temperature=0.1,
        pilot_limit=100,
        alpha=0.6,  # Higher weight for SWS
        beta=0.2,   # Lower weight for PC
        gamma=0.2,  # Lower weight for RA
        log_level="DEBUG"
    )
    
    # Initialize pipeline with custom config
    pipeline = CognitivePresencePipeline(config)
    
    # Run pipeline
    results = pipeline.run()
    
    print(f"Custom configuration results:")
    print(f"  CPI: {results.cpi:.3f}")
    print(f"  SWS: {results.sws:.3f}")
    print(f"  PC: {results.pc:.3f}")
    print(f"  RA: {results.ra:.3f}")

def example_stage_by_stage():
    """Example 3: Running stages individually."""
    print("\n" + "=" * 60)
    print("EXAMPLE 3: Stage-by-Stage Execution")
    print("=" * 60)
    
    pipeline = CognitivePresencePipeline(DEVELOPMENT_CONFIG)
    
    # Run individual stages
    print("Loading data...")
    messages = pipeline.run_stage('load', subset_size=25)
    print(f"Loaded {len(messages)} messages")
    
    print("Classifying messages...")
    raw_classifications = pipeline.run_stage('classify', messages=messages)
    print(f"Classified {len(raw_classifications)} messages")
    
    print("Post-processing...")
    final_classifications = pipeline.run_stage('postprocess', raw_classifications=raw_classifications)
    print(f"Post-processed {len(final_classifications)} messages")
    
    print("Computing metrics...")
    thread_metrics = pipeline.run_stage('metrics', classifications=final_classifications)
    print(f"Computed metrics for {len(thread_metrics)} threads")

def example_production_run():
    """Example 4: Production configuration."""
    print("\n" + "=" * 60)
    print("EXAMPLE 4: Production Configuration")
    print("=" * 60)
    
    # Use production config (full dataset, optimized settings)
    pipeline = CognitivePresencePipeline(PRODUCTION_CONFIG)
    
    # Check status before running
    status = pipeline.get_status()
    print(f"Pipeline status: {status}")
    
    # Run with full dataset (comment out for demo)
    # results = pipeline.run()
    # print(f"Production results: CPI = {results.cpi:.3f}")

def example_error_handling():
    """Example 5: Error handling and validation."""
    print("\n" + "=" * 60)
    print("EXAMPLE 5: Error Handling")
    print("=" * 60)
    
    try:
        # Try with invalid configuration
        invalid_config = Config(
            alpha=0.8,  # These weights don't sum to 1.0
            beta=0.3,
            gamma=0.2
        )
        
        # This should raise an error
        pipeline = CognitivePresencePipeline(invalid_config)
        
    except ValueError as e:
        print(f"Caught configuration error: {e}")
        print("Using valid configuration instead...")
        
        # Use valid config
        valid_config = Config()
        pipeline = CognitivePresencePipeline(valid_config)
        
        # Run with small subset
        results = pipeline.run(subset_size=25)
        print(f"Successfully ran with valid config: CPI = {results.cpi:.3f}")

def example_analysis_access():
    """Example 6: Accessing analysis results."""
    print("\n" + "=" * 60)
    print("EXAMPLE 6: Accessing Analysis Results")
    print("=" * 60)
    
    pipeline = CognitivePresencePipeline(DEVELOPMENT_CONFIG)
    results = pipeline.run(subset_size=30)
    
    # Access detailed results
    print("Detailed Results:")
    print(f"  Messages processed: {results.message_count}")
    print(f"  Threads analyzed: {results.thread_count}")
    print(f"  Processing time: {results.processing_time:.2f}s")
    
    print("\nCP-Bench Metrics:")
    print(f"  CPI (Cognitive Presence Index): {results.cpi:.3f}")
    print(f"  SWS (Stage Weighted Score): {results.sws:.3f}")
    print(f"  PC (Progressive Coherence): {results.pc:.3f}")
    print(f"  RA (Resolution Attainment): {results.ra:.3f}")
    
    print("\nStage Distribution:")
    for stage, count in results.stage_distribution.items():
        percentage = (count / results.message_count) * 100
        stage_names = {1: "Triggering", 2: "Exploration", 3: "Integration", 4: "Resolution"}
        print(f"  {stage_names[stage]}: {count} messages ({percentage:.1f}%)")
    
    print("\nConfidence Statistics:")
    print(f"  Mean confidence: {results.confidence_stats['mean']:.1f}%")
    print(f"  Standard deviation: {results.confidence_stats['std']:.1f}%")
    print(f"  Range: {results.confidence_stats['min']:.1f}% - {results.confidence_stats['max']:.1f}%")

def main():
    """Run all examples."""
    print("📚 StudyChat Cognitive Presence Pipeline - Usage Examples")
    print("=" * 60)
    
    # Run examples
    example_basic_usage()
    example_custom_config()
    example_stage_by_stage()
    example_production_run()
    example_error_handling()
    example_analysis_access()
    
    print("\n" + "=" * 60)
    print("✅ All examples completed successfully!")
    print("\nNext steps:")
    print("  1. Try running the pipeline: python scripts/run_pipeline.py --subset 50")
    print("  2. Check the generated results in the analysis/ directory")
    print("  3. Modify configurations in config/ directory")
    print("  4. Explore the documentation in docs/ directory")

if __name__ == "__main__":
    main() 