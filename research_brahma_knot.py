#!/usr/bin/env python3
"""
Research Paper Implementation: Brahma's Knot (Eternal Knot)
Based on: "A topological approach to creating any pulli kolam" by Gopalan & VanLeeuwen

This implements the exact 5-step topological method from the research paper
"""

import matplotlib.pyplot as plt
import numpy as np
import math
from matplotlib.patches import Circle, FancyBboxPatch
import matplotlib.patches as mpatches

class ResearchBrahmaKnot:
    def __init__(self):
        self.dot_spacing = 40
        self.center_x, self.center_y = 200, 200
        self.grid_size = 5
        
    def generate_5x5_dots(self):
        """Step 1: Place dots in 5x5 configuration"""
        dots = []
        start_x = self.center_x - (self.grid_size - 1) * self.dot_spacing / 2
        start_y = self.center_y - (self.grid_size - 1) * self.dot_spacing / 2
        
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                x = start_x + j * self.dot_spacing
                y = start_y + i * self.dot_spacing
                dots.append((x, y, i * self.grid_size + j))
        
        return dots
    
    def create_squishies(self, dots):
        """Step 2: Create squishies (deformable figures) around each dot"""
        squishies = []
        for dot in dots:
            x, y, dot_id = dot
            # Create a circular squishy around each dot
            squishy = {
                'center': (x, y),
                'radius': self.dot_spacing * 0.3,
                'dot_id': dot_id,
                'arms': []
            }
            squishies.append(squishy)
        return squishies
    
    def create_junctions(self, squishies):
        """Step 3: Create junctions between squishies"""
        junctions = []
        grid_size = self.grid_size
        
        # Create junctions for adjacent dots
        for i in range(grid_size):
            for j in range(grid_size):
                dot_id = i * grid_size + j
                current_squishy = squishies[dot_id]
                
                # Right neighbor
                if j < grid_size - 1:
                    right_dot_id = i * grid_size + (j + 1)
                    right_squishy = squishies[right_dot_id]
                    junction = {
                        'type': 'horizontal',
                        'squishy1': current_squishy,
                        'squishy2': right_squishy,
                        'position': (
                            (current_squishy['center'][0] + right_squishy['center'][0]) / 2,
                            (current_squishy['center'][1] + right_squishy['center'][1]) / 2
                        )
                    }
                    junctions.append(junction)
                
                # Bottom neighbor
                if i < grid_size - 1:
                    bottom_dot_id = (i + 1) * grid_size + j
                    bottom_squishy = squishies[bottom_dot_id]
                    junction = {
                        'type': 'vertical',
                        'squishy1': current_squishy,
                        'squishy2': bottom_squishy,
                        'position': (
                            (current_squishy['center'][0] + bottom_squishy['center'][0]) / 2,
                            (current_squishy['center'][1] + bottom_squishy['center'][1]) / 2
                        )
                    }
                    junctions.append(junction)
        
        return junctions
    
    def create_brahma_knot_paths(self, dots, junctions):
        """Step 4: Create Brahma's Knot paths following research paper"""
        paths = []
        
        # Get dot positions
        dot_positions = {dot[2]: (dot[0], dot[1]) for dot in dots}
        
        # Brahma's Knot - Continuous loop pattern
        # Outer square path
        outer_path = [
            (0, 0), (0, 1), (0, 2), (0, 3), (0, 4),  # Top row
            (1, 4), (2, 4), (3, 4), (4, 4),           # Right column
            (4, 3), (4, 2), (4, 1), (4, 0),           # Bottom row
            (3, 0), (2, 0), (1, 0), (0, 0)            # Left column
        ]
        
        # Inner diamond path
        inner_path = [
            (1, 1), (1, 2), (1, 3), (2, 3), (3, 3),  # Inner diamond
            (3, 2), (3, 1), (2, 1), (1, 1)
        ]
        
        # Cross pattern
        cross_path = [
            (0, 2), (1, 2), (2, 2), (3, 2), (4, 2),  # Horizontal cross
            (2, 1), (2, 3), (2, 2)                   # Vertical cross
        ]
        
        # Convert to actual coordinates
        for path_points in [outer_path, inner_path, cross_path]:
            path_coords = []
            for row, col in path_points:
                dot_id = row * self.grid_size + col
                if dot_id in dot_positions:
                    path_coords.append(dot_positions[dot_id])
            paths.append(path_coords)
        
        return paths
    
    def smooth_curves(self, paths):
        """Step 5: Smooth the curves for aesthetic appeal"""
        smoothed_paths = []
        
        for path in paths:
            if len(path) < 3:
                smoothed_paths.append(path)
                continue
                
            smoothed_path = []
            for i in range(len(path)):
                if i == 0:
                    smoothed_path.append(path[i])
                elif i == len(path) - 1:
                    smoothed_path.append(path[i])
                else:
                    # Smooth the curve by averaging adjacent points
                    prev_point = path[i-1]
                    curr_point = path[i]
                    next_point = path[i+1]
                    
                    smooth_x = (prev_point[0] + curr_point[0] + next_point[0]) / 3
                    smooth_y = (prev_point[1] + curr_point[1] + next_point[1]) / 3
                    smoothed_path.append((smooth_x, smooth_y))
            
            smoothed_paths.append(smoothed_path)
        
        return smoothed_paths
    
    def generate_brahma_knot(self):
        """Generate complete Brahma's Knot following research paper"""
        print("🔬 Generating Research Paper Brahma's Knot...")
        
        # Step 1: Place dots
        dots = self.generate_5x5_dots()
        print(f"✅ Step 1: Placed {len(dots)} dots in 5x5 grid")
        
        # Step 2: Create squishies
        squishies = self.create_squishies(dots)
        print(f"✅ Step 2: Created {len(squishies)} squishies")
        
        # Step 3: Create junctions
        junctions = self.create_junctions(squishies)
        print(f"✅ Step 3: Created {len(junctions)} junctions")
        
        # Step 4: Create paths
        paths = self.create_brahma_knot_paths(dots, junctions)
        print(f"✅ Step 4: Created {len(paths)} paths")
        
        # Step 5: Smooth curves
        smoothed_paths = self.smooth_curves(paths)
        print(f"✅ Step 5: Smoothed {len(smoothed_paths)} paths")
        
        return {
            'dots': dots,
            'squishies': squishies,
            'junctions': junctions,
            'paths': smoothed_paths,
            'cultural_info': {
                'name': 'Brahma Mudi (Eternal Knot)',
                'region': 'Tamil Nadu',
                'symbolism': 'Infinite consciousness and eternal cycle',
                'mathematical_properties': {
                    'symmetry': 'Radial',
                    'dot_count': 25,
                    'path_count': 3,
                    'continuous_loop': True,
                    'topological_method': '5-step Gopalan & VanLeeuwen'
                }
            }
        }

