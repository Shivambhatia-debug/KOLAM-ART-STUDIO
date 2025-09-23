#!/usr/bin/env python3
"""
Simple Turtle Graphics Brahma's Knot
- Working version
- Step-by-step generation
"""

import turtle
import time
import math

def setup_screen():
    """Setup turtle screen"""
    screen = turtle.Screen()
    screen.bgcolor("white")
    screen.title("Brahma's Knot - Turtle Graphics")
    screen.setup(800, 600)
    return screen

def setup_turtle():
    """Setup turtle pen"""
    pen = turtle.Turtle()
    pen.speed(1)  # Slow speed for animation
    pen.width(3)
    pen.hideturtle()
    return pen

def draw_dot(pen, x, y, size=8, color="red"):
    """Draw a dot at position"""
    pen.penup()
    pen.goto(x, y)
    pen.pendown()
    pen.dot(size, color)
    pen.penup()

def draw_line(pen, x1, y1, x2, y2, color="black"):
    """Draw a line between two points"""
    pen.penup()
    pen.goto(x1, y1)
    pen.pendown()
    pen.pencolor(color)
    pen.goto(x2, y2)
    pen.penup()

def generate_brahma_dots():
    """Generate 29 dots for Brahma's Knot"""
    dots = []
    center_x, center_y = 0, 0
    grid_spacing = 40
    
    # 5x5 grid dots (25 dots)
    for i in range(5):
        for j in range(5):
            x = center_x + (j - 2) * grid_spacing
            y = center_y + (i - 2) * grid_spacing
            dots.append((x, y, 'grid'))
    
    # 4 outer petal dots
    petal_radius = 80
    petal_angles = [90, 0, -90, 180]  # Top, Right, Bottom, Left
    for angle in petal_angles:
        x = center_x + petal_radius * math.cos(math.radians(angle))
        y = center_y + petal_radius * math.sin(math.radians(angle))
        dots.append((x, y, 'petal'))
    
    return dots

def create_brahma_path(dots):
    """Create Brahma's Knot path"""
    # Get dot positions
    dot_positions = [(dot[0], dot[1]) for dot in dots]
    
    # Simplified Brahma's Knot path
    path_sequence = [
        # Start from top petal (index 25)
        25, 0, 1, 2, 3, 4, 26,  # Top row to right petal
        9, 8, 7, 6, 5,          # Back through top row
        10, 11, 12, 13, 14,     # Second row
        19, 18, 17, 16, 15,     # Third row
        20, 21, 22, 23, 24,     # Fourth row
        28, 27, 26,             # Bottom row to left petal
        24, 23, 22, 21, 20,     # Back through bottom row
        15, 16, 17, 18, 19,     # Back through third row
        14, 13, 12, 11, 10,     # Back through second row
        5, 6, 7, 8, 9,          # Back through top row
        0, 25                    # Back to start
    ]
    
    # Convert to coordinates
    path_coords = []
    for dot_id in path_sequence:
        if dot_id < len(dot_positions):
            path_coords.append(dot_positions[dot_id])
    
    return path_coords

def animate_brahma_knot():
    """Animate Brahma's Knot drawing"""
    print("🐢 Starting Turtle Graphics Brahma's Knot...")
    
    # Setup
    screen = setup_screen()
    pen = setup_turtle()
    
    # Generate dots
    dots = generate_brahma_dots()
    print(f"✅ Generated {len(dots)} dots")
    
    # Step 1: Draw all dots
    print("Step 1: Drawing dots...")
    for i, dot in enumerate(dots):
        x, y, dot_type = dot
        if dot_type == 'grid':
            draw_dot(pen, x, y, 6, "red")
        else:  # petal
            draw_dot(pen, x, y, 8, "darkred")
        
        time.sleep(0.2)  # Animation delay
        screen.update()
    
    print(f"✅ Drew {len(dots)} dots")
    
    # Step 2: Create and draw path
    print("Step 2: Creating path...")
    path_coords = create_brahma_path(dots)
    print(f"✅ Created path with {len(path_coords)} points")
    
    # Step 3: Draw continuous path
    print("Step 3: Drawing continuous path...")
    pen.pencolor("black")
    pen.width(4)
    
    if len(path_coords) > 1:
        pen.penup()
        pen.goto(path_coords[0])
        pen.pendown()
        
        for i, point in enumerate(path_coords[1:]):
            pen.goto(point)
            time.sleep(0.1)  # Animation delay
            screen.update()
        
        pen.penup()
    
    print(f"✅ Drew continuous path")
    
    # Step 4: Add center dot
    print("Step 4: Adding center decoration...")
    draw_dot(pen, 0, 0, 10, "red")
    
    print("✅ Brahma's Knot complete!")
    print("🎨 Close window to exit.")
    
    # Keep window open
    screen.exitonclick()

def main():
    """Main function"""
    print("🐢 Simple Turtle Graphics Brahma's Knot")
    print("=" * 50)
    
    try:
        animate_brahma_knot()
        print("\n✅ Brahma's Knot generated successfully!")
    except Exception as e:
        print(f"❌ Error: {e}")
        print("Trying alternative method...")
        
        # Alternative: Simple matplotlib version
        create_matplotlib_version()

def create_matplotlib_version():
    """Create matplotlib version as fallback"""
    try:
        import matplotlib.pyplot as plt
        import numpy as np
        
        print("📊 Creating matplotlib version...")
        
        # Generate dots
        dots = generate_brahma_dots()
        
        # Create figure
        fig, ax = plt.subplots(1, 1, figsize=(10, 10))
        ax.set_xlim(-120, 120)
        ax.set_ylim(-120, 120)
        ax.set_aspect('equal')
        ax.set_facecolor('white')
        
        # Draw dots
        for dot in dots:
            x, y, dot_type = dot
            if dot_type == 'grid':
                ax.plot(x, y, 'ro', markersize=8)
            else:
                ax.plot(x, y, 'ro', markersize=10)
        
        # Draw path
        path_coords = create_brahma_path(dots)
        if len(path_coords) > 1:
            x_coords = [p[0] for p in path_coords]
            y_coords = [p[1] for p in path_coords]
            ax.plot(x_coords, y_coords, 'k-', linewidth=3)
        
        ax.set_title('Brahma\'s Knot - Turtle Graphics Style', fontsize=16)
        ax.set_xticks([])
        ax.set_yticks([])
        
        plt.tight_layout()
        plt.savefig('turtle_brahma_knot.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        print("✅ Matplotlib version created!")
        
    except Exception as e:
        print(f"❌ Matplotlib error: {e}")

if __name__ == "__main__":
    main()













