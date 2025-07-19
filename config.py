import os
import random
import numpy as np
from pathlib import Path

# Directory setup
BASE_DIR = Path(".")
DATA_DIR = BASE_DIR / "data"
RAW_DIR = DATA_DIR / "raw"
PROC_DIR = DATA_DIR / "processed"
LABELS_DIR = BASE_DIR / "labels_gold"
RESULTS_DIR = BASE_DIR / "results"
FIG_DIR = BASE_DIR / "figures"
LOG_DIR = BASE_DIR / "logs"

for d in [DATA_DIR, RAW_DIR, PROC_DIR, LABELS_DIR, RESULTS_DIR, FIG_DIR, LOG_DIR]:
    d.mkdir(parents=True, exist_ok=True)

# Random seed
SEED = 42
random.seed(SEED)
np.random.seed(SEED)

# LLM model
OPENAI_MODEL = "gpt-4"  # Set to the model you intend to use
MAX_RETRIES = 5
BACKOFF_BASE = 2  # seconds

# CP-Bench weights
ALPHA, BETA, GAMMA = 0.5, 0.3, 0.2
STAGE_WEIGHTS = {1: 1, 2: 2, 3: 3, 4: 4}

# Confidence gating (not yet used for second pass, but reserved)
CONF_THRESHOLD = 55

# Sample size for gold (optional)
GOLD_SAMPLE_MESSAGES = 600  # adjust freely

# Subset for quick pilot (None for full). Set e.g. 2000 for a cheap test.
PILOT_LIMIT = 50  # or 2000 