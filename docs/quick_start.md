# Quick Start Guide

Get up and running with the StudyChat Cognitive Presence Analysis Pipeline in minutes!

## 🚀 5-Minute Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Set Your API Key
```bash
export OPENAI_API_KEY="your-openai-api-key-here"
```

### 3. Run a Quick Test
```bash
# Test with 50 messages (fast and cheap)
python scripts/run_pipeline.py --subset 50

# Or use development mode
python scripts/run_pipeline.py --dev
```

### 4. Check Results
```bash
# View the overview dashboard
open analysis/overview_dashboard.png

# Read the results explanation
cat analysis/results_explanation.md
```

## 📊 Understanding Your Results

After running the pipeline, you'll get:

- **CPI (Cognitive Presence Index)**: Overall measure of cognitive engagement
- **Stage Distribution**: How many messages are in each cognitive stage
- **Confidence Scores**: How reliable the classifications are
- **Visualizations**: Charts showing patterns and trends

### What the Stages Mean:
1. **Triggering**: Questions, problems, confusion
2. **Exploration**: Information seeking, brainstorming
3. **Integration**: Synthesizing ideas, explanations
4. **Resolution**: Applying solutions, confirming results

## 🔧 Common Usage Patterns

### Quick Testing
```bash
# Test with small subset
python scripts/run_pipeline.py --subset 25

# Test with different model
python scripts/run_pipeline.py --model gpt-3.5-turbo --subset 50
```

### Production Runs
```bash
# Run on full dataset
python scripts/run_pipeline.py --full

# Use production settings
python scripts/run_pipeline.py --prod
```

### Custom Analysis
```bash
# Use custom configuration
python scripts/run_pipeline.py --config config/custom.json

# Run with verbose logging
python scripts/run_pipeline.py --verbose --subset 100
```

## 🐛 Troubleshooting

### API Key Issues
```bash
# Check if API key is set
echo $OPENAI_API_KEY

# Test API connection
python scripts/test_api.py
```

### Memory Issues
```bash
# Reduce batch size
export BATCH_SIZE=5
python scripts/run_pipeline.py --subset 50
```

### Classification Failures
```bash
# Check prompt formatting
python scripts/validate_prompt.py

# Run with debug logging
python scripts/run_pipeline.py --verbose --subset 10
```

## 📈 Next Steps

1. **Scale Up**: Run on larger subsets (100-500 messages)
2. **Customize**: Modify configuration files for your needs
3. **Analyze**: Use the generated visualizations and reports
4. **Extend**: Add your own analysis scripts

## 💡 Tips

- Start with small subsets (25-50 messages) for testing
- Use `--dev` mode for debugging
- Check logs in the `logs/` directory for detailed information
- The pipeline saves intermediate results, so you can resume if interrupted

## 🆘 Need Help?

- Check the full documentation in `docs/`
- Look at example configurations in `config/`
- Review the main README for detailed information
- Open an issue if you encounter problems

---

**Ready to analyze cognitive presence in your conversations!** 🎉 