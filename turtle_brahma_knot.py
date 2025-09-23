#!/usr/bin/env python3
"""
Turtle Graphics Style Brahma's Knot
- Exactly like Python terminal
- Step-by-step generation
- Animated drawing
"""

import turtle
import time
import math

class TurtleBrahmaKnot:
    def __init__(self):
        self.screen = turtle.Screen()
        self.screen.bgcolor("white")
        self.screen.title("Brahma's Knot - Turtle Graphics")
        self.screen.setup(800, 600)
        
        self.pen = turtle.Turtle()
        self.pen.speed(0)
        self.pen.width(3)
        
        # Colors
        self.dot_color = "#DC143C"
        self.line_color = "#000000"
        
    def setup_turtle(self):
        """Setup turtle for drawing"""
        self.pen.hideturtle()
        self.pen.penup()
        
    def draw_dot(self, x, y, size=8, color=None):
        """Draw a dot at position"""
        if color is None:
            color = self.dot_color
            
        self.pen.goto(x, y)
        self.pen.pendown()
        self.pen.dot(size, color)
        self.pen.penup()
        
    def draw_line(self, x1, y1, x2, y2, color=None):
        """Draw a line between two points"""
        if color is None:
            color = self.line_color
            
        self.pen.pencolor(color)
        self.pen.goto(x1, y1)
        self.pen.pendown()
        self.pen.goto(x2, y2)
        self.pen.penup()
        
    def draw_curve(self, points, color=None):
        """Draw a smooth curve through points"""
        if color is None:
            color = self.line_color
            
        self.pen.pencolor(color)
        self.pen.goto(points[0])
        self.pen.pendown()
        
        for point in points[1:]:
            self.pen.goto(point)
            
        self.pen.penup()
        
    def generate_29_dots(self):
        """Generate 29 dots for Brahma's Knot"""
        dots = []
        center_x, center_y = 0, 0
        grid_spacing = 40
        outer_radius = 80
        
        # 5x5 grid dots (25 dots)
        for i in range(5):
            for j in range(5):
                x = center_x + (j - 2) * grid_spacing
                y = center_y + (i - 2) * grid_spacing
                dots.append((x, y, 'grid'))
        
        # 4 outer petal dots
        petal_angles = [90, 0, -90, 180]  # Top, Right, Bottom, Left
        for angle in petal_angles:
            x = center_x + outer_radius * math.cos(math.radians(angle))
            y = center_y + outer_radius * math.sin(math.radians(angle))
            dots.append((x, y, 'petal'))
        
        return dots
    
    def create_brahma_path(self, dots):
        """Create Brahma's Knot path"""
        # Get dot positions
        dot_positions = [(dot[0], dot[1]) for dot in dots]
        
        # Brahma's Knot path sequence
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
    
    def animate_drawing(self, dots, path_coords):
        """Animate the drawing process"""
        print("🐢 Starting Turtle Graphics Animation...")
        
        # Step 1: Draw all dots
        print("Step 1: Drawing dots...")
        for i, dot in enumerate(dots):
            x, y, dot_type = dot
            if dot_type == 'grid':
                self.draw_dot(x, y, 6, self.dot_color)
            else:  # petal
                self.draw_dot(x, y, 8, "#B22222")
            
            time.sleep(0.1)  # Animation delay
            self.screen.update()
        
        print(f"✅ Drew {len(dots)} dots")
        
        # Step 2: Draw continuous path
        print("Step 2: Drawing continuous path...")
        self.pen.pencolor(self.line_color)
        self.pen.width(4)
        
        if len(path_coords) > 1:
            self.pen.goto(path_coords[0])
            self.pen.pendown()
            
            for i, point in enumerate(path_coords[1:]):
                self.pen.goto(point)
                time.sleep(0.05)  # Animation delay
                self.screen.update()
            
            self.pen.penup()
        
        print(f"✅ Drew continuous path with {len(path_coords)} points")
        
        # Step 3: Add decorative elements
        print("Step 3: Adding decorative elements...")
        self.add_decorative_elements()
        
        print("✅ Animation complete!")
        
    def add_decorative_elements(self):
        """Add decorative elements"""
        # Add corner decorations
        corner_positions = [(-120, 120), (120, 120), (-120, -120), (120, -120)]
        
        for x, y in corner_positions:
            self.draw_dot(x, y, 3, "#FF69B4")
        
        # Add center decoration
        self.draw_dot(0, 0, 10, "#DC143C")
        
    def generate_brahma_knot(self):
        """Generate complete Brahma's Knot"""
        print("🎯 Generating Brahma's Knot with Turtle Graphics...")
        
        # Setup
        self.setup_turtle()
        
        # Generate dots
        dots = self.generate_29_dots()
        print(f"✅ Generated {len(dots)} dots")
        
        # Create path
        path_coords = self.create_brahma_path(dots)
        print(f"✅ Created path with {len(path_coords)} points")
        
        # Animate drawing
        self.animate_drawing(dots, path_coords)
        
        # Keep window open
        print("🎨 Brahma's Knot complete! Close window to exit.")
        self.screen.exitonclick()
        
        return {
            'dots': dots,
            'path': path_coords,
            'type': 'turtle_brahma'
        }

def main():
    """Main function"""
    print("🐢 Turtle Graphics Brahma's Knot")
    print("=" * 50)
    
    brahma = TurtleBrahmaKnot()
    data = brahma.generate_brahma_knot()
    
    print("\n✅ Brahma's Knot generated successfully!")
    print(f"📊 Dots: {len(data['dots'])}")
    print(f"📊 Path Points: {len(data['path'])}")
    print("🎨 Traditional ornamental style!")

if __name__ == "__main__":
    main()













