#!/usr/bin/env python3
"""
Test Script for Kolam Diffusion API
===================================

Simple test script to verify the API is working correctly.
"""

import requests
import json
import time
from pathlib import Path

def test_health_endpoint():
    """Test the health endpoint"""
    print("🔍 Testing health endpoint...")
    try:
        response = requests.get("http://localhost:5000/health", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Health check passed: {data}")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Health check failed: {e}")
        return False

def test_models_status():
    """Test the models status endpoint"""
    print("🔍 Testing models status...")
    try:
        response = requests.get("http://localhost:5000/models/status", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Models status: {data}")
            return data.get('models_loaded', False)
        else:
            print(f"❌ Models status failed: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Models status failed: {e}")
        return False

def test_generation_with_sample():
    """Test generation with a sample image"""
    print("🔍 Testing generation with sample image...")
    
    # Create a simple test image
    try:
        from PIL import Image
        import io
        
        # Create a simple test image (white circle on black background)
        img = Image.new('RGB', (256, 256), 'black')
        # Draw a simple circle (this is a basic test)
        # For a real test, you'd want to use a proper Kolam image
        
        # Save to bytes
        img_bytes = io.BytesIO()
        img.save(img_bytes, format='PNG')
        img_bytes.seek(0)
        
        # Test the generation endpoint
        files = {'image': ('test_kolam.png', img_bytes, 'image/png')}
        
        print("⏳ Sending test image (this may take a few minutes)...")
        response = requests.post(
            "http://localhost:5000/generate",
            files=files,
            timeout=300  # 5 minutes timeout
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print(f"✅ Generation successful!")
                print(f"   Session ID: {data.get('session_id')}")
                print(f"   Generated {len(data.get('generated_images', []))} variants")
                return True
            else:
                print(f"❌ Generation failed: {data.get('error')}")
                return False
        else:
            print(f"❌ Generation failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Generation test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 Kolam Diffusion API Test Suite")
    print("=" * 40)
    
    # Test 1: Health check
    if not test_health_endpoint():
        print("\n❌ API is not running. Please start the server first:")
        print("   python kolam_diffusion_api.py")
        return
    
    # Test 2: Models status
    models_loaded = test_models_status()
    if not models_loaded:
        print("\n⚠️  Models are not loaded. This may take a few minutes on first run.")
        print("   Please wait and try again.")
        return
    
    # Test 3: Generation (optional)
    print("\n🤔 Do you want to test image generation? (y/n): ", end="")
    try:
        choice = input().lower().strip()
        if choice in ['y', 'yes']:
            test_generation_with_sample()
        else:
            print("⏭️  Skipping generation test")
    except KeyboardInterrupt:
        print("\n⏭️  Skipping generation test")
    
    print("\n🎉 Test suite completed!")
    print("\n📋 Next steps:")
    print("1. Open kolam_diffusion_test.html in your browser")
    print("2. Upload a real Kolam image")
    print("3. Generate your variants!")

if __name__ == "__main__":
    main()












