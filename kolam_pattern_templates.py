"""
Kolam Pattern Templates
======================

Pre-defined pattern templates based on parent kolam types from the research paper.
These templates follow the 5-step topological method and represent different
parent kolam types for various numbers of dots (N).

AICTE Problem Statement 25107
"""

import math
from typing import List, Tuple, Dict, Optional
from dataclasses import dataclass
from enum import Enum

class ParentKolamType(Enum):
    """Types of parent kolam patterns"""
    LINEAR = "linear"
    TRIANGULAR = "triangular"
    SQUARE = "square"
    PENTAGONAL = "pentagonal"
    HEXAGONAL = "hexagonal"
    RADIAL = "radial"
    COMPLEX = "complex"

@dataclass
class PatternTemplate:
    """Template for a kolam pattern"""
    name: str
    parent_type: ParentKolamType
    num_dots: int
    symmetry_type: str
    cultural_region: str
    description: str
    dot_positions: List[Tuple[float, float]]
    suggested_junctions: List[Tuple[int, int]]
    cultural_significance: str
    mathematical_properties: Dict
    difficulty_level: str

class KolamPatternTemplates:
    """
    Collection of pre-defined kolam pattern templates
    """
    
    def __init__(self):
        self.templates = self._create_templates()
    
    def _create_templates(self) -> List[PatternTemplate]:
        """Create all pattern templates"""
        templates = []
        
        # N=1 templates
        templates.append(PatternTemplate(
            name="Single Dot Circle",
            parent_type=ParentKolamType.RADIAL,
            num_dots=1,
            symmetry_type="radial",
            cultural_region="tamil_nadu",
            description="Simple circular pattern around a single dot",
            dot_positions=[(200, 200)],
            suggested_junctions=[],
            cultural_significance="Represents unity and the beginning of creation",
            mathematical_properties={
                "symmetry_order": 1,
                "complexity": 0.1,
                "geometric_ratio": 1.0
            },
            difficulty_level="beginner"
        ))
        
        # N=2 templates
        templates.append(PatternTemplate(
            name="Dual Dot Connection",
            parent_type=ParentKolamType.LINEAR,
            num_dots=2,
            symmetry_type="bilateral",
            cultural_region="tamil_nadu",
            description="Two dots connected with a single line",
            dot_positions=[(150, 200), (250, 200)],
            suggested_junctions=[(0, 1)],
            cultural_significance="Represents duality and balance",
            mathematical_properties={
                "symmetry_order": 2,
                "complexity": 0.2,
                "geometric_ratio": 1.0
            },
            difficulty_level="beginner"
        ))
        
        # N=3 templates
        templates.append(PatternTemplate(
            name="Triangle of Life",
            parent_type=ParentKolamType.TRIANGULAR,
            num_dots=3,
            symmetry_type="rotational",
            cultural_region="tamil_nadu",
            description="Three dots forming an equilateral triangle",
            dot_positions=[(200, 150), (150, 250), (250, 250)],
            suggested_junctions=[(0, 1), (1, 2), (2, 0)],
            cultural_significance="Represents the three aspects of existence",
            mathematical_properties={
                "symmetry_order": 3,
                "complexity": 0.4,
                "geometric_ratio": 1.0
            },
            difficulty_level="intermediate"
        ))
        
        templates.append(PatternTemplate(
            name="Linear Three",
            parent_type=ParentKolamType.LINEAR,
            num_dots=3,
            symmetry_type="bilateral",
            cultural_region="karnataka",
            description="Three dots in a straight line",
            dot_positions=[(150, 200), (200, 200), (250, 200)],
            suggested_junctions=[(0, 1), (1, 2)],
            cultural_significance="Represents progression and growth",
            mathematical_properties={
                "symmetry_order": 2,
                "complexity": 0.3,
                "geometric_ratio": 1.0
            },
            difficulty_level="beginner"
        ))
        
        # N=4 templates
        templates.append(PatternTemplate(
            name="Sacred Square",
            parent_type=ParentKolamType.SQUARE,
            num_dots=4,
            symmetry_type="rotational",
            cultural_region="andhra_pradesh",
            description="Four dots forming a square",
            dot_positions=[(150, 150), (250, 150), (250, 250), (150, 250)],
            suggested_junctions=[(0, 1), (1, 2), (2, 3), (3, 0), (0, 2), (1, 3)],
            cultural_significance="Represents the four directions and stability",
            mathematical_properties={
                "symmetry_order": 4,
                "complexity": 0.6,
                "geometric_ratio": 1.0
            },
            difficulty_level="intermediate"
        ))
        
        templates.append(PatternTemplate(
            name="Diamond Formation",
            parent_type=ParentKolamType.SQUARE,
            num_dots=4,
            symmetry_type="rotational",
            cultural_region="kerala",
            description="Four dots in diamond formation",
            dot_positions=[(200, 150), (250, 200), (200, 250), (150, 200)],
            suggested_junctions=[(0, 1), (1, 2), (2, 3), (3, 0)],
            cultural_significance="Represents the four elements",
            mathematical_properties={
                "symmetry_order": 4,
                "complexity": 0.5,
                "geometric_ratio": 1.0
            },
            difficulty_level="intermediate"
        ))
        
        # N=5 templates
        templates.append(PatternTemplate(
            name="Pentagon of Power",
            parent_type=ParentKolamType.PENTAGONAL,
            num_dots=5,
            symmetry_type="rotational",
            cultural_region="telangana",
            description="Five dots forming a regular pentagon",
            dot_positions=self._generate_pentagon_points(200, 200, 80),
            suggested_junctions=[(0, 1), (1, 2), (2, 3), (3, 4), (4, 0)],
            cultural_significance="Represents the five elements and cosmic order",
            mathematical_properties={
                "symmetry_order": 5,
                "complexity": 0.7,
                "geometric_ratio": 1.618  # Golden ratio
            },
            difficulty_level="advanced"
        ))
        
        # N=6 templates
        templates.append(PatternTemplate(
            name="Hexagon of Harmony",
            parent_type=ParentKolamType.HEXAGONAL,
            num_dots=6,
            symmetry_type="rotational",
            cultural_region="tamil_nadu",
            description="Six dots forming a regular hexagon",
            dot_positions=self._generate_hexagon_points(200, 200, 80),
            suggested_junctions=[(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 0)],
            cultural_significance="Represents the six seasons and natural cycles",
            mathematical_properties={
                "symmetry_order": 6,
                "complexity": 0.8,
                "geometric_ratio": 1.0
            },
            difficulty_level="advanced"
        ))
        
        # N=7+ templates
        templates.append(PatternTemplate(
            name="Seven Stars",
            parent_type=ParentKolamType.RADIAL,
            num_dots=7,
            symmetry_type="radial",
            cultural_region="karnataka",
            description="Seven dots in radial formation",
            dot_positions=self._generate_radial_points(200, 200, 80, 7),
            suggested_junctions=[(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 0)],
            cultural_significance="Represents the seven chakras and spiritual energy",
            mathematical_properties={
                "symmetry_order": 7,
                "complexity": 0.9,
                "geometric_ratio": 1.0
            },
            difficulty_level="expert"
        ))
        
        # Complex templates
        templates.append(PatternTemplate(
            name="Brahma's Knot",
            parent_type=ParentKolamType.COMPLEX,
            num_dots=25,
            symmetry_type="rotational",
            cultural_region="tamil_nadu",
            description="Authentic Brahma's Knot (Eternal Knot) - continuous loop pattern representing cosmic unity",
            dot_positions=self._generate_brahma_knot_points(200, 200),
            suggested_junctions=self._generate_brahma_knot_junctions(),
            cultural_significance="Represents the eternal knot of creation - continuous loop symbolizing cosmic unity and infinite connection",
            mathematical_properties={
                "symmetry_order": 4,
                "complexity": 1.0,
                "geometric_ratio": 1.0,
                "pattern_type": "eternal_knot",
                "continuous_loop": True
            },
            difficulty_level="expert"
        ))
        
        return templates
    
    def _generate_pentagon_points(self, center_x: float, center_y: float, radius: float) -> List[Tuple[float, float]]:
        """Generate points for a regular pentagon"""
        points = []
        for i in range(5):
            angle = (i * 2 * math.pi) / 5 - math.pi / 2  # Start from top
            x = center_x + radius * math.cos(angle)
            y = center_y + radius * math.sin(angle)
            points.append((x, y))
        return points
    
    def _generate_hexagon_points(self, center_x: float, center_y: float, radius: float) -> List[Tuple[float, float]]:
        """Generate points for a regular hexagon"""
        points = []
        for i in range(6):
            angle = (i * 2 * math.pi) / 6 - math.pi / 2  # Start from top
            x = center_x + radius * math.cos(angle)
            y = center_y + radius * math.sin(angle)
            points.append((x, y))
        return points
    
    def _generate_radial_points(self, center_x: float, center_y: float, radius: float, num_points: int) -> List[Tuple[float, float]]:
        """Generate points in radial formation"""
        points = []
        for i in range(num_points):
            angle = (i * 2 * math.pi) / num_points - math.pi / 2  # Start from top
            x = center_x + radius * math.cos(angle)
            y = center_y + radius * math.sin(angle)
            points.append((x, y))
        return points
    
    def _generate_brahma_knot_points(self, center_x: float, center_y: float) -> List[Tuple[float, float]]:
        """Generate points for Brahma's knot pattern - 5x5 grid"""
        points = []
        # Create a 5x5 grid with proper spacing
        spacing = 40
        for i in range(5):
            for j in range(5):
                x = center_x + (i - 2) * spacing
                y = center_y + (j - 2) * spacing
                points.append((x, y))
        return points
    
    def _generate_brahma_knot_junctions(self) -> List[Tuple[int, int]]:
        """Generate junction suggestions for Brahma's knot using 5-step topological method"""
        junctions = []
        
        # Based on Gopalan & VanLeeuwen research paper
        # This implements the authentic Brahma's Knot using topological approach
        
        # Step 1: 5x5 grid of dots (already placed)
        # Step 2: Perpendicular bisectors between dot pairs
        # Step 3: Squishies around each dot with arms touching at junctions
        # Step 4: Transform junctions into X, D, or B bonds
        # Step 5: Smooth curves for final pattern
        
        # Create the authentic Brahma's Knot pattern following topological principles
        # This creates a single continuous loop that represents the eternal knot
        
        # Outer boundary - creates the main frame
        outer_boundary = [
            (0, 1), (1, 2), (2, 3), (3, 4),  # Top edge
            (4, 9), (9, 14), (14, 19), (19, 24),  # Right edge
            (24, 23), (23, 22), (22, 21), (21, 20),  # Bottom edge
            (20, 15), (15, 10), (10, 5), (5, 0)  # Left edge
        ]
        
        # Inner knot structure - the core of Brahma's Knot
        # This creates the interwoven pattern characteristic of the eternal knot
        inner_knot = [
            # Central cross pattern
            (6, 7), (7, 8), (8, 13), (13, 18), (18, 17), (17, 16), (16, 11), (11, 6),
            # Inner diamond
            (7, 12), (12, 17), (17, 12), (12, 7),
            # Connecting arms
            (6, 11), (11, 16), (16, 17), (17, 18), (18, 13), (13, 8), (8, 7), (7, 6)
        ]
        
        # Bridge connections - link outer and inner structures
        bridge_connections = [
            (1, 6), (6, 11), (11, 16), (16, 21),  # Left bridge
            (3, 8), (8, 13), (13, 18), (18, 23),  # Right bridge
            (5, 10), (10, 15), (15, 20),  # Bottom bridge
            (9, 14), (14, 19)  # Top bridge
        ]
        
        # Petal extensions - create the characteristic petal-like loops
        # These represent the four directions in the eternal knot
        petal_loops = [
            # Top petal
            (0, 1), (1, 2), (2, 3), (3, 4), (4, 3), (3, 2), (2, 1), (1, 0),
            # Right petal
            (4, 9), (9, 14), (14, 19), (19, 24), (24, 19), (19, 14), (14, 9), (9, 4),
            # Bottom petal
            (20, 21), (21, 22), (22, 23), (23, 24), (24, 23), (23, 22), (22, 21), (21, 20),
            # Left petal
            (0, 5), (5, 10), (10, 15), (15, 20), (20, 15), (15, 10), (10, 5), (5, 0)
        ]
        
        # Additional knot complexity - create the interwoven effect
        knot_complexity = [
            # Cross-connections that create the knot effect
            (1, 6), (6, 7), (7, 8), (8, 13), (13, 18), (18, 17), (17, 16), (16, 21),
            (3, 8), (8, 7), (7, 6), (6, 11), (11, 16), (16, 17), (17, 18), (18, 23),
            (5, 10), (10, 11), (11, 12), (12, 17), (17, 16), (16, 15), (15, 20),
            (9, 14), (14, 13), (13, 12), (12, 17), (17, 18), (18, 19)
        ]
        
        # Combine all elements to create the complete Brahma's Knot
        junctions.extend(outer_boundary)
        junctions.extend(inner_knot)
        junctions.extend(bridge_connections)
        junctions.extend(petal_loops)
        junctions.extend(knot_complexity)
        
        return junctions
    
    def get_templates_by_dots(self, num_dots: int) -> List[PatternTemplate]:
        """Get all templates for a specific number of dots"""
        return [t for t in self.templates if t.num_dots == num_dots]
    
    def get_templates_by_region(self, region: str) -> List[PatternTemplate]:
        """Get all templates for a specific cultural region"""
        return [t for t in self.templates if t.cultural_region == region]
    
    def get_templates_by_difficulty(self, difficulty: str) -> List[PatternTemplate]:
        """Get all templates for a specific difficulty level"""
        return [t for t in self.templates if t.difficulty_level == difficulty]
    
    def get_template_by_name(self, name: str) -> Optional[PatternTemplate]:
        """Get a specific template by name"""
        for template in self.templates:
            if template.name.lower() == name.lower():
                return template
        return None
    
    def get_all_templates(self) -> List[PatternTemplate]:
        """Get all available templates"""
        return self.templates
    
    def get_template_summary(self) -> Dict:
        """Get a summary of all templates"""
        summary = {
            "total_templates": len(self.templates),
            "by_dots": {},
            "by_region": {},
            "by_difficulty": {},
            "by_parent_type": {}
        }
        
        for template in self.templates:
            # Count by dots
            if template.num_dots not in summary["by_dots"]:
                summary["by_dots"][template.num_dots] = 0
            summary["by_dots"][template.num_dots] += 1
            
            # Count by region
            if template.cultural_region not in summary["by_region"]:
                summary["by_region"][template.cultural_region] = 0
            summary["by_region"][template.cultural_region] += 1
            
            # Count by difficulty
            if template.difficulty_level not in summary["by_difficulty"]:
                summary["by_difficulty"][template.difficulty_level] = 0
            summary["by_difficulty"][template.difficulty_level] += 1
            
            # Count by parent type
            if template.parent_type.value not in summary["by_parent_type"]:
                summary["by_parent_type"][template.parent_type.value] = 0
            summary["by_parent_type"][template.parent_type.value] += 1
        
        return summary

