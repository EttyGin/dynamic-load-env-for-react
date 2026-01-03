#!/usr/bin/env python3
"""
Demonstration script for testing the HTTP Bearer authentication.

Shows:
1. Request WITHOUT authentication token -> 401 Unauthorized
2. Request WITH incorrect token -> 401 Unauthorized  
3. Request WITH correct token -> 200 Success

Usage:
    python test_auth.py

Make sure the backend is running:
    MASTER_API_KEY=super-secret-key python backend/main.py
"""

import requests
import json

BASE_URL = "http://localhost:8000"
CORRECT_TOKEN = "super-secret-key"
INCORRECT_TOKEN = "wrong-token"

print("=" * 70)
print("Testing HTTP Bearer Authentication")
print("=" * 70)

# Test 1: Request without token
print("\n[Test 1] Request WITHOUT Authorization header:")
print(f"GET {BASE_URL}/api/hello")
try:
    response = requests.get(f"{BASE_URL}/api/hello")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
except Exception as e:
    print(f"Error: {e}")

# Test 2: Request with incorrect token
print("\n[Test 2] Request WITH incorrect token:")
print(f"GET {BASE_URL}/api/hello")
print(f"Authorization: Bearer {INCORRECT_TOKEN}")
try:
    response = requests.get(
        f"{BASE_URL}/api/hello",
        headers={"Authorization": f"Bearer {INCORRECT_TOKEN}"}
    )
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
except Exception as e:
    print(f"Error: {e}")

# Test 3: Request with correct token
print("\n[Test 3] Request WITH correct token:")
print(f"GET {BASE_URL}/api/hello")
print(f"Authorization: Bearer {CORRECT_TOKEN}")
try:
    response = requests.get(
        f"{BASE_URL}/api/hello",
        headers={"Authorization": f"Bearer {CORRECT_TOKEN}"}
    )
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
except Exception as e:
    print(f"Error: {e}")

print("\n" + "=" * 70)
print("Demo complete!")
print("=" * 70)
