#!/usr/bin/env python3
"""
Simple Brahma's Knot test without matplotlib
"""

from topological_kolam_generator import TopologicalKolamGenerator, Point
from kolam_pattern_templates import KolamPatternTemplates

def simple_brahma_test():
    """Simple test of Brahma's Knot generation"""
    print("🎨 Simple Brahma's Knot Test")
    print("=" * 40)
    
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
    print(f"   Symmetry: {brahma_template.symmetry_type}")
    print()
    
    # Create points
    points = []
    for i, dot_pos in enumerate(brahma_template.dot_positions):
        points.append(Point(dot_pos[0], dot_pos[1]))
        if i < 5:  # Show first 5 points
            print(f"   Point {i}: ({dot_pos[0]:.1f}, {dot_pos[1]:.1f})")
    
    print(f"✅ Created {len(points)} points")
    
    # Show junctions
    junctions = brahma_template.suggested_junctions
    print(f"✅ Junctions: {len(junctions)}")
    print("   First 5 junctions:")
    for i, junction in enumerate(junctions[:5]):
        print(f"   Junction {i}: {junction}")
    
    print()
    
    # Test the Brahma's Knot path generation directly
    print("🔄 Testing Brahma's Knot path generation...")
    
    try:
        # Use the specialized Brahma's Knot method
        brahma_paths = generator._create_brahma_knot_paths(points)
        print(f"✅ Generated {len(brahma_paths)} Brahma's Knot paths")
        
        if brahma_paths:
            main_path = brahma_paths[0]
            print(f"   Main path has {len(main_path)} points")
            print("   First 10 path points:")
            for i, point in enumerate(main_path[:10]):
                print(f"     {i}: ({point[0]:.1f}, {point[1]:.1f})")
        
        print("\n🎉 Brahma's Knot generation successful!")
        
    except Exception as e:
        print(f"❌ Error in Brahma's Knot generation: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    simple_brahma_test()


































