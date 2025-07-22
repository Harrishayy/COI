# Cognitive Presence Evaluation - Uniform JSON Schema

## Overview

This document describes the uniform JSON schema created for cognitive presence evaluation of chat discourse. Both datasets in `src/data/` have been standardized to this format for consistent analysis.

## Schema Structure

### Top Level
```json
{
  "conversations": [
    // Array of conversation objects
  ]
}
```

### Conversation Object
```json
{
  "conversation_id": "unique_id",
  "metadata": {
    "course_id": "course_identifier",
    "created_timestamp": 1600134095485,
    "closed_timestamp": 1600301046718,
    "total_messages": 11,
    "participants": ["user_id_1", "user_id_2"]
  },
  "discourse": [
    // Array of chat discourse objects
  ]
}
```

### Chat Discourse Object
```json
{
  "message_id": "unique_message_id",
  "sequence_number": 0,
  "speaker_id": "user_or_system_id",
  "speaker_role": "student|ta|instructor|system|user|assistant",
  "content": "The actual message content",
  "timestamp": 1600134095502,
  "cognitive_presence": {
    "phase": "triggering_event|exploration|integration|resolution",
    "indicators": ["list", "of", "indicators"],
    "confidence": 0.85
  }
}
```

## Transformed Datasets

### Original → Transformed
- `src/data/chat_cleaned (1).json` → `src/data/chat_cleaned_uniform.json`
- `src/data/filtered_a1_to_a7_dataset (1).json` → `src/data/filtered_dataset_uniform.json`

### Dataset Statistics
| Dataset | Conversations | Total Messages | Avg Messages/Conv |
|---------|---------------|----------------|-------------------|
| Chat Cleaned | 17,698 | 309,539 | 17.5 |
| Filtered Dataset | 6,864 | 140,516 | 20.5 |

## Speaker Roles

The schema supports the following speaker roles:
- **student**: Student participants
- **ta**: Teaching assistants
- **instructor**: Course instructors  
- **system**: System messages
- **user**: Generic user (for LLM conversations)
- **assistant**: AI assistant responses

## Cognitive Presence Fields

The optional `cognitive_presence` object is designed for analysis and can include:
- **phase**: One of the four cognitive presence phases (Garrison et al.)
- **indicators**: Specific textual or behavioral indicators
- **confidence**: Confidence score for the classification (0-1)

## Usage

### Transformation Scripts
```bash
# Transform chat_cleaned format
python3 transform_chat_data.py "input.json" "output.json" --format chat_cleaned

# Transform filtered_dataset format  
python3 transform_chat_data.py "input.json" "output.json" --format filtered_dataset
```

### Validation
```bash
# Validate transformed data
python3 validate_schema.py "transformed_data.json" --sample 3
```

## Files

- `cognitive_presence_schema.json`: JSON Schema specification
- `transform_chat_data.py`: Transformation script for both formats
- `validate_schema.py`: Validation and inspection tool
- `src/data/chat_cleaned_uniform.json`: Transformed chat_cleaned data
- `src/data/filtered_dataset_uniform.json`: Transformed filtered dataset

## Next Steps for Cognitive Presence Analysis

1. **Load uniform data**: Use either transformed dataset
2. **Iterate through conversations**: Each conversation has ordered discourse
3. **Analyze message content**: Apply cognitive presence indicators
4. **Populate cognitive_presence fields**: Add phase classifications and indicators
5. **Aggregate results**: Analyze patterns across conversations and courses

This uniform format ensures consistent processing regardless of the original data source and facilitates comprehensive cognitive presence evaluation. 