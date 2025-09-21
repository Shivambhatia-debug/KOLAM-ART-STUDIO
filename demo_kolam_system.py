"""
Kolam System Demonstration
==========================

This script demonstrates the complete Kolam analysis and generation system
for the AICTE problem statement 25107.
"""

import matplotlib.pyplot as plt
import numpy as np
from kolam_analyzer import (
    KolamGenerator, KolamAnalyzer, KolamVisualizer, 
    SymmetryType, KolamPattern
)
from advanced_kolam_analysis import (
    generate_lsystem_kolam, KolamClassifier, 
    CulturalSignificanceAnalyzer
)

def demonstrate_basic_patterns():
    """Demonstrate basic Kolam pattern generation and analysis"""
    print("🎨 Basic Kolam Pattern Generation")
    print("=" * 50)
    
    generator = KolamGenerator()
    analyzer = KolamAnalyzer()
    visualizer = KolamVisualizer()
    
    # Generate different types of patterns
    patterns = []
    pattern_names = []
    
    # 1. Radial Symmetry Pattern
    radial_pattern = generator.generate_grid_pattern((5, 5), SymmetryType.RADIAL)
    patterns.append(radial_pattern)
    pattern_names.append("Radial Symmetry")
    
    # 2. Bilateral Symmetry Pattern
    bilateral_pattern = generator.generate_grid_pattern((4, 4), SymmetryType.BILATERAL)
    patterns.append(bilateral_pattern)
    pattern_names.append("Bilateral Symmetry")
    
    # 3. Rotational Symmetry Pattern
    rotational_pattern = generator.generate_grid_pattern((6, 6), SymmetryType.ROTATIONAL)
    patterns.append(rotational_pattern)
    pattern_names.append("Rotational Symmetry")
    
    # 4. Fractal Pattern
    base_pattern = generator.generate_grid_pattern((3, 3), SymmetryType.RADIAL)
    fractal_pattern = generator.generate_fractal_kolam(base_pattern, 2)
    patterns.append(fractal_pattern)
    pattern_names.append("Fractal Pattern")
    
    # Analyze each pattern
    print("\n📊 Pattern Analysis Results:")
    print("-" * 30)
    
    for i, (pattern, name) in enumerate(zip(patterns, pattern_names)):
        symmetry = analyzer.analyze_symmetry(pattern.points)
        fractal_props = analyzer.analyze_fractal_properties(pattern)
        
        print(f"\n{name}:")
        print(f"  Symmetry Type: {symmetry.value}")
        print(f"  Fractal Dimension: {fractal_props['fractal_dimension']:.3f}")
        print(f"  Self-Similarity: {fractal_props['self_similarity']}")
        print(f"  Complexity: {fractal_props['complexity_level']}")
        print(f"  Points: {len(pattern.points)}, Lines: {len(pattern.lines)}")
    
    # Visualize patterns
    print("\n🖼️  Visualizing patterns...")
    visualizer.compare_patterns(patterns, pattern_names)
    
    return patterns

def demonstrate_advanced_analysis():
    """Demonstrate advanced analysis capabilities"""
    print("\n🔬 Advanced Kolam Analysis")
    print("=" * 50)
    
    # Generate L-System pattern
    print("\n1. Generating L-System Kolam...")
    lsystem_pattern = generate_lsystem_kolam(iterations=3)
    print(f"✓ Generated L-System pattern with {len(lsystem_pattern.points)} points")
    
    # Advanced classification
    print("\n2. Advanced pattern classification...")
    classifier = KolamClassifier()
    features = classifier.extract_features(lsystem_pattern)
    
    print("Advanced Features:")
    key_features = ['fractal_dimension', 'self_similarity', 'recursive_structure', 
                   'point_count', 'density', 'spread']
    for feature in key_features:
        if feature in features:
            print(f"  {feature}: {features[feature]:.3f}")
    
    # Cultural analysis
    print("\n3. Cultural significance analysis...")
    cultural_analyzer = CulturalSignificanceAnalyzer()
    interpretation = cultural_analyzer.get_cultural_interpretation(lsystem_pattern)
    
    print(f"Most likely region: {interpretation['most_likely_region']}")
    print(f"Confidence: {interpretation['confidence']:.2f}")
    print(f"Cultural significance: {interpretation['cultural_significance']}")
    
    return lsystem_pattern

