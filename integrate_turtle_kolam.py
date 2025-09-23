#!/usr/bin/env python3
"""
Integrate Turtle Kolam with Frontend Data
Generate colorful Kolam patterns and convert to frontend format
"""

import turtle
import colorsys
import json
import math

def generate_turtle_kolam_data():
    """Generate Kolam data using Turtle graphics for frontend"""
    print("🎨 Generating Turtle Kolam Data for Frontend...")
    print("=" * 50)
    
    # Generate colors
    num_colors = 36
    colors = []
    for i in range(num_colors):
        hue = i / num_colors
        col = colorsys.hsv_to_rgb(hue, 1, 1)
        colors.append(col)
    
    print(f"✅ Generated {num_colors} colors")
    
    # Generate pattern points
    points = []
    paths = []
    
    # Create circular pattern points
    center_x, center_y = 0, 0
    base_radius = 50
    
    for r in range(6):  # layers
        radius = base_radius + r * 20
        petals = 12 + r * 6
        
        for j in range(petals):
            angle = (j * 360 / petals) * math.pi / 180
            x = center_x + radius * math.cos(angle)
            y = center_y + radius * math.sin(angle)
            
            points.append({
                "x": x,
                "y": y,
                "id": len(points),
                "type": "dot",
                "color": colors[j % num_colors]
            })
    
    # Create paths (circles)
    for r in range(6):
        radius = base_radius + r * 20
        petals = 12 + r * 6
        
        path_points = []
        for j in range(petals + 1):  # +1 to close the circle
            angle = (j * 360 / petals) * math.pi / 180
            x = center_x + radius * math.cos(angle)
            y = center_y + radius * math.sin(angle)
            path_points.append({"x": x, "y": y})
        
        paths.append({
            "id": r,
            "points": path_points,
            "type": "path",
            "color": colors[r % num_colors]
        })
    
    # Create frontend data
    frontend_data = {
        "points": points,
        "paths": paths,
        "colors": [f"rgb({int(c[0]*255)},{int(c[1]*255)},{int(c[2]*255)})" for c in colors],
        "cultural_info": {
            "traditional_name": "Colorful Kolam Design",
            "symbolism": "Vibrant circular patterns representing cosmic harmony",
            "region": "South India",
            "type": "colorful_kolam"
        },
        "mathematical_properties": {
            "symmetry_type": "radial",
            "dot_count": len(points),
            "path_count": len(paths),
            "pattern_type": "circular_layers",
            "continuous_loop": True
        },
        "region": "south_india",
        "complexity": "medium",
        "analysis": {
            "total_points": len(points),
            "total_paths": len(paths),
            "color_count": num_colors,
            "layers": 6,
            "authenticity": "high"
        }
    }
    
    print(f"✅ Generated frontend data:")
    print(f"   Points: {len(points)}")
    print(f"   Paths: {len(paths)}")
    print(f"   Colors: {num_colors}")
    print()
    
    # Save to JSON
    output_file = "turtle_kolam_frontend_data.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(frontend_data, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Data saved to '{output_file}'")
    
    return frontend_data

def create_enhanced_turtle_kolam():
    """Create enhanced Turtle Kolam with more patterns"""
    print("🎨 Creating Enhanced Turtle Kolam...")
    
    # Setup turtle (hidden for data generation)
    screen = turtle.Screen()
    screen.setup(800, 800)
    pen = turtle.Turtle()
    pen.speed(0)
    pen.hideturtle()
    
    # Generate colors
    colors = []
    for i in range(48):
        hue = i / 48
        col = colorsys.hsv_to_rgb(hue, 0.9, 1.0)
        colors.append(col)
    
    # Generate pattern data
    points = []
    paths = []
    
    # Multiple pattern centers
    centers = [(0, 0), (200, 0), (-200, 0), (0, 200), (0, -200)]
    
    for center_idx, (cx, cy) in enumerate(centers):
        for r in range(4):  # layers per center
            radius = 30 + r * 15
            petals = 8 + r * 2
            
            for j in range(petals):
                angle = (j * 360 / petals) * math.pi / 180
                x = cx + radius * math.cos(angle)
                y = cy + radius * math.sin(angle)
                
                points.append({
                    "x": x,
                    "y": y,
                    "id": len(points),
                    "type": "dot",
                    "color": colors[(center_idx + r + j) % len(colors)]
                })
            
            # Create path for this layer
            path_points = []
            for j in range(petals + 1):
                angle = (j * 360 / petals) * math.pi / 180
                x = cx + radius * math.cos(angle)
                y = cy + radius * math.sin(angle)
                path_points.append({"x": x, "y": y})
            
            paths.append({
                "id": len(paths),
                "points": path_points,
                "type": "path",
                "color": colors[(center_idx + r) % len(colors)]
            })
    
    # Create enhanced frontend data
    enhanced_data = {
        "points": points,
        "paths": paths,
        "colors": [f"rgb({int(c[0]*255)},{int(c[1]*255)},{int(c[2]*255)})" for c in colors],
        "cultural_info": {
            "traditional_name": "Enhanced Colorful Kolam",
            "symbolism": "Multiple interconnected patterns representing cosmic unity",
            "region": "South India",
            "type": "enhanced_kolam"
        },
        "mathematical_properties": {
            "symmetry_type": "radial",
            "dot_count": len(points),
            "path_count": len(paths),
            "pattern_type": "multi_center",
            "continuous_loop": True
        },
        "region": "south_india",
        "complexity": "high",
        "analysis": {
            "total_points": len(points),
            "total_paths": len(paths),
            "color_count": len(colors),
            "centers": len(centers),
            "authenticity": "high"
        }
    }
    
    # Save enhanced data
    output_file = "enhanced_turtle_kolam_data.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(enhanced_data, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Enhanced data saved to '{output_file}'")
    print(f"   Points: {len(points)}")
    print(f"   Paths: {len(paths)}")
    print(f"   Colors: {len(colors)}")
    
    return enhanced_data

if __name__ == "__main__":
    print("🎨 Turtle Kolam Frontend Integration")
    print("=" * 40)
    
    # Generate basic turtle kolam data
    basic_data = generate_turtle_kolam_data()
    
    print("\n" + "=" * 40)
    
    # Generate enhanced turtle kolam data
    enhanced_data = create_enhanced_turtle_kolam()
    
    print("\n🎉 Turtle Kolam data generation complete!")
    print("   Files created:")
    print("   - turtle_kolam_frontend_data.json")
    print("   - enhanced_turtle_kolam_data.json")
    print("   Ready for frontend integration!")













