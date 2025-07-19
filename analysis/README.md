# StudyChat Cognitive Presence Analysis

This folder contains comprehensive visualizations and analysis of the StudyChat cognitive presence classification results.

## 📊 Generated Files

### Visualizations
- **`overview_dashboard.png`** - Overview dashboard with 4 key plots:
  1. Cognitive Presence Stage Distribution
  2. Classification Confidence Distribution  
  3. CP-Bench Metrics (SWS, PC, RA, CPI)
  4. Thread CPI Distribution

- **`detailed_analysis.png`** - Detailed analysis with 4 advanced plots:
  1. Stage Transition Probabilities (heatmap)
  2. Average Confidence by Cognitive Stage
  3. Thread Length vs Cognitive Presence Index
  4. Role × Stage Distribution (heatmap)

### Documentation
- **`results_explanation.md`** - Comprehensive explanation of results with interpretations and recommendations

## 🧠 Understanding the Results

### Cognitive Presence Stages
1. **Triggering (Stage 1)** - Problem identification, questions, confusion
2. **Exploration (Stage 2)** - Information seeking, brainstorming, divergent thinking
3. **Integration (Stage 3)** - Synthesizing ideas, connecting concepts, convergent thinking
4. **Resolution (Stage 4)** - Applying solutions, testing, confirming results

### CP-Bench Metrics
- **SWS (Stage Weighted Score)**: Measures how many messages are in higher cognitive stages
- **PC (Progressive Coherence)**: Measures how well conversations progress through stages 1→2→3→4
- **RA (Resolution Attainment)**: Measures how many threads reach a resolution
- **CPI (Cognitive Presence Index)**: Overall measure combining all three metrics

## 📈 Key Findings (50-message subset)

### Classification Performance
- ✅ **100% success rate** (50/50 messages classified)
- **Average confidence**: 84.7% (high confidence)
- **Model**: GPT-4 with one-shot prompting

### Stage Distribution
- **Triggering**: 70% (35 messages) - High problem identification
- **Exploration**: 20% (10 messages) - Moderate information seeking
- **Integration**: 4% (2 messages) - Low synthesis
- **Resolution**: 6% (3 messages) - Low resolution

### CP-Bench Metrics
- **SWS**: 0.334 (Moderate cognitive engagement)
- **PC**: 0.120 (Poor stage progression)
- **RA**: 0.667 (Good resolution rate)
- **CPI**: 0.336 (Moderate overall cognitive presence)

## 🔍 Key Insights

### 1. High Triggering Rate (70%)
- StudyChat conversations are primarily focused on problem identification
- Users ask many questions and identify issues
- Typical for educational support contexts

### 2. Limited Integration (4%)
- Very few messages synthesize ideas into coherent explanations
- While problems are identified and explored, there's limited synthesis
- Opportunity for improvement in educational design

### 3. Good Resolution Rate (67%)
- Most threads successfully reach a resolution
- Shows effective problem-solving despite limited integration
- Conversations move from problem to solution

### 4. Role-Based Patterns
- **Users**: Primarily in Triggering stage (asking questions)
- **Assistants**: Primarily in Exploration and Integration stages (providing explanations)
- **System**: Mix of Triggering and Resolution (setup and confirmation)

## 🎯 Recommendations

### For Educational Design
1. **Encourage Integration**: Design prompts that encourage students to synthesize information
2. **Scaffold Progression**: Create conversation flows that naturally progress through all stages
3. **Monitor Resolution**: Ensure conversations reach satisfactory conclusions

### For Model Improvement
1. **Context Awareness**: Add conversation context to improve classification accuracy
2. **Role-Specific Training**: Train models with role-specific examples to reduce bias
3. **Confidence Calibration**: Implement thresholds for low-confidence classifications

## 📊 How to Read the Visualizations

### Overview Dashboard
- **Top Left**: Stage distribution shows the balance of cognitive stages
- **Top Right**: Confidence distribution shows classification reliability
- **Bottom Left**: CP-Bench metrics show overall performance
- **Bottom Right**: Thread CPI distribution shows variation across conversations

### Detailed Analysis
- **Top Left**: Transition matrix shows how conversations flow between stages
- **Top Right**: Confidence by stage shows which stages are classified most reliably
- **Bottom Left**: Thread length vs CPI shows if longer conversations have better cognitive presence
- **Bottom Right**: Role × stage heatmap shows speaker-specific patterns

## 🚀 Next Steps

1. **Scale up**: Run on larger dataset (500-1000 messages)
2. **Gold standard**: Create human-annotated gold standard for evaluation
3. **Active learning**: Use low-confidence samples for model improvement
4. **Context variants**: Test different context window sizes
5. **Cross-validation**: Test on different conversation types

## 📁 Related Files

- `../data/processed/studychat_auto_final.parquet` - Final classifications
- `../data/processed/studychat_auto_raw.parquet` - Raw LLM outputs
- `../results/thread_metrics_studychat.csv` - Thread-level metrics
- `../results/aggregate_metrics_studychat.csv` - Aggregate statistics
- `../results/role_stage_distribution.csv` - Role × stage analysis

---

*Analysis generated on 50-message StudyChat subset using GPT-4 classification and CP-Bench metrics.* 