def demonstrate_mathematical_principles():
    """Demonstrate the mathematical principles identified"""
    print("\n📐 Mathematical Principles in Kolam Design")
    print("=" * 50)
    
    principles = {
        "Grid-based Dot Patterns (Pulli)": {
            "description": "Traditional foundation using equidistant points",
            "mathematical_concept": "Cartesian coordinate system, spatial reasoning",
            "implementation": "Grid generation with configurable spacing"
        },
        "Symmetry Types": {
            "description": "Radial, bilateral, and rotational symmetry",
            "mathematical_concept": "Group theory, transformation geometry",
            "implementation": "Geometric analysis of point distributions"
        },
        "Fractal Properties": {
            "description": "Self-similarity and recursive patterns",
            "mathematical_concept": "Fractal geometry, L-Systems",
            "implementation": "Box-counting dimension, recursive generation"
        },
        "Geometric Shapes": {
            "description": "Circles, squares, triangles, and curves",
            "mathematical_concept": "Euclidean geometry, parametric curves",
            "implementation": "Shape generation and pattern recognition"
        },
        "Continuous Line Patterns": {
            "description": "Sikku Kolam with unbroken lines",
            "mathematical_concept": "Graph theory, Eulerian paths",
            "implementation": "Line generation algorithms"
        }
    }
    
    for principle, details in principles.items():
        print(f"\n{principle}:")
        print(f"  Description: {details['description']}")
        print(f"  Mathematical Concept: {details['mathematical_concept']}")
        print(f"  Implementation: {details['implementation']}")

def demonstrate_cultural_significance():
    """Demonstrate cultural significance analysis"""
    print("\n🏛️  Cultural Significance Analysis")
    print("=" * 50)
    
    cultural_analyzer = CulturalSignificanceAnalyzer()
    
    # Create patterns representing different regions
    generator = KolamGenerator()
    
    # Tamil Nadu style (radial, circular)
    tamil_pattern = generator.generate_grid_pattern((7, 7), SymmetryType.RADIAL)
    tamil_analysis = cultural_analyzer.get_cultural_interpretation(tamil_pattern)
    
    # Karnataka style (bilateral, geometric)
    karnataka_pattern = generator.generate_grid_pattern((6, 6), SymmetryType.BILATERAL)
    karnataka_analysis = cultural_analyzer.get_cultural_interpretation(karnataka_pattern)
    
    # Andhra Pradesh style (rotational, floral)
    andhra_pattern = generator.generate_grid_pattern((8, 8), SymmetryType.ROTATIONAL)
    andhra_analysis = cultural_analyzer.get_cultural_interpretation(andhra_pattern)
    
    print("\nRegional Pattern Analysis:")
    print("-" * 30)
    
    patterns = [
        ("Tamil Nadu Style", tamil_pattern, tamil_analysis),
        ("Karnataka Style", karnataka_pattern, karnataka_analysis),
        ("Andhra Pradesh Style", andhra_pattern, andhra_analysis)
    ]
    
    for name, pattern, analysis in patterns:
        print(f"\n{name}:")
        print(f"  Detected Region: {analysis['most_likely_region']}")
        print(f"  Confidence: {analysis['confidence']:.2f}")
        print(f"  Cultural Significance: {analysis['cultural_significance']}")
        
        print("  Regional Scores:")
        for region, score in analysis['regional_scores'].items():
            print(f"    {region}: {score:.3f}")

