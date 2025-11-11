#!/usr/bin/env python
"""Test script to verify the generate endpoint works correctly."""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from website.app import app

def test_generate_endpoint():
    """Test the /generate/1 endpoint."""
    with app.test_client() as client:
        print("Testing /generate/1 endpoint...")
        response = client.get('/generate/1')

        print(f"Status Code: {response.status_code}")
        print(f"Content-Type: {response.content_type}")

        try:
            data = response.get_json()
            print(f"Response JSON: {data}")

            if response.status_code == 200:
                if data.get('success'):
                    print("✓ SUCCESS: Generation endpoint works correctly!")
                else:
                    print(f"✗ FAIL: Generation failed with message: {data.get('message')}")
            else:
                print(f"✗ FAIL: Non-200 status code: {response.status_code}")
                print(f"   Error: {data.get('message', 'No message')}")
        except Exception as e:
            print(f"✗ FAIL: Could not parse JSON response")
            print(f"   Error: {e}")
            print(f"   Response: {response.data[:200]}")

if __name__ == '__main__':
    test_generate_endpoint()

