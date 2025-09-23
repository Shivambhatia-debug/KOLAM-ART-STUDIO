#!/usr/bin/env python3
"""
Animated Spiral Kolam with Dotted Squares
=========================================

Creates a beautiful animated spiral Kolam pattern
"""

import turtle
import time
import math

def create_animated_spiral():
    """Create animated spiral Kolam pattern"""
    # Setup screen
    screen = turtle.Screen()
    screen.bgcolor("black")
    screen.title("Animated Spiral Kolam with Dotted Squares")
    screen.setup(1000, 800)
    screen.tracer(0)  # Manual animation control
    
    # Setup turtle
    pen = turtle.Turtle()
    pen.speed(0)
    pen.color("cyan")
    pen.pensize(2)
    pen.hideturtle()
    
    print("🎨 Starting Animated Spiral Kolam Generation...")
    print("📐 Pattern: Spiral with Dotted Squares")
    print("🎯 Colors: Cyan spiral, White dotted squares")
    print("=" * 60)
    
    # Animation parameters
    turns = 6
    step_angle = 15
    step_length = 8
    total_steps = int((360 / step_angle) * turns)
    
    # Start from center
    pen.penup()
    pen.goto(0, 0)
    pen.pendown()
    
    print(f"🔄 Generating {turns} turns with {total_steps} steps...")
    print("⏳ Watch the animation...")
    
    # Generate spiral with animation
    for i in range(total_steps):
        # Draw spiral line
        pen.forward(step_length)
        pen.right(step_angle)
        
        # Add dotted square every 15 steps
        if i % 15 == 0 and i > 5:
            current_x = pen.xcor()
            current_y = pen.ycor()
            
            # Move forward for square placement
            pen.forward(20)
            square_x = pen.xcor()
            square_y = pen.ycor()
            
            # Draw dotted square
            pen.penup()
            pen.goto(square_x, square_y)
            pen.pendown()
            pen.color("white")
            
            # Draw square with dots
            for _ in range(4):
                for j in range(3):
                    pen.dot(4, "white")
                    pen.forward(12)
                pen.right(90)
            
            pen.color("cyan")  # Reset color
            pen.penup()
            pen.goto(current_x, current_y)
            pen.pendown()
        
        # Update screen every few steps for smooth animation
        if i % 3 == 0:
            screen.update()
            time.sleep(0.05)  # Animation delay
        
        # Progress indicator
        if i % 20 == 0:
            progress = (i / total_steps) * 100
            print(f"⏳ Progress: {progress:.1f}% - Step {i}/{total_steps}")
    
    # Final update
    screen.update()
    
    print("✅ Pattern generation complete!")
    print("🎉 Beautiful Spiral Kolam created!")
    print("🖼️  Close the window to continue...")
    
    # Add some final touches
    pen.penup()
    pen.goto(0, 0)
    pen.color("yellow")
    pen.write("Spiral Kolam", align="center", font=("Arial", 16, "bold"))
    
    # Keep window open
    screen.exitonclick()

def create_simple_spiral():
    """Create a simple spiral for quick demo"""
    screen = turtle.Screen()
    screen.bgcolor("black")
    screen.title("Simple Spiral Kolam")
    screen.setup(600, 600)
    
    pen = turtle.Turtle()
    pen.speed(2)
    pen.color("cyan")
    pen.pensize(2)
    
    print("🎨 Drawing Simple Spiral Kolam...")
    
    # Draw spiral with dots
    for i in range(80):
        pen.forward(6)
        pen.right(12)
        
        # Add dots along the way
        if i % 8 == 0:
            pen.dot(5, "white")
    
    print("✅ Simple spiral complete!")
    turtle.done()

if __name__ == "__main__":
    print("🎨 Kolam Spiral Generator")
    print("Choose animation type:")
    print("1. Animated Spiral (beautiful animation)")
    print("2. Simple Spiral (quick demo)")
    
    try:
        choice = input("Enter choice (1 or 2): ").strip()
        
        if choice == "1":
            create_animated_spiral()
        else:
            create_simple_spiral()
    except KeyboardInterrupt:
        print("\n👋 Animation stopped by user")
    except Exception as e:
        print(f"❌ Error: {e}")
        print("🔄 Trying simple version...")
        create_simple_spiral()












