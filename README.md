This repository provides an automated cognitive presence labeling + CP-Bench metric pipeline for the StudyChat dataset.

Pipeline:
1. Load dataset (studychat_load.py)
2. LLM one-shot classification (auto_label.py)
3. Rule post-processing (postprocess.py)
4. Metrics (compute_metrics.py + bootstrap_ci.py)
5. Visualization & diagnostics (visuals.py, bias_checks.py)
6. (Optional) Gold labeling + evaluation (sample_gold.py, eval_humans.py, eval_model.py)

Metrics:
- SWS, PC, RA, CPI (α=0.5, β=0.3, γ=0.2)
- Transition matrix, resolution attainment curve

Security:
- Set OPENAI_API_KEY in environment only; do not commit secrets.
