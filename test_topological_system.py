#!/usr/bin/env python3
"""
Test script for the Topological Kolam Generation System
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_topological_generator():
    """Test the topological kolam generator"""
    print("Testing Topological Kolam Generator...")
    
    try:
        from topological_kolam_generator import TopologicalKolamGenerator, BondType, SymmetryType
        
        generator = TopologicalKolamGenerator()
        
        # Test with 3 dots
        dots = [(100, 100), (200, 100), (150, 173)]
        pattern = generator.generate_kolam(
            dots=dots,
            num_junctions=1,
            bond_types=[BondType.CROSS, BondType.DOUBLE],
            symmetry_type=SymmetryType.RADIAL,
            cultural_region="tamil_nadu"
        )
        
        print(f"✅ Generated pattern with {len(pattern.points)} points")
        print(f"✅ Created {len(pattern.junctions)} junctions")
        print(f"✅ Generated {len(pattern.paths)} paths")
        print(f"✅ Parent type: {pattern.parent_type}")
        print(f"✅ Symmetry: {pattern.symmetry_type.value}")
        print(f"✅ Numeric representation: {pattern.numeric_representation[:50]}...")
        print(f"✅ Cultural name: {pattern.cultural_metadata['name']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing topological generator: {e}")
        return False

def test_rules_validator():
    """Test the kolam rules validator"""
    print("\nTesting Kolam Rules Validator...")
    
    try:
        from kolam_rules_validator import KolamRulesValidator
        
        validator = KolamRulesValidator()
        
        # Test with a valid pattern
        points = [(100, 100), (200, 100), (150, 173)]
        paths = [
            [(100, 100), (200, 100), (150, 173), (100, 100)]  # Closed triangle
        ]
        
        result = validator.validate_pattern(points, paths)
        
        print(f"✅ Validation result: {result['valid']}")
        print(f"✅ Score: {result['score']}")
        print(f"✅ Rules status: {result['rules_status']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing rules validator: {e}")
        return False

def test_pattern_templates():
    """Test the pattern templates"""
    print("\nTesting Pattern Templates...")
    
    try:
        from kolam_pattern_templates import KolamPatternTemplates
        
        templates = KolamPatternTemplates()
        
        # Test getting templates
        three_dot_templates = templates.get_templates_by_dots(3)
        tamil_templates = templates.get_templates_by_region("tamil_nadu")
        summary = templates.get_template_summary()
        
        print(f"✅ Found {len(three_dot_templates)} templates for 3 dots")
        print(f"✅ Found {len(tamil_templates)} Tamil Nadu templates")
        print(f"✅ Total templates: {summary['total_templates']}")
        print(f"✅ Templates by dots: {summary['by_dots']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing pattern templates: {e}")
        return False

def test_backend_api():
    """Test the backend API endpoints"""
    print("\nTesting Backend API...")
    
    try:
        import requests
        import json
        
        # Test health endpoint
        response = requests.get('http://localhost:5000/api/health', timeout=5)
        if response.status_code == 200:
            health_data = response.json()
            print(f"✅ Backend is healthy: {health_data['status']}")
            print(f"✅ Advanced features: {health_data['advanced_features']}")
        else:
            print(f"❌ Backend health check failed: {response.status_code}")
            return False
        
        # Test pattern templates endpoint
        response = requests.get('http://localhost:5000/api/patterns', timeout=5)
        if response.status_code == 200:
            patterns_data = response.json()
            print(f"✅ Found {patterns_data['count']} pattern templates")
        else:
            print(f"❌ Pattern templates endpoint failed: {response.status_code}")
            return False
        
        # Test topological generation endpoint
        test_data = {
            "num_dots": 3,
            "num_junctions": 1,
            "bond_types": ["CROSS", "DOUBLE"],
            "symmetry_type": "RADIAL",
            "cultural_region": "tamil_nadu"
        }
        
        response = requests.post(
            'http://localhost:5000/api/generate-topological',
            json=test_data,
            timeout=10
        )
        
        if response.status_code == 200:
            pattern_data = response.json()
            print(f"✅ Generated topological pattern successfully")
            print(f"✅ Pattern has {len(pattern_data['pattern']['points'])} points")
        else:
            print(f"❌ Topological generation failed: {response.status_code}")
            return False
        
        return True
        
    except requests.exceptions.ConnectionError:
        print("❌ Backend not running. Please start the backend server first.")
        return False
    except Exception as e:
        print(f"❌ Error testing backend API: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 Testing Topological Kolam Generation System")
    print("=" * 60)
    
    tests = [
        test_topological_generator,
        test_rules_validator,
        test_pattern_templates,
        test_backend_api
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("=" * 60)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The system is working correctly.")
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)













