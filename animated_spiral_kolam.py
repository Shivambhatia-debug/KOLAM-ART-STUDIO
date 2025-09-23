#!/usr/bin/env python3
"""
Animated Spiral Kolam Generator
==============================

Creates an animated spiral Kolam pattern with dotted squares
"""

import turtle
import time
import math

def setup_screen():
    """Setup the turtle screen"""
    screen = turtle.Screen()
    screen.bgcolor("black")
    screen.title("Animated Spiral Kolam with Dotted Squares")
    screen.setup(1000, 800)
    screen.tracer(0)  # Turn off animation for manual control
    return screen

def setup_turtle():
    """Setup the turtle pen"""
    pen = turtle.Turtle()
    pen.speed(0)
    pen.color("cyan")
    pen.pensize(2)
    pen.hideturtle()
    return pen

def draw_dotted_square(pen, x, y, size=15, dots=3):
    """Draw a dotted square at given position"""
    pen.penup()
    pen.goto(x, y)
    pen.pendown()
    pen.color("white")
    
    for _ in range(4):
        for i in range(dots):
            pen.dot(4, "white")
            pen.forward(size / dots)
        pen.right(90)
    
    pen.color("cyan")  # Reset color
    pen.penup()

def animated_spiral_kolam():
    """Create animated spiral Kolam pattern"""
    screen = setup_screen()
    pen = setup_turtle()
    
    print("🎨 Starting Animated Spiral Kolam Generation...")
    print("📐 Pattern: Spiral with Dotted Squares")
    print("🎯 Colors: Cyan spiral, White dotted squares")
    print("=" * 50)
    
    # Animation parameters
    turns = 8
    step_angle = 10
    step_length = 5
    total_steps = int((360 / step_angle) * turns)
    
    # Start from center
    pen.penup()
    pen.goto(0, 0)
    pen.pendown()
    
    print(f"🔄 Generating {turns} turns with {total_steps} steps...")
    
    # Generate spiral with animation
    for i in range(total_steps):
        # Draw spiral line
        pen.forward(step_length)
        pen.right(step_angle)
        
        # Add dotted square every 20 steps
        if i % 20 == 0 and i > 0:
            current_x = pen.xcor()
            current_y = pen.ycor()
            
            # Move forward for square placement
            pen.forward(15)
            square_x = pen.xcor()
            square_y = pen.ycor()
            
            # Draw dotted square
            draw_dotted_square(pen, square_x, square_y, 15, 3)
            
            # Return to spiral path
            pen.goto(current_x, current_y)
            pen.pendown()
        
        # Update screen every few steps for animation
        if i % 5 == 0:
            screen.update()
            time.sleep(0.01)  # Small delay for animation effect
        
        # Progress indicator
        if i % 50 == 0:
            progress = (i / total_steps) * 100
            print(f"⏳ Progress: {progress:.1f}% - Step {i}/{total_steps}")
    
    # Final update
    screen.update()
    
    print("✅ Pattern generation complete!")
    print("🎉 Spiral Kolam with dotted squares created!")
    print("🖼️  Close the window to continue...")
    
    # Keep window open
    screen.exitonclick()

def simple_spiral_demo():
    """Simple spiral demo without complex animation"""
    screen = turtle.Screen()
    screen.bgcolor("black")
    screen.title("Simple Spiral Kolam Demo")
    screen.setup(800, 600)
    
    pen = turtle.Turtle()
    pen.speed(1)  # Slow speed for visibility
    pen.color("cyan")
    pen.pensize(2)
    
    print("🎨 Drawing Simple Spiral Kolam...")
    
    # Draw spiral
    for i in range(100):
        pen.forward(5)
        pen.right(10)
        
        # Add dots along the way
        if i % 10 == 0:
            pen.dot(5, "white")
    
    print("✅ Simple spiral complete!")
    turtle.done()

if __name__ == "__main__":
    print("🎨 Kolam Spiral Generator")
    print("1. Animated Spiral (complex)")
    print("2. Simple Spiral (basic)")
    
    choice = input("Choose option (1 or 2): ").strip()
    
    if choice == "1":
        animated_spiral_kolam()
    else:
        simple_spiral_demo()












