#!/usr/bin/env python3
"""
Validate transformed chat data against cognitive presence schema.
"""

import json
import argparse
from typing import Dict, List, Any


def validate_conversation(conversation: Dict) -> List[str]:
    """Validate a single conversation object against schema."""
    errors = []
    
    # Check required fields
    required_fields = ["conversation_id", "discourse"]
    for field in required_fields:
        if field not in conversation:
            errors.append(f"Missing required field: {field}")
    
    # Validate discourse array
    if "discourse" in conversation:
        discourse = conversation["discourse"]
        if not isinstance(discourse, list):
            errors.append("discourse must be an array")
        else:
            for i, message in enumerate(discourse):
                errors.extend(validate_message(message, i))
    
    return errors


def validate_message(message: Dict, index: int) -> List[str]:
    """Validate a single message object."""
    errors = []
    prefix = f"Message {index}: "
    
    # Check required fields
    required_fields = ["message_id", "sequence_number", "speaker_id", "speaker_role", "content", "timestamp"]
    for field in required_fields:
        if field not in message:
            errors.append(f"{prefix}Missing required field: {field}")
    
    # Validate speaker_role enum
    valid_roles = ["student", "ta", "instructor", "system", "user", "assistant"]
    if "speaker_role" in message and message["speaker_role"] not in valid_roles:
        errors.append(f"{prefix}Invalid speaker_role: {message['speaker_role']}")
    
    # Validate sequence_number is integer
    if "sequence_number" in message and not isinstance(message["sequence_number"], int):
        errors.append(f"{prefix}sequence_number must be an integer")
    
    # Validate timestamp is number
    if "timestamp" in message and not isinstance(message["timestamp"], (int, float)):
        errors.append(f"{prefix}timestamp must be a number")
    
    return errors


def validate_schema(data: Dict) -> List[str]:
    """Validate complete data structure."""
    errors = []
    
    # Check top-level structure
    if not isinstance(data, dict):
        errors.append("Root must be an object")
        return errors
    
    if "conversations" not in data:
        errors.append("Missing required field: conversations")
        return errors
    
    conversations = data["conversations"]
    if not isinstance(conversations, list):
        errors.append("conversations must be an array")
        return errors
    
    # Validate each conversation
    for i, conversation in enumerate(conversations):
        conv_errors = validate_conversation(conversation)
        for error in conv_errors:
            errors.append(f"Conversation {i}: {error}")
    
    return errors


def main():
    parser = argparse.ArgumentParser(description="Validate transformed chat data against schema")
    parser.add_argument("input_file", help="JSON file to validate")
    parser.add_argument("--sample", type=int, default=0, help="Show sample of N conversations")
    
    args = parser.parse_args()
    
    # Load and validate data
    with open(args.input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    errors = validate_schema(data)
    
    if errors:
        print(f"❌ Validation failed with {len(errors)} errors:")
        for error in errors[:10]:  # Show first 10 errors
            print(f"  - {error}")
        if len(errors) > 10:
            print(f"  ... and {len(errors) - 10} more errors")
    else:
        print("✅ Validation passed!")
        
        total_conversations = len(data["conversations"])
        total_messages = sum(len(conv["discourse"]) for conv in data["conversations"])
        
        print(f"📊 Dataset summary:")
        print(f"  - {total_conversations} conversations")
        print(f"  - {total_messages} total messages")
        print(f"  - Average messages per conversation: {total_messages/total_conversations:.1f}")
    
    # Show sample if requested
    if args.sample > 0 and "conversations" in data:
        print(f"\n📝 Sample of {args.sample} conversation(s):")
        for i in range(min(args.sample, len(data["conversations"]))):
            conv = data["conversations"][i]
            print(f"\nConversation {i+1} (ID: {conv['conversation_id']}):")
            print(f"  Messages: {len(conv['discourse'])}")
            if conv["discourse"]:
                print("  Sample messages:")
                for j, msg in enumerate(conv["discourse"][:3]):  # Show first 3 messages
                    content_preview = msg["content"][:100] + "..." if len(msg["content"]) > 100 else msg["content"]
                    print(f"    {j+1}. [{msg['speaker_role']}] {content_preview}")


if __name__ == "__main__":
    main() 