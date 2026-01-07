#!/usr/bin/env python3
"""Helper script to encode Google Service Account JSON credentials to base64."""

import base64
import json
import sys
from pathlib import Path


def encode_credentials(json_file_path: str) -> str:
    """Encode credentials JSON file to base64.
    
    Args:
        json_file_path: Path to the credentials.json file
        
    Returns:
        Base64-encoded string
    """
    file_path = Path(json_file_path)
    
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {json_file_path}")
    
    # Read and parse JSON to validate it
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            credentials_dict = json.load(f)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON file: {e}")
    
    # Convert back to JSON string (ensures proper formatting)
    json_str = json.dumps(credentials_dict)
    
    # Encode to base64
    encoded = base64.b64encode(json_str.encode('utf-8')).decode('utf-8')
    
    return encoded


def decode_and_verify(base64_str: str) -> dict:
    """Decode base64 string and verify it's valid JSON.
    
    Args:
        base64_str: Base64-encoded JSON string
        
    Returns:
        Decoded credentials dictionary
    """
    try:
        decoded_bytes = base64.b64decode(base64_str)
        json_str = decoded_bytes.decode('utf-8')
        return json.loads(json_str)
    except Exception as e:
        raise ValueError(f"Failed to decode/parse base64: {e}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python encode_credentials.py <path_to_credentials.json>")
        print("\nExample:")
        print("  python encode_credentials.py credentials.json")
        print("\nOr to verify an existing base64 string:")
        print("  python encode_credentials.py --verify <base64_string>")
        sys.exit(1)
    
    if sys.argv[1] == "--verify" and len(sys.argv) == 3:
        # Verify mode
        base64_str = sys.argv[2]
        try:
            creds = decode_and_verify(base64_str)
            print("✓ Base64 string is valid!")
            print(f"✓ Project ID: {creds.get('project_id', 'N/A')}")
            print(f"✓ Client Email: {creds.get('client_email', 'N/A')}")
        except Exception as e:
            print(f"✗ Error: {e}")
            sys.exit(1)
    else:
        # Encode mode
        json_file = sys.argv[1]
        try:
            encoded = encode_credentials(json_file)
            print("=" * 70)
            print("Base64-encoded credentials (copy this to your .env file):")
            print("=" * 70)
            print(encoded)
            print("=" * 70)
            print("\nAdd this to your .env file:")
            print(f"GOOGLE_SERVICE_ACCOUNT_JSON={encoded}")
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)