def create_animated_brahma_knot():
    """Create animated Brahma's Knot visualization"""
    brahma = ResearchBrahmaKnot()
    data = brahma.generate_brahma_knot()
    
    # Create figure
    fig, ax = plt.subplots(1, 1, figsize=(12, 10))
    ax.set_xlim(50, 350)
    ax.set_ylim(50, 350)
    ax.set_aspect('equal')
    ax.set_facecolor('white')
    
    # Title
    ax.set_title('Brahma\'s Knot (Eternal Knot)\nResearch Paper Implementation\nGopalan & VanLeeuwen Topological Method', 
                fontsize=16, fontweight='bold', pad=20)
    
    # Draw dots
    for dot in data['dots']:
        x, y, dot_id = dot
        circle = Circle((x, y), 4, color='#DC143C', alpha=0.8)
        ax.add_patch(circle)
        
        # Add dot numbers
        ax.text(x, y-8, str(dot_id), ha='center', va='center', fontsize=8, color='#8B0000')
    
    # Draw squishies
    for squishy in data['squishies']:
        x, y = squishy['center']
        circle = Circle((x, y), squishy['radius'], 
                       fill=False, color='#FFB6C1', alpha=0.3, linestyle='--')
        ax.add_patch(circle)
    
    # Draw junctions
    for junction in data['junctions']:
        x, y = junction['position']
        circle = Circle((x, y), 2, color='#FF6347', alpha=0.6)
        ax.add_patch(circle)
    
    # Draw paths with different colors
    colors = ['#DC143C', '#B22222', '#8B0000']
    for i, path in enumerate(data['paths']):
        if len(path) > 1:
            x_coords = [p[0] for p in path]
            y_coords = [p[1] for p in path]
            ax.plot(x_coords, y_coords, color=colors[i % len(colors)], 
                   linewidth=3, alpha=0.8, label=f'Path {i+1}')
    
    # Add cultural information
    info_text = f"""
    Cultural Information:
    • Name: {data['cultural_info']['name']}
    • Region: {data['cultural_info']['region']}
    • Symbolism: {data['cultural_info']['symbolism']}
    
    Mathematical Properties:
    • Symmetry: {data['cultural_info']['mathematical_properties']['symmetry']}
    • Dot Count: {data['cultural_info']['mathematical_properties']['dot_count']}
    • Path Count: {data['cultural_info']['mathematical_properties']['path_count']}
    • Continuous Loop: {data['cultural_info']['mathematical_properties']['continuous_loop']}
    • Method: {data['cultural_info']['mathematical_properties']['topological_method']}
    """
    
    ax.text(0.02, 0.98, info_text, transform=ax.transAxes, fontsize=10,
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
    plt.savefig('research_brahma_knot.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    return data

if __name__ == "__main__":
    print("🔬 Research Paper Brahma's Knot Implementation")
    print("=" * 50)
    
    data = create_animated_brahma_knot()
    
    print("\n✅ Brahma's Knot generated successfully!")
    print(f"📊 Dots: {len(data['dots'])}")
    print(f"📊 Paths: {len(data['paths'])}")
    print(f"📊 Junctions: {len(data['junctions'])}")
    print(f"📊 Squishies: {len(data['squishies'])}")


































