#!/usr/bin/env python3
"""
Traditional Cultural Version: Ornamental Brahmamudi Kolam
- Continuous, interlaced loop
- Curved, smooth lines
- Decorative and ornamental
- Chalk/rangoli style
"""

import matplotlib.pyplot as plt
import numpy as np
import math
from matplotlib.patches import Circle, FancyBboxPatch
import matplotlib.patches as mpatches

class TraditionalCulturalBrahma:
    def __init__(self):
        self.center_x, self.center_y = 200, 200
        self.radius = 80
        
    def generate_cultural_dots(self):
        """Generate dots in traditional kolam style"""
        dots = []
        
        # Outer ring dots
        outer_radius = 80
        for i in range(8):
            angle = i * math.pi / 4
            x = self.center_x + outer_radius * math.cos(angle)
            y = self.center_y + outer_radius * math.sin(angle)
            dots.append({'x': x, 'y': y, 'type': 'outer'})
        
        # Inner ring dots
        inner_radius = 40
        for i in range(8):
            angle = i * math.pi / 4 + math.pi / 8  # Offset by 22.5 degrees
            x = self.center_x + inner_radius * math.cos(angle)
            y = self.center_y + inner_radius * math.sin(angle)
            dots.append({'x': x, 'y': y, 'type': 'inner'})
        
        # Center dot
        dots.append({'x': self.center_x, 'y': self.center_y, 'type': 'center'})
        
        return dots
    
    def create_eternal_knot_path(self, dots):
        """Create continuous eternal knot path"""
        # Create smooth, curved paths for eternal knot
        paths = []
        
        # Outer continuous loop
        outer_path = []
        for i in range(8):
            angle = i * math.pi / 4
            x = self.center_x + 80 * math.cos(angle)
            y = self.center_y + 80 * math.sin(angle)
            outer_path.append((x, y))
        outer_path.append(outer_path[0])  # Close the loop
        paths.append(outer_path)
        
        # Inner continuous loop
        inner_path = []
        for i in range(8):
            angle = i * math.pi / 4 + math.pi / 8
            x = self.center_x + 40 * math.cos(angle)
            y = self.center_y + 40 * math.sin(angle)
            inner_path.append((x, y))
        inner_path.append(inner_path[0])  # Close the loop
        paths.append(inner_path)
        
        # Interlaced strands (eternal knot style)
        strand1 = []
        strand2 = []
        strand3 = []
        
        # Create three interlaced strands
        for i in range(16):
            angle = i * math.pi / 8
            if i % 3 == 0:
                x = self.center_x + 60 * math.cos(angle)
                y = self.center_y + 60 * math.sin(angle)
                strand1.append((x, y))
            elif i % 3 == 1:
                x = self.center_x + 50 * math.cos(angle)
                y = self.center_y + 50 * math.sin(angle)
                strand2.append((x, y))
            else:
                x = self.center_x + 70 * math.cos(angle)
                y = self.center_y + 70 * math.sin(angle)
                strand3.append((x, y))
        
        # Close strands
        strand1.append(strand1[0])
        strand2.append(strand2[0])
        strand3.append(strand3[0])
        
        paths.extend([strand1, strand2, strand3])
        
        return paths
    
    def smooth_curves(self, paths):
        """Smooth curves for ornamental appearance"""
        smoothed_paths = []
        
        for path in paths:
            if len(path) < 3:
                smoothed_paths.append(path)
                continue
            
            # Use spline interpolation for smooth curves
            x_coords = [p[0] for p in path]
            y_coords = [p[1] for p in path]
            
            # Create smooth curve
            t = np.linspace(0, 1, len(path))
            t_smooth = np.linspace(0, 1, len(path) * 4)
            
            # Interpolate
            x_smooth = np.interp(t_smooth, t, x_coords)
            y_smooth = np.interp(t_smooth, t, y_coords)
            
            # Apply smoothing
            from scipy import interpolate
            try:
                tck, u = interpolate.splprep([x_smooth, y_smooth], s=0)
                u_smooth = np.linspace(0, 1, len(path) * 4)
                smooth_coords = interpolate.splev(u_smooth, tck)
                smoothed_path = list(zip(smooth_coords[0], smooth_coords[1]))
            except:
                # Fallback to simple interpolation
                smoothed_path = list(zip(x_smooth, y_smooth))
            
            smoothed_paths.append(smoothed_path)
        
        return smoothed_paths
    
    def add_decorative_elements(self, ax):
        """Add decorative elements for cultural version"""
        # Add decorative circles
        for i in range(3):
            radius = 20 + i * 10
            circle = Circle((self.center_x, self.center_y), radius, 
                          fill=False, color='#FFB6C1', alpha=0.3, linewidth=1)
            ax.add_patch(circle)
        
        # Add corner decorations
        corner_positions = [
            (self.center_x - 100, self.center_y - 100),
            (self.center_x + 100, self.center_y - 100),
            (self.center_x - 100, self.center_y + 100),
            (self.center_x + 100, self.center_y + 100)
        ]
        
        for pos in corner_positions:
            x, y = pos
            # Add small decorative elements
            for i in range(4):
                angle = i * math.pi / 2
                dx = 15 * math.cos(angle)
                dy = 15 * math.sin(angle)
                circle = Circle((x + dx, y + dy), 3, color='#FF69B4', alpha=0.6)
                ax.add_patch(circle)
    
    def generate_cultural_brahma(self):
        """Generate complete cultural version"""
        print("🎨 Generating Traditional Cultural Brahma's Knot...")
        
        # Generate dots
        dots = self.generate_cultural_dots()
        print(f"✅ Generated {len(dots)} cultural dots")
        
        # Create paths
        paths = self.create_eternal_knot_path(dots)
        print(f"✅ Created {len(paths)} paths")
        
        # Smooth curves
        smoothed_paths = self.smooth_curves(paths)
        print(f"✅ Smoothed {len(smoothed_paths)} paths")
        
        return {
            'dots': dots,
            'paths': smoothed_paths,
            'type': 'traditional_cultural'
        }

