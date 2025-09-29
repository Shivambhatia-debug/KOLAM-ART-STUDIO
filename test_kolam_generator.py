#!/usr/bin/env python3
"""
Test Script for Kolam Pattern Generator
======================================

Comprehensive test of all features of the Kolam Pattern Generator.
"""

import os
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from kolam_pattern_generator_ml import KolamPatternGenerator, create_sample_csv, create_sample_image

def test_csv_processing():
    """Test CSV pattern processing"""
    print("🧪 Testing CSV Pattern Processing...")
    
    # Create test CSV with coordinates
    test_coords = [
        [0, 0], [1, 0], [1, 1], [0, 1], [0, 0],  # Square
        [0.5, 0.5], [1.5, 0.5], [1.5, 1.5], [0.5, 1.5], [0.5, 0.5]  # Inner square
    ]
    
    df = pd.DataFrame(test_coords, columns=['x', 'y'])
    df.to_csv('test_coordinates.csv', index=False)
    
    # Test coordinate-based CSV
    generator = KolamPatternGenerator("test_output_csv")
    pattern_data = generator.load_csv_pattern('test_coordinates.csv')
    
    print(f"   ✅ Loaded {pattern_data['n_points']} points from CSV")
    
    # Generate variations
    variations = generator.generate_variations(pattern_data, 6)
    ml_patterns = generator.apply_ml_transformations(pattern_data)
    
    all_patterns = variations + ml_patterns
    generator.visualize_and_save(all_patterns, pattern_data)
    
    print(f"   ✅ Generated {len(all_patterns)} patterns from CSV")
    
    # Cleanup
    os.remove('test_coordinates.csv')
    
    return True

def test_edge_based_csv():
    """Test edge-based CSV processing"""
    print("🧪 Testing Edge-based CSV Processing...")
    
    # Create test CSV with edges
    test_edges = [
        {'source': 0, 'target': 1},
        {'source': 1, 'target': 2},
        {'source': 2, 'target': 3},
        {'source': 3, 'target': 0},
        {'source': 0, 'target': 2},  # Diagonal
        {'source': 1, 'target': 3}   # Diagonal
    ]
    
    df = pd.DataFrame(test_edges)
    df.to_csv('test_edges.csv', index=False)
    
    # Test edge-based CSV
    generator = KolamPatternGenerator("test_output_edges")
    pattern_data = generator.load_csv_pattern('test_edges.csv')
    
    print(f"   ✅ Loaded {pattern_data['n_edges']} edges from CSV")
    
    # Generate variations
    variations = generator.generate_variations(pattern_data, 4)
    generator.visualize_and_save(variations, pattern_data)
    
    print(f"   ✅ Generated {len(variations)} patterns from edges")
    
    # Cleanup
    os.remove('test_edges.csv')
    
    return True

def test_image_processing():
    """Test image pattern processing"""
    print("🧪 Testing Image Pattern Processing...")
    
    # Create a test image
    fig, ax = plt.subplots(figsize=(8, 8))
    
    # Draw a complex Kolam pattern
    # Outer circle
    circle1 = plt.Circle((0, 0), 3, fill=False, linewidth=4, color='black')
    ax.add_patch(circle1)
    
    # Inner circles
    circle2 = plt.Circle((0, 0), 2, fill=False, linewidth=3, color='black')
    ax.add_patch(circle2)
    
    circle3 = plt.Circle((0, 0), 1, fill=False, linewidth=2, color='black')
    ax.add_patch(circle3)
    
    # Cross pattern
    ax.plot([-2, 2], [0, 0], 'k-', linewidth=3)
    ax.plot([0, 0], [-2, 2], 'k-', linewidth=3)
    
    # Dots
    for angle in np.linspace(0, 2*np.pi, 8, endpoint=False):
        x = 2.5 * np.cos(angle)
        y = 2.5 * np.sin(angle)
        dot = plt.Circle((x, y), 0.2, color='black')
        ax.add_patch(dot)
    
    ax.set_xlim(-4, 4)
    ax.set_ylim(-4, 4)
    ax.set_aspect('equal')
    ax.axis('off')
    
    plt.savefig('test_kolam_image.png', dpi=150, bbox_inches='tight', 
                facecolor='white', edgecolor='none')
    plt.close()
    
    # Test image processing
    generator = KolamPatternGenerator("test_output_image")
    pattern_data = generator.extract_image_pattern('test_kolam_image.png')
    
    print(f"   ✅ Extracted {pattern_data['n_points']} points from image")
    
    # Generate variations
    variations = generator.generate_variations(pattern_data, 6)
    ml_patterns = generator.apply_ml_transformations(pattern_data)
    
    all_patterns = variations + ml_patterns
    generator.visualize_and_save(all_patterns, pattern_data)
    
    print(f"   ✅ Generated {len(all_patterns)} patterns from image")
    
    # Cleanup
    os.remove('test_kolam_image.png')
    
    return True

