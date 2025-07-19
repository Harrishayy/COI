#!/usr/bin/env python3
"""
Test script for validating the StudyChat Cognitive Presence Pipeline setup.

This script checks all dependencies, configuration, and environment variables
to ensure the pipeline is ready to run.
"""

import sys
import os
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

def test_imports():
    """Test that all required packages can be imported."""
    print("🔍 Testing package imports...")
    
    required_packages = [
        ("pandas", "Data manipulation"),
        ("numpy", "Numerical computing"),
        ("matplotlib", "Plotting"),
        ("seaborn", "Statistical visualization"),
        ("openai", "OpenAI API client"),
        ("huggingface_hub", "HuggingFace datasets"),
        ("scikit-learn", "Machine learning utilities"),
        ("tqdm", "Progress bars")
    ]
    
    failed_imports = []
    
    for package, description in required_packages:
        try:
            __import__(package)
            print(f"  ✅ {package} - {description}")
        except ImportError as e:
            print(f"  ❌ {package} - {description} (Error: {e})")
            failed_imports.append(package)
    
    if failed_imports:
        print(f"\n❌ Missing packages: {', '.join(failed_imports)}")
        print("Please install missing packages:")
        print("  pip install -r requirements.txt")
        return False
    
    print("✅ All required packages available")
    return True

def test_environment():
    """Test environment variables and configuration."""
    print("\n🔍 Testing environment...")
    
    # Check OpenAI API key
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("  ❌ OPENAI_API_KEY not set")
        print("  Please set your OpenAI API key:")
        print("    export OPENAI_API_KEY='your-api-key-here'")
        return False
    else:
        print(f"  ✅ OPENAI_API_KEY is set ({api_key[:10]}...)")
    
    # Check directories
    required_dirs = ["data", "results", "analysis", "figures", "logs"]
    for directory in required_dirs:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"  ✅ Directory ready: {directory}")
    
    print("✅ Environment validation passed")
    return True

def test_configuration():
    """Test configuration loading and validation."""
    print("\n🔍 Testing configuration...")
    
    try:
        from utils.config import Config, DEFAULT_CONFIG
        
        # Test default config
        config = DEFAULT_CONFIG
        config.validate()
        print("  ✅ Default configuration is valid")
        
        # Test environment config
        env_config = Config.from_env()
        env_config.validate()
        print("  ✅ Environment configuration is valid")
        
        # Test file paths
        file_paths = config.get_file_paths()
        print(f"  ✅ File paths configured ({len(file_paths)} paths)")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Configuration error: {e}")
        return False

def test_api_connection():
    """Test OpenAI API connection."""
    print("\n🔍 Testing OpenAI API connection...")
    
    try:
        import openai
        
        # Test simple API call
        client = openai.OpenAI()
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "Hello"}],
            max_tokens=5
        )
        
        if response.choices:
            print("  ✅ OpenAI API connection successful")
            return True
        else:
            print("  ❌ OpenAI API returned empty response")
            return False
            
    except Exception as e:
        print(f"  ❌ OpenAI API connection failed: {e}")
        print("  Please check your API key and internet connection")
        return False

def test_data_access():
    """Test access to StudyChat dataset."""
    print("\n🔍 Testing dataset access...")
    
    try:
        from datasets import load_dataset
        
        # Try to load a small sample
        dataset = load_dataset("studychat", split="train", streaming=True)
        sample = next(iter(dataset))
        
        print("  ✅ StudyChat dataset accessible")
        print(f"  ✅ Sample data structure: {list(sample.keys())}")
        return True
        
    except Exception as e:
        print(f"  ❌ Dataset access failed: {e}")
        print("  This might be a network issue or dataset availability problem")
        return False

def test_pipeline_components():
    """Test that pipeline components can be imported."""
    print("\n🔍 Testing pipeline components...")
    
    try:
        # Test main pipeline
        from pipeline import CognitivePresencePipeline
        print("  ✅ Main pipeline component")
        
        # Test configuration
        from utils.config import Config
        print("  ✅ Configuration component")
        
        # Test logger
        from utils.logger import setup_logger
        print("  ✅ Logging component")
        
        print("✅ All pipeline components available")
        return True
        
    except Exception as e:
        print(f"  ❌ Pipeline component error: {e}")
        return False

def run_quick_test():
    """Run a quick test of the pipeline."""
    print("\n🔍 Running quick pipeline test...")
    
    try:
        from pipeline import CognitivePresencePipeline
        from utils.config import DEVELOPMENT_CONFIG
        
        # Initialize pipeline with development config
        pipeline = CognitivePresencePipeline(DEVELOPMENT_CONFIG)
        
        # Test status
        status = pipeline.get_status()
        print("  ✅ Pipeline initialized successfully")
        print(f"  ✅ Configuration: {status['config']}")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Pipeline test failed: {e}")
        return False

def main():
    """Run all tests."""
    print("🧪 StudyChat Cognitive Presence Pipeline - Setup Test")
    print("=" * 60)
    
    tests = [
        ("Package Imports", test_imports),
        ("Environment", test_environment),
        ("Configuration", test_configuration),
        ("OpenAI API", test_api_connection),
        ("Dataset Access", test_data_access),
        ("Pipeline Components", test_pipeline_components),
        ("Quick Pipeline Test", run_quick_test)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"  ❌ {test_name} failed with exception: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 TEST SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! Your setup is ready.")
        print("\nNext steps:")
        print("  1. Run a quick test: python scripts/run_pipeline.py --subset 50")
        print("  2. Check the quick start guide: docs/quick_start.md")
        print("  3. Review the main README for detailed usage")
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Please fix the issues above.")
        print("\nCommon solutions:")
        print("  1. Install missing packages: pip install -r requirements.txt")
        print("  2. Set your API key: export OPENAI_API_KEY='your-key'")
        print("  3. Check your internet connection")
        print("  4. Review the troubleshooting section in the README")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 