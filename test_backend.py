#!/usr/bin/env python3
"""
Test script to verify backend API endpoints
"""
import requests
import json

def test_backend():
    base_url = "http://localhost:5000"
    
    print("Testing Kolam Analysis Backend API...")
    print("=" * 50)
    
    # Test 1: Health check
    try:
        response = requests.get(f"{base_url}/")
        print(f"✓ Health check: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"  Message: {data.get('message')}")
            print(f"  Version: {data.get('version')}")
    except Exception as e:
        print(f"✗ Health check failed: {e}")
    
    # Test 2: Patterns endpoint
    try:
        response = requests.get(f"{base_url}/api/patterns")
        print(f"✓ Patterns endpoint: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"  Found {data.get('count', 0)} patterns")
    except Exception as e:
        print(f"✗ Patterns endpoint failed: {e}")
    
    # Test 3: Analyze endpoint
    try:
        test_image = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg=="
        response = requests.post(f"{base_url}/api/analyze", 
                               json={"image": test_image})
        print(f"✓ Analyze endpoint: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"  Analysis successful: {data.get('success')}")
    except Exception as e:
        print(f"✗ Analyze endpoint failed: {e}")
    
    print("=" * 50)
    print("Backend test completed!")

if __name__ == "__main__":
    test_backend()






