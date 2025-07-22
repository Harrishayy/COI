import json
from config import OPENAI_MODEL, ALPHA, BETA, GAMMA, STAGE_WEIGHTS, SEED
from codebook import CODEBOOK_MIN, ONE_SHOT_PROMPT


def save_artifacts():
    """Save reproducibility artifacts."""
    
    # Save runtime configuration
    with open("config_runtime.json", "w") as f:
        json.dump({
            "model": OPENAI_MODEL,
            "weights": {"alpha": ALPHA, "beta": BETA, "gamma": GAMMA},
            "stage_weights": STAGE_WEIGHTS,
            "seed": SEED
        }, f, indent=2)
    
    # Save prompt template
    with open("prompt_one_shot.txt", "w") as f:
        f.write(ONE_SHOT_PROMPT)
    
    # Save codebook
    with open("codebook_min.json", "w") as f:
        json.dump(CODEBOOK_MIN, f, indent=2)
    
    print("Saved reproducibility artifacts:")
    print("  - config_runtime.json")
    print("  - prompt_one_shot.txt")
    print("  - codebook_min.json")


def main():
    """Save all reproducibility artifacts."""
    save_artifacts()
    return True


if __name__ == "__main__":
    main() 