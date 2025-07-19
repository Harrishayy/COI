#!/usr/bin/env python3
"""
Test script to verify StudyChat Cognitive Presence pipeline installation.
"""

import os
import sys
from pathlib import Path

def test_imports():
    """Test that all required modules can be imported."""
    print("🔍 Testing imports...")
    
    try:
        import pandas as pd
        print("✅ pandas")
    except ImportError:
        print("❌ pandas")
        return False
    
    try:
        import numpy as np
        print("✅ numpy")
    except ImportError:
        print("❌ numpy")
        return False
    
    try:
        import matplotlib.pyplot as plt
        print("✅ matplotlib")
    except ImportError:
        print("❌ matplotlib")
        return False
    
    try:
        from datasets import load_dataset
        print("✅ datasets")
    except ImportError:
        print("❌ datasets")
        return False
    
    try:
        import openai
        print("✅ openai")
    except ImportError:
        print("❌ openai")
        return False
    
    try:
        from sklearn.metrics import classification_report
        print("✅ scikit-learn")
    except ImportError:
        print("❌ scikit-learn")
        return False
    
    try:
        from tqdm.auto import tqdm
        print("✅ tqdm")
    except ImportError:
        print("❌ tqdm")
        return False
    
    return True

def test_config():
    """Test configuration loading."""
    print("\n🔍 Testing configuration...")
    
    try:
        from config import OPENAI_MODEL, ALPHA, BETA, GAMMA
        print(f"✅ Configuration loaded")
        print(f"   Model: {OPENAI_MODEL}")
        print(f"   Weights: α={ALPHA}, β={BETA}, γ={GAMMA}")
        return True
    except ImportError as e:
        print(f"❌ Configuration error: {e}")
        return False

def test_codebook():
    """Test codebook loading."""
    print("\n🔍 Testing codebook...")
    
    try:
        from codebook import CODEBOOK_MIN, ONE_SHOT_PROMPT
        print(f"✅ Codebook loaded")
        print(f"   Stages: {len(CODEBOOK_MIN)}")
        print(f"   Prompt length: {len(ONE_SHOT_PROMPT)} chars")
        return True
    except ImportError as e:
        print(f"❌ Codebook error: {e}")
        return False

def test_directories():
    """Test directory creation."""
    print("\n🔍 Testing directory structure...")
    
    try:
        from config import DATA_DIR, PROC_DIR, RESULTS_DIR, FIG_DIR, LABELS_DIR
        
        dirs = [DATA_DIR, PROC_DIR, RESULTS_DIR, FIG_DIR, LABELS_DIR]
        for d in dirs:
            d.mkdir(parents=True, exist_ok=True)
            print(f"✅ {d}")
        
        return True
    except Exception as e:
        print(f"❌ Directory error: {e}")
        return False

def test_api_key():
    """Test OpenAI API key."""
    print("\n🔍 Testing OpenAI API key...")
    
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ OPENAI_API_KEY not set")
        print("   Please set: export OPENAI_API_KEY='your-key-here'")
        return False
    
    if not api_key.startswith("sk-"):
        print("❌ Invalid API key format")
        return False
    
    print("✅ API key found")
    return True

def main():
    """Run all tests."""
    print("🧪 StudyChat Cognitive Presence Pipeline - Installation Test")
    print("=" * 60)
    
    tests = [
        ("Imports", test_imports),
        ("Configuration", test_config),
        ("Codebook", test_codebook),
        ("Directories", test_directories),
        ("API Key", test_api_key),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {e}")
            results.append((test_name, False))
    
    # Summary
    print(f"\n{'='*60}")
    print("📊 Test Results:")
    print(f"{'='*60}")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {test_name:<15} {status}")
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Pipeline is ready to run.")
        print("\nNext steps:")
        print("  1. Run: python run_pipeline.py")
        print("  2. Or use individual scripts: python studychat_load.py")
        return 0
    else:
        print("❌ Some tests failed. Please fix issues before running pipeline.")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 