def create_cultural_diagram():
    """Create traditional cultural diagram"""
    brahma = TraditionalCulturalBrahma()
    data = brahma.generate_cultural_brahma()
    
    # Create figure
    fig, ax = plt.subplots(1, 1, figsize=(12, 10))
    ax.set_xlim(50, 350)
    ax.set_ylim(50, 350)
    ax.set_aspect('equal')
    ax.set_facecolor('white')
    
    # Title
    ax.set_title('Traditional Cultural Version: Brahmamudi Kolam\nContinuous Interlaced Loop\nDecorative & Ornamental Style', 
                fontsize=16, fontweight='bold', pad=20)
    
    # Add decorative elements
    brahma.add_decorative_elements(ax)
    
    # Draw dots
    for dot in data['dots']:
        x, y = dot['x'], dot['y']
        if dot['type'] == 'center':
            circle = Circle((x, y), 8, color='#DC143C', alpha=0.9)
        elif dot['type'] == 'outer':
            circle = Circle((x, y), 5, color='#B22222', alpha=0.8)
        else:
            circle = Circle((x, y), 4, color='#8B0000', alpha=0.7)
        ax.add_patch(circle)
    
    # Draw paths with different colors and styles
    colors = ['#DC143C', '#B22222', '#8B0000', '#FF69B4', '#FF1493']
    styles = ['-', '--', '-.', ':', '-']
    
    for i, path in enumerate(data['paths']):
        if len(path) > 1:
            x_coords = [p[0] for p in path]
            y_coords = [p[1] for p in path]
            ax.plot(x_coords, y_coords, color=colors[i % len(colors)], 
                   linewidth=4, alpha=0.8, linestyle=styles[i % len(styles)],
                   label=f'Strand {i+1}')
    
    # Add cultural information
    cultural_text = f"""
    Cultural Information:
    • Name: Brahmamudi Kolam (Eternal Knot)
    • Style: Traditional South Indian
    • Purpose: Decorative, Religious
    • Material: Chalk/Rangoli powder
    • Symbolism: Eternal cycle, Infinity
    
    Characteristics:
    • Continuous interlaced loop
    • Smooth curved lines
    • Decorative elements
    • Ornamental appearance
    • Cultural significance
    """
    
    ax.text(0.02, 0.98, cultural_text, transform=ax.transAxes, fontsize=10,
            verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
    
    # Add legend
    ax.legend(loc='upper right', bbox_to_anchor=(0.98, 0.98))
    
    # Remove axes
    ax.set_xticks([])
    ax.set_yticks([])
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)
    
    plt.tight_layout()
    plt.savefig('traditional_cultural_brahma.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    return data

if __name__ == "__main__":
    print("🎨 Traditional Cultural Brahma's Knot")
    print("=" * 50)
    
    data = create_cultural_diagram()
    
    print("\n✅ Cultural version generated successfully!")
    print(f"📊 Dots: {len(data['dots'])}")
    print(f"📊 Paths: {len(data['paths'])}")
    print("🎨 Decorative and ornamental style!")













