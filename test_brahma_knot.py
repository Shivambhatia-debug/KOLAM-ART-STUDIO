#!/usr/bin/env python3
"""
Test Brahma's Knot generation directly in Python
"""

import matplotlib.pyplot as plt
import numpy as np
from topological_kolam_generator import TopologicalKolamGenerator, Point
from kolam_pattern_templates import KolamPatternTemplates

def test_brahma_knot_generation():
    """Test Brahma's Knot generation and display"""
    print("🎨 Testing Brahma's Knot Generation...")
    print("=" * 50)
    
    # Initialize the generator
    generator = TopologicalKolamGenerator()
    templates = KolamPatternTemplates()
    
    # Get Brahma's Knot template
    brahma_template = None
    for template in templates.templates:
        if "brahma" in template.name.lower():
            brahma_template = template
            break
    
    if not brahma_template:
        print("❌ Brahma's Knot template not found!")
        return
    
    print(f"✅ Found template: {brahma_template.name}")
    print(f"   Dots: {brahma_template.num_dots}")
    print(f"   Type: {brahma_template.symmetry_type}")
    print(f"   Region: {brahma_template.region}")
    print()
    
    # Generate the pattern
    print("🔄 Generating Brahma's Knot pattern...")
    
    # Create points from template
    points = []
    for dot_pos in brahma_template.dot_positions:
        points.append(Point(dot_pos[0], dot_pos[1]))
    
    print(f"✅ Created {len(points)} points")
    
    # Generate junctions
    junctions = brahma_template.suggested_junctions
    print(f"✅ Created {len(junctions)} junctions")
    
    # Generate the pattern using topological method
    pattern = generator.generate_pattern(
        points=points,
        num_dots=brahma_template.num_dots,
        symmetry_type=brahma_template.symmetry_type,
        complexity=brahma_template.complexity
    )
    
    print(f"✅ Generated pattern with {len(pattern['paths'])} paths")
    print(f"   Points: {len(pattern['points'])}")
    print(f"   Junctions: {len(pattern['junctions'])}")
    print()
    
    # Display pattern details
    print("📊 Pattern Details:")
    print(f"   Numeric Representation: {pattern['numeric_representation']}")
    print(f"   Angle Encoding: {pattern['angle_encoding']}")
    print(f"   Tracing Sequence: {pattern['tracing_sequence']}")
    print()
    
    # Create visualization
    print("🎨 Creating visualization...")
    
    fig, ax = plt.subplots(1, 1, figsize=(12, 12))
    ax.set_aspect('equal')
    ax.set_title(f"Brahma's Knot - {brahma_template.name}", fontsize=16, fontweight='bold')
    
    # Draw paths
    if pattern['paths']:
        for i, path in enumerate(pattern['paths']):
            if len(path) >= 2:
                x_coords = [point[0] for point in path]
                y_coords = [point[1] for point in path]
                ax.plot(x_coords, y_coords, 'r-', linewidth=3, alpha=0.8, label=f'Path {i+1}' if i == 0 else "")
    
    # Draw dots
    for i, point in enumerate(pattern['points']):
        ax.plot(point.x, point.y, 'ro', markersize=8, markeredgecolor='white', markeredgewidth=2)
        if i < 5:  # Label first few dots
            ax.annotate(f'{i}', (point.x, point.y), xytext=(5, 5), textcoords='offset points', fontsize=8)
    
    # Draw junctions
    if pattern['junctions']:
        for junction in pattern['junctions']:
            p1 = pattern['points'][junction.point1_idx]
            p2 = pattern['points'][junction.point2_idx]
            ax.plot([p1.x, p2.x], [p1.y, p2.y], 'b--', alpha=0.5, linewidth=1)
    
    # Set up the plot
    ax.grid(True, alpha=0.3)
    ax.legend()
    ax.set_xlabel('X Coordinate')
    ax.set_ylabel('Y Coordinate')
    
    # Save the plot
    plt.tight_layout()
    plt.savefig('brahma_knot_test.png', dpi=300, bbox_inches='tight')
    print("✅ Pattern saved as 'brahma_knot_test.png'")
    
    # Show the plot
    plt.show()
    
    print("\n🎉 Brahma's Knot generation test completed!")
    print("   Check 'brahma_knot_test.png' for the visual result")

if __name__ == "__main__":
    test_brahma_knot_generation()
