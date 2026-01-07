#!/usr/bin/env python3
"""Quick script to encode JSON credentials to base64."""

import base64
import json
import sys

if len(sys.argv) < 2:
    print("Usage: python encode_json.py <path_to_json_file>")
    print("\nExample:")
    print("  python encode_json.py credentials.json")
    print("  python encode_json.py \"C:\\Users\\bened\\Downloads\\Telegram Desktop\\acpffunnelleads-150c3a3058d5.json\"")
    sys.exit(1)

json_file = sys.argv[1]

try:
    # Read and validate JSON
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Convert to properly formatted JSON string
    json_str = json.dumps(data)
    
    # Encode to base64
    encoded = base64.b64encode(json_str.encode('utf-8')).decode('utf-8')
    
    print("\n" + "="*70)
    print("SUCCESS! Base64-encoded credentials:")
    print("="*70)
    print(encoded)
    print("="*70)
    print("\nCopy the above string and add it to your .env file:")
    print(f"GOOGLE_SERVICE_ACCOUNT_JSON={encoded}")
    print("\n")
    
except FileNotFoundError:
    print(f"Error: File not found: {json_file}")
    sys.exit(1)
except json.JSONDecodeError as e:
    print(f"Error: Invalid JSON file: {e}")
    sys.exit(1)
except Exception as e:
    print(f"Error: {e}")
    sys.exit(1)

