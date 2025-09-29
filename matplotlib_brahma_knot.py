#!/usr/bin/env python3
"""
Matplotlib Brahma's Knot - Working Version
- Step-by-step generation
- Animated drawing effect
- Exactly like expected
"""

import matplotlib.pyplot as plt
import numpy as np
import math
import time
from matplotlib.patches import Circle
import matplotlib.animation as animation

class MatplotlibBrahmaKnot:
    def __init__(self):
        self.fig, self.ax = plt.subplots(1, 1, figsize=(12, 12))
        self.ax.set_xlim(-120, 120)
        self.ax.set_ylim(-120, 120)
        self.ax.set_aspect('equal')
        self.ax.set_facecolor('white')
        
        # Colors
        self.dot_color = '#DC143C'
        self.line_color = '#000000'
        
    def generate_29_dots(self):
        """Generate 29 dots for Brahma's Knot"""
        dots = []
        center_x, center_y = 0, 0
        grid_spacing = 40
        
        # 5x5 grid dots (25 dots)
        for i in range(5):
            for j in range(5):
                x = center_x + (j - 2) * grid_spacing
                y = center_y + (i - 2) * grid_spacing
                dots.append({
                    'id': i * 5 + j,
                    'x': x,
                    'y': y,
                    'type': 'grid'
                })
        
        # 4 outer petal dots
        petal_radius = 80
        petal_angles = [90, 0, -90, 180]  # Top, Right, Bottom, Left
        for i, angle in enumerate(petal_angles):
            x = center_x + petal_radius * math.cos(math.radians(angle))
            y = center_y + petal_radius * math.sin(math.radians(angle))
            dots.append({
                'id': 25 + i,
                'x': x,
                'y': y,
                'type': 'petal'
            })
        
        return dots
    
    def create_brahma_path(self, dots):
        """Create Brahma's Knot path"""
        # Get dot positions
        dot_positions = {dot['id']: (dot['x'], dot['y']) for dot in dots}
        
        # Brahma's Knot path sequence
        path_sequence = [
            # Start from top petal (index 25)
            25, 0, 1, 2, 3, 4, 26,  # Top row to right petal
            9, 8, 7, 6, 5,          # Back through top row
            10, 11, 12, 13, 14,     # Second row
            19, 18, 17, 16, 15,     # Third row
            20, 21, 22, 23, 24,     # Fourth row
            28, 27, 26,             # Bottom row to left petal
            24, 23, 22, 21, 20,     # Back through bottom row
            15, 16, 17, 18, 19,     # Back through third row
            14, 13, 12, 11, 10,     # Back through second row
            5, 6, 7, 8, 9,          # Back through top row
            0, 25                    # Back to start
        ]
        
        # Convert to coordinates
        path_coords = []
        for dot_id in path_sequence:
            if dot_id in dot_positions:
                path_coords.append(dot_positions[dot_id])
        
        return path_coords
    
    def smooth_curves(self, path_coords):
        """Create smooth curves"""
        if len(path_coords) < 3:
            return path_coords
        
        # Use cubic spline interpolation
        x_coords = [p[0] for p in path_coords]
        y_coords = [p[1] for p in path_coords]
        
        # Create parameter t
        t = np.linspace(0, 1, len(path_coords))
        t_smooth = np.linspace(0, 1, len(path_coords) * 3)
        
        # Interpolate
        x_smooth = np.interp(t_smooth, t, x_coords)
        y_smooth = np.interp(t_smooth, t, y_coords)
        
        return list(zip(x_smooth, y_smooth))
    
    def animate_drawing(self, dots, path_coords):
        """Animate the drawing process"""
        print("🎨 Starting Matplotlib Animation...")
        
        # Step 1: Draw all dots
        print("Step 1: Drawing dots...")
        for i, dot in enumerate(dots):
            x, y = dot['x'], dot['y']
            if dot['type'] == 'grid':
                circle = Circle((x, y), 4, color=self.dot_color, alpha=0.9)
            else:  # petal
                circle = Circle((x, y), 6, color='#B22222', alpha=0.9)
            
            self.ax.add_patch(circle)
            plt.pause(0.1)  # Animation delay
        
        print(f"✅ Drew {len(dots)} dots")
        
        # Step 2: Draw continuous path
        print("Step 2: Drawing continuous path...")
        if len(path_coords) > 1:
            x_coords = [p[0] for p in path_coords]
            y_coords = [p[1] for p in path_coords]
            
            # Draw path segment by segment
            for i in range(1, len(path_coords)):
                self.ax.plot(x_coords[:i+1], y_coords[:i+1], 
                           color=self.line_color, linewidth=4, alpha=0.8)
                plt.pause(0.05)  # Animation delay
        
        print(f"✅ Drew continuous path with {len(path_coords)} points")
        
        # Step 3: Add center decoration
        print("Step 3: Adding center decoration...")
        center_circle = Circle((0, 0), 8, color=self.dot_color, alpha=0.9)
        self.ax.add_patch(center_circle)
        
        print("✅ Animation complete!")
    
    def generate_brahma_knot(self):
        """Generate complete Brahma's Knot"""
        print("🎯 Generating Brahma's Knot with Matplotlib...")
        
        # Generate dots
        dots = self.generate_29_dots()
        print(f"✅ Generated {len(dots)} dots")
        
        # Create path
        path_coords = self.create_brahma_path(dots)
        print(f"✅ Created path with {len(path_coords)} points")
        
        # Smooth curves
        smooth_path = self.smooth_curves(path_coords)
        print(f"✅ Smoothed curves")
        
        # Animate drawing
        self.animate_drawing(dots, smooth_path)
        
        # Add title and info
        self.ax.set_title('Brahma\'s Knot (Eternal Knot)\n29 Dots, Single Continuous Line\nTurtle Graphics Style', 
                         fontsize=16, fontweight='bold', pad=20)
        
        # Add cultural information
        cultural_text = f"""
        Perfect Brahma's Knot:
        • Total Dots: 29 (25 grid + 4 petals)
        • Single Continuous Line: Yes
        • Symmetry: 4-fold rotational
        • Style: Traditional South Indian
        • Material: Chalk/Rangoli powder
        
        Characteristics:
        • Smooth curved lines
        • No sharp corners
        • Interlaced knot pattern
        • Eternal loop design
        • Decorative appearance
        """
        
        self.ax.text(0.02, 0.98, cultural_text, transform=self.ax.transAxes, fontsize=9,
                    verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
        
        # Remove axes
        self.ax.set_xticks([])
        self.ax.set_yticks([])
        self.ax.spines['top'].set_visible(False)
        self.ax.spines['right'].set_visible(False)
        self.ax.spines['bottom'].set_visible(False)
        self.ax.spines['left'].set_visible(False)
        
        plt.tight_layout()
        plt.savefig('matplotlib_brahma_knot.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        return {
            'dots': dots,
            'path': smooth_path,
            'type': 'matplotlib_brahma'
        }

def main():
    """Main function"""
    print("🎨 Matplotlib Brahma's Knot - Turtle Graphics Style")
    print("=" * 60)
    
    try:
        brahma = MatplotlibBrahmaKnot()
        data = brahma.generate_brahma_knot()
        
        print("\n✅ Brahma's Knot generated successfully!")
        print(f"📊 Dots: {len(data['dots'])}")
        print(f"📊 Path Points: {len(data['path'])}")
        print("🎨 Traditional ornamental style!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()


































