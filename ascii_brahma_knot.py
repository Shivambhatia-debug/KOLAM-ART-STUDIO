#!/usr/bin/env python3
"""
Generate ASCII art of Brahma's Knot
"""

from topological_kolam_generator import TopologicalKolamGenerator, Point
from kolam_pattern_templates import KolamPatternTemplates

def generate_ascii_brahma():
    """Generate ASCII art of Brahma's Knot"""
    print("🎨 ASCII Brahma's Knot Generation")
    print("=" * 50)
    
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
    
    # Create ASCII representation
    print("\n🎨 Creating ASCII representation...")
    ascii_art = create_ascii_brahma(points, brahma_paths[0] if brahma_paths else [])
    
    print("\n" + "="*60)
    print("BRAHMA'S KNOT - ASCII ART")
    print("="*60)
    print(ascii_art)
    print("="*60)
    
    # Save to file
    with open('brahma_knot_ascii.txt', 'w', encoding='utf-8') as f:
        f.write("BRAHMA'S KNOT - ASCII ART\n")
        f.write("="*60 + "\n")
        f.write(ascii_art)
        f.write("\n" + "="*60 + "\n")
    
    print("\n✅ ASCII art saved to 'brahma_knot_ascii.txt'")
    print("\n🎉 ASCII Brahma's Knot generated successfully!")

def create_ascii_brahma(points, path):
    """Create ASCII art representation"""
    
    # Find bounds
    min_x = min(point.x for point in points)
    max_x = max(point.x for point in points)
    min_y = min(point.y for point in points)
    max_y = max(point.y for point in points)
    
    # Scale to fit in ASCII grid
    width = 80
    height = 40
    
    scale_x = width / (max_x - min_x) if max_x > min_x else 1
    scale_y = height / (max_y - min_y) if max_y > min_y else 1
    scale = min(scale_x, scale_y) * 0.8  # Leave some margin
    
    # Create grid
    grid = [[' ' for _ in range(width)] for _ in range(height)]
    
    # Draw path
    if path:
        for i in range(len(path) - 1):
            x1 = int((path[i][0] - min_x) * scale)
            y1 = int((path[i][1] - min_y) * scale)
            x2 = int((path[i+1][0] - min_x) * scale)
            y2 = int((path[i+1][1] - min_y) * scale)
            
            # Draw line between points
            draw_line(grid, x1, y1, x2, y2, '*')
    
    # Draw dots
    for point in points:
        x = int((point.x - min_x) * scale)
        y = int((point.y - min_y) * scale)
        if 0 <= x < width and 0 <= y < height:
            grid[y][x] = 'O'
    
    # Convert to string
    ascii_lines = []
    for row in grid:
        ascii_lines.append(''.join(row))
    
    return '\n'.join(ascii_lines)

def draw_line(grid, x1, y1, x2, y2, char):
    """Draw a line between two points"""
    width = len(grid[0])
    height = len(grid)
    
    # Simple line drawing algorithm
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    
    if dx > dy:
        # Horizontal line
        for x in range(min(x1, x2), max(x1, x2) + 1):
            y = y1 + (y2 - y1) * (x - x1) // (x2 - x1) if x2 != x1 else y1
            if 0 <= x < width and 0 <= y < height:
                grid[y][x] = char
    else:
        # Vertical line
        for y in range(min(y1, y2), max(y1, y2) + 1):
            x = x1 + (x2 - x1) * (y - y1) // (y2 - y1) if y2 != y1 else x1
            if 0 <= x < width and 0 <= y < height:
                grid[y][x] = char

if __name__ == "__main__":
    generate_ascii_brahma()
