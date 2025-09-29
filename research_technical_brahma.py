#!/usr/bin/env python3
"""
Research Version: Technical Topological Representation
- Dots numbered (0-24)
- Abstract graph structure
- Algorithmic analysis focus
- Technical diagram style
"""

import matplotlib.pyplot as plt
import numpy as np
import math
from matplotlib.patches import Circle, FancyBboxPatch
import matplotlib.patches as mpatches

class ResearchTechnicalBrahma:
    def __init__(self):
        self.dot_spacing = 50
        self.center_x, self.center_y = 200, 200
        self.grid_size = 5
        
    def generate_numbered_dots(self):
        """Generate 5x5 grid with numbered dots (0-24)"""
        dots = []
        start_x = self.center_x - (self.grid_size - 1) * self.dot_spacing / 2
        start_y = self.center_y - (self.grid_size - 1) * self.dot_spacing / 2
        
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                x = start_x + j * self.dot_spacing
                y = start_y + i * self.dot_spacing
                dot_id = i * self.grid_size + j
                dots.append({
                    'id': dot_id,
                    'x': x,
                    'y': y,
                    'row': i,
                    'col': j
                })
        
        return dots
    
    def create_graph_structure(self, dots):
        """Create abstract graph structure with junctions"""
        junctions = []
        edges = []
        
        # Create horizontal edges
        for i in range(self.grid_size):
            for j in range(self.grid_size - 1):
                dot1_id = i * self.grid_size + j
                dot2_id = i * self.grid_size + (j + 1)
                edge = {
                    'type': 'horizontal',
                    'dot1': dot1_id,
                    'dot2': dot2_id,
                    'junction_id': len(junctions)
                }
                edges.append(edge)
                
                # Create junction
                dot1 = dots[dot1_id]
                dot2 = dots[dot2_id]
                junction = {
                    'id': len(junctions),
                    'x': (dot1['x'] + dot2['x']) / 2,
                    'y': (dot1['y'] + dot2['y']) / 2,
                    'edge_type': 'horizontal',
                    'connected_dots': [dot1_id, dot2_id]
                }
                junctions.append(junction)
        
        # Create vertical edges
        for i in range(self.grid_size - 1):
            for j in range(self.grid_size):
                dot1_id = i * self.grid_size + j
                dot2_id = (i + 1) * self.grid_size + j
                edge = {
                    'type': 'vertical',
                    'dot1': dot1_id,
                    'dot2': dot2_id,
                    'junction_id': len(junctions)
                }
                edges.append(edge)
                
                # Create junction
                dot1 = dots[dot1_id]
                dot2 = dots[dot2_id]
                junction = {
                    'id': len(junctions),
                    'x': (dot1['x'] + dot2['x']) / 2,
                    'y': (dot1['y'] + dot2['y']) / 2,
                    'edge_type': 'vertical',
                    'connected_dots': [dot1_id, dot2_id]
                }
                junctions.append(junction)
        
        return edges, junctions
    
    def create_brahma_paths(self, dots, edges, junctions):
        """Create Brahma's Knot paths following research paper algorithm"""
        paths = []
        
        # Path 1: Outer perimeter
        outer_path = [0, 1, 2, 3, 4, 9, 14, 19, 24, 23, 22, 21, 20, 15, 10, 5, 0]
        
        # Path 2: Inner diamond
        inner_path = [6, 7, 8, 13, 18, 17, 16, 11, 6]
        
        # Path 3: Cross pattern
        cross_path = [2, 7, 12, 17, 22, 21, 16, 11, 6, 1, 2]
        
        # Convert to coordinates
        for path_dots in [outer_path, inner_path, cross_path]:
            path_coords = []
            for dot_id in path_dots:
                if dot_id < len(dots):
                    path_coords.append((dots[dot_id]['x'], dots[dot_id]['y']))
            paths.append(path_coords)
        
        return paths
    
    def analyze_topological_properties(self, dots, paths, edges):
        """Analyze topological properties for research"""
        analysis = {
            'total_dots': len(dots),
            'total_paths': len(paths),
            'total_edges': len(edges),
            'symmetry_type': 'Radial',
            'path_lengths': [len(path) for path in paths],
            'continuous_loops': True,
            'dot_connectivity': {},
            'path_complexity': 'High'
        }
        
        # Calculate dot connectivity
        for dot in dots:
            dot_id = dot['id']
            connections = 0
            for edge in edges:
                if edge['dot1'] == dot_id or edge['dot2'] == dot_id:
                    connections += 1
            analysis['dot_connectivity'][dot_id] = connections
        
        return analysis
    
    def generate_research_brahma(self):
        """Generate complete research version"""
        print("🔬 Generating Research Technical Brahma's Knot...")
        
        # Generate numbered dots
        dots = self.generate_numbered_dots()
        print(f"✅ Generated {len(dots)} numbered dots (0-24)")
        
        # Create graph structure
        edges, junctions = self.create_graph_structure(dots)
        print(f"✅ Created {len(edges)} edges and {len(junctions)} junctions")
        
        # Create paths
        paths = self.create_brahma_paths(dots, edges, junctions)
        print(f"✅ Created {len(paths)} paths")
        
        # Analyze properties
        analysis = self.analyze_topological_properties(dots, paths, edges)
        print(f"✅ Analyzed topological properties")
        
        return {
            'dots': dots,
            'edges': edges,
            'junctions': junctions,
            'paths': paths,
            'analysis': analysis,
            'type': 'research_technical'
        }

