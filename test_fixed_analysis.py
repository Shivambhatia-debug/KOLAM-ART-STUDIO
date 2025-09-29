#!/usr/bin/env python3
"""
Test Fixed Analysis System
==========================

Test the fixed analysis system with different images.
"""

import requests
import base64
import numpy as np
from PIL import Image, ImageDraw
import io

def create_simple_kolam():
    """Create a simple Kolam pattern"""
    img = Image.new('RGB', (200, 200), 'white')
    draw = ImageDraw.Draw(img)
    
    # Simple dot pattern
    center = (100, 100)
    for radius in [20, 40, 60]:
        draw.ellipse([center[0]-radius, center[1]-radius, center[0]+radius, center[1]+radius], outline='black', width=2)
    
    # Convert to base64
    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    img_bytes = buffer.getvalue()
    img_base64 = base64.b64encode(img_bytes).decode('utf-8')
    
    return f"data:image/png;base64,{img_base64}"

def create_complex_kolam():
    """Create a complex Kolam pattern"""
    img = Image.new('RGB', (200, 200), 'white')
    draw = ImageDraw.Draw(img)
    
    # Complex pattern with many elements
    center = (100, 100)
    
    # Multiple circles
    for radius in [10, 20, 30, 40, 50, 60, 70, 80]:
        draw.ellipse([center[0]-radius, center[1]-radius, center[0]+radius, center[1]+radius], outline='black', width=1)
    
    # Add lines
    for angle in range(0, 360, 30):
        x1 = 100 + 20 * np.cos(np.radians(angle))
        y1 = 100 + 20 * np.sin(np.radians(angle))
        x2 = 100 + 60 * np.cos(np.radians(angle))
        y2 = 100 + 60 * np.sin(np.radians(angle))
        draw.line([x1, y1, x2, y2], fill='black', width=2)
    
    # Convert to base64
    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    img_bytes = buffer.getvalue()
    img_base64 = base64.b64encode(img_bytes).decode('utf-8')
    
    return f"data:image/png;base64,{img_base64}"

def create_random_pattern():
    """Create a random pattern"""
    img_array = np.random.randint(0, 255, (200, 200, 3), dtype=np.uint8)
    
    # Add some structure
    center = (100, 100)
    for i in range(50):
        angle = i * 2 * np.pi / 50
        x = int(100 + 80 * np.cos(angle))
        y = int(100 + 80 * np.sin(angle))
        if 0 <= x < 200 and 0 <= y < 200:
            img_array[y-5:y+5, x-5:x+5] = [0, 0, 0]
    
    img = Image.fromarray(img_array)
    
    # Convert to base64
    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    img_bytes = buffer.getvalue()
    img_base64 = base64.b64encode(img_bytes).decode('utf-8')
    
    return f"data:image/png;base64,{img_base64}"

def test_image_analysis(image_name, image_data):
    """Test analysis for a specific image"""
    print(f"\n🔍 Testing {image_name}...")
    
    try:
        url = "http://localhost:5000/api/improved-analysis"
        data = {"image": image_data}
        
        response = requests.post(url, json=data, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            analysis = result.get('analysis', {})
            
            print(f"✅ {image_name} Analysis:")
            print(f"   Kolam Type: {analysis.get('kolam_type')}")
            print(f"   Symmetry Type: {analysis.get('symmetry_type')}")
            print(f"   Cultural Region: {analysis.get('cultural_region')}")
            print(f"   Complexity Score: {analysis.get('complexity_score'):.3f}")
            print(f"   Confidence: {analysis.get('confidence'):.3f}")
            print(f"   Analysis Method: {analysis.get('analysis_method')}")
            
            return analysis
        else:
            print(f"❌ {image_name} failed: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"❌ {image_name} error: {e}")
        return None

def main():
    """Test different images"""
    print("🎯 TESTING FIXED ANALYSIS SYSTEM")
    print("=" * 60)
    
    # Create different test images
    images = {
        "Simple Kolam": create_simple_kolam(),
        "Complex Kolam": create_complex_kolam(),
        "Random Pattern": create_random_pattern()
    }
    
    results = {}
    
    for name, image_data in images.items():
        result = test_image_analysis(name, image_data)
        if result:
            results[name] = result
    
    # Compare results
    print(f"\n{'='*60}")
    print("📊 COMPARISON OF RESULTS")
    print(f"{'='*60}")
    
    if len(results) > 1:
        print("Image Type Variations:")
        
        # Check if results are different
        kolam_types = [r.get('kolam_type') for r in results.values()]
        symmetry_types = [r.get('symmetry_type') for r in results.values()]
        complexity_scores = [r.get('complexity_score') for r in results.values()]
        confidences = [r.get('confidence') for r in results.values()]
        analysis_methods = [r.get('analysis_method') for r in results.values()]
        
        print(f"   Kolam Types: {set(kolam_types)}")
        print(f"   Symmetry Types: {set(symmetry_types)}")
        print(f"   Complexity Scores: {[f'{c:.3f}' for c in complexity_scores]}")
        print(f"   Confidences: {[f'{c:.3f}' for c in confidences]}")
        print(f"   Analysis Methods: {set(analysis_methods)}")
        
        # Check if results are varied
        if len(set(kolam_types)) > 1:
            print("✅ Kolam types vary across images")
        else:
            print("⚠️ Kolam types are the same (possible issue)")
        
        if len(set(symmetry_types)) > 1:
            print("✅ Symmetry types vary across images")
        else:
            print("⚠️ Symmetry types are the same (possible issue)")
        
        if max(complexity_scores) - min(complexity_scores) > 0.1:
            print("✅ Complexity scores vary across images")
        else:
            print("⚠️ Complexity scores are similar (possible issue)")
        
        if max(confidences) - min(confidences) > 0.1:
            print("✅ Confidence scores vary across images")
        else:
            print("⚠️ Confidence scores are similar (possible issue)")
        
        if 'simple_enhanced' in analysis_methods:
            print("🎉 SUCCESS: Using simple enhanced analyzer!")
        else:
            print(f"⚠️ Using: {set(analysis_methods)}")
    
    print(f"\n🎯 Analysis complete! Tested {len(results)} images.")

if __name__ == "__main__":
    main()















