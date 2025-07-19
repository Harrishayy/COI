#!/usr/bin/env python3
"""
StudyChat Cognitive Presence Pipeline Runner

This script orchestrates the complete pipeline from data loading to final results.
"""

import os
import sys
from pathlib import Path

# Add current directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

def check_environment():
    """Check if environment is properly set up."""
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ ERROR: OPENAI_API_KEY not set!")
        print("Please set your API key:")
        print("  export OPENAI_API_KEY='your-key-here'")
        return False
    
    try:
        import openai
        import pandas as pd
        import numpy as np
        import matplotlib.pyplot as plt
        from datasets import load_dataset
        print("✅ All dependencies available")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("Please install requirements: pip install -r requirements.txt")
        return False

def run_step(step_name, step_func, *args, **kwargs):
    """Run a pipeline step with error handling."""
    print(f"\n{'='*50}")
    print(f"🔄 Running: {step_name}")
    print(f"{'='*50}")
    
    try:
        result = step_func(*args, **kwargs)
        print(f"✅ Completed: {step_name}")
        return result
    except Exception as e:
        print(f"❌ Failed: {step_name}")
        print(f"Error: {e}")
        return None

def main():
    """Run the complete StudyChat Cognitive Presence pipeline."""
    print("🚀 StudyChat Cognitive Presence Pipeline")
    print("=" * 50)
    
    # Check environment
    if not check_environment():
        return 1
    
    # Import pipeline modules
    try:
        from studychat_load import main as load_data
        from auto_label import main as auto_label
        from postprocess import main as postprocess
        from compute_metrics import main as compute_metrics
        from bootstrap_ci import main as bootstrap_ci
        from visuals import main as generate_visuals
        from bias_checks import main as bias_checks
        from save_artifacts import main as save_artifacts
    except ImportError as e:
        print(f"❌ Failed to import pipeline modules: {e}")
        return 1
    
    # Pipeline steps
    steps = [
        ("Data Loading", load_data),
        ("LLM Classification", auto_label),
        ("Post-processing", postprocess),
        ("Metrics Computation", compute_metrics),
        ("Bootstrap CIs", bootstrap_ci),
        ("Visualizations", generate_visuals),
        ("Bias Analysis", bias_checks),
        ("Save Artifacts", save_artifacts),
    ]
    
    # Run pipeline
    results = {}
    for step_name, step_func in steps:
        result = run_step(step_name, step_func)
        if result is None:
            print(f"\n❌ Pipeline failed at: {step_name}")
            return 1
        results[step_name] = result
    
    # Summary
    print(f"\n{'='*50}")
    print("🎉 Pipeline completed successfully!")
    print(f"{'='*50}")
    
    print("\n📊 Results available in:")
    print("  - data/processed/ (raw and final classifications)")
    print("  - results/ (thread metrics and aggregates)")
    print("  - figures/ (visualizations)")
    print("  - labels_gold/ (gold samples for manual annotation)")
    
    print("\n📈 Next steps:")
    print("  1. Review visualizations in figures/")
    print("  2. Analyze results in results/")
    print("  3. Optionally run sample_gold.py for manual annotation")
    print("  4. Optionally run eval_model.py if you have gold labels")
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 