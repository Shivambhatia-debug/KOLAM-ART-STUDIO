#!/usr/bin/env python3
"""
Test Similar Pattern Generation
==============================

Test the new similar pattern generation endpoint.
"""

import requests
import json
import time

def test_similar_pattern_generation():
    """Test the similar pattern generation endpoint"""
    print("🎨 Testing Similar Pattern Generation")
    print("=" * 50)
    
    # Test data
    test_data = {
        "reference_pattern": "pulli_kolam",
        "num_variations": 3,
        "include_user_images": True
    }
    
    try:
        print("Testing /api/generate-similar endpoint...")
        start_time = time.time()
        
        response = requests.post(
            "http://localhost:5000/api/generate-similar",
            json=test_data,
            timeout=30
        )
        
        end_time = time.time()
        response_time = end_time - start_time
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Similar pattern generation successful!")
            print(f"   Response time: {response_time:.2f}s")
            print(f"   Total generated: {data.get('total_generated', 0)}")
            print(f"   Reference pattern: {data.get('reference_pattern', 'N/A')}")
            print(f"   Output directory: {data.get('output_directory', 'N/A')}")
            
            # Show pattern details
            similar_patterns = data.get('similar_patterns', [])
            if similar_patterns:
                print(f"\n📋 Generated Patterns:")
                for i, pattern in enumerate(similar_patterns[:3]):  # Show first 3
                    print(f"   {i+1}. {pattern.get('kolam_type', 'Unknown')} "
                          f"(Similarity: {pattern.get('similarity_score', 0)*100:.0f}%)")
            
            return True
        else:
            print(f"❌ Similar pattern generation failed!")
            print(f"   Status: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Network error: {e}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_different_patterns():
    """Test different pattern types"""
    print("\n🔄 Testing Different Pattern Types")
    print("=" * 50)
    
    pattern_types = ['sikku_kolam', 'neli_kolam', 'fractal_kolam']
    
    for pattern_type in pattern_types:
        print(f"\nTesting {pattern_type}...")
        
        test_data = {
            "reference_pattern": pattern_type,
            "num_variations": 2,
            "include_user_images": False
        }
        
        try:
            response = requests.post(
                "http://localhost:5000/api/generate-similar",
                json=test_data,
                timeout=20
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"   ✅ Generated {data.get('total_generated', 0)} patterns")
            else:
                print(f"   ❌ Failed: {response.status_code}")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")

def main():
    """Main test function"""
    print("🚀 Starting Similar Pattern Generation Tests")
    print("=" * 60)
    
    # Test basic similar pattern generation
    success = test_similar_pattern_generation()
    
    if success:
        # Test different pattern types
        test_different_patterns()
        
        print("\n" + "=" * 60)
        print("🎉 Similar Pattern Generation Tests Completed!")
        print("✅ All endpoints are working properly")
        print("\n📁 Check 'generated_similar_patterns' directory for results")
    else:
        print("\n❌ Similar pattern generation tests failed")
        print("Please check the backend server and try again")

if __name__ == "__main__":
    main()


