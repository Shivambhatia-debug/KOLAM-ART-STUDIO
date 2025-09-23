#!/usr/bin/env python3
"""
Colorful Kolam Design using Turtle Graphics
Based on user's provided code with enhancements
"""

import turtle
import colorsys
import math

def setup_screen():
    """Setup the turtle screen"""
    screen = turtle.Screen()
    screen.bgcolor("black")
    screen.title("Colorful Kolam Design - Brahma's Knot Style")
    screen.setup(800, 800)
    return screen

def setup_turtle():
    """Setup the turtle pen"""
    pen = turtle.Turtle()
    pen.speed(0)  # fastest
    pen.width(3)
    return pen

def generate_colors(num_colors=36):
    """Generate beautiful colors using HSV"""
    colors = []
    for i in range(num_colors):
        hue = i / num_colors
        # Create vibrant colors with high saturation
        col = colorsys.hsv_to_rgb(hue, 0.9, 1.0)  # (r,g,b)
        colors.append(col)
    return colors

def draw_brahma_knot_pattern(pen, colors):
    """Draw Brahma's Knot inspired pattern"""
    pen.penup()
    pen.goto(0, -150)
    pen.pendown()
    
    # Draw multiple concentric patterns
    for layer in range(8):
        pen.color(colors[layer % len(colors)])
        
        # Draw the main circular pattern
        for petal in range(12 + layer * 4):
            pen.circle(60 + layer * 15)
            pen.right(360 / (12 + layer * 4))
        
        # Add spiral effect
        pen.right(15)
    
    # Draw center mandala
    pen.penup()
    pen.goto(0, 0)
    pen.pendown()
    
    for i in range(6):
        pen.color(colors[i % len(colors)])
        pen.circle(30, 360)
        pen.right(60)

def draw_enhanced_kolam(pen, colors):
    """Draw enhanced Kolam with multiple patterns"""
    pen.penup()
    pen.goto(0, -200)
    pen.pendown()
    
    # Main pattern layers
    for r in range(6):  # layers
        pen.color(colors[r % len(colors)])
        
        # Draw petals
        petals = 12 + r * 6
        for j in range(petals):
            pen.circle(50 + r * 20)
            pen.right(360 / petals)
        
        # Rotate for next layer
        pen.right(10)
    
    # Add center details
    pen.penup()
    pen.goto(0, 0)
    pen.pendown()
    
    # Draw center mandala
    for i in range(8):
        pen.color(colors[i % len(colors)])
        pen.circle(25 + i * 5)
        pen.right(45)

def draw_geometric_kolam(pen, colors):
    """Draw geometric Kolam pattern"""
    pen.penup()
    pen.goto(0, -100)
    pen.pendown()
    
    # Draw geometric shapes
    for i in range(12):
        pen.color(colors[i % len(colors)])
        
        # Draw square
        for _ in range(4):
            pen.forward(50)
            pen.right(90)
        
        # Draw circle
        pen.circle(30)
        
        pen.right(30)

def main():
    """Main function to create colorful Kolam"""
    print("🎨 Creating Colorful Kolam Design...")
    print("=" * 40)
    
    # Setup
    screen = setup_screen()
    pen = setup_turtle()
    colors = generate_colors(48)  # More colors for variety
    
    print(f"✅ Generated {len(colors)} colors")
    print("✅ Screen setup complete")
    print("✅ Turtle configured")
    print()
    
    print("🎨 Drawing patterns...")
    
    # Draw multiple patterns
    try:
        # Pattern 1: Enhanced Kolam
        print("   Drawing enhanced Kolam pattern...")
        draw_enhanced_kolam(pen, colors)
        
        # Pattern 2: Brahma's Knot inspired
        print("   Drawing Brahma's Knot inspired pattern...")
        pen.penup()
        pen.goto(200, 0)
        pen.pendown()
        draw_brahma_knot_pattern(pen, colors)
        
        # Pattern 3: Geometric Kolam
        print("   Drawing geometric Kolam pattern...")
        pen.penup()
        pen.goto(-200, 0)
        pen.pendown()
        draw_geometric_kolam(pen, colors)
        
        print("✅ All patterns drawn successfully!")
        
    except Exception as e:
        print(f"❌ Error during drawing: {e}")
    
    # Hide turtle and keep window open
    pen.hideturtle()
    
    print("\n🎉 Colorful Kolam Design Complete!")
    print("   Close the window to exit")
    
    # Keep window open
    turtle.done()

if __name__ == "__main__":
    main()













