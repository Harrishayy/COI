#!/usr/bin/env python3
"""
Transform chat datasets to uniform cognitive presence evaluation schema.

This script converts both chat_cleaned.json and filtered_a1_to_a7_dataset.json
to a standardized format for cognitive presence analysis.
"""

import json
import argparse
from pathlib import Path
from typing import Dict, List, Any


def transform_chat_cleaned(data: List[Dict]) -> Dict:
    """Transform chat_cleaned.json format to uniform schema."""
    conversations = []
    
    for idx, conversation in enumerate(data):
        # Extract metadata
        metadata = {
            "course_id": str(conversation.get("course_id", "")),
            "created_timestamp": conversation.get("created_datetime", 0),
            "closed_timestamp": conversation.get("closed_datetime", 0),
            "total_messages": len(conversation.get("comments", [])),
            "participants": []
        }
        
        # Transform comments to discourse
        discourse = []
        comments = conversation.get("comments", [])
        
        # Collect unique participants
        participants = set()
        for comment in comments:
            user_id = str(comment.get("user_id", ""))
            participants.add(user_id)
        metadata["participants"] = list(participants)
        
        for seq_num, comment in enumerate(comments):
            user_id = str(comment.get("user_id", ""))
            
            # Determine speaker role based on conversation context
            # If user matches student_user_id, it's a student; if ta_user_id, it's TA
            speaker_role = "student"  # default
            if user_id == str(conversation.get("ta_user_id", "")):
                speaker_role = "ta"
            elif user_id == str(conversation.get("student_user_id", "")):
                speaker_role = "student"
            else:
                # Check if it's instructor or other role based on context
                speaker_role = "student"  # fallback
                
            message = {
                "message_id": str(comment.get("id", f"{conversation.get('id', idx)}_{seq_num}")),
                "sequence_number": seq_num,
                "speaker_id": user_id,
                "speaker_role": speaker_role,
                "content": comment.get("content", ""),
                "timestamp": comment.get("created_datetime", 0)
            }
            discourse.append(message)
        
        conversation_obj = {
            "conversation_id": str(conversation.get("id", idx)),
            "metadata": metadata,
            "discourse": discourse
        }
        conversations.append(conversation_obj)
    
    return {"conversations": conversations}


def transform_filtered_dataset(data: List[Dict]) -> Dict:
    """Transform filtered_a1_to_a7_dataset.json format to uniform schema."""
    conversations = []
    
    for idx, conversation in enumerate(data):
        # Extract metadata
        metadata = {
            "course_id": "",  # Not available in this dataset
            "created_timestamp": conversation.get("timestamp", 0),
            "closed_timestamp": conversation.get("timestamp", 0),  # Same as created for single-turn
            "total_messages": len(conversation.get("messages", [])) + (1 if conversation.get("response") else 0),
            "participants": [conversation.get("userId", ""), "assistant"]
        }
        
        # Transform messages and response to discourse
        discourse = []
        messages = conversation.get("messages", [])
        
        # Add messages
        for seq_num, message in enumerate(messages):
            role = message.get("role", "user")
            
            # Map roles to our schema
            speaker_role_map = {
                "system": "system",
                "user": "user", 
                "assistant": "assistant"
            }
            
            discourse_message = {
                "message_id": f"{conversation.get('chatId', idx)}_{seq_num}",
                "sequence_number": seq_num,
                "speaker_id": conversation.get("userId", "") if role == "user" else "assistant",
                "speaker_role": speaker_role_map.get(role, "user"),
                "content": message.get("content", ""),
                "timestamp": conversation.get("timestamp", 0)
            }
            discourse.append(discourse_message)
        
        # Add response as final message if present
        if conversation.get("response"):
            response_seq = len(messages)
            response_message = {
                "message_id": f"{conversation.get('chatId', idx)}_response",
                "sequence_number": response_seq,
                "speaker_id": "assistant",
                "speaker_role": "assistant",
                "content": conversation.get("response", ""),
                "timestamp": conversation.get("timestamp", 0)
            }
            discourse.append(response_message)
        
        conversation_obj = {
            "conversation_id": conversation.get("chatId", str(idx)),
            "metadata": metadata,
            "discourse": discourse
        }
        conversations.append(conversation_obj)
    
    return {"conversations": conversations}


def main():
    parser = argparse.ArgumentParser(description="Transform chat datasets to uniform schema")
    parser.add_argument("input_file", help="Input JSON file to transform")
    parser.add_argument("output_file", help="Output JSON file")
    parser.add_argument("--format", choices=["chat_cleaned", "filtered_dataset"], 
                       required=True, help="Input file format")
    
    args = parser.parse_args()
    
    # Load input data
    with open(args.input_file, 'r', encoding='utf-8') as f:
        input_data = json.load(f)
    
    # Transform based on format
    if args.format == "chat_cleaned":
        transformed_data = transform_chat_cleaned(input_data)
    elif args.format == "filtered_dataset":
        transformed_data = transform_filtered_dataset(input_data)
    
    # Save transformed data
    with open(args.output_file, 'w', encoding='utf-8') as f:
        json.dump(transformed_data, f, indent=2, ensure_ascii=False)
    
    print(f"Transformed {len(input_data)} conversations to {args.output_file}")
    print(f"Schema: {len(transformed_data['conversations'])} conversations with uniform discourse format")


if __name__ == "__main__":
    main() 