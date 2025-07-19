#!/usr/bin/env python3
"""
Main script for running the StudyChat Cognitive Presence Analysis Pipeline.

This script provides a command-line interface for running the complete pipeline
with various options for customization and control.
"""

import argparse
import sys
import os
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

try:
    from pipeline import CognitivePresencePipeline
    from utils.config import Config, PRODUCTION_CONFIG, DEVELOPMENT_CONFIG
    from utils.logger import setup_logger
except ImportError:
    # Fallback to direct imports if package structure fails
    import sys
    sys.path.insert(0, str(Path(__file__).parent.parent))
    
    # Import the modules directly
    from src.pipeline import CognitivePresencePipeline
    from src.utils.config import Config, PRODUCTION_CONFIG, DEVELOPMENT_CONFIG
    from src.utils.logger import setup_logger

def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="StudyChat Cognitive Presence Analysis Pipeline",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run on small subset for testing
  python scripts/run_pipeline.py --subset 50

  # Run on full dataset
  python scripts/run_pipeline.py --full

  # Run with custom configuration
  python scripts/run_pipeline.py --config config/custom.json

  # Run in development mode
  python scripts/run_pipeline.py --dev

  # Run with verbose logging
  python scripts/run_pipeline.py --verbose --subset 100
        """
    )
    
    # Data options
    data_group = parser.add_mutually_exclusive_group()
    data_group.add_argument(
        "--subset", 
        type=int, 
        help="Number of messages to process (subset for testing)"
    )
    data_group.add_argument(
        "--full", 
        action="store_true", 
        help="Process the full dataset"
    )
    
    # Configuration options
    parser.add_argument(
        "--config", 
        type=str, 
        help="Path to custom configuration JSON file"
    )
    parser.add_argument(
        "--dev", 
        action="store_true", 
        help="Use development configuration (small subset, debug logging)"
    )
    parser.add_argument(
        "--prod", 
        action="store_true", 
        help="Use production configuration (full dataset, optimized settings)"
    )
    
    # Model options
    parser.add_argument(
        "--model", 
        type=str, 
        choices=["gpt-4", "gpt-3.5-turbo", "gpt-4-turbo"],
        help="OpenAI model to use for classification"
    )
    parser.add_argument(
        "--temperature", 
        type=float, 
        help="Sampling temperature for LLM (0.0-2.0)"
    )
    
    # Output options
    parser.add_argument(
        "--output-dir", 
        type=str, 
        help="Output directory for results"
    )
    parser.add_argument(
        "--no-visualization", 
        action="store_true", 
        help="Skip visualization generation"
    )
    
    # Logging options
    parser.add_argument(
        "--verbose", 
        action="store_true", 
        help="Enable verbose logging (DEBUG level)"
    )
    parser.add_argument(
        "--quiet", 
        action="store_true", 
        help="Suppress console output (ERROR level only)"
    )
    
    # Pipeline control
    parser.add_argument(
        "--stage", 
        type=str, 
        choices=["load", "classify", "postprocess", "metrics", "bootstrap", "bias", "visualize"],
        help="Run only a specific pipeline stage"
    )
    parser.add_argument(
        "--skip-stages", 
        nargs="+", 
        choices=["load", "classify", "postprocess", "metrics", "bootstrap", "bias", "visualize"],
        help="Skip specific pipeline stages"
    )
    
    # Validation
    parser.add_argument(
        "--validate-only", 
        action="store_true", 
        help="Only validate configuration and environment, don't run pipeline"
    )
    
    return parser.parse_args()

def load_config(args) -> Config:
    """
    Load configuration based on command line arguments.
    
    Args:
        args: Parsed command line arguments
        
    Returns:
        Configuration object
    """
    # Priority: custom config file > preset > environment > default
    if args.config:
        if not os.path.exists(args.config):
            raise FileNotFoundError(f"Configuration file not found: {args.config}")
        config = Config.from_file(args.config)
    elif args.dev:
        config = DEVELOPMENT_CONFIG
    elif args.prod:
        config = PRODUCTION_CONFIG
    else:
        config = Config.from_env()
    
    # Override with command line arguments
    if args.subset:
        config.pilot_limit = args.subset
    elif args.full:
        config.pilot_limit = None
    
    if args.model:
        config.model_name = args.model
    if args.temperature:
        config.temperature = args.temperature
    if args.output_dir:
        config.data_dir = args.output_dir
        config.results_dir = args.output_dir
        config.analysis_dir = args.output_dir
    
    # Set log level based on arguments
    if args.verbose:
        config.log_level = "DEBUG"
    elif args.quiet:
        config.log_level = "ERROR"
    
    return config

def validate_environment():
    """Validate that the environment is ready for the pipeline."""
    logger = setup_logger("validation")
    
    # Check OpenAI API key
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        logger.error("OPENAI_API_KEY environment variable not set")
        logger.info("Please set your OpenAI API key:")
        logger.info("  export OPENAI_API_KEY='your-api-key-here'")
        return False
    
    if not api_key.startswith("sk-"):
        logger.warning("OPENAI_API_KEY doesn't look like a valid OpenAI API key")
    
    # Check required directories
    required_dirs = ["data", "results", "analysis", "figures", "logs"]
    for directory in required_dirs:
        Path(directory).mkdir(parents=True, exist_ok=True)
        logger.debug(f"Directory ready: {directory}")
    
    # Check Python dependencies
    try:
        import pandas
        import numpy
        import matplotlib
        import openai
        logger.debug("All required Python packages available")
    except ImportError as e:
        logger.error(f"Missing required package: {e}")
        logger.info("Please install requirements: pip install -r requirements.txt")
        return False
    
    logger.info("Environment validation passed")
    return True

def main():
    """Main function."""
    # Parse arguments
    args = parse_arguments()
    
    # Set up logging
    log_level = "DEBUG" if args.verbose else "ERROR" if args.quiet else "INFO"
    logger = setup_logger("pipeline", level=log_level)
    
    try:
        # Validate environment
        logger.info("Validating environment...")
        if not validate_environment():
            sys.exit(1)
        
        # Load configuration
        logger.info("Loading configuration...")
        config = load_config(args)
        
        # Validate configuration
        logger.info("Validating configuration...")
        config.validate()
        
        if args.validate_only:
            logger.info("Configuration validation completed successfully")
            return
        
        # Initialize pipeline
        logger.info("Initializing pipeline...")
        pipeline = CognitivePresencePipeline(config)
        
        # Run pipeline
        if args.stage:
            # Run single stage
            logger.info(f"Running single stage: {args.stage}")
            result = pipeline.run_stage(args.stage)
            logger.info(f"Stage {args.stage} completed")
        else:
            # Run complete pipeline
            logger.info("Starting complete pipeline...")
            result = pipeline.run(subset_size=config.pilot_limit)
            
            # Print summary
            print("\n" + "="*60)
            print("PIPELINE RESULTS SUMMARY")
            print("="*60)
            print(f"Messages processed: {result.message_count}")
            print(f"Threads analyzed: {result.thread_count}")
            print(f"Processing time: {result.processing_time:.2f}s")
            print()
            print("CP-Bench Metrics:")
            print(f"  CPI (Cognitive Presence Index): {result.cpi:.3f}")
            print(f"  SWS (Stage Weighted Score): {result.sws:.3f}")
            print(f"  PC (Progressive Coherence): {result.pc:.3f}")
            print(f"  RA (Resolution Attainment): {result.ra:.3f}")
            print()
            print("Stage Distribution:")
            for stage, count in result.stage_distribution.items():
                percentage = (count / result.message_count) * 100
                print(f"  Stage {stage}: {count} messages ({percentage:.1f}%)")
            print()
            print("Confidence Statistics:")
            print(f"  Mean: {result.confidence_stats['mean']:.1f}%")
            print(f"  Std Dev: {result.confidence_stats['std']:.1f}%")
            print(f"  Range: {result.confidence_stats['min']:.1f}% - {result.confidence_stats['max']:.1f}%")
            print()
            print("Output Files:")
            file_paths = config.get_file_paths()
            for name, path in file_paths.items():
                if path.exists():
                    print(f"  ✓ {name}: {path}")
                else:
                    print(f"  ✗ {name}: {path} (not found)")
            print("="*60)
        
        logger.info("Pipeline completed successfully")
        
    except KeyboardInterrupt:
        logger.warning("Pipeline interrupted by user")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Pipeline failed: {str(e)}")
        if args.verbose:
            import traceback
            logger.error(traceback.format_exc())
        sys.exit(1)

if __name__ == "__main__":
    main() 