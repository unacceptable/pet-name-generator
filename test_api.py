#!/usr/bin/env python3
"""
Simple test script for the Pet Name Generator API
Run this after starting the API to verify it's working correctly.
"""

import requests
import json
import sys

import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

API_BASE = "http://localhost:8000"

def test_endpoint(method, endpoint, data=None, expected_status=200):
    """Test an API endpoint and return the result."""
    url = f"{API_BASE}{endpoint}"

    try:
        if method.upper() == "GET":
            response = requests.get(url)
        elif method.upper() == "POST":
            response = requests.post(url, json=data)
        else:
            print(f"❌ Unsupported method: {method}")
            return False

        if response.status_code == expected_status:
            print(f"✅ {method} {endpoint} - Status: {response.status_code}")

            # Handle different content types
            content_type = response.headers.get('content-type', '').lower()
            if 'application/json' in content_type:
                try:
                    result = response.json()
                    print(f"   Response: {json.dumps(result, indent=2)[:200]}...")
                except json.JSONDecodeError:
                    print(f"   Response: {response.text[:200]}...")
            else:
                # For HTML, CSS, JS files, just show content length
                print(f"   Content-Type: {content_type}")
                print(f"   Content-Length: {len(response.text)} characters")
                if endpoint.endswith(('.html', '.css', '.js')):
                    print(f"   Preview: {response.text[:100].strip()}...")

            return True
        else:
            print(f"❌ {method} {endpoint} - Expected {expected_status}, got {response.status_code}")
            print(f"   Response: {response.text}")
            return False

    except requests.exceptions.ConnectionError:
        print(f"❌ Could not connect to {API_BASE}")
        print("   Make sure the API is running with: docker-compose up")
        return False
    except Exception as e:
        print(f"❌ Error testing {endpoint}: {e}")
        return False

def main():
    """Run all API tests."""
    print("🐾 Testing Pet Name Generator API")
    print("=" * 40)

    tests = [
        ("GET", "/", None, 200),  # Frontend
        ("GET", "/health", None, 200),
        ("GET", "/pets", None, 200),
        ("GET", "/pets/dog/names?count=3", None, 200),
        ("GET", "/pets/cat/random", None, 200),
        ("GET", "/pets/dog/facts", None, 200),  # Pet facts
        ("GET", "/pets/cat/facts/random", None, 200),  # Random pet fact
        ("GET", "/facts", None, 200),  # All facts
        ("GET", "/facts/random", None, 200),  # Random fact from any pet
        ("GET", "/pets/invalid/names", None, 404),  # Test error handling
        ("GET", "/static/styles.css", None, 200),  # Static files
    ]

    passed = 0
    total = len(tests)

    for method, endpoint, data, expected_status in tests:
        if test_endpoint(method, endpoint, data, expected_status):
            passed += 1
        print()

    print("=" * 40)
    print(f"🎯 Tests passed: {passed}/{total}")

    if passed == total:
        print("🎉 All tests passed! The Pet Name API is working correctly.")
        return 0
    else:
        print("⚠️  Some tests failed. Check the API and try again.")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
