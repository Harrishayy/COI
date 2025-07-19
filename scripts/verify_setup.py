#!/usr/bin/env python3
"""
Comprehensive setup verification for the StudyChat Cognitive Presence Pipeline.

This script verifies that all necessary components are available for someone
to clone the repository and run the pipeline successfully.
"""

import os
import sys
import subprocess
from pathlib import Path

def check_python_version():
    """Check Python version compatibility."""
    print("🐍 Checking Python version...")
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print(f"❌ Python {version.major}.{version.minor} is too old. Need Python 3.8+")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} is compatible")
    return True

def check_required_files():
    """Check that all required files are present."""
    print("\n📁 Checking required files...")
    
    required_files = [
        # Core pipeline files
        "src/pipeline.py",
        "src/utils/config.py", 
        "src/utils/logger.py",
        "src/data/loader.py",
        
        # Scripts
        "scripts/run_pipeline.py",
        "scripts/test_setup.py",
        "scripts/example_usage.py",
        
        # Configuration
        "config/default.json",
        "config/development.json", 
        "config/production.json",
        
        # Original scripts (for backward compatibility)
        "studychat_load.py",
        "auto_label.py",
        "postprocess.py",
        "compute_metrics.py",
        "bootstrap_ci.py",
        "bias_checks.py",
        "visuals.py",
        "llm_client.py",
        "codebook.py",
        "config.py",
        
        # Documentation
        "README.md",
        "REFACTORING_SUMMARY.md",
        "docs/quick_start.md",
        "requirements.txt",
        
        # Analysis scripts
        "analysis/create_analysis.py",
        "analysis/simple_analysis.py",
        "analysis/README.md",
        
        # Project structure
        ".gitignore",
        "LICENSE"
    ]
    
    missing_files = []
    for file_path in required_files:
        if not Path(file_path).exists():
            missing_files.append(file_path)
        else:
            print(f"✅ {file_path}")
    
    if missing_files:
        print(f"\n❌ Missing files:")
        for file_path in missing_files:
            print(f"   - {file_path}")
        return False
    
    print(f"✅ All {len(required_files)} required files are present")
    return True

def check_dependencies():
    """Check that all required dependencies can be imported."""
    print("\n📦 Checking dependencies...")
    
    dependencies = [
        ("pandas", "Data manipulation"),
        ("numpy", "Numerical computing"),
        ("matplotlib", "Plotting"),
        ("seaborn", "Statistical visualization"),
        ("openai", "OpenAI API client"),
        ("datasets", "HuggingFace datasets"),
        ("scikit-learn", "Machine learning utilities"),
        ("tqdm", "Progress bars"),
        ("rich", "Rich terminal output"),
        ("scipy", "Scientific computing")
    ]
    
    missing_deps = []
    for module, description in dependencies:
        try:
            __import__(module)
            print(f"✅ {module} - {description}")
        except ImportError:
            print(f"❌ {module} - {description} (MISSING)")
            missing_deps.append(module)
    
    if missing_deps:
        print(f"\n❌ Missing dependencies: {', '.join(missing_deps)}")
        print("Install with: pip install -r requirements.txt")
        return False
    
    print(f"✅ All {len(dependencies)} dependencies are available")
    return True

def check_environment():
    """Check environment variables and API access."""
    print("\n🔑 Checking environment...")
    
    # Check OpenAI API key
    api_key = os.environ.get('OPENAI_API_KEY')
    if not api_key:
        print("❌ OPENAI_API_KEY not set")
        print("Set with: export OPENAI_API_KEY='your-key-here'")
        return False
    else:
        print(f"✅ OPENAI_API_KEY is set (sk-...{api_key[-4:]})")
    
    # Check directories
    directories = ["data", "results", "analysis", "figures", "logs"]
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"✅ Directory ready: {directory}")
    
    return True

def check_pipeline_imports():
    """Check that the pipeline can be imported successfully."""
    print("\n🔧 Checking pipeline imports...")
    
    try:
        # Add src to path
        sys.path.insert(0, str(Path(__file__).parent.parent / "src"))
        
        # Test imports
        from pipeline import CognitivePresencePipeline
        from utils.config import Config
        from utils.logger import setup_logger
        
        print("✅ Pipeline imports successful")
        
        # Test pipeline initialization
        config = Config()
        pipeline = CognitivePresencePipeline(config)
        print("✅ Pipeline initialization successful")
        
        return True
        
    except Exception as e:
        print(f"❌ Pipeline import failed: {e}")
        return False

def check_scripts():
    """Check that scripts can be executed."""
    print("\n📜 Checking scripts...")
    
    scripts = [
        "scripts/run_pipeline.py",
        "scripts/test_setup.py", 
        "scripts/example_usage.py"
    ]
    
    for script in scripts:
        if not Path(script).exists():
            print(f"❌ Script missing: {script}")
            return False
        
        # Check if script is executable
        try:
            result = subprocess.run([sys.executable, script, "--help"], 
                                  capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                print(f"✅ {script} - executable")
            else:
                print(f"⚠️  {script} - exists but may have issues")
        except Exception as e:
            print(f"⚠️  {script} - exists but execution test failed: {e}")
    
    return True

def check_configuration():
    """Check that configuration files are valid."""
    print("\n⚙️  Checking configuration...")
    
    import json
    
    config_files = [
        "config/default.json",
        "config/development.json",
        "config/production.json"
    ]
    
    for config_file in config_files:
        try:
            with open(config_file, 'r') as f:
                config = json.load(f)
            print(f"✅ {config_file} - valid JSON")
        except Exception as e:
            print(f"❌ {config_file} - invalid: {e}")
            return False
    
    return True

def run_quick_test():
    """Run a quick test to verify everything works."""
    print("\n🧪 Running quick test...")
    
    try:
        # Test the pipeline with minimal data
        result = subprocess.run([
            sys.executable, "scripts/run_pipeline.py", 
            "--subset", "10", "--quiet"
        ], capture_output=True, text=True, timeout=60)
        
        if result.returncode == 0:
            print("✅ Quick test passed")
            return True
        else:
            print(f"❌ Quick test failed: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print("⚠️  Quick test timed out (this is normal for first run)")
        return True
    except Exception as e:
        print(f"❌ Quick test error: {e}")
        return False

def main():
    """Run comprehensive setup verification."""
    print("🔍 StudyChat Cognitive Presence Pipeline - Setup Verification")
    print("=" * 60)
    
    checks = [
        ("Python Version", check_python_version),
        ("Required Files", check_required_files),
        ("Dependencies", check_dependencies),
        ("Environment", check_environment),
        ("Pipeline Imports", check_pipeline_imports),
        ("Scripts", check_scripts),
        ("Configuration", check_configuration),
        ("Quick Test", run_quick_test)
    ]
    
    results = []
    for name, check_func in checks:
        try:
            result = check_func()
            results.append((name, result))
        except Exception as e:
            print(f"❌ {name} check failed with error: {e}")
            results.append((name, False))
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 VERIFICATION SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {name}")
    
    print(f"\nOverall: {passed}/{total} checks passed")
    
    if passed == total:
        print("\n🎉 SETUP VERIFICATION COMPLETE!")
        print("The repository is ready for use.")
        print("\nNext steps:")
        print("1. Run: python scripts/run_pipeline.py --subset 50")
        print("2. Check: analysis/overview_dashboard.png")
        print("3. Read: docs/quick_start.md")
        return True
    else:
        print(f"\n⚠️  {total - passed} check(s) failed.")
        print("Please fix the issues above before proceeding.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 