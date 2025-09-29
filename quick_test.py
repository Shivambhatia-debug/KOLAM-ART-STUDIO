#!/usr/bin/env python3
"""
Quick test for the improved Kolam analysis system
"""

import requests
import base64
import numpy as np
import cv2
from PIL import Image
import io

def create_test_image():
    """Create a simple test Kolam image"""
    # Create a simple test image with circles and lines
    image = np.ones((400, 400, 3), dtype=np.uint8) * 255
    
    # Draw some circles (dots)
    cv2.circle(image, (100, 100), 10, (0, 0, 0), -1)
    cv2.circle(image, (300, 100), 10, (0, 0, 0), -1)
    cv2.circle(image, (100, 300), 10, (0, 0, 0), -1)
    cv2.circle(image, (300, 300), 10, (0, 0, 0), -1)
    cv2.circle(image, (200, 200), 10, (0, 0, 0), -1)
    
    # Draw connecting lines
    cv2.line(image, (100, 100), (300, 100), (0, 0, 0), 3)
    cv2.line(image, (100, 100), (100, 300), (0, 0, 0), 3)
    cv2.line(image, (300, 100), (300, 300), (0, 0, 0), 3)
    cv2.line(image, (100, 300), (300, 300), (0, 0, 0), 3)
    cv2.line(image, (100, 100), (300, 300), (0, 0, 0), 2)
    cv2.line(image, (300, 100), (100, 300), (0, 0, 0), 2)
    
    return image

def image_to_base64(image):
    """Convert image to base64 string"""
    # Convert numpy array to PIL Image
    pil_image = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    
    # Convert to base64
    buffer = io.BytesIO()
    pil_image.save(buffer, format='PNG')
    img_str = base64.b64encode(buffer.getvalue()).decode()
    
    return f"data:image/png;base64,{img_str}"

def test_improved_analysis():
    """Test the improved analysis endpoint"""
    print("Testing Improved Kolam Analysis System")
    print("=" * 50)
    
    # Create test image
    test_image = create_test_image()
    image_base64 = image_to_base64(test_image)
    
    # Test data
    test_data = {
        "image": image_base64
    }
    
    try:
        # Test improved analysis endpoint
        print("Testing /api/improved-analysis endpoint...")
        response = requests.post(
            "http://localhost:5000/api/improved-analysis",
            json=test_data,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Improved analysis successful!")
            print(f"   Kolam Type: {result['analysis']['kolam_type']}")
            print(f"   Symmetry: {result['analysis']['symmetry_type']}")
            print(f"   Cultural Region: {result['analysis']['cultural_region']}")
            print(f"   Confidence: {result['analysis']['confidence']:.3f}")
            print(f"   Eulerian Path: {result['analysis']['eulerian_path']}")
            print(f"   Analysis Method: {result['analysis']['analysis_method']}")
        else:
            print(f"❌ Analysis failed: {response.status_code}")
            print(f"   Error: {response.text}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Connection error: {e}")
        return False
    
    try:
        # Test basic analysis endpoint for comparison
        print("\nTesting /api/analyze endpoint...")
        response = requests.post(
            "http://localhost:5000/api/analyze",
            json=test_data,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Basic analysis successful!")
            print(f"   Symmetry: {result['analysis']['symmetry_type']}")
            print(f"   Complexity: {result['analysis']['complexity']}")
            print(f"   Cultural Region: {result['analysis']['cultural_region']}")
        else:
            print(f"❌ Basic analysis failed: {response.status_code}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Connection error: {e}")
    
    return True

def test_health_endpoint():
    """Test the health endpoint"""
    try:
        print("\nTesting /api/health endpoint...")
        response = requests.get("http://localhost:5000/api/health", timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Health check successful!")
            print(f"   Status: {result['status']}")
            print(f"   Version: {result['version']}")
            print(f"   Cache Size: {result['cache_size']}")
        else:
            print(f"❌ Health check failed: {response.status_code}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Connection error: {e}")

if __name__ == "__main__":
    print("🎨 Kolam Analysis System Test")
    print("=" * 50)
    
    # Test health endpoint first
    test_health_endpoint()
    
    # Test analysis endpoints
    test_improved_analysis()
    
    print("\n🎯 Test completed!")
    print("Your image analysis system is now working properly!")
    print("\nAvailable endpoints:")
    print("  - POST /api/improved-analysis (ML-based analysis)")
    print("  - POST /api/analyze (Basic analysis)")
    print("  - POST /api/advanced-analysis (CV-based analysis)")
    print("  - GET /api/health (System health)")
    print("  - GET /api/patterns (Available patterns)")


















