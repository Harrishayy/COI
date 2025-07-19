import os
import re
import json
import time
import openai
from config import OPENAI_MODEL, MAX_RETRIES, BACKOFF_BASE
from codebook import ONE_SHOT_PROMPT


def setup_openai():
    """Setup OpenAI client with API key."""
    if not os.getenv("OPENAI_API_KEY"):
        raise EnvironmentError("Set OPENAI_API_KEY before running classification.")
    openai.api_key = os.getenv("OPENAI_API_KEY")


def classify_message(text: str,
                    model: str = OPENAI_MODEL,
                    prompt_template: str = ONE_SHOT_PROMPT,
                    max_retries: int = MAX_RETRIES) -> dict:
    """
    Classify a single message using OpenAI API.
    
    Args:
        text: Message text to classify
        model: OpenAI model to use
        prompt_template: Prompt template with {text} placeholder
        max_retries: Maximum retry attempts
        
    Returns:
        Dict with stage, label, confidence, rationale
    """
    prompt = prompt_template.format(text=text)
    
    for attempt in range(max_retries):
        try:
            client = openai.OpenAI()
            resp = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0
            )
            content = resp.choices[0].message.content
            
            # Extract JSON from response
            m = re.search(r"\{.*\}", content, re.S)
            if m:
                try:
                    data = json.loads(m.group(0))
                    data["stage"] = int(data.get("stage"))
                    return data
                except Exception as e:
                    print(f"JSON parse error: {e}")
                    print(f"Raw content: {content}")
                    pass
            
            print(f"Failed to extract JSON from: {content}")
            return {"stage": None, "label": None, "confidence": 0, "rationale": "ParseFail"}
            
        except Exception as e:
            print(f"API error (attempt {attempt + 1}): {e}")
            if attempt < max_retries - 1:
                time.sleep(BACKOFF_BASE * (attempt + 1))
    
    return {"stage": None, "label": None, "confidence": 0, "rationale": "ErrorRetries"}


def main():
    """Test the classification function."""
    setup_openai()
    
    # Test with a sample message
    test_message = "I'm stuck, my loop never terminates."
    result = classify_message(test_message)
    print("Test classification result:", result)


if __name__ == "__main__":
    main() 