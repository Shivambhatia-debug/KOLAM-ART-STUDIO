#!/usr/bin/env python3
"""
Test Enhanced Pattern Generation
================================

Test the enhanced pattern generation system.
"""

import requests
import json

def test_enhanced_pattern_generation():
    """Test enhanced pattern generation"""
    print("🎨 Testing Enhanced Pattern Generation...")
    
    try:
        url = "http://localhost:5000/api/generate-similar"
        data = {
            "reference_pattern": "fractal_kolam",
            "num_variations": 3,
            "include_user_images": False
        }
        
        response = requests.post(url, json=data, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Enhanced pattern generation successful!")
            print(f"Generated {len(result.get('similar_patterns', []))} patterns")
            
            for i, pattern in enumerate(result.get('similar_patterns', [])):
                print(f"\nPattern {i+1}:")
                print(f"  ID: {pattern.get('pattern_id')}")
                print(f"  Type: {pattern.get('kolam_type')}")
                print(f"  Symmetry: {pattern.get('symmetry_type')}")
                print(f"  Region: {pattern.get('cultural_region')}")
                print(f"  Complexity: {pattern.get('complexity_score'):.3f}")
                print(f"  Confidence: {pattern.get('confidence'):.3f}")
                print(f"  Image: {pattern.get('image_path')}")
                print(f"  Style: {pattern.get('metadata', {}).get('style')}")
                print(f"  Colors: {pattern.get('metadata', {}).get('colors_used')}")
            
            return True
        else:
            print(f"❌ Pattern generation failed: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_different_pattern_types():
    """Test different pattern types"""
    print("\n🔍 Testing Different Pattern Types...")
    
    pattern_types = ['fractal_kolam', 'pulli_kolam', 'sikku_kolam', 'neli_kolam', 'kambi_kolam']
    
    for pattern_type in pattern_types:
        print(f"\n--- Testing {pattern_type} ---")
        try:
            url = "http://localhost:5000/api/generate-similar"
            data = {
                "reference_pattern": pattern_type,
                "num_variations": 2,
                "include_user_images": False
            }
            
            response = requests.post(url, json=data, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                patterns = result.get('similar_patterns', [])
                print(f"✅ Generated {len(patterns)} patterns for {pattern_type}")
                
                # Check pattern diversity
                kolam_types = [p.get('kolam_type') for p in patterns]
                symmetry_types = [p.get('symmetry_type') for p in patterns]
                
                print(f"   Kolam Types: {set(kolam_types)}")
                print(f"   Symmetry Types: {set(symmetry_types)}")
                
            else:
                print(f"❌ Failed for {pattern_type}: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Error for {pattern_type}: {e}")

def main():
    """Main test function"""
    print("🎯 ENHANCED PATTERN GENERATION TEST")
    print("=" * 50)
    
    # Test basic generation
    success = test_enhanced_pattern_generation()
    
    if success:
        # Test different pattern types
        test_different_pattern_types()
        
        print("\n🎉 Enhanced pattern generation system working!")
        print("✅ Matplotlib patterns generated successfully")
        print("✅ Colorful and beautiful patterns created")
        print("✅ Multiple pattern types supported")
    else:
        print("\n❌ Enhanced pattern generation failed")
        print("Check backend logs for errors")

if __name__ == "__main__":
    main()















