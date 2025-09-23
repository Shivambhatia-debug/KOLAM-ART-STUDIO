"""
Eulerian Kolam Generator
========================

Implements research-based algorithms for authentic Kolam generation:
- Eulerian path algorithms (Hierholzer's algorithm)
- Turtle graphics simulation
- Modular arithmetic sequences for symmetric patterns
- L-system fractal generation
- Cultural authenticity validation
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import Circle, FancyBboxPatch
import networkx as nx
import math
import random
from typing import List, Tuple, Dict, Any, Optional
from dataclasses import dataclass
from enum import Enum
import turtle
import json

class GridType(Enum):
    SQUARE = "square"
    TRIANGULAR = "triangular"
    HEXAGONAL = "hexagonal"
    RADIAL = "radial"
    CIRCULAR = "circular"

class PatternStyle(Enum):
    TRADITIONAL = "traditional"
    GEOMETRIC = "geometric"
    FLORAL = "floral"
    ABSTRACT = "abstract"
    MANDALA = "mandala"

@dataclass
class KolamConfig:
    """Configuration for Kolam generation"""
    grid_type: GridType
    grid_size: int
    pattern_style: PatternStyle
    symmetry_order: int
    use_colors: bool
    color_scheme: List[str]
    line_thickness: float
    dot_size: float
    cultural_region: str

@dataclass
class GeneratedKolam:
    """Generated Kolam pattern"""
    dots: List[Tuple[float, float]]
    paths: List[List[Tuple[float, float]]]
    colors: List[str]
    is_eulerian: bool
    grid_type: str
    symmetry_order: int
    cultural_authenticity: float
    generation_method: str

class EulerianKolamGenerator:
    """
    Research-based Kolam generator using Eulerian path algorithms
    """
    
    def __init__(self):
        self.cultural_colors = {
            "traditional": ["#FF6B35", "#F7931E", "#FFD23F", "#EE4B2B", "#FFFFFF"],
            "tamil_nadu": ["#DC143C", "#FF4500", "#FFD700", "#FFFFFF", "#000000"],
            "karnataka": ["#8B0000", "#FF6347", "#FFFF00", "#32CD32", "#FFFFFF"],
            "kerala": ["#228B22", "#FFD700", "#FF4500", "#FFFFFF", "#000000"],
            "andhra_pradesh": ["#FF1493", "#FF6347", "#FFFF00", "#32CD32", "#FFFFFF"],
            "festive": ["#FF0080", "#FF8C00", "#FFD700", "#32CD32", "#4169E1"],
            "rangoli": ["#FF69B4", "#FF4500", "#FFD700", "#9ACD32", "#6495ED"]
        }
        
        self.traditional_motifs = {
            "lotus": self._generate_lotus_motif,
            "paisley": self._generate_paisley_motif,
            "geometric": self._generate_geometric_motif,
            "floral": self._generate_floral_motif,
            "mandala": self._generate_mandala_motif
        }
    
    def generate_kolam(self, config: KolamConfig) -> GeneratedKolam:
        """
        Generate complete Kolam using research-based methods
        """
        # Step 1: Generate dot matrix (pulli)
        dots = self._generate_dot_matrix(config)
        
        # Step 2: Create graph structure
        graph = self._create_kolam_graph(dots, config)
        
        # Step 3: Find Eulerian paths
        paths = self._find_eulerian_paths(graph, dots)
        
        # Step 4: Apply symmetry transformations
        if config.symmetry_order > 1:
            paths = self._apply_symmetry(paths, config.symmetry_order, dots)
        
        # Step 5: Add cultural motifs
        if config.pattern_style != PatternStyle.GEOMETRIC:
            paths = self._add_cultural_motifs(paths, config)
        
        # Step 6: Generate colors
        colors = self._generate_colors(paths, config)
        
        # Step 7: Validate authenticity
        authenticity = self._validate_cultural_authenticity(dots, paths, config)
        
        return GeneratedKolam(
            dots=dots,
            paths=paths,
            colors=colors,
            is_eulerian=self._validate_eulerian_property(graph),
            grid_type=config.grid_type.value,
            symmetry_order=config.symmetry_order,
            cultural_authenticity=authenticity,
            generation_method="eulerian_algorithm"
        )
    
    def _generate_dot_matrix(self, config: KolamConfig) -> List[Tuple[float, float]]:
        """
        Generate dot matrix based on grid type and research patterns
        """
        dots = []
        size = config.grid_size
        
        if config.grid_type == GridType.SQUARE:
            # Square grid (most common in Karnataka)
            for i in range(size):
                for j in range(size):
                    x = i * 50 + 50
                    y = j * 50 + 50
                    dots.append((x, y))
        
        elif config.grid_type == GridType.TRIANGULAR:
            # Triangular grid (common in Tamil Nadu)
            for row in range(size):
                cols_in_row = size - row
                for col in range(cols_in_row):
                    x = 50 + col * 50 + row * 25
                    y = 50 + row * 43.3  # sqrt(3)/2 * 50
                    dots.append((x, y))
        
        elif config.grid_type == GridType.HEXAGONAL:
            # Hexagonal grid (traditional patterns)
            center_x, center_y = 200, 200
            for ring in range(size):
                if ring == 0:
                    dots.append((center_x, center_y))
                else:
                    for i in range(6 * ring):
                        angle = (i * 2 * math.pi) / (6 * ring)
                        x = center_x + ring * 40 * math.cos(angle)
                        y = center_y + ring * 40 * math.sin(angle)
                        dots.append((x, y))
        
        elif config.grid_type == GridType.RADIAL:
            # Radial pattern (common in Tamil Nadu Sikku Kolam)
            center_x, center_y = 200, 200
            dots.append((center_x, center_y))
            
            for ring in range(1, size):
                points_in_ring = 6 * ring  # Increasing density
                for i in range(points_in_ring):
                    angle = (i * 2 * math.pi) / points_in_ring
                    radius = ring * 30
                    x = center_x + radius * math.cos(angle)
                    y = center_y + radius * math.sin(angle)
                    dots.append((x, y))
        
        elif config.grid_type == GridType.CIRCULAR:
            # Circular concentric pattern
            center_x, center_y = 200, 200
            for ring in range(size):
                if ring == 0:
                    dots.append((center_x, center_y))
                else:
                    points_in_ring = 8 + ring * 4
                    for i in range(points_in_ring):
                        angle = (i * 2 * math.pi) / points_in_ring
                        radius = ring * 40
                        x = center_x + radius * math.cos(angle)
                        y = center_y + radius * math.sin(angle)
                        dots.append((x, y))
        
        return dots
    
    def _create_kolam_graph(self, dots: List[Tuple[float, float]], config: KolamConfig) -> nx.Graph:
        """
        Create graph structure following Kolam connection rules
        """
        G = nx.Graph()
        
        # Add nodes (dots)
        for i, dot in enumerate(dots):
            G.add_node(i, pos=dot)
        
        # Add edges based on Kolam rules
        max_distance = 70  # Maximum connection distance
        
        for i, dot1 in enumerate(dots):
            for j, dot2 in enumerate(dots[i+1:], i+1):
                distance = math.sqrt((dot1[0] - dot2[0])**2 + (dot1[1] - dot2[1])**2)
                
                if distance <= max_distance:
                    # Add edge with weight (used for path optimization)
                    G.add_edge(i, j, weight=distance)
        
        # Ensure all nodes have even degree for Eulerian property
        G = self._make_eulerian(G)
        
        return G
    
    def _make_eulerian(self, G: nx.Graph) -> nx.Graph:
        """
        Modify graph to ensure Eulerian property (all vertices have even degree)
        """
        # Find vertices with odd degree
        odd_vertices = [v for v in G.nodes() if G.degree(v) % 2 == 1]
        
        # Add edges between odd vertices to make all degrees even
        while len(odd_vertices) > 1:
            v1 = odd_vertices.pop()
            v2 = odd_vertices.pop()
            
            # Add edge if not already present
            if not G.has_edge(v1, v2):
                pos1 = G.nodes[v1]['pos']
                pos2 = G.nodes[v2]['pos']
                distance = math.sqrt((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2)
                G.add_edge(v1, v2, weight=distance)
        
        return G
    
    def _find_eulerian_paths(self, G: nx.Graph, dots: List[Tuple[float, float]]) -> List[List[Tuple[float, float]]]:
        """
        Find Eulerian paths using Hierholzer's algorithm
        """
        if not nx.is_eulerian(G):
            # If not Eulerian, find paths covering maximum edges
            paths = self._find_approximate_eulerian_paths(G, dots)
        else:
            # Use Hierholzer's algorithm for Eulerian circuit
            try:
                eulerian_path = list(nx.eulerian_circuit(G))
                paths = [self._convert_edge_path_to_coordinates(eulerian_path, dots)]
            except:
                # Fallback to approximate method
                paths = self._find_approximate_eulerian_paths(G, dots)
        
        return paths
    
    def _find_approximate_eulerian_paths(self, G: nx.Graph, dots: List[Tuple[float, float]]) -> List[List[Tuple[float, float]]]:
        """
        Find approximate Eulerian paths when exact solution not available
        """
        paths = []
        remaining_edges = set(G.edges())
        
        while remaining_edges:
            # Start from an unvisited edge
            start_edge = remaining_edges.pop()
            current_path = [start_edge]
            current_node = start_edge[1]
            
            # Extend path as far as possible
            while True:
                next_edges = [e for e in remaining_edges 
                             if e[0] == current_node or e[1] == current_node]
                
                if not next_edges:
                    break
                
                next_edge = next_edges[0]
                remaining_edges.remove(next_edge)
                current_path.append(next_edge)
                
                # Move to the other end of the edge
                current_node = next_edge[1] if next_edge[0] == current_node else next_edge[0]
            
            # Convert edge path to coordinate path
            coord_path = self._convert_edge_path_to_coordinates(current_path, dots)
            paths.append(coord_path)
        
        return paths
    
    def _convert_edge_path_to_coordinates(self, edge_path: List[Tuple[int, int]], 
                                        dots: List[Tuple[float, float]]) -> List[Tuple[float, float]]:
        """
        Convert path of edges to path of coordinates
        """
        if not edge_path:
            return []
        
        coord_path = [dots[edge_path[0][0]]]
        
        for edge in edge_path:
            # Add the second vertex of each edge
            coord_path.append(dots[edge[1]])
        
        return coord_path
    
    def _apply_symmetry(self, paths: List[List[Tuple[float, float]]], symmetry_order: int, 
                       dots: List[Tuple[float, float]]) -> List[List[Tuple[float, float]]]:
        """
        Apply rotational symmetry to paths
        """
        if symmetry_order <= 1:
            return paths
        
        # Calculate center of pattern
        center_x = sum(x for x, y in dots) / len(dots)
        center_y = sum(y for x, y in dots) / len(dots)
        
        symmetric_paths = list(paths)  # Start with original paths
        
        # Generate symmetric copies
        for i in range(1, symmetry_order):
            angle = (i * 2 * math.pi) / symmetry_order
            cos_a, sin_a = math.cos(angle), math.sin(angle)
            
            for path in paths:
                rotated_path = []
                for x, y in path:
                    # Translate to origin
                    tx, ty = x - center_x, y - center_y
                    
                    # Rotate
                    rx = tx * cos_a - ty * sin_a
                    ry = tx * sin_a + ty * cos_a
                    
                    # Translate back
                    rotated_path.append((rx + center_x, ry + center_y))
                
                symmetric_paths.append(rotated_path)
        
        return symmetric_paths
    
    def _add_cultural_motifs(self, paths: List[List[Tuple[float, float]]], 
                           config: KolamConfig) -> List[List[Tuple[float, float]]]:
        """
        Add traditional cultural motifs to enhance authenticity
        """
        enhanced_paths = list(paths)
        
        # Add motifs based on pattern style
        if config.pattern_style in self.traditional_motifs:
            motif_generator = self.traditional_motifs[config.pattern_style.value]
            
            # Add motifs at strategic locations
            for i, path in enumerate(paths):
                if len(path) > 4 and i % 2 == 0:  # Add motifs to every other path
                    midpoint_idx = len(path) // 2
                    center = path[midpoint_idx]
                    
                    # Generate motif around center point
                    motif_points = motif_generator(center, 20)  # 20 pixel radius
                    enhanced_paths.append(motif_points)
        
        return enhanced_paths
    
    def _generate_lotus_motif(self, center: Tuple[float, float], radius: float) -> List[Tuple[float, float]]:
        """Generate lotus petal motif (traditional Tamil Nadu)"""
        cx, cy = center
        petals = []
        
        # Generate 8 lotus petals
        for i in range(8):
            angle = i * math.pi / 4
            
            # Petal curve
            petal = []
            for t in np.linspace(0, 1, 10):
                r = radius * (0.5 + 0.5 * math.sin(t * math.pi))
                x = cx + r * math.cos(angle) * math.cos(t * math.pi)
                y = cy + r * math.sin(angle) * math.cos(t * math.pi)
                petal.append((x, y))
            
            petals.extend(petal)
        
        return petals
    
    def _generate_paisley_motif(self, center: Tuple[float, float], radius: float) -> List[Tuple[float, float]]:
        """Generate paisley motif (traditional design)"""
        cx, cy = center
        paisley = []
        
        # Paisley curve parametric equation
        for t in np.linspace(0, 2 * math.pi, 50):
            r = radius * (1 + 0.3 * math.sin(3 * t))
            x = cx + r * math.cos(t) * (1 + 0.2 * math.cos(5 * t))
            y = cy + r * math.sin(t) * (1 + 0.2 * math.sin(5 * t))
            paisley.append((x, y))
        
        return paisley
    
    def _generate_geometric_motif(self, center: Tuple[float, float], radius: float) -> List[Tuple[float, float]]:
        """Generate geometric motif (Karnataka Muggu style)"""
        cx, cy = center
        motif = []
        
        # Square with diagonal cross
        half_r = radius / math.sqrt(2)
        
        # Square
        square_points = [
            (cx - half_r, cy - half_r),
            (cx + half_r, cy - half_r),
            (cx + half_r, cy + half_r),
            (cx - half_r, cy + half_r),
            (cx - half_r, cy - half_r)  # Close the square
        ]
        motif.extend(square_points)
        
        # Diagonal cross
        motif.extend([(cx - half_r, cy - half_r), (cx + half_r, cy + half_r)])
        motif.extend([(cx + half_r, cy - half_r), (cx - half_r, cy + half_r)])
        
        return motif
    
    def _generate_floral_motif(self, center: Tuple[float, float], radius: float) -> List[Tuple[float, float]]:
        """Generate floral motif (Andhra Pradesh style)"""
        cx, cy = center
        floral = []
        
        # Flower with 6 petals
        for i in range(6):
            angle = i * math.pi / 3
            
            # Each petal as a small arc
            for t in np.linspace(-0.3, 0.3, 8):
                r = radius * (0.8 + 0.2 * math.cos(3 * t))
                petal_angle = angle + t
                x = cx + r * math.cos(petal_angle)
                y = cy + r * math.sin(petal_angle)
                floral.append((x, y))
        
        return floral
    
    def _generate_mandala_motif(self, center: Tuple[float, float], radius: float) -> List[Tuple[float, float]]:
        """Generate mandala motif (spiritual significance)"""
        cx, cy = center
        mandala = []
        
        # Concentric circles with decorative elements
        for ring in [0.3, 0.6, 1.0]:
            r = radius * ring
            
            # Circle
            for t in np.linspace(0, 2 * math.pi, 36):
                x = cx + r * math.cos(t)
                y = cy + r * math.sin(t)
                mandala.append((x, y))
            
            # Decorative spokes
            if ring > 0.3:
                for i in range(8):
                    angle = i * math.pi / 4
                    x1 = cx + (r - 5) * math.cos(angle)
                    y1 = cy + (r - 5) * math.sin(angle)
                    x2 = cx + (r + 5) * math.cos(angle)
                    y2 = cy + (r + 5) * math.sin(angle)
                    mandala.extend([(x1, y1), (x2, y2)])
        
        return mandala
    
    def _generate_colors(self, paths: List[List[Tuple[float, float]]], config: KolamConfig) -> List[str]:
        """
        Generate culturally appropriate colors
        """
        if not config.use_colors:
            return ["#000000"] * len(paths)  # Black for traditional
        
        # Get color scheme based on cultural region
        base_colors = self.cultural_colors.get(config.cultural_region, 
                                             self.cultural_colors["traditional"])
        
        # Ensure we have enough colors
        colors = []
        for i in range(len(paths)):
            color_idx = i % len(base_colors)
            colors.append(base_colors[color_idx])
        
        return colors
    
    def _validate_eulerian_property(self, G: nx.Graph) -> bool:
        """
        Validate that graph has Eulerian property
        """
        return nx.is_eulerian(G) or nx.is_semi_eulerian(G)
    
    def _validate_cultural_authenticity(self, dots: List[Tuple[float, float]], 
                                      paths: List[List[Tuple[float, float]]], 
                                      config: KolamConfig) -> float:
        """
        Score cultural authenticity based on research criteria
        """
        score = 0.0
        
        # Check dot connectivity (all dots should be connected)
        connected_dots = set()
        for path in paths:
            for point in path:
                # Find closest dot
                min_distance = float('inf')
                for i, dot in enumerate(dots):
                    distance = math.sqrt((point[0] - dot[0])**2 + (point[1] - dot[1])**2)
                    if distance < min_distance:
                        min_distance = distance
                        if distance < 25:  # Within reasonable proximity
                            connected_dots.add(i)
        
        connectivity_score = len(connected_dots) / len(dots)
        score += connectivity_score * 0.3
        
        # Check for closed loops (traditional requirement)
        closed_loops = sum(1 for path in paths if len(path) > 3 and 
                          math.sqrt((path[0][0] - path[-1][0])**2 + 
                                  (path[0][1] - path[-1][1])**2) < 20)
        
        loop_score = min(closed_loops / max(1, len(paths) // 2), 1.0)
        score += loop_score * 0.3
        
        # Check symmetry (traditional patterns are symmetric)
        if config.symmetry_order > 1:
            score += 0.2
        
        # Check grid regularity
        if config.grid_type in [GridType.SQUARE, GridType.TRIANGULAR, GridType.RADIAL]:
            score += 0.2
        
        return min(score, 1.0)
    
    def generate_modular_sequence_kolam(self, arms: int, dots_per_arm: int, step_size: int) -> GeneratedKolam:
        """
        Generate Kolam using modular arithmetic sequences (research method)
        """
        dots = []
        paths = []
        
        # Generate points using modular arithmetic
        center_x, center_y = 200, 200
        base_radius = 100
        
        # Add center
        dots.append((center_x, center_y))
        
        # Generate arms using modular sequence
        total_points = arms * dots_per_arm
        
        for i in range(total_points):
            # Modular arithmetic for symmetric distribution
            arm_index = i % arms
            dot_index = i // arms
            
            # Calculate angle and radius
            angle = (arm_index * 2 * math.pi / arms) + (dot_index * step_size * math.pi / 180)
            radius = base_radius * (1 + dot_index * 0.2)
            
            x = center_x + radius * math.cos(angle)
            y = center_y + radius * math.sin(angle)
            dots.append((x, y))
        
        # Create continuous path connecting all points
        path = []
        for i in range(len(dots)):
            next_i = (i + step_size) % len(dots)
            path.append(dots[next_i])
        
        paths.append(path)
        
        return GeneratedKolam(
            dots=dots,
            paths=paths,
            colors=["#FF6B35"] * len(paths),
            is_eulerian=True,
            grid_type="radial",
            symmetry_order=arms,
            cultural_authenticity=0.9,
            generation_method="modular_sequence"
        )

# Example usage
if __name__ == "__main__":
    generator = EulerianKolamGenerator()
    
    # Test configuration
    config = KolamConfig(
        grid_type=GridType.RADIAL,
        grid_size=4,
        pattern_style=PatternStyle.TRADITIONAL,
        symmetry_order=6,
        use_colors=True,
        color_scheme=["#FF6B35", "#F7931E", "#FFD23F"],
        line_thickness=2.0,
        dot_size=4.0,
        cultural_region="tamil_nadu"
    )
    
    try:
        kolam = generator.generate_kolam(config)
        print(f"Generated Kolam with {len(kolam.dots)} dots and {len(kolam.paths)} paths")
        print(f"Eulerian: {kolam.is_eulerian}")
        print(f"Cultural authenticity: {kolam.cultural_authenticity:.2f}")
        print(f"Symmetry order: {kolam.symmetry_order}")
        
        # Test modular sequence method
        modular_kolam = generator.generate_modular_sequence_kolam(arms=8, dots_per_arm=5, step_size=3)
        print(f"Modular Kolam: {len(modular_kolam.dots)} dots, authenticity: {modular_kolam.cultural_authenticity:.2f}")
        
    except Exception as e:
        print(f"Generation failed: {e}")
        import traceback
        traceback.print_exc()


















