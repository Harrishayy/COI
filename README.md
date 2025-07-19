# StudyChat Cognitive Presence Analysis Pipeline

A comprehensive pipeline for analyzing cognitive presence in educational conversations using LLM-based classification and CP-Bench metrics.

## 🏗️ Project Structure

```
COI/
├── 📁 src/                    # Core pipeline modules
│   ├── data/                  # Data loading and processing
│   ├── classification/        # LLM classification components
│   ├── evaluation/           # Metrics and evaluation
│   ├── visualization/        # Plotting and analysis
│   └── utils/               # Utilities and helpers
├── 📁 config/               # Configuration files
├── 📁 data/                 # Data storage
│   ├── raw/                 # Original datasets
│   └── processed/           # Processed data
├── 📁 results/              # Pipeline outputs
├── 📁 analysis/             # Analysis and visualizations
├── 📁 notebooks/            # Jupyter notebooks
├── 📁 scripts/              # Standalone scripts
└── 📁 docs/                 # Documentation
```

## 🚀 Quick Start

### 1. Installation
```bash
# Clone the repository
git clone <repository-url>
cd COI

# Install dependencies
pip install -r requirements.txt

# Set your OpenAI API key
export OPENAI_API_KEY="your-api-key-here"
```

### 2. Run the Complete Pipeline
```bash
# Run the entire pipeline on a subset
python scripts/run_pipeline.py --subset 100

# Run on full dataset
python scripts/run_pipeline.py --full

# Run with custom configuration
python scripts/run_pipeline.py --config config/custom_config.json
```

### 3. Generate Analysis
```bash
# Create comprehensive analysis and visualizations
python scripts/generate_analysis.py

# View results
open analysis/overview_dashboard.png
```

## 📋 Pipeline Overview

The pipeline consists of 4 main stages:

### Stage 1: Data Loading & Preprocessing
- Load StudyChat dataset from HuggingFace
- Filter and clean messages
- Create conversation threads
- Save processed data

### Stage 2: LLM Classification
- Classify messages using GPT-4
- Apply post-processing rules
- Generate confidence scores
- Save raw and final classifications

### Stage 3: Metrics Computation
- Calculate CP-Bench metrics (SWS, PC, RA, CPI)
- Generate bootstrap confidence intervals
- Compute thread-level statistics
- Analyze role-based patterns

### Stage 4: Analysis & Visualization
- Create comprehensive visualizations
- Generate detailed reports
- Perform bias analysis
- Save reproducibility artifacts

## 🛠️ Usage Examples

### Basic Usage
```python
from src.pipeline import CognitivePresencePipeline

# Initialize pipeline
pipeline = CognitivePresencePipeline()

# Run complete analysis
results = pipeline.run(subset_size=100)

# Access results
print(f"CPI: {results.cpi:.3f}")
print(f"Stage distribution: {results.stage_distribution}")
```

### Custom Configuration
```python
from src.config import Config

# Create custom config
config = Config(
    model_name="gpt-4",
    max_tokens=100,
    temperature=0.1,
    pilot_limit=500
)

# Run with custom config
pipeline = CognitivePresencePipeline(config)
results = pipeline.run()
```

### Individual Components
```python
from src.data import StudyChatLoader
from src.classification import LLMClassifier
from src.evaluation import CPBenchMetrics

# Load data
loader = StudyChatLoader()
messages = loader.load(subset_size=100)

# Classify messages
classifier = LLMClassifier()
classifications = classifier.classify(messages)

# Compute metrics
metrics = CPBenchMetrics()
results = metrics.compute(classifications)
```

## 📊 Output Files

### Data Files
- `data/processed/messages.parquet` - Processed messages
- `data/processed/classifications_raw.parquet` - Raw LLM outputs
- `data/processed/classifications_final.parquet` - Post-processed classifications

### Results Files
- `results/thread_metrics.csv` - Per-thread CP-Bench metrics
- `results/aggregate_metrics.csv` - Bootstrap confidence intervals
- `results/role_stage_distribution.csv` - Role × stage analysis

### Visualizations
- `analysis/overview_dashboard.png` - Key metrics overview
- `analysis/detailed_analysis.png` - Advanced analysis plots
- `analysis/results_explanation.md` - Detailed results explanation

### Artifacts
- `config_runtime.json` - Runtime configuration
- `prompt_one_shot.txt` - Classification prompt
- `codebook_min.json` - Stage definitions

## 🔧 Configuration

### Environment Variables
```bash
export OPENAI_API_KEY="your-api-key"
export PILOT_LIMIT=100          # Subset size for testing
export MODEL_NAME="gpt-4"       # LLM model to use
export TEMPERATURE=0.1          # Sampling temperature
```

### Configuration Files
- `config/default.json` - Default settings
- `config/production.json` - Production settings
- `config/development.json` - Development settings

## 📈 Understanding Results

### Cognitive Presence Stages
1. **Triggering (Stage 1)** - Problem identification, questions
2. **Exploration (Stage 2)** - Information seeking, brainstorming
3. **Integration (Stage 3)** - Synthesizing ideas, explanations
4. **Resolution (Stage 4)** - Applying solutions, confirming results

### CP-Bench Metrics
- **SWS (Stage Weighted Score)**: Measures cognitive engagement level
- **PC (Progressive Coherence)**: Measures stage progression quality
- **RA (Resolution Attainment)**: Measures problem-solving success
- **CPI (Cognitive Presence Index)**: Overall cognitive presence score

### Interpretation Guidelines
- **CPI > 0.6**: Strong cognitive presence
- **CPI 0.3-0.6**: Moderate cognitive presence
- **CPI < 0.3**: Weak cognitive presence

## 🧪 Advanced Usage

### Active Learning
```python
from src.active_learning import ActiveLearningSelector

# Find low-confidence samples for annotation
selector = ActiveLearningSelector()
samples = selector.select_low_confidence(classifications, n=50)
```

### Bias Analysis
```python
from src.evaluation import BiasAnalyzer

# Analyze role-based bias
analyzer = BiasAnalyzer()
bias_report = analyzer.analyze(classifications)
```

### Context Variants
```python
from src.classification import ContextVariantClassifier

# Test different context windows
classifier = ContextVariantClassifier()
results = classifier.classify_with_context(messages, context_size=5)
```

## 📚 Documentation

- `docs/user_guide.md` - Detailed usage guide
- `docs/api_reference.md` - API documentation
- `docs/interpretation_guide.md` - Results interpretation
- `docs/development_guide.md` - Development guidelines

## 🐛 Troubleshooting

### Common Issues

**1. OpenAI API Errors**
```bash
# Check API key
echo $OPENAI_API_KEY

# Test connection
python scripts/test_api.py
```

**2. Memory Issues**
```bash
# Reduce batch size
export BATCH_SIZE=10

# Use smaller subset
export PILOT_LIMIT=50
```

**3. Classification Failures**
```bash
# Check prompt formatting
python scripts/validate_prompt.py

# Test with sample data
python scripts/test_classification.py
```

### Debug Mode
```bash
# Enable debug logging
export LOG_LEVEL=DEBUG

# Run with verbose output
python scripts/run_pipeline.py --verbose
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- StudyChat dataset from HuggingFace
- CP-Bench metrics framework
- OpenAI GPT-4 for classification
- Community contributors

---

**For questions and support**: Open an issue or contact the maintainers.
