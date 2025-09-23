#!/usr/bin/env python3
"""
Generate Brahma's Knot with lines (not just dots)
"""

import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import numpy as np
from topological_kolam_generator import TopologicalKolamGenerator, Point
from kolam_pattern_templates import KolamPatternTemplates

def generate_line_brahma():
    """Generate Brahma's Knot with lines"""
    print("🎨 Line Brahma's Knot Generation")
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
    print()
    
    # Create points
    points = []
    for dot_pos in brahma_template.dot_positions:
        points.append(Point(dot_pos[0], dot_pos[1]))
    
    print(f"✅ Created {len(points)} points")
    
    # Generate Brahma's Knot paths
    print("🔄 Generating Brahma's Knot paths...")
    brahma_paths = generator._create_brahma_knot_paths(points)
    
    print(f"✅ Generated {len(brahma_paths)} paths")
    if brahma_paths:
        print(f"   Main path has {len(brahma_paths[0])} points")
    
    # Create the figure with lines
    print("🎨 Creating figure with lines...")
    
    fig, ax = plt.subplots(1, 1, figsize=(15, 15))
    ax.set_aspect('equal')
    ax.set_title(f"Brahma's Knot - {brahma_template.name} (With Lines)", fontsize=20, fontweight='bold', pad=20)
    
    # Draw the pattern with lines
    draw_line_brahma_pattern(ax, brahma_paths, points)
    
    # Set up the plot
    ax.grid(True, alpha=0.3)
    ax.set_xlabel('X Coordinate', fontsize=12)
    ax.set_ylabel('Y Coordinate', fontsize=12)
    
    # Add pattern info
    info_text = f"""
Pattern Details:
• Dots: {len(points)}
• Paths: {len(brahma_paths)}
• Main Path Points: {len(brahma_paths[0]) if brahma_paths else 0}
• Template: {brahma_template.name}
• Style: Lines + Dots
    """
    
    ax.text(0.02, 0.98, info_text, transform=ax.transAxes, fontsize=10,
            verticalalignment='top', bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8))
    
    # Save the figure
    plt.tight_layout()
    plt.savefig('brahma_knot_lines.png', dpi=300, bbox_inches='tight')
    print("✅ Figure saved as 'brahma_knot_lines.png'")
    
    print("\n🎉 Line Brahma's Knot generated successfully!")
    print("   Check 'brahma_knot_lines.png' for the high-quality image")

def draw_line_brahma_pattern(ax, paths, points):
    """Draw the Brahma's Knot pattern with lines"""
    
    # Draw paths first (so they appear behind dots)
    if paths:
        print(f"   Drawing {len(paths)} paths...")
        for i, path in enumerate(paths):
            if path and len(path) >= 2:
                x_coords = [point[0] for point in path]
                y_coords = [point[1] for point in path]
                
                # Draw thick red lines
                ax.plot(x_coords, y_coords, 'r-', linewidth=6, alpha=0.9, 
                       label=f'Brahma\'s Knot Path' if i == 0 else "")
                
                # Add line segments for better visibility
                for j in range(len(path) - 1):
                    x1, y1 = path[j]
                    x2, y2 = path[j + 1]
                    ax.plot([x1, x2], [y1, y2], 'r-', linewidth=4, alpha=0.8)
    
    # Draw dots
    print(f"   Drawing {len(points)} dots...")
    for i, point in enumerate(points):
        # Draw dot with white center
        ax.plot(point.x, point.y, 'ro', markersize=15, markeredgecolor='white', markeredgewidth=4)
        
        # Label some key dots
        if i in [0, 4, 12, 20, 24]:  # Corner and center dots
            ax.annotate(f'{i}', (point.x, point.y), xytext=(10, 10), 
                       textcoords='offset points', fontsize=12, fontweight='bold',
                       bbox=dict(boxstyle='round,pad=0.3', facecolor='yellow', alpha=0.8))
    
    # Draw grid lines for reference
    print("   Drawing grid lines...")
    for i in range(5):
        # Vertical lines
        ax.axvline(x=points[i*5].x, color='gray', linestyle='--', alpha=0.3, linewidth=1)
        # Horizontal lines
        ax.axhline(y=points[i].y, color='gray', linestyle='--', alpha=0.3, linewidth=1)

if __name__ == "__main__":
    generate_line_brahma()