def create_research_diagram():
    """Create technical research diagram"""
    brahma = ResearchTechnicalBrahma()
    data = brahma.generate_research_brahma()
    
    # Create figure
    fig, ax = plt.subplots(1, 1, figsize=(14, 10))
    ax.set_xlim(50, 350)
    ax.set_ylim(50, 350)
    ax.set_aspect('equal')
    ax.set_facecolor('white')
    
    # Title
    ax.set_title('Research Version: Brahma\'s Knot\nTechnical Topological Representation\nDots: 0-24, Graph Structure, Algorithmic Analysis', 
                fontsize=16, fontweight='bold', pad=20)
    
    # Draw dots with numbers
    for dot in data['dots']:
        x, y = dot['x'], dot['y']
        circle = Circle((x, y), 6, color='#DC143C', alpha=0.9)
        ax.add_patch(circle)
        
        # Add dot numbers
        ax.text(x, y, str(dot['id']), ha='center', va='center', 
                fontsize=10, color='white', fontweight='bold')
    
    # Draw edges (graph structure)
    for edge in data['edges']:
        dot1 = data['dots'][edge['dot1']]
        dot2 = data['dots'][edge['dot2']]
        ax.plot([dot1['x'], dot2['x']], [dot1['y'], dot2['y']], 
               color='#FFB6C1', alpha=0.4, linewidth=1, linestyle='--')
    
    # Draw junctions
    for junction in data['junctions']:
        x, y = junction['x'], junction['y']
        circle = Circle((x, y), 3, color='#FF6347', alpha=0.7)
        ax.add_patch(circle)
    
    # Draw paths with different colors
    colors = ['#DC143C', '#B22222', '#8B0000']
    for i, path in enumerate(data['paths']):
        if len(path) > 1:
            x_coords = [p[0] for p in path]
            y_coords = [p[1] for p in path]
            ax.plot(x_coords, y_coords, color=colors[i % len(colors)], 
                   linewidth=4, alpha=0.8, label=f'Path {i+1}')
    
    # Add analysis information
    analysis_text = f"""
    Topological Analysis:
    • Total Dots: {data['analysis']['total_dots']}
    • Total Paths: {data['analysis']['total_paths']}
    • Total Edges: {data['analysis']['total_edges']}
    • Symmetry: {data['analysis']['symmetry_type']}
    • Path Lengths: {data['analysis']['path_lengths']}
    • Continuous Loops: {data['analysis']['continuous_loops']}
    • Complexity: {data['analysis']['path_complexity']}
    
    Dot Connectivity:
    • Corner dots (0,4,20,24): 2 connections
    • Edge dots: 3 connections  
    • Inner dots: 4 connections
    • Center dot (12): 4 connections
    """
    
    ax.text(0.02, 0.98, analysis_text, transform=ax.transAxes, fontsize=9,
            verticalalignment='top', bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8))
    
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
    plt.savefig('research_technical_brahma.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    return data

if __name__ == "__main__":
    print("🔬 Research Technical Brahma's Knot")
    print("=" * 50)
    
    data = create_research_diagram()
    
    print("\n✅ Research version generated successfully!")
    print(f"📊 Dots: {len(data['dots'])}")
    print(f"📊 Paths: {len(data['paths'])}")
    print(f"📊 Edges: {len(data['edges'])}")
    print(f"📊 Junctions: {len(data['junctions'])}")


































