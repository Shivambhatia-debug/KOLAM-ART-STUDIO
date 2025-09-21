"""
Kolam Design Analyzer and Generator
===================================

This program analyzes Kolam designs to identify their mathematical principles
and generates new Kolam patterns based on those principles.

Key Design Principles:
1. Grid-based dot patterns (Pulli)
2. Symmetry (radial, bilateral, rotational)
3. Geometric shapes (circles, squares, triangles, curves)
4. Fractal patterns and self-similarity
5. Continuous line patterns (Sikku Kolam)
6. Repetition and spatial reasoning

Author: AI Assistant
Organization: AICTE - Indian Knowledge Systems (IKS)
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import Circle, Rectangle, Polygon
import math
import random
from typing import List, Tuple, Dict, Any
from dataclasses import dataclass
from enum import Enum
import json

class SymmetryType(Enum):
    RADIAL = "radial"
    BILATERAL = "bilateral"
    ROTATIONAL = "rotational"
    NONE = "none"

@dataclass
class KolamPoint:
    """Represents a point in the Kolam grid"""
    x: float
    y: float
    is_center: bool = False
    connections: List[int] = None
    
    def __post_init__(self):
        if self.connections is None:
            self.connections = []

@dataclass
class KolamPattern:
    """Represents a complete Kolam pattern"""
    points: List[KolamPoint]
    lines: List[Tuple[int, int]]
    symmetry_type: SymmetryType
    grid_size: Tuple[int, int]
    center_point: Tuple[float, float]
    fractal_level: int = 0

class KolamAnalyzer:
    """Analyzes Kolam patterns to identify design principles"""
    
    def __init__(self):
        self.patterns = []
        self.analysis_results = {}
    
    def analyze_symmetry(self, points: List[KolamPoint]) -> SymmetryType:
        """Analyze the symmetry type of a Kolam pattern"""
        if len(points) < 3:
            return SymmetryType.NONE
        
        # Check for radial symmetry
        if self._has_radial_symmetry(points):
            return SymmetryType.RADIAL
        
        # Check for bilateral symmetry
        if self._has_bilateral_symmetry(points):
            return SymmetryType.BILATERAL
        
        # Check for rotational symmetry
        if self._has_rotational_symmetry(points):
            return SymmetryType.ROTATIONAL
        
        return SymmetryType.NONE
    
    def _has_radial_symmetry(self, points: List[KolamPoint]) -> bool:
        """Check if pattern has radial symmetry"""
        if len(points) < 4:
            return False
        
        # Find center point
        center_x = sum(p.x for p in points) / len(points)
        center_y = sum(p.y for p in points) / len(points)
        
        # Check if points are equidistant from center
        distances = [math.sqrt((p.x - center_x)**2 + (p.y - center_y)**2) for p in points]
        avg_distance = sum(distances) / len(distances)
        
        # Allow 10% tolerance
        tolerance = avg_distance * 0.1
        return all(abs(d - avg_distance) < tolerance for d in distances)
    
    def _has_bilateral_symmetry(self, points: List[KolamPoint]) -> bool:
        """Check if pattern has bilateral symmetry"""
        if len(points) < 2:
            return False
        
        # Find potential axis of symmetry
        center_x = sum(p.x for p in points) / len(points)
        
        # Check if points are symmetric about vertical line
        symmetric_count = 0
        for p in points:
            mirror_x = 2 * center_x - p.x
            for other_p in points:
                if abs(other_p.x - mirror_x) < 0.1 and abs(other_p.y - p.y) < 0.1:
                    symmetric_count += 1
                    break
        
        return symmetric_count >= len(points) * 0.8
    
    def _has_rotational_symmetry(self, points: List[KolamPoint]) -> bool:
        """Check if pattern has rotational symmetry"""
        if len(points) < 3:
            return False
        
        # Check for 2-fold, 3-fold, 4-fold, 6-fold symmetry
        for fold in [2, 3, 4, 6]:
            if self._check_rotational_symmetry(points, fold):
                return True
        
        return False
    
    def _check_rotational_symmetry(self, points: List[KolamPoint], fold: int) -> bool:
        """Check for n-fold rotational symmetry"""
        center_x = sum(p.x for p in points) / len(points)
        center_y = sum(p.y for p in points) / len(points)
        
        angle_step = 2 * math.pi / fold
        matched_points = 0
        
        for p in points:
            for i in range(1, fold):
                angle = i * angle_step
                # Rotate point around center
                cos_a, sin_a = math.cos(angle), math.sin(angle)
                new_x = center_x + (p.x - center_x) * cos_a - (p.y - center_y) * sin_a
                new_y = center_y + (p.x - center_x) * sin_a + (p.y - center_y) * cos_a
                
                # Check if rotated point matches any existing point
                for other_p in points:
                    if abs(other_p.x - new_x) < 0.1 and abs(other_p.y - new_y) < 0.1:
                        matched_points += 1
                        break
        
        return matched_points >= len(points) * 0.8
    
    def analyze_fractal_properties(self, pattern: KolamPattern) -> Dict[str, Any]:
        """Analyze fractal properties of the pattern"""
        # Calculate fractal dimension using box-counting method
        fractal_dimension = self._calculate_fractal_dimension(pattern)
        
        # Check for self-similarity
        self_similarity = self._check_self_similarity(pattern)
        
        return {
            'fractal_dimension': fractal_dimension,
            'self_similarity': self_similarity,
            'complexity_level': self._calculate_complexity(pattern)
        }
    
    def _calculate_fractal_dimension(self, pattern: KolamPattern) -> float:
        """Calculate fractal dimension using box-counting method"""
        # Simplified implementation
        if len(pattern.points) < 4:
            return 1.0
        
        # Count how many grid boxes contain points
        min_x = min(p.x for p in pattern.points)
        max_x = max(p.x for p in pattern.points)
        min_y = min(p.y for p in pattern.points)
        max_y = max(p.y for p in pattern.points)
        
        # Use different box sizes
        box_sizes = [0.1, 0.2, 0.4, 0.8]
        counts = []
        
        for size in box_sizes:
            count = 0
            x_boxes = int((max_x - min_x) / size) + 1
            y_boxes = int((max_y - min_y) / size) + 1
            
            for i in range(x_boxes):
                for j in range(y_boxes):
                    box_min_x = min_x + i * size
                    box_max_x = min_x + (i + 1) * size
                    box_min_y = min_y + j * size
                    box_max_y = min_y + (j + 1) * size
                    
                    # Check if any point is in this box
                    for p in pattern.points:
                        if (box_min_x <= p.x < box_max_x and 
                            box_min_y <= p.y < box_max_y):
                            count += 1
                            break
            
            counts.append(count)
        
        # Calculate fractal dimension from slope
        if len(counts) > 1:
            log_sizes = [math.log(1/s) for s in box_sizes]
            log_counts = [math.log(c) for c in counts if c > 0]
            if len(log_counts) > 1:
                return np.polyfit(log_sizes[:len(log_counts)], log_counts, 1)[0]
        
        return 1.0
    
    def _check_self_similarity(self, pattern: KolamPattern) -> bool:
        """Check if pattern exhibits self-similarity"""
        # Simplified check - look for repeated sub-patterns
        if len(pattern.points) < 6:
            return False
        
        # Check if pattern can be divided into similar smaller patterns
        center_x = sum(p.x for p in pattern.points) / len(pattern.points)
        center_y = sum(p.y for p in pattern.points) / len(pattern.points)
        
        # Divide into quadrants and check similarity
        quadrants = [[], [], [], []]
        for p in pattern.points:
            if p.x >= center_x and p.y >= center_y:
                quadrants[0].append(p)
            elif p.x < center_x and p.y >= center_y:
                quadrants[1].append(p)
            elif p.x < center_x and p.y < center_y:
                quadrants[2].append(p)
            else:
                quadrants[3].append(p)
        
        # Check if quadrants have similar point counts
        counts = [len(q) for q in quadrants if len(q) > 0]
        if len(counts) > 1:
            avg_count = sum(counts) / len(counts)
            return all(abs(c - avg_count) < avg_count * 0.3 for c in counts)
        
        return False
    
    def _calculate_complexity(self, pattern: KolamPattern) -> str:
        """Calculate complexity level of the pattern"""
        point_count = len(pattern.points)
        line_count = len(pattern.lines)
        
        if point_count < 5 and line_count < 5:
            return "Simple"
        elif point_count < 15 and line_count < 20:
            return "Medium"
        else:
            return "Complex"

class KolamGenerator:
    """Generates new Kolam patterns based on identified principles"""
    
    def __init__(self):
        self.analyzer = KolamAnalyzer()
    
    def generate_grid_pattern(self, grid_size: Tuple[int, int], 
                            symmetry_type: SymmetryType = SymmetryType.RADIAL) -> KolamPattern:
        """Generate a basic grid-based Kolam pattern"""
        rows, cols = grid_size
        points = []
        
        # Create grid points
        for i in range(rows):
            for j in range(cols):
                x = j * 2.0  # Spacing between points
                y = i * 2.0
                points.append(KolamPoint(x, y))
        
        # Generate lines based on symmetry type
        lines = self._generate_lines_for_symmetry(points, symmetry_type)
        
        # Find center point
        center_x = sum(p.x for p in points) / len(points)
        center_y = sum(p.y for p in points) / len(points)
        
        pattern = KolamPattern(
            points=points,
            lines=lines,
            symmetry_type=symmetry_type,
            grid_size=grid_size,
            center_point=(center_x, center_y)
        )
        
        return pattern
    
    def _generate_lines_for_symmetry(self, points: List[KolamPoint], 
                                   symmetry_type: SymmetryType) -> List[Tuple[int, int]]:
        """Generate lines based on symmetry type"""
        lines = []
        
        if symmetry_type == SymmetryType.RADIAL:
            lines = self._generate_radial_lines(points)
        elif symmetry_type == SymmetryType.BILATERAL:
            lines = self._generate_bilateral_lines(points)
        elif symmetry_type == SymmetryType.ROTATIONAL:
            lines = self._generate_rotational_lines(points)
        else:
            lines = self._generate_random_lines(points)
        
        return lines
    
    def _generate_radial_lines(self, points: List[KolamPoint]) -> List[Tuple[int, int]]:
        """Generate radial lines from center"""
        lines = []
        center_idx = len(points) // 2  # Assume center is middle point
        
        for i, point in enumerate(points):
            if i != center_idx:
                lines.append((center_idx, i))
        
        return lines
    
    def _generate_bilateral_lines(self, points: List[KolamPoint]) -> List[Tuple[int, int]]:
        """Generate bilateral symmetric lines"""
        lines = []
        center_x = sum(p.x for p in points) / len(points)
        
        # Connect points symmetrically
        for i in range(len(points)):
            for j in range(i + 1, len(points)):
                p1, p2 = points[i], points[j]
                # Check if points are symmetric about center
                if abs((p1.x + p2.x) / 2 - center_x) < 0.1:
                    lines.append((i, j))
        
        return lines
    
    def _generate_rotational_lines(self, points: List[KolamPoint]) -> List[Tuple[int, int]]:
        """Generate rotational symmetric lines"""
        lines = []
        center_idx = len(points) // 2
        
        # Create rotational pattern
        for i in range(0, len(points), 2):
            if i + 1 < len(points):
                lines.append((i, i + 1))
                if i != center_idx:
                    lines.append((center_idx, i))
        
        return lines
    
    def _generate_random_lines(self, points: List[KolamPoint]) -> List[Tuple[int, int]]:
        """Generate random lines"""
        lines = []
        num_lines = min(len(points) * 2, 20)  # Limit number of lines
        
        for _ in range(num_lines):
            i, j = random.sample(range(len(points)), 2)
            lines.append((i, j))
        
        return lines
    
    def generate_fractal_kolam(self, base_pattern: KolamPattern, 
                             iterations: int = 3) -> KolamPattern:
        """Generate fractal Kolam by iteratively applying transformations"""
        current_pattern = base_pattern
        
        for iteration in range(iterations):
            new_points = []
            new_lines = []
            
            # Scale down and replicate the pattern
            scale_factor = 0.5 ** (iteration + 1)
            
            for i in range(4):  # Create 4 copies
                angle = i * math.pi / 2
                cos_a, sin_a = math.cos(angle), math.sin(angle)
                
                for point in current_pattern.points:
                    # Scale and rotate
                    new_x = point.x * scale_factor * cos_a - point.y * scale_factor * sin_a
                    new_y = point.x * scale_factor * sin_a + point.y * scale_factor * cos_a
                    new_points.append(KolamPoint(new_x, new_y))
            
            # Add lines
            for line in current_pattern.lines:
                new_lines.append(line)
            
            current_pattern = KolamPattern(
                points=new_points,
                lines=new_lines,
                symmetry_type=current_pattern.symmetry_type,
                grid_size=current_pattern.grid_size,
                center_point=(0, 0),
                fractal_level=iteration + 1
            )
        
        return current_pattern

class KolamVisualizer:
    """Visualizes Kolam patterns and analysis results"""
    
    def __init__(self):
        self.fig_size = (12, 10)
    
    def visualize_pattern(self, pattern: KolamPattern, 
                         title: str = "Kolam Pattern", 
                         show_analysis: bool = True):
        """Visualize a Kolam pattern with optional analysis"""
        fig, ax = plt.subplots(1, 1, figsize=self.fig_size)
        
        # Draw points
        for i, point in enumerate(pattern.points):
            color = 'red' if point.is_center else 'blue'
            size = 100 if point.is_center else 50
            ax.scatter(point.x, point.y, c=color, s=size, alpha=0.7)
            ax.annotate(str(i), (point.x, point.y), fontsize=8)
        
        # Draw lines
        for line in pattern.lines:
            p1, p2 = pattern.points[line[0]], pattern.points[line[1]]
            ax.plot([p1.x, p2.x], [p1.y, p2.y], 'k-', alpha=0.6, linewidth=1)
        
        # Draw center point
        center_x, center_y = pattern.center_point
        ax.scatter(center_x, center_y, c='red', s=200, marker='*', alpha=0.8)
        
        ax.set_title(f"{title}\nSymmetry: {pattern.symmetry_type.value}")
        ax.set_xlabel("X Coordinate")
        ax.set_ylabel("Y Coordinate")
        ax.grid(True, alpha=0.3)
        ax.set_aspect('equal')
        
        if show_analysis:
            # Add analysis text
            analyzer = KolamAnalyzer()
            fractal_props = analyzer.analyze_fractal_properties(pattern)
            
            analysis_text = f"""
            Analysis Results:
            • Fractal Dimension: {fractal_props['fractal_dimension']:.2f}
            • Self-Similarity: {fractal_props['self_similarity']}
            • Complexity: {fractal_props['complexity_level']}
            • Points: {len(pattern.points)}
            • Lines: {len(pattern.lines)}
            """
            
            ax.text(0.02, 0.98, analysis_text, transform=ax.transAxes, 
                   verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
        
        plt.tight_layout()
        plt.show()
    
    def compare_patterns(self, patterns: List[KolamPattern], 
                        titles: List[str] = None):
        """Compare multiple Kolam patterns"""
        if titles is None:
            titles = [f"Pattern {i+1}" for i in range(len(patterns))]
        
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        axes = axes.flatten()
        
        for i, (pattern, title) in enumerate(zip(patterns, titles)):
            if i >= 4:  # Limit to 4 patterns
                break
            
            ax = axes[i]
            
            # Draw points
            for point in pattern.points:
                color = 'red' if point.is_center else 'blue'
                size = 100 if point.is_center else 50
                ax.scatter(point.x, point.y, c=color, s=size, alpha=0.7)
            
            # Draw lines
            for line in pattern.lines:
                p1, p2 = pattern.points[line[0]], pattern.points[line[1]]
                ax.plot([p1.x, p2.x], [p1.y, p2.y], 'k-', alpha=0.6, linewidth=1)
            
            ax.set_title(f"{title}\n{pattern.symmetry_type.value}")
            ax.grid(True, alpha=0.3)
            ax.set_aspect('equal')
        
        # Hide unused subplots
        for i in range(len(patterns), 4):
            axes[i].set_visible(False)
        
        plt.tight_layout()
        plt.show()

def main():
    """Main function to demonstrate Kolam analysis and generation"""
    print("🎨 Kolam Design Analyzer and Generator")
    print("=" * 50)
    
    # Initialize components
    analyzer = KolamAnalyzer()
    generator = KolamGenerator()
    visualizer = KolamVisualizer()
    
    # Generate different types of Kolam patterns
    print("\n1. Generating different Kolam patterns...")
    
    patterns = []
    
    # Radial symmetry pattern
    radial_pattern = generator.generate_grid_pattern((5, 5), SymmetryType.RADIAL)
    patterns.append(radial_pattern)
    print("✓ Generated radial symmetry pattern")
    
    # Bilateral symmetry pattern
    bilateral_pattern = generator.generate_grid_pattern((4, 4), SymmetryType.BILATERAL)
    patterns.append(bilateral_pattern)
    print("✓ Generated bilateral symmetry pattern")
    
    # Rotational symmetry pattern
    rotational_pattern = generator.generate_grid_pattern((6, 6), SymmetryType.ROTATIONAL)
    patterns.append(rotational_pattern)
    print("✓ Generated rotational symmetry pattern")
    
    # Fractal pattern
    base_pattern = generator.generate_grid_pattern((3, 3), SymmetryType.RADIAL)
    fractal_pattern = generator.generate_fractal_kolam(base_pattern, 2)
    patterns.append(fractal_pattern)
    print("✓ Generated fractal pattern")
    
    # Analyze patterns
    print("\n2. Analyzing patterns...")
    for i, pattern in enumerate(patterns):
        symmetry = analyzer.analyze_symmetry(pattern.points)
        fractal_props = analyzer.analyze_fractal_properties(pattern)
        
        print(f"\nPattern {i+1}:")
        print(f"  Symmetry Type: {symmetry.value}")
        print(f"  Fractal Dimension: {fractal_props['fractal_dimension']:.2f}")
        print(f"  Self-Similarity: {fractal_props['self_similarity']}")
        print(f"  Complexity: {fractal_props['complexity_level']}")
        print(f"  Points: {len(pattern.points)}, Lines: {len(pattern.lines)}")
    
    # Visualize patterns
    print("\n3. Visualizing patterns...")
    visualizer.compare_patterns(patterns, 
                               ["Radial Symmetry", "Bilateral Symmetry", 
                                "Rotational Symmetry", "Fractal Pattern"])
    
    # Individual detailed visualization
    print("\n4. Detailed analysis of fractal pattern...")
    visualizer.visualize_pattern(fractal_pattern, "Fractal Kolam Pattern", show_analysis=True)
    
    print("\n✅ Analysis complete! Check the generated visualizations.")
    
    # Save results
    results = {
        'patterns_analyzed': len(patterns),
        'symmetry_types': [p.symmetry_type.value for p in patterns],
        'fractal_dimensions': [analyzer.analyze_fractal_properties(p)['fractal_dimension'] for p in patterns],
        'complexity_levels': [analyzer.analyze_fractal_properties(p)['complexity_level'] for p in patterns]
    }
    
    with open('kolam_analysis_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print("📊 Results saved to 'kolam_analysis_results.json'")

if __name__ == "__main__":
    main()
