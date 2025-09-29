#!/usr/bin/env python3
"""
Turtle Pattern Generator
========================

Generate Kolam patterns using turtle graphics for better visualization.
"""

import turtle
import json
import os
import random
import math
from typing import List, Dict, Any

class TurtlePatternGenerator:
    """Generate Kolam patterns using turtle graphics"""
    
    def __init__(self):
        self.screen = None
        self.t = None
        self.patterns = []
        
    def setup_turtle(self, width=800, height=600):
        """Setup turtle screen"""
        self.screen = turtle.Screen()
        self.screen.setup(width, height)
        self.screen.bgcolor("white")
        self.screen.title("Kolam Pattern Generator")
        
        self.t = turtle.Turtle()
        self.t.speed(0)  # Fastest speed
        self.t.penup()
        
    def generate_fractal_kolam(self, complexity=5):
        """Generate fractal Kolam pattern"""
        self.t.penup()
        self.t.goto(0, 0)
        self.t.pendown()
        
        # Fractal pattern
        for i in range(complexity):
            angle = i * 72  # 72 degrees for pentagon
            self.t.setheading(angle)
            self.t.forward(50)
            self.t.left(120)
            self.t.forward(30)
            self.t.right(60)
            self.t.forward(20)
            self.t.left(90)
            self.t.forward(15)
            
    def generate_pulli_kolam(self, dots=5):
        """Generate Pulli Kolam pattern"""
        self.t.penup()
        
        # Draw dots
        for i in range(dots):
            for j in range(dots):
                x = (i - dots//2) * 40
                y = (j - dots//2) * 40
                self.t.goto(x, y)
                self.t.dot(8, "black")
        
        # Draw lines connecting dots
        self.t.pendown()
        self.t.pensize(2)
        
        # Connect dots in a pattern
        for i in range(dots):
            for j in range(dots-1):
                x1 = (i - dots//2) * 40
                y1 = (j - dots//2) * 40
                x2 = (i - dots//2) * 40
                y2 = ((j+1) - dots//2) * 40
                
                self.t.penup()
                self.t.goto(x1, y1)
                self.t.pendown()
                self.t.goto(x2, y2)
                
    def generate_sikku_kolam(self):
        """Generate Sikku Kolam pattern"""
        self.t.penup()
        self.t.goto(0, 0)
        self.t.pendown()
        self.t.pensize(3)
        
        # Sikku pattern - continuous line
        for i in range(8):
            self.t.forward(60)
            self.t.left(45)
            self.t.forward(40)
            self.t.right(90)
            self.t.forward(30)
            self.t.left(60)
            
    def generate_neli_kolam(self):
        """Generate Neli Kolam pattern"""
        self.t.penup()
        self.t.goto(0, 0)
        self.t.pendown()
        self.t.pensize(2)
        
        # Neli pattern - spiral
        for i in range(20):
            self.t.forward(i * 3)
            self.t.left(90)
            
    def generate_kambi_kolam(self):
        """Generate Kambi Kolam pattern"""
        self.t.penup()
        self.t.goto(0, 0)
        self.t.pendown()
        self.t.pensize(2)
        
        # Kambi pattern - grid-like
        for i in range(5):
            for j in range(5):
                x = (i - 2) * 30
                y = (j - 2) * 30
                self.t.penup()
                self.t.goto(x, y)
                self.t.pendown()
                self.t.circle(15)
                
    def generate_random_pattern(self):
        """Generate random pattern"""
        self.t.penup()
        self.t.goto(0, 0)
        self.t.pendown()
        self.t.pensize(2)
        
        # Random pattern
        for i in range(20):
            angle = random.randint(0, 360)
            distance = random.randint(10, 50)
            self.t.setheading(angle)
            self.t.forward(distance)
            self.t.left(random.randint(30, 120))
            
    def save_pattern(self, filename, pattern_type):
        """Save pattern as image"""
        if self.screen:
            # Get the canvas
            canvas = self.screen.getcanvas()
            canvas.postscript(file=f"{filename}.eps")
            
            # Convert to PNG using PIL if available
            try:
                from PIL import Image
                img = Image.open(f"{filename}.eps")
                img.save(f"{filename}.png")
                os.remove(f"{filename}.eps")
                print(f"✅ Pattern saved as {filename}.png")
            except ImportError:
                print(f"✅ Pattern saved as {filename}.eps")
                
    def generate_multiple_patterns(self, count=5):
        """Generate multiple patterns"""
        patterns = []
        
        for i in range(count):
            # Clear screen
            self.t.clear()
            self.t.penup()
            self.t.goto(0, 0)
            
            # Choose random pattern type
            pattern_types = [
                ("fractal", self.generate_fractal_kolam),
                ("pulli", self.generate_pulli_kolam),
                ("sikku", self.generate_sikku_kolam),
                ("neli", self.generate_neli_kolam),
                ("kambi", self.generate_kambi_kolam),
                ("random", self.generate_random_pattern)
            ]
            
            pattern_type, pattern_func = random.choice(pattern_types)
            
            # Generate pattern
            pattern_func()
            
            # Save pattern
            filename = f"turtle_pattern_{i:03d}"
            self.save_pattern(filename, pattern_type)
            
            # Store pattern info
            pattern_info = {
                "pattern_id": f"turtle_{i:03d}",
                "pattern_type": pattern_type,
                "filename": f"{filename}.png",
                "complexity": random.uniform(0.3, 0.9),
                "symmetry": random.choice(["bilateral", "radial", "grid", "rotational", "asymmetric"]),
                "cultural_region": random.choice(["tamil_nadu", "karnataka", "kerala", "andhra_pradesh"])
            }
            
            patterns.append(pattern_info)
            
        return patterns
        
    def close(self):
        """Close turtle screen"""
        if self.screen:
            self.screen.bye()

def test_turtle_generator():
    """Test turtle pattern generator"""
    print("🐢 Testing Turtle Pattern Generator...")
    
    generator = TurtlePatternGenerator()
    generator.setup_turtle()
    
    # Generate single patterns
    print("\n--- Generating Fractal Kolam ---")
    generator.generate_fractal_kolam()
    generator.save_pattern("fractal_kolam", "fractal")
    
    print("\n--- Generating Pulli Kolam ---")
    generator.t.clear()
    generator.generate_pulli_kolam()
    generator.save_pattern("pulli_kolam", "pulli")
    
    print("\n--- Generating Sikku Kolam ---")
    generator.t.clear()
    generator.generate_sikku_kolam()
    generator.save_pattern("sikku_kolam", "sikku")
    
    # Generate multiple patterns
    print("\n--- Generating Multiple Patterns ---")
    patterns = generator.generate_multiple_patterns(3)
    
    # Save metadata
    with open("turtle_patterns_metadata.json", "w") as f:
        json.dump(patterns, f, indent=2)
    
    print(f"\n📊 Generated {len(patterns)} patterns:")
    for pattern in patterns:
        print(f"   {pattern['pattern_id']}: {pattern['pattern_type']} ({pattern['filename']})")
    
    generator.close()
    print("\n✅ Turtle pattern generation complete!")

if __name__ == "__main__":
    test_turtle_generator()