def test_ml_transformations():
    """Test ML transformations specifically"""
    print("🧪 Testing ML Transformations...")
    
    # Create a complex pattern for ML testing
    angles = np.linspace(0, 2*np.pi, 16, endpoint=False)
    radius = 2
    x = radius * np.cos(angles)
    y = radius * np.sin(angles)
    
    # Add some noise for more interesting ML results
    x += np.random.normal(0, 0.1, len(x))
    y += np.random.normal(0, 0.1, len(y))
    
    coordinates = np.column_stack([x, y])
    
    pattern_data = {
        'type': 'test_ml',
        'coordinates': coordinates,
        'edges': [(i, (i+1)%len(coordinates)) for i in range(len(coordinates))],
        'source': 'test_ml_pattern',
        'n_points': len(coordinates),
        'n_edges': len(coordinates)
    }
    
    generator = KolamPatternGenerator("test_output_ml")
    
    # Test ML transformations
    ml_patterns = generator.apply_ml_transformations(pattern_data)
    
    print(f"   ✅ Generated {len(ml_patterns)} ML transformations")
    
    # Visualize ML patterns
    generator.visualize_and_save(ml_patterns, pattern_data)
    
    return True

def test_hybrid_patterns():
    """Test hybrid pattern generation"""
    print("🧪 Testing Hybrid Pattern Generation...")
    
    generator = KolamPatternGenerator("test_output_hybrid")
    
    # Create two different patterns
    # Pattern 1: Square
    square_coords = np.array([[0, 0], [2, 0], [2, 2], [0, 2], [0, 0]])
    pattern1 = {
        'type': 'square',
        'coordinates': square_coords,
        'edges': [(i, (i+1)%len(square_coords)) for i in range(len(square_coords))],
        'source': 'square_pattern',
        'n_points': len(square_coords),
        'n_edges': len(square_coords)
    }
    
    # Pattern 2: Triangle
    triangle_coords = np.array([[1, 0], [0, 2], [2, 2], [1, 0]])
    pattern2 = {
        'type': 'triangle',
        'coordinates': triangle_coords,
        'edges': [(i, (i+1)%len(triangle_coords)) for i in range(len(triangle_coords))],
        'source': 'triangle_pattern',
        'n_points': len(triangle_coords),
        'n_edges': len(triangle_coords)
    }
    
    # Store both patterns
    generator.patterns = [pattern1, pattern2]
    
    # Generate hybrid patterns
    hybrid_patterns = generator.apply_ml_transformations(pattern2)
    
    print(f"   ✅ Generated {len(hybrid_patterns)} hybrid patterns")
    
    # Visualize
    generator.visualize_and_save(hybrid_patterns, pattern2)
    
    return True

def run_comprehensive_test():
    """Run all tests"""
    print("🚀 COMPREHENSIVE KOLAM PATTERN GENERATOR TEST")
    print("=" * 60)
    
    tests = [
        ("CSV Coordinate Processing", test_csv_processing),
        ("CSV Edge Processing", test_edge_based_csv),
        ("Image Processing", test_image_processing),
        ("ML Transformations", test_ml_transformations),
        ("Hybrid Patterns", test_hybrid_patterns)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            print(f"\n📋 Running: {test_name}")
            success = test_func()
            results.append((test_name, "✅ PASSED" if success else "❌ FAILED"))
        except Exception as e:
            print(f"   ❌ Error: {e}")
            results.append((test_name, f"❌ ERROR: {e}"))
    
    # Print results
    print("\n" + "=" * 60)
    print("📊 TEST RESULTS")
    print("=" * 60)
    
    for test_name, result in results:
        print(f"{result} {test_name}")
    
    passed = sum(1 for _, result in results if "✅" in result)
    total = len(results)
    
    print(f"\n🎯 Overall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 ALL TESTS PASSED! System is ready for SIH presentation!")
    else:
        print("⚠️ Some tests failed. Please check the errors above.")
    
    print("=" * 60)

if __name__ == "__main__":
    run_comprehensive_test()















