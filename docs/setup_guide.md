# Setup Guide for StudyChat Cognitive Presence Pipeline

This guide will help you set up and run the cognitive presence analysis pipeline from scratch.

## 🚀 Quick Setup (5 minutes)

### 1. Clone the Repository
```bash
git clone https://github.com/Harrishayy/COI.git
cd COI
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Set Your OpenAI API Key
```bash
export OPENAI_API_KEY="your-api-key-here"
```

### 4. Verify Setup
```bash
python scripts/verify_setup.py
```

### 5. Run the Pipeline
```bash
python scripts/run_pipeline.py --subset 50
```

## 📋 Detailed Setup

### Prerequisites

**Python 3.8+ Required**
```bash
python --version  # Should be 3.8 or higher
```

**OpenAI API Key**
- Get your API key from [OpenAI Platform](https://platform.openai.com/api-keys)
- Set it as an environment variable:
  ```bash
  export OPENAI_API_KEY="sk-your-key-here"
  ```

### Installation Options

#### Option 1: Using pip (Recommended)
```bash
pip install -r requirements.txt
```

#### Option 2: Using conda
```bash
conda create -n coi python=3.9
conda activate coi
pip install -r requirements.txt
```

#### Option 3: Using virtual environment
```bash
python -m venv coi_env
source coi_env/bin/activate  # On Windows: coi_env\Scripts\activate
pip install -r requirements.txt
```

### Verification Steps

Run the comprehensive verification script:
```bash
python scripts/verify_setup.py
```

This will check:
- ✅ Python version compatibility
- ✅ All required files are present
- ✅ Dependencies are installed
- ✅ Environment variables are set
- ✅ Pipeline can be imported
- ✅ Scripts are executable
- ✅ Configuration files are valid
- ✅ Quick test run

## 🧪 Testing the Setup

### Quick Test (10 messages)
```bash
python scripts/run_pipeline.py --subset 10 --quiet
```

### Small Test (50 messages)
```bash
python scripts/run_pipeline.py --subset 50
```

### Development Test (100 messages)
```bash
python scripts/run_pipeline.py --dev --subset 100
```

## 📁 Understanding the Repository Structure

```
COI/
├── 📁 src/                    # Core pipeline modules
│   ├── pipeline.py           # Main pipeline orchestrator
│   ├── data/loader.py        # Data loading utilities
│   └── utils/                # Configuration and logging
├── 📁 scripts/               # Executable scripts
│   ├── run_pipeline.py       # Main CLI interface
│   ├── test_setup.py         # Environment validation
│   └── example_usage.py      # Usage examples
├── 📁 config/                # Configuration files
│   ├── default.json          # Default settings
│   ├── development.json      # Development preset
│   └── production.json       # Production preset
├── 📁 docs/                  # Documentation
│   ├── quick_start.md        # Quick start guide
│   └── setup_guide.md        # This file
├── 📁 analysis/              # Analysis scripts
│   ├── create_analysis.py    # Comprehensive analysis
│   └── simple_analysis.py    # Simplified analysis
└── 📁 data/                  # Data storage (created automatically)
```

## 🔧 Configuration

### Environment Variables
```bash
export OPENAI_API_KEY="your-key"
export PILOT_LIMIT=100        # Subset size for testing
export MODEL_NAME="gpt-4"     # LLM model to use
export TEMPERATURE=0.1        # Sampling temperature
```

### Configuration Files
- `config/default.json` - Default settings
- `config/development.json` - Development settings (smaller subsets)
- `config/production.json` - Production settings (full dataset)

### Custom Configuration
Create your own config file:
```json
{
  "model_name": "gpt-4",
  "temperature": 0.1,
  "max_tokens": 100,
  "pilot_limit": 200
}
```

Then use it:
```bash
python scripts/run_pipeline.py --config my_config.json
```

## 🚨 Troubleshooting

### Common Issues

#### 1. OpenAI API Errors
```bash
# Check if API key is set
echo $OPENAI_API_KEY

# Test API connection
python scripts/test_setup.py
```

#### 2. Import Errors
```bash
# Check Python path
python -c "import sys; print(sys.path)"

# Install missing dependencies
pip install -r requirements.txt
```

#### 3. Memory Issues
```bash
# Use smaller subset
python scripts/run_pipeline.py --subset 25

# Reduce batch size in config
```

#### 4. Permission Errors
```bash
# Make scripts executable
chmod +x scripts/*.py

# Or run with python explicitly
python scripts/run_pipeline.py
```

### Debug Mode
```bash
# Enable verbose logging
python scripts/run_pipeline.py --verbose --subset 10

# Check logs
tail -f logs/pipeline.log
```

## 📊 Expected Outputs

After running the pipeline, you should see:

### Files Created
- `data/processed/messages.parquet` - Processed messages
- `data/processed/studychat_auto_final.parquet` - Classifications
- `results/thread_metrics_studychat.csv` - Thread-level metrics
- `results/aggregate_metrics_studychat.csv` - Aggregate metrics
- `analysis/overview_dashboard.png` - Visualization
- `analysis/results_explanation.md` - Results explanation

### Console Output
```
============================================================
PIPELINE RESULTS SUMMARY
============================================================
Messages processed: 50
Threads analyzed: 3
Processing time: 5.02s

CP-Bench Metrics:
  CPI (Cognitive Presence Index): 0.336
  SWS (Stage Weighted Score): 0.334
  PC (Progressive Coherence): 0.120
  RA (Resolution Attainment): 0.667
```

## 🎯 Next Steps

1. **Run your first analysis**: `python scripts/run_pipeline.py --subset 50`
2. **Explore results**: Check `analysis/overview_dashboard.png`
3. **Read documentation**: See `docs/quick_start.md`
4. **Customize**: Modify `config/` files
5. **Extend**: Add your own analysis scripts

## 📞 Getting Help

If you encounter issues:

1. **Check the troubleshooting section above**
2. **Run the verification script**: `python scripts/verify_setup.py`
3. **Check the logs**: Look in `logs/` directory
4. **Open an issue**: On the GitHub repository
5. **Read the documentation**: Check `docs/` directory

## ✅ Success Checklist

- [ ] Repository cloned successfully
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] OpenAI API key set (`export OPENAI_API_KEY="your-key"`)
- [ ] Setup verified (`python scripts/verify_setup.py`)
- [ ] Quick test passed (`python scripts/run_pipeline.py --subset 10`)
- [ ] Results generated (check `analysis/` directory)
- [ ] Documentation read (`docs/quick_start.md`)

Once all items are checked, you're ready to use the pipeline! 🎉 