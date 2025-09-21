"""
Advanced Kolam Analysis Module
=============================

This module provides advanced analysis techniques for Kolam patterns including:
- L-System based pattern generation
- Advanced fractal analysis
- Pattern classification using machine learning
- Cultural significance analysis
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle, Polygon
import math
import random
from typing import List, Tuple, Dict, Any, Optional
from dataclasses import dataclass
from enum import Enum
import json
from kolam_analyzer import KolamPattern, KolamPoint, SymmetryType

class LSystemRule:
    """Represents a rule in an L-System"""
    def __init__(self, predecessor: str, successor: str, probability: float = 1.0):
        self.predecessor = predecessor
        self.successor = successor
        self.probability = probability

class LSystem:
    """Lindenmayer System for generating Kolam patterns"""
    
    def __init__(self, axiom: str, rules: List[LSystemRule], angle: float = 90):
        self.axiom = axiom
        self.rules = rules
        self.angle = math.radians(angle)
        self.current_string = axiom
    
    def iterate(self, iterations: int = 1) -> str:
        """Apply L-System rules for specified iterations"""
        for _ in range(iterations):
            new_string = ""
            for char in self.current_string:
                # Find applicable rules
                applicable_rules = [rule for rule in self.rules 
                                 if rule.predecessor == char and random.random() < rule.probability]
                
                if applicable_rules:
                    rule = random.choice(applicable_rules)
                    new_string += rule.successor
                else:
                    new_string += char
            
            self.current_string = new_string
        
        return self.current_string
    
    def interpret_to_points(self, start_pos: Tuple[float, float] = (0, 0), 
                          step_size: float = 1.0) -> List[KolamPoint]:
        """Interpret L-System string as Kolam points"""
        points = []
        current_pos = start_pos
        current_angle = 0
        stack = []  # For saving/restoring state
        
        for char in self.current_string:
            if char == 'F':  # Forward
                new_x = current_pos[0] + step_size * math.cos(current_angle)
                new_y = current_pos[1] + step_size * math.sin(current_angle)
                new_pos = (new_x, new_y)
                points.append(KolamPoint(new_x, new_y))
                current_pos = new_pos
            elif char == '+':  # Turn right
                current_angle += self.angle
            elif char == '-':  # Turn left
                current_angle -= self.angle
            elif char == '[':  # Save state
                stack.append((current_pos, current_angle))
            elif char == ']':  # Restore state
                if stack:
                    current_pos, current_angle = stack.pop()
        
        return points

class KolamClassifier:
    """Machine learning-based Kolam pattern classifier"""
    
    def __init__(self):
        self.features = {}
        self.classification_model = None
    
    def extract_features(self, pattern: KolamPattern) -> Dict[str, float]:
        """Extract numerical features from a Kolam pattern"""
        features = {}
        
        # Basic geometric features
        features['point_count'] = len(pattern.points)
        features['line_count'] = len(pattern.lines)
        features['density'] = len(pattern.points) / (pattern.grid_size[0] * pattern.grid_size[1])
        
        # Symmetry features
        features['radial_symmetry'] = 1.0 if pattern.symmetry_type == SymmetryType.RADIAL else 0.0
        features['bilateral_symmetry'] = 1.0 if pattern.symmetry_type == SymmetryType.BILATERAL else 0.0
        features['rotational_symmetry'] = 1.0 if pattern.symmetry_type == SymmetryType.ROTATIONAL else 0.0
        
        # Geometric complexity
        if pattern.points:
            x_coords = [p.x for p in pattern.points]
            y_coords = [p.y for p in pattern.points]
            
            features['x_variance'] = np.var(x_coords)
            features['y_variance'] = np.var(y_coords)
            features['spread'] = math.sqrt(features['x_variance'] + features['y_variance'])
            
            # Center distance variance
            center_x = np.mean(x_coords)
            center_y = np.mean(y_coords)
            distances = [math.sqrt((p.x - center_x)**2 + (p.y - center_y)**2) for p in pattern.points]
            features['distance_variance'] = np.var(distances)
        
        # Line features
        if pattern.lines:
            line_lengths = []
            for line in pattern.lines:
                p1, p2 = pattern.points[line[0]], pattern.points[line[1]]
                length = math.sqrt((p1.x - p2.x)**2 + (p1.y - p2.y)**2)
                line_lengths.append(length)
            
            features['avg_line_length'] = np.mean(line_lengths)
            features['line_length_variance'] = np.var(line_lengths)
            features['max_line_length'] = max(line_lengths)
            features['min_line_length'] = min(line_lengths)
        
        # Fractal features
        fractal_props = self._calculate_fractal_features(pattern)
        features.update(fractal_props)
        
        return features
    
    def _calculate_fractal_features(self, pattern: KolamPattern) -> Dict[str, float]:
        """Calculate fractal-related features"""
        features = {}
        
        # Box-counting fractal dimension
        features['fractal_dimension'] = self._box_counting_dimension(pattern)
        
        # Self-similarity measure
        features['self_similarity'] = self._self_similarity_measure(pattern)
        
        # Recursive structure indicator
        features['recursive_structure'] = self._recursive_structure_measure(pattern)
        
        return features
    
    def _box_counting_dimension(self, pattern: KolamPattern) -> float:
        """Calculate fractal dimension using box-counting method"""
        if len(pattern.points) < 4:
            return 1.0
        
        # Get bounding box
        min_x = min(p.x for p in pattern.points)
        max_x = max(p.x for p in pattern.points)
        min_y = min(p.y for p in pattern.points)
        max_y = max(p.y for p in pattern.points)
        
        # Use different box sizes
        box_sizes = [0.1, 0.2, 0.4, 0.8, 1.6]
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
        if len(counts) > 1 and all(c > 0 for c in counts):
            log_sizes = [math.log(1/s) for s in box_sizes]
            log_counts = [math.log(c) for c in counts]
            if len(log_counts) > 1:
                slope, _ = np.polyfit(log_sizes, log_counts, 1)
                return max(0, min(2, slope))  # Clamp between 0 and 2
        
        return 1.0
    
    def _self_similarity_measure(self, pattern: KolamPattern) -> float:
        """Measure self-similarity in the pattern"""
        if len(pattern.points) < 6:
            return 0.0
        
        # Divide pattern into quadrants and compare
        center_x = sum(p.x for p in pattern.points) / len(pattern.points)
        center_y = sum(p.y for p in pattern.points) / len(pattern.points)
        
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
        
        # Calculate similarity between quadrants
        similarities = []
        for i in range(len(quadrants)):
            for j in range(i + 1, len(quadrants)):
                if len(quadrants[i]) > 0 and len(quadrants[j]) > 0:
                    sim = self._quadrant_similarity(quadrants[i], quadrants[j])
                    similarities.append(sim)
        
        return np.mean(similarities) if similarities else 0.0
    
    def _quadrant_similarity(self, q1: List[KolamPoint], q2: List[KolamPoint]) -> float:
        """Calculate similarity between two quadrants"""
        if len(q1) == 0 or len(q2) == 0:
            return 0.0
        
        # Normalize by size
        size_ratio = min(len(q1), len(q2)) / max(len(q1), len(q2))
        
        # Calculate geometric similarity
        if len(q1) == len(q2):
            # Compare point distributions
            q1_coords = [(p.x, p.y) for p in q1]
            q2_coords = [(p.x, p.y) for p in q2]
            
            # Simple distance-based similarity
            distances = []
            for p1 in q1_coords:
                min_dist = min(math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2) 
                              for p2 in q2_coords)
                distances.append(min_dist)
            
            avg_distance = np.mean(distances)
            max_possible_distance = math.sqrt(2)  # Diagonal of unit square
            geometric_sim = 1.0 - (avg_distance / max_possible_distance)
        else:
            geometric_sim = 0.5  # Neutral similarity for different sizes
        
        return (size_ratio + geometric_sim) / 2
    
    def _recursive_structure_measure(self, pattern: KolamPattern) -> float:
        """Measure how recursive/self-similar the structure is"""
        if len(pattern.points) < 4:
            return 0.0
        
        # Look for repeated sub-patterns
        center_x = sum(p.x for p in pattern.points) / len(pattern.points)
        center_y = sum(p.y for p in pattern.points) / len(pattern.points)
        
        # Check for concentric patterns
        distances = [math.sqrt((p.x - center_x)**2 + (p.y - center_y)**2) for p in pattern.points]
        unique_distances = list(set(round(d, 1) for d in distances))
        
        # More unique distances suggest more recursive structure
        max_possible_distances = len(pattern.points)
        recursive_measure = len(unique_distances) / max_possible_distances
        
        return min(1.0, recursive_measure)

class CulturalSignificanceAnalyzer:
    """Analyzes cultural significance of Kolam patterns"""
    
    def __init__(self):
        self.regional_patterns = {
            'tamil_nadu': {
                'characteristics': ['radial_symmetry', 'circular_patterns', 'sikku_kolam'],
                'typical_grid_sizes': [(5, 5), (7, 7), (9, 9)]
            },
            'karnataka': {
                'characteristics': ['bilateral_symmetry', 'geometric_shapes', 'rectangular_patterns'],
                'typical_grid_sizes': [(4, 4), (6, 6), (8, 8)]
            },
            'andhra_pradesh': {
                'characteristics': ['rotational_symmetry', 'floral_patterns', 'curved_lines'],
                'typical_grid_sizes': [(6, 6), (8, 8), (10, 10)]
            },
            'kerala': {
                'characteristics': ['asymmetric_patterns', 'nature_inspired', 'free_form'],
                'typical_grid_sizes': [(3, 3), (5, 5), (7, 7)]
            }
        }
    
    def analyze_regional_characteristics(self, pattern: KolamPattern) -> Dict[str, float]:
        """Analyze which regional characteristics the pattern exhibits"""
        classifier = KolamClassifier()
        features = classifier.extract_features(pattern)
        
        regional_scores = {}
        
        for region, characteristics in self.regional_patterns.items():
            score = 0.0
            total_checks = 0
            
            # Check symmetry characteristics
            if 'radial_symmetry' in characteristics and features['radial_symmetry'] > 0.5:
                score += 1.0
            total_checks += 1
            
            if 'bilateral_symmetry' in characteristics and features['bilateral_symmetry'] > 0.5:
                score += 1.0
            total_checks += 1
            
            if 'rotational_symmetry' in characteristics and features['rotational_symmetry'] > 0.5:
                score += 1.0
            total_checks += 1
            
            # Check grid size characteristics
            grid_area = pattern.grid_size[0] * pattern.grid_size[1]
            typical_sizes = characteristics['typical_grid_sizes']
            typical_areas = [w * h for w, h in typical_sizes]
            
            if any(abs(grid_area - area) < 5 for area in typical_areas):
                score += 1.0
            total_checks += 1
            
            # Check fractal characteristics
            if 'sikku_kolam' in characteristics and features['fractal_dimension'] > 1.3:
                score += 1.0
            total_checks += 1
            
            if 'free_form' in characteristics and features['fractal_dimension'] < 1.2:
                score += 1.0
            total_checks += 1
            
            regional_scores[region] = score / total_checks if total_checks > 0 else 0.0
        
        return regional_scores
    
    def get_cultural_interpretation(self, pattern: KolamPattern) -> Dict[str, Any]:
        """Get cultural interpretation of the pattern"""
        regional_scores = self.analyze_regional_characteristics(pattern)
        best_match = max(regional_scores.items(), key=lambda x: x[1])
        
        interpretation = {
            'most_likely_region': best_match[0],
            'confidence': best_match[1],
            'regional_scores': regional_scores,
            'cultural_significance': self._get_significance_meaning(best_match[0])
        }
        
        return interpretation
    
    def _get_significance_meaning(self, region: str) -> str:
        """Get cultural significance meaning for a region"""
        meanings = {
            'tamil_nadu': "Traditional Tamil Kolam with radial symmetry, often used in daily rituals and festivals",
            'karnataka': "Karnataka Muggu with geometric precision, reflecting mathematical traditions",
            'andhra_pradesh': "Andhra Rangoli with floral motifs, celebrating nature and beauty",
            'kerala': "Kerala Asymmetric patterns, representing natural flow and organic forms"
        }
        return meanings.get(region, "Traditional Indian Kolam pattern")

def generate_lsystem_kolam(iterations: int = 3) -> KolamPattern:
    """Generate a Kolam using L-System"""
    # Define L-System rules for Kolam generation
    rules = [
        LSystemRule('F', 'F+F-F-F+F', 0.8),  # Main growth rule
        LSystemRule('F', 'F-F+F+F-F', 0.2),  # Alternative growth rule
        LSystemRule('+', '+', 1.0),          # Preserve turns
        LSystemRule('-', '-', 1.0),          # Preserve turns
        LSystemRule('[', '[', 1.0),          # Preserve stack operations
        LSystemRule(']', ']', 1.0)           # Preserve stack operations
    ]
    
    # Create L-System
    lsystem = LSystem('F', rules, angle=90)
    
    # Iterate the system
    lsystem.iterate(iterations)
    
    # Convert to points
    points = lsystem.interpret_to_points(start_pos=(0, 0), step_size=2.0)
    
    # Generate lines connecting nearby points
    lines = []
    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            p1, p2 = points[i], points[j]
            distance = math.sqrt((p1.x - p2.x)**2 + (p1.y - p2.y)**2)
            if distance < 3.0:  # Connect nearby points
                lines.append((i, j))
    
    # Create pattern
    center_x = sum(p.x for p in points) / len(points) if points else 0
    center_y = sum(p.y for p in points) / len(points) if points else 0
    
    pattern = KolamPattern(
        points=points,
        lines=lines,
        symmetry_type=SymmetryType.ROTATIONAL,
        grid_size=(len(points), len(points)),
        center_point=(center_x, center_y),
        fractal_level=iterations
    )
    
    return pattern

def main():
    """Demonstrate advanced Kolam analysis"""
    print("🔬 Advanced Kolam Analysis")
    print("=" * 40)
    
    # Generate L-System Kolam
    print("\n1. Generating L-System Kolam...")
    lsystem_pattern = generate_lsystem_kolam(iterations=3)
    print(f"✓ Generated L-System pattern with {len(lsystem_pattern.points)} points")
    
    # Classify pattern
    print("\n2. Classifying pattern...")
    classifier = KolamClassifier()
    features = classifier.extract_features(lsystem_pattern)
    
    print("Key Features:")
    for key, value in features.items():
        if isinstance(value, float):
            print(f"  {key}: {value:.3f}")
        else:
            print(f"  {key}: {value}")
    
    # Cultural analysis
    print("\n3. Cultural significance analysis...")
    cultural_analyzer = CulturalSignificanceAnalyzer()
    interpretation = cultural_analyzer.get_cultural_interpretation(lsystem_pattern)
    
    print(f"Most likely region: {interpretation['most_likely_region']}")
    print(f"Confidence: {interpretation['confidence']:.2f}")
    print(f"Cultural significance: {interpretation['cultural_significance']}")
    
    print("\nRegional scores:")
    for region, score in interpretation['regional_scores'].items():
        print(f"  {region}: {score:.3f}")
    
    # Visualize
    print("\n4. Visualizing advanced pattern...")
    from kolam_analyzer import KolamVisualizer
    visualizer = KolamVisualizer()
    visualizer.visualize_pattern(lsystem_pattern, "L-System Kolam Pattern", show_analysis=True)
    
    print("\n✅ Advanced analysis complete!")

if __name__ == "__main__":
    main()