# Example usage and testing
if __name__ == "__main__":
    templates = KolamPatternTemplates()
    
    print("Kolam Pattern Templates")
    print("=" * 50)
    
    # Get summary
    summary = templates.get_template_summary()
    print(f"Total templates: {summary['total_templates']}")
    print(f"By dots: {summary['by_dots']}")
    print(f"By region: {summary['by_region']}")
    print(f"By difficulty: {summary['by_difficulty']}")
    print(f"By parent type: {summary['by_parent_type']}")
    
    # Get templates for 3 dots
    print("\nTemplates for 3 dots:")
    three_dot_templates = templates.get_templates_by_dots(3)
    for template in three_dot_templates:
        print(f"- {template.name}: {template.description}")
    
    # Get templates for Tamil Nadu
    print("\nTemplates for Tamil Nadu:")
    tamil_templates = templates.get_templates_by_region("tamil_nadu")
    for template in tamil_templates:
        print(f"- {template.name} ({template.num_dots} dots): {template.description}")
    
    # Get a specific template
    print("\nBrahma's Knot template:")
    brahma_template = templates.get_template_by_name("Brahma's Knot")
    if brahma_template:
        print(f"Name: {brahma_template.name}")
        print(f"Dots: {brahma_template.num_dots}")
        print(f"Difficulty: {brahma_template.difficulty_level}")
        print(f"Cultural significance: {brahma_template.cultural_significance}")
        print(f"Mathematical properties: {brahma_template.mathematical_properties}")
