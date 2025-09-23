#!/usr/bin/env python3
"""
Generate Brahma's Knot figure directly in Python terminal
"""

import matplotlib.pyplot as plt
import numpy as np
from topological_kolam_generator import TopologicalKolamGenerator, Point
from kolam_pattern_templates import KolamPatternTemplates

def generate_brahma_figure():
    """Generate and display Brahma's Knot figure"""
    print("🎨 Generating Brahma's Knot Figure...")
    print("=" * 50)
    
    # Initialize
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
    
    print(f"✅ Template: {brahma_template.name}")
    print(f"   Dots: {brahma_template.num_dots}")
    print(f"   Symmetry: {brahma_template.symmetry_type}")
    print()
    
    # Create points
    points = []
    for dot_pos in brahma_template.dot_positions:
        points.append(Point(dot_pos[0], dot_pos[1]))
    
    print(f"✅ Created {len(points)} points")
    
    # Generate the pattern using topological method
    print("🔄 Generating pattern using topological method...")
    
    # Convert points to dots format
    dots = [(point.x, point.y) for point in points]
    
    pattern = generator.generate_kolam(
        dots=dots,
        num_junctions=1,
        symmetry_type=brahma_template.symmetry_type,
        cultural_region=brahma_template.region.lower().replace(' ', '_')
    )
    
    print(f"✅ Generated pattern:")
    print(f"   Paths: {len(pattern['paths'])}")
    print(f"   Points: {len(pattern['points'])}")
    print(f"   Junctions: {len(pattern['junctions'])}")
    print()
    
    # Create the figure
    print("🎨 Creating figure...")
    
    fig, ax = plt.subplots(1, 1, figsize=(15, 15))
    ax.set_aspect('equal')
    ax.set_title(f"Brahma's Knot - {brahma_template.name}", fontsize=20, fontweight='bold', pad=20)
    
    # Draw the pattern
    draw_brahma_pattern(ax, pattern, points)
    
    # Set up the plot
    ax.grid(True, alpha=0.3)
    ax.set_xlabel('X Coordinate', fontsize=12)
    ax.set_ylabel('Y Coordinate', fontsize=12)
    
    # Add pattern info
    info_text = f"""
Pattern Details:
• Dots: {len(points)}
• Paths: {len(pattern['paths'])}
• Junctions: {len(pattern['junctions'])}
• Symmetry: {brahma_template.symmetry_type}
• Region: {brahma_template.region}
• Complexity: {brahma_template.complexity}
    """
    
    ax.text(0.02, 0.98, info_text, transform=ax.transAxes, fontsize=10,
            verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
    
    # Save the figure
    plt.tight_layout()
    plt.savefig('brahma_knot_figure.png', dpi=300, bbox_inches='tight')
    print("✅ Figure saved as 'brahma_knot_figure.png'")
    
    # Show the figure
    plt.show()
    
    print("\n🎉 Brahma's Knot figure generated successfully!")
    print("   Check 'brahma_knot_figure.png' for the high-quality image")

def draw_brahma_pattern(ax, pattern, points):
    """Draw the Brahma's Knot pattern"""
    
    # Draw paths first (so they appear behind dots)
    if pattern['paths']:
        print(f"   Drawing {len(pattern['paths'])} paths...")
        for i, path in enumerate(pattern['paths']):
            if path and len(path) >= 2:
                x_coords = [point[0] for point in path]
                y_coords = [point[1] for point in path]
                ax.plot(x_coords, y_coords, 'r-', linewidth=4, alpha=0.8, 
                       label=f'Brahma\'s Knot Path' if i == 0 else "")
    
    # Draw dots
    print(f"   Drawing {len(points)} dots...")
    for i, point in enumerate(points):
        ax.plot(point.x, point.y, 'ro', markersize=12, markeredgecolor='white', markeredgewidth=3)
        # Label some key dots
        if i in [0, 4, 12, 20, 24]:  # Corner and center dots
            ax.annotate(f'{i}', (point.x, point.y), xytext=(8, 8), 
                       textcoords='offset points', fontsize=10, fontweight='bold',
                       bbox=dict(boxstyle='round,pad=0.3', facecolor='yellow', alpha=0.7))
    
    # Draw junctions (optional, for debugging)
    if pattern['junctions']:
        print(f"   Drawing {len(pattern['junctions'])} junctions...")
        for junction in pattern['junctions'][:20]:  # Show first 20 junctions
            p1 = points[junction.point1_idx]
            p2 = points[junction.point2_idx]
            ax.plot([p1.x, p2.x], [p1.y, p2.y], 'b--', alpha=0.3, linewidth=1)

if __name__ == "__main__":
    generate_brahma_figure()
