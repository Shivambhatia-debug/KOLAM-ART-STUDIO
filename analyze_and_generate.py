#!/usr/bin/env python3
"""
Analyze and generate Brahma's Knot pattern for frontend display
"""

import json
import sys
import os
from topological_kolam_generator import TopologicalKolamGenerator, Point
from kolam_pattern_templates import KolamPatternTemplates

def analyze_and_generate():
    """Analyze and generate Brahma's Knot for frontend"""
    print("🎨 Analyzing and Generating Brahma's Knot for Frontend")
    print("=" * 60)
    
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
        return None
    
    print(f"✅ Template: {brahma_template.name}")
    print(f"   Dots: {brahma_template.num_dots}")
    print(f"   Symmetry: {brahma_template.symmetry_type}")
    print(f"   Region: Tamil Nadu")  # Default region
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
    
    # Create frontend-compatible data structure
    print("🎨 Creating frontend-compatible data...")
    
    # Convert points to frontend format
    frontend_points = []
    for i, point in enumerate(points):
        frontend_points.append({
            "x": point.x,
            "y": point.y,
            "id": i,
            "type": "dot"
        })
    
    # Convert paths to frontend format
    frontend_paths = []
    for i, path in enumerate(brahma_paths):
        if path and len(path) >= 2:
            path_points = []
            for point in path:
                path_points.append({
                    "x": point[0],
                    "y": point[1]
                })
            frontend_paths.append({
                "id": i,
                "points": path_points,
                "type": "path",
                "color": "#DC143C"  # Red color
            })
    
    # Create lines (junctions) for frontend
    frontend_lines = []
    junction_indices = brahma_template.suggested_junctions
    for i, (p1_idx, p2_idx) in enumerate(junction_indices[:20]):  # First 20 junctions
        if p1_idx < len(points) and p2_idx < len(points):
            p1 = points[p1_idx]
            p2 = points[p2_idx]
            frontend_lines.append({
                "id": i,
                "start": {"x": p1.x, "y": p1.y},
                "end": {"x": p2.x, "y": p2.y},
                "type": "junction",
                "color": "#333333"  # Dark gray
            })
    
    # Create complete pattern data
    pattern_data = {
        "points": frontend_points,
        "paths": frontend_paths,
        "lines": frontend_lines,
        "colors": ["#DC143C", "#B22222", "#8B0000", "#FF6347"],  # Red tones
        "cultural_info": {
            "traditional_name": brahma_template.name,
            "symbolism": brahma_template.cultural_significance,
            "region": "Tamil Nadu",
            "type": "eternal_knot"
        },
        "mathematical_properties": {
            "symmetry_type": brahma_template.symmetry_type,
            "dot_count": brahma_template.num_dots,
            "path_count": len(frontend_paths),
            "line_count": len(frontend_lines),
            "pattern_type": "eternal_knot",
            "continuous_loop": True
        },
        "region": "tamil_nadu",
        "complexity": "high",
        "analysis": {
            "total_points": len(frontend_points),
            "total_paths": len(frontend_paths),
            "total_lines": len(frontend_lines),
            "main_path_length": len(brahma_paths[0]) if brahma_paths else 0,
            "grid_size": "5x5",
            "authenticity": "high"
        }
    }
    
    print(f"✅ Frontend data created:")
    print(f"   Points: {len(frontend_points)}")
    print(f"   Paths: {len(frontend_paths)}")
    print(f"   Lines: {len(frontend_lines)}")
    print()
    
    # Save to JSON file for frontend
    output_file = "brahma_knot_frontend_data.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(pattern_data, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Data saved to '{output_file}'")
    
    # Display pattern summary
    print("\n📊 Pattern Analysis Summary:")
    print("=" * 40)
    print(f"Pattern Name: {brahma_template.name}")
    print(f"Cultural Type: Eternal Knot (Brahma Mudi)")
    print(f"Grid Size: 5x5 ({brahma_template.num_dots} dots)")
    print(f"Symmetry: {brahma_template.symmetry_type}")
    print(f"Region: Tamil Nadu")
    print(f"Main Path Points: {len(brahma_paths[0]) if brahma_paths else 0}")
    print(f"Junctions: {len(frontend_lines)}")
    print(f"Authenticity: High (Research-based)")
    print()
    
    # Display cultural significance
    print("🏛️ Cultural Significance:")
    print("=" * 30)
    print("• Brahma Mudi (Eternal Knot)")
    print("• Symbol of cosmic unity and infinity")
    print("• Continuous loop represents eternal cycle")
    print("• 5x5 grid represents five elements")
    print("• No loose ends = completeness")
    print("• Traditional South Indian art form")
    print()
    
    print("🎉 Pattern analysis and generation complete!")
    print(f"   Frontend data ready in '{output_file}'")
    
    return pattern_data

if __name__ == "__main__":
    result = analyze_and_generate()
    if result:
        print("\n✅ Success! Pattern ready for frontend display.")
    else:
        print("\n❌ Failed to generate pattern.")
