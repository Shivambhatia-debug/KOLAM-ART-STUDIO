#!/usr/bin/env python3
"""
Matplotlib Pattern Generator
============================

Generate Kolam patterns using matplotlib for better visualization.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import json
import os
import random
import math
from typing import List, Dict, Any

# Set matplotlib backend
import matplotlib
matplotlib.use('Agg')

class MatplotlibPatternGenerator:
    """Generate Kolam patterns using matplotlib"""
    
    def __init__(self):
        self.fig = None
        self.ax = None
        
    def setup_plot(self, size=(10, 10)):
        """Setup matplotlib plot"""
        self.fig, self.ax = plt.subplots(figsize=size)
        self.ax.set_xlim(-5, 5)
        self.ax.set_ylim(-5, 5)
        self.ax.set_aspect('equal')
        self.ax.axis('off')
        
    def generate_fractal_kolam(self, complexity=5):
        """Generate fractal Kolam pattern"""
        # Fractal pattern
        angles = np.linspace(0, 2*np.pi, complexity+1)
        
        for i, angle in enumerate(angles[:-1]):
            # Main line
            x1, y1 = 0, 0
            x2, y2 = 2 * np.cos(angle), 2 * np.sin(angle)
            self.ax.plot([x1, x2], [y1, y2], 'k-', linewidth=2)
            
            # Sub-lines
            mid_x, mid_y = x2/2, y2/2
            perp_angle = angle + np.pi/2
            x3 = mid_x + 0.5 * np.cos(perp_angle)
            y3 = mid_y + 0.5 * np.sin(perp_angle)
            x4 = mid_x - 0.5 * np.cos(perp_angle)
            y4 = mid_y - 0.5 * np.sin(perp_angle)
            self.ax.plot([x3, x4], [y3, y4], 'k-', linewidth=1)
            
    def generate_pulli_kolam(self, dots=5):
        """Generate Pulli Kolam pattern"""
        # Draw dots
        for i in range(dots):
            for j in range(dots):
                x = (i - dots//2) * 0.8
                y = (j - dots//2) * 0.8
                circle = patches.Circle((x, y), 0.1, color='black')
                self.ax.add_patch(circle)
        
        # Draw lines connecting dots
        for i in range(dots):
            for j in range(dots-1):
                x1 = (i - dots//2) * 0.8
                y1 = (j - dots//2) * 0.8
                x2 = (i - dots//2) * 0.8
                y2 = ((j+1) - dots//2) * 0.8
                self.ax.plot([x1, x2], [y1, y2], 'k-', linewidth=1)
                
    def generate_sikku_kolam(self):
        """Generate Sikku Kolam pattern"""
        # Sikku pattern - continuous line
        t = np.linspace(0, 4*np.pi, 100)
        x = np.cos(t) * (1 + 0.5*np.cos(5*t))
        y = np.sin(t) * (1 + 0.5*np.cos(5*t))
        self.ax.plot(x, y, 'k-', linewidth=2)
        
    def generate_neli_kolam(self):
        """Generate Neli Kolam pattern"""
        # Neli pattern - spiral
        t = np.linspace(0, 6*np.pi, 200)
        r = t / (6*np.pi) * 2
        x = r * np.cos(t)
        y = r * np.sin(t)
        self.ax.plot(x, y, 'k-', linewidth=2)
        
    def generate_kambi_kolam(self):
        """Generate Kambi Kolam pattern"""
        # Kambi pattern - grid-like
        for i in range(5):
            for j in range(5):
                x = (i - 2) * 0.6
                y = (j - 2) * 0.6
                circle = patches.Circle((x, y), 0.2, fill=False, linewidth=2)
                self.ax.add_patch(circle)
                
    def generate_random_pattern(self):
        """Generate random pattern"""
        # Random pattern
        n_points = 20
        angles = np.random.uniform(0, 2*np.pi, n_points)
        distances = np.random.uniform(0.5, 2, n_points)
        
        x = distances * np.cos(angles)
        y = distances * np.sin(angles)
        
        # Connect points
        for i in range(n_points-1):
            self.ax.plot([x[i], x[i+1]], [y[i], y[i+1]], 'k-', linewidth=1)
            
    def generate_spiral_pattern(self):
        """Generate spiral pattern"""
        t = np.linspace(0, 8*np.pi, 300)
        r = t / (8*np.pi) * 3
        x = r * np.cos(t)
        y = r * np.sin(t)
        self.ax.plot(x, y, 'k-', linewidth=2)
        
    def generate_flower_pattern(self):
        """Generate flower pattern"""
        # Flower pattern
        for i in range(8):
            angle = i * np.pi / 4
            t = np.linspace(0, 2*np.pi, 50)
            r = 1 + 0.5 * np.cos(4*t)
            x = r * np.cos(t + angle) * 0.8
            y = r * np.sin(t + angle) * 0.8
            self.ax.plot(x, y, 'k-', linewidth=1)
            
    def save_pattern(self, filename, pattern_type):
        """Save pattern as image"""
        if self.fig:
            plt.savefig(f"{filename}.png", dpi=300, bbox_inches='tight', 
                       facecolor='white', edgecolor='none')
            print(f"✅ Pattern saved as {filename}.png")
            
    def generate_multiple_patterns(self, count=5):
        """Generate multiple patterns"""
        patterns = []
        
        for i in range(count):
            # Clear plot
            self.ax.clear()
            self.ax.set_xlim(-5, 5)
            self.ax.set_ylim(-5, 5)
            self.ax.set_aspect('equal')
            self.ax.axis('off')
            
            # Choose random pattern type
            pattern_types = [
                ("fractal", self.generate_fractal_kolam),
                ("pulli", self.generate_pulli_kolam),
                ("sikku", self.generate_sikku_kolam),
                ("neli", self.generate_neli_kolam),
                ("kambi", self.generate_kambi_kolam),
                ("spiral", self.generate_spiral_pattern),
                ("flower", self.generate_flower_pattern),
                ("random", self.generate_random_pattern)
            ]
            
            pattern_type, pattern_func = random.choice(pattern_types)
            
            # Generate pattern
            pattern_func()
            
            # Save pattern
            filename = f"matplotlib_pattern_{i:03d}"
            self.save_pattern(filename, pattern_type)
            
            # Store pattern info
            pattern_info = {
                "pattern_id": f"matplotlib_{i:03d}",
                "pattern_type": pattern_type,
                "filename": f"{filename}.png",
                "complexity": random.uniform(0.3, 0.9),
                "symmetry": random.choice(["bilateral", "radial", "grid", "rotational", "asymmetric"]),
                "cultural_region": random.choice(["tamil_nadu", "karnataka", "kerala", "andhra_pradesh"])
            }
            
            patterns.append(pattern_info)
            
        return patterns
        
    def close(self):
        """Close matplotlib figure"""
        if self.fig:
            plt.close(self.fig)

def test_matplotlib_generator():
    """Test matplotlib pattern generator"""
    print("📊 Testing Matplotlib Pattern Generator...")
    
    generator = MatplotlibPatternGenerator()
    generator.setup_plot()
    
    # Generate single patterns
    print("\n--- Generating Fractal Kolam ---")
    generator.generate_fractal_kolam()
    generator.save_pattern("fractal_kolam", "fractal")
    
    print("\n--- Generating Pulli Kolam ---")
    generator.ax.clear()
    generator.ax.set_xlim(-5, 5)
    generator.ax.set_ylim(-5, 5)
    generator.ax.set_aspect('equal')
    generator.ax.axis('off')
    generator.generate_pulli_kolam()
    generator.save_pattern("pulli_kolam", "pulli")
    
    print("\n--- Generating Sikku Kolam ---")
    generator.ax.clear()
    generator.ax.set_xlim(-5, 5)
    generator.ax.set_ylim(-5, 5)
    generator.ax.set_aspect('equal')
    generator.ax.axis('off')
    generator.generate_sikku_kolam()
    generator.save_pattern("sikku_kolam", "sikku")
    
    # Generate multiple patterns
    print("\n--- Generating Multiple Patterns ---")
    patterns = generator.generate_multiple_patterns(5)
    
    # Save metadata
    with open("matplotlib_patterns_metadata.json", "w") as f:
        json.dump(patterns, f, indent=2)
    
    print(f"\n📊 Generated {len(patterns)} patterns:")
    for pattern in patterns:
        print(f"   {pattern['pattern_id']}: {pattern['pattern_type']} ({pattern['filename']})")
    
    generator.close()
    print("\n✅ Matplotlib pattern generation complete!")

if __name__ == "__main__":
    test_matplotlib_generator()