def generate_comprehensive_report():
    """Generate a comprehensive analysis report"""
    print("\n📋 Comprehensive Analysis Report")
    print("=" * 50)
    
    # Generate various patterns
    generator = KolamGenerator()
    analyzer = KolamAnalyzer()
    classifier = KolamClassifier()
    cultural_analyzer = CulturalSignificanceAnalyzer()
    
    patterns = []
    
    # Basic patterns
    patterns.append(("Radial", generator.generate_grid_pattern((5, 5), SymmetryType.RADIAL)))
    patterns.append(("Bilateral", generator.generate_grid_pattern((4, 4), SymmetryType.BILATERAL)))
    patterns.append(("Rotational", generator.generate_grid_pattern((6, 6), SymmetryType.ROTATIONAL)))
    
    # Fractal pattern
    base = generator.generate_grid_pattern((3, 3), SymmetryType.RADIAL)
    patterns.append(("Fractal", generator.generate_fractal_kolam(base, 2)))
    
    # L-System pattern
    patterns.append(("L-System", generate_lsystem_kolam(3)))
    
    # Analyze all patterns
    report_data = []
    
    for name, pattern in patterns:
        # Basic analysis
        symmetry = analyzer.analyze_symmetry(pattern.points)
        fractal_props = analyzer.analyze_fractal_properties(pattern)
        
        # Advanced analysis
        features = classifier.extract_features(pattern)
        cultural_analysis = cultural_analyzer.get_cultural_interpretation(pattern)
        
        report_data.append({
            'name': name,
            'symmetry_type': symmetry.value,
            'fractal_dimension': fractal_props['fractal_dimension'],
            'self_similarity': fractal_props['self_similarity'],
            'complexity': fractal_props['complexity_level'],
            'point_count': len(pattern.points),
            'line_count': len(pattern.lines),
            'cultural_region': cultural_analysis['most_likely_region'],
            'cultural_confidence': cultural_analysis['confidence']
        })
    
    # Print report
    print("\nPattern Analysis Summary:")
    print("-" * 40)
    
    for data in report_data:
        print(f"\n{data['name']} Pattern:")
        print(f"  Symmetry: {data['symmetry_type']}")
        print(f"  Fractal Dimension: {data['fractal_dimension']:.3f}")
        print(f"  Self-Similarity: {data['self_similarity']}")
        print(f"  Complexity: {data['complexity']}")
        print(f"  Points: {data['point_count']}, Lines: {data['line_count']}")
        print(f"  Cultural Region: {data['cultural_region']} ({data['cultural_confidence']:.2f})")
    
    # Save detailed report
    import json
    with open('kolam_comprehensive_report.json', 'w') as f:
        json.dump(report_data, f, indent=2)
    
    print(f"\n📊 Detailed report saved to 'kolam_comprehensive_report.json'")
    
    return report_data

def main():
    """Main demonstration function"""
    print("🎨 KOLAM DESIGN ANALYZER AND GENERATOR")
    print("=" * 60)
    print("AICTE Problem Statement 25107")
    print("Indian Knowledge Systems (IKS)")
    print("Category: Software | Theme: Heritage & Culture")
    print("=" * 60)
    
    try:
        # 1. Demonstrate basic patterns
        basic_patterns = demonstrate_basic_patterns()
        
        # 2. Demonstrate advanced analysis
        advanced_pattern = demonstrate_advanced_analysis()
        
        # 3. Show mathematical principles
        demonstrate_mathematical_principles()
        
        # 4. Show cultural significance
        demonstrate_cultural_significance()
        
        # 5. Generate comprehensive report
        report_data = generate_comprehensive_report()
        
        print("\n✅ DEMONSTRATION COMPLETE!")
        print("=" * 60)
        print("Key Achievements:")
        print("✓ Identified design principles behind Kolam designs")
        print("✓ Developed algorithms for pattern analysis")
        print("✓ Created Kolam generation system")
        print("✓ Implemented cultural significance analysis")
        print("✓ Demonstrated mathematical foundations")
        print("✓ Generated comprehensive analysis report")
        
        print("\n📁 Generated Files:")
        print("  - kolam_analyzer.py (Main analysis module)")
        print("  - advanced_kolam_analysis.py (Advanced features)")
        print("  - demo_kolam_system.py (This demonstration)")
        print("  - requirements.txt (Dependencies)")
        print("  - README.md (Documentation)")
        print("  - kolam_comprehensive_report.json (Analysis results)")
        
        print("\n🎯 Problem Statement Addressed:")
        print("  ✓ Computer programs developed in Python")
        print("  ✓ Design principles identified and analyzed")
        print("  ✓ Kolam recreation capabilities implemented")
        print("  ✓ Mathematical underpinnings demonstrated")
        print("  ✓ Cultural significance preserved")
        
    except Exception as e:
        print(f"\n❌ Error during demonstration: {e}")
        print("Please ensure all dependencies are installed:")
        print("pip install -r requirements.txt")

if __name__ == "__main__":
    main()

