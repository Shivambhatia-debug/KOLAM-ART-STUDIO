#!/usr/bin/env python3
"""
Enhanced Line Brahma's Knot with better visualization
"""

import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import numpy as np
from topological_kolam_generator import TopologicalKolamGenerator, Point
from kolam_pattern_templates import KolamPatternTemplates

def enhanced_line_brahma():
    """Generate enhanced line Brahma's Knot"""
    print("🎨 Enhanced Line Brahma's Knot Generation")
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
    
    # Create enhanced figure
    print("🎨 Creating enhanced figure...")
    
    fig, ax = plt.subplots(1, 1, figsize=(20, 20))
    ax.set_aspect('equal')
    ax.set_title(f"Enhanced Brahma's Knot - {brahma_template.name}", 
                fontsize=24, fontweight='bold', pad=30)
    
    # Draw the enhanced pattern
    draw_enhanced_brahma_pattern(ax, brahma_paths, points)
    
    # Set up the plot
    ax.grid(True, alpha=0.2, linewidth=0.5)
    ax.set_xlabel('X Coordinate', fontsize=14, fontweight='bold')
    ax.set_ylabel('Y Coordinate', fontsize=14, fontweight='bold')
    
    # Add enhanced pattern info
    info_text = f"""
Enhanced Brahma's Knot Details:
• Dots: {len(points)}
• Paths: {len(brahma_paths)}
• Main Path Points: {len(brahma_paths[0]) if brahma_paths else 0}
• Template: {brahma_template.name}
• Style: Enhanced Lines + Dots + Grid
• Symmetry: Rotational
• Cultural: Eternal Knot Symbol
    """
    
    ax.text(0.02, 0.98, info_text, transform=ax.transAxes, fontsize=12,
            verticalalignment='top', bbox=dict(boxstyle='round,pad=0.5', 
            facecolor='lightcyan', alpha=0.9, edgecolor='navy', linewidth=2))
    
    # Add cultural significance
    cultural_text = """
Cultural Significance:
• Brahma Mudi (Eternal Knot)
• Symbol of cosmic unity
• Continuous loop = infinite cycle
• 5x5 grid = five elements
• No loose ends = completeness
    """
    
    ax.text(0.98, 0.02, cultural_text, transform=ax.transAxes, fontsize=10,
            verticalalignment='bottom', horizontalalignment='right',
            bbox=dict(boxstyle='round,pad=0.5', facecolor='lightyellow', 
            alpha=0.9, edgecolor='orange', linewidth=2))
    
    # Save the figure
    plt.tight_layout()
    plt.savefig('enhanced_brahma_knot.png', dpi=300, bbox_inches='tight')
    print("✅ Enhanced figure saved as 'enhanced_brahma_knot.png'")
    
    print("\n🎉 Enhanced Line Brahma's Knot generated successfully!")
    print("   Check 'enhanced_brahma_knot.png' for the high-quality image")

def draw_enhanced_brahma_pattern(ax, paths, points):
    """Draw the enhanced Brahma's Knot pattern"""
    
    # Draw paths first (so they appear behind dots)
    if paths:
        print(f"   Drawing {len(paths)} enhanced paths...")
        for i, path in enumerate(paths):
            if path and len(path) >= 2:
                x_coords = [point[0] for point in path]
                y_coords = [point[1] for point in path]
                
                # Draw thick red lines with gradient effect
                ax.plot(x_coords, y_coords, 'r-', linewidth=8, alpha=0.9, 
                       label=f'Brahma\'s Knot Path' if i == 0 else "")
                
                # Add line segments for better visibility
                for j in range(len(path) - 1):
                    x1, y1 = path[j]
                    x2, y2 = path[j + 1]
                    ax.plot([x1, x2], [y1, y2], 'r-', linewidth=6, alpha=0.8)
                
                # Add shadow effect
                ax.plot(x_coords, y_coords, 'darkred', linewidth=10, alpha=0.3)
    
    # Draw enhanced dots
    print(f"   Drawing {len(points)} enhanced dots...")
    for i, point in enumerate(points):
        # Draw dot with white center and shadow
        ax.plot(point.x, point.y, 'ro', markersize=20, markeredgecolor='white', markeredgewidth=6)
        ax.plot(point.x, point.y, 'darkred', markersize=22, alpha=0.3)
        
        # Label key dots with enhanced styling
        if i in [0, 4, 12, 20, 24]:  # Corner and center dots
            ax.annotate(f'{i}', (point.x, point.y), xytext=(15, 15), 
                       textcoords='offset points', fontsize=14, fontweight='bold',
                       bbox=dict(boxstyle='round,pad=0.5', facecolor='gold', 
                       alpha=0.9, edgecolor='darkorange', linewidth=2))
    
    # Draw enhanced grid lines
    print("   Drawing enhanced grid lines...")
    for i in range(5):
        # Vertical lines
        ax.axvline(x=points[i*5].x, color='gray', linestyle='--', alpha=0.4, linewidth=2)
        # Horizontal lines
        ax.axhline(y=points[i].y, color='gray', linestyle='--', alpha=0.4, linewidth=2)
    
    # Add decorative elements
    print("   Adding decorative elements...")
    
    # Add corner decorations
    corners = [(points[0].x, points[0].y), (points[4].x, points[4].y), 
               (points[20].x, points[20].y), (points[24].x, points[24].y)]
    
    for corner_x, corner_y in corners:
        # Draw decorative circles
        circle = plt.Circle((corner_x, corner_y), 15, fill=False, 
                          color='gold', linewidth=3, alpha=0.7)
        ax.add_patch(circle)
    
    # Add center decoration
    center_x, center_y = points[12].x, points[12].y
    center_circle = plt.Circle((center_x, center_y), 25, fill=False, 
                              color='navy', linewidth=4, alpha=0.8)
    ax.add_patch(center_circle)

if __name__ == "__main__":
    enhanced_line_brahma()













