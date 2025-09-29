#!/usr/bin/env python3
"""
Test Script for Kolam Diffusion Integration
===========================================

Test the integrated diffusion API endpoints.
"""

import requests
import json
import time
from pathlib import Path

def test_diffusion_health():
    """Test the diffusion health endpoint"""
    print("🔍 Testing diffusion health endpoint...")
    try:
        response = requests.get("http://localhost:5000/api/diffusion/health", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Diffusion health check passed: {data}")
            return True
        else:
            print(f"❌ Diffusion health check failed: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Diffusion health check failed: {e}")
        return False

def test_diffusion_status():
    """Test the diffusion status endpoint"""
    print("🔍 Testing diffusion status...")
    try:
        response = requests.get("http://localhost:5000/api/diffusion/status", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Diffusion status: {data}")
            return data.get('models_loaded', False)
        else:
            print(f"❌ Diffusion status failed: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Diffusion status failed: {e}")
        return False

def test_general_health():
    """Test the general health endpoint"""
    print("🔍 Testing general health endpoint...")
    try:
        response = requests.get("http://localhost:5000/api/health", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ General health check passed: {data}")
            return True
        else:
            print(f"❌ General health check failed: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ General health check failed: {e}")
        return False

def create_test_image():
    """Create a simple test image"""
    try:
        from PIL import Image, ImageDraw
        import numpy as np
        
        # Create a simple test image
        img = Image.new('RGB', (256, 256), 'white')
        draw = ImageDraw.Draw(img)
        
        # Draw a simple pattern
        center = 128
        for i in range(8):
            angle = i * 3.14159 / 4
            x = center + 50 * np.cos(angle)
            y = center + 50 * np.sin(angle)
            draw.line([(center, center), (x, y)], fill='black', width=2)
        
        # Save test image
        test_img_path = Path("test_kolam.png")
        img.save(test_img_path)
        print(f"✅ Created test image: {test_img_path}")
        return test_img_path
        
    except Exception as e:
        print(f"❌ Failed to create test image: {e}")
        return None

def test_diffusion_generation():
    """Test diffusion generation with a sample image"""
    print("🔍 Testing diffusion generation...")
    
    # Create test image
    test_img_path = create_test_image()
    if not test_img_path:
        return False
    
    try:
        # Test the generation endpoint
        with open(test_img_path, 'rb') as f:
            files = {'image': ('test_kolam.png', f, 'image/png')}
            
            print("⏳ Sending test image to diffusion API (this may take a few minutes)...")
            response = requests.post(
                "http://localhost:5000/api/diffusion/generate",
                files=files,
                timeout=300  # 5 minutes timeout
            )
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print(f"✅ Diffusion generation successful!")
                print(f"   Session ID: {data.get('session_id')}")
                print(f"   Generated {len(data.get('generated_images', []))} variants")
                print(f"   Generation type: {data.get('generation_type')}")
                return True
            else:
                print(f"❌ Diffusion generation failed: {data.get('error')}")
                return False
        else:
            print(f"❌ Diffusion generation failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Diffusion generation test failed: {e}")
        return False
    finally:
        # Clean up test image
        if test_img_path and test_img_path.exists():
            test_img_path.unlink()
            print(f"🧹 Cleaned up test image")

def main():
    """Run all tests"""
    print("🧪 Kolam Diffusion Integration Test Suite")
    print("=" * 50)
    
    # Test 1: General health
    if not test_general_health():
        print("\n❌ Backend is not running. Please start the server first:")
        print("   python production_backend.py")
        return
    
    # Test 2: Diffusion health
    if not test_diffusion_health():
        print("\n⚠️  Diffusion health check failed. AI features may not be available.")
        return
    
    # Test 3: Diffusion status
    models_loaded = test_diffusion_status()
    if not models_loaded:
        print("\n⚠️  Diffusion models are not loaded.")
        print("   This may take 5-10 minutes on first run to download models.")
        print("   Check the backend logs for model loading progress.")
        return
    
    # Test 4: Generation (optional)
    print("\n🤔 Do you want to test diffusion generation? (y/n): ", end="")
    try:
        choice = input().lower().strip()
        if choice in ['y', 'yes']:
            test_diffusion_generation()
        else:
            print("⏭️  Skipping generation test")
    except KeyboardInterrupt:
        print("\n⏭️  Skipping generation test")
    
    print("\n🎉 Integration test completed!")
    print("\n📋 Next steps:")
    print("1. Open your React frontend: npm start")
    print("2. Navigate to /ai-diffusion")
    print("3. Upload a Kolam image and generate AI variants!")

if __name__ == "__main__":
    main()












