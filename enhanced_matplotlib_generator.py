#!/usr/bin/env python3
"""
Enhanced Matplotlib Pattern Generator
======================================

Generate beautiful Kolam patterns using matplotlib with better visualization.
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

class EnhancedMatplotlibGenerator:
    """Generate beautiful Kolam patterns using matplotlib"""
    
    def __init__(self):
        self.fig = None
        self.ax = None
        
    def setup_plot(self, size=(12, 12), style='white'):
        """Setup matplotlib plot with style"""
        plt.style.use('default')
        self.fig, self.ax = plt.subplots(figsize=size)
        self.ax.set_xlim(-6, 6)
        self.ax.set_ylim(-6, 6)
        self.ax.set_aspect('equal')
        self.ax.axis('off')
        
        if style == 'white':
            self.ax.set_facecolor('white')
        elif style == 'black':
            self.ax.set_facecolor('black')
            
    def generate_enhanced_fractal_kolam(self, complexity=6):
        """Generate enhanced fractal Kolam pattern"""
        # Fractal pattern with multiple levels
        angles = np.linspace(0, 2*np.pi, complexity+1)
        colors = ['red', 'blue', 'green', 'purple', 'orange', 'brown']
        
        for level in range(3):
            for i, angle in enumerate(angles[:-1]):
                # Main line
                x1, y1 = 0, 0
                x2, y2 = (2-level*0.5) * np.cos(angle), (2-level*0.5) * np.sin(angle)
                self.ax.plot([x1, x2], [y1, y2], color=colors[i%len(colors)], 
                           linewidth=3-level, alpha=0.8)
                
                # Sub-lines
                mid_x, mid_y = x2/2, y2/2
                perp_angle = angle + np.pi/2
                x3 = mid_x + 0.3 * np.cos(perp_angle)
                y3 = mid_y + 0.3 * np.sin(perp_angle)
                x4 = mid_x - 0.3 * np.cos(perp_angle)
                y4 = mid_y - 0.3 * np.sin(perp_angle)
                self.ax.plot([x3, x4], [y3, y4], color=colors[i%len(colors)], 
                           linewidth=2-level, alpha=0.6)
                
    def generate_enhanced_pulli_kolam(self, dots=7):
        """Generate enhanced Pulli Kolam pattern"""
        # Draw dots with different sizes
        colors = ['red', 'blue', 'green', 'purple', 'orange']
        for i in range(dots):
            for j in range(dots):
                x = (i - dots//2) * 1.2
                y = (j - dots//2) * 1.2
                size = 0.15 + (i+j) * 0.02
                color = colors[(i+j) % len(colors)]
                circle = patches.Circle((x, y), size, color=color, alpha=0.8)
                self.ax.add_patch(circle)
        
        # Draw lines connecting dots
        for i in range(dots):
            for j in range(dots-1):
                x1 = (i - dots//2) * 1.2
                y1 = (j - dots//2) * 1.2
                x2 = (i - dots//2) * 1.2
                y2 = ((j+1) - dots//2) * 1.2
                self.ax.plot([x1, x2], [y1, y2], 'k-', linewidth=2, alpha=0.7)
                
    def generate_enhanced_sikku_kolam(self):
        """Generate enhanced Sikku Kolam pattern"""
        # Sikku pattern - continuous line with colors
        t = np.linspace(0, 6*np.pi, 200)
        x = np.cos(t) * (1 + 0.3*np.cos(7*t))
        y = np.sin(t) * (1 + 0.3*np.cos(7*t))
        
        # Color gradient
        colors = plt.cm.rainbow(np.linspace(0, 1, len(t)))
        for i in range(len(t)-1):
            self.ax.plot([x[i], x[i+1]], [y[i], y[i+1]], 
                        color=colors[i], linewidth=3, alpha=0.8)
        
    def generate_enhanced_neli_kolam(self):
        """Generate enhanced Neli Kolam pattern"""
        # Neli pattern - spiral with colors
        t = np.linspace(0, 8*np.pi, 300)
        r = t / (8*np.pi) * 3
        x = r * np.cos(t)
        y = r * np.sin(t)
        
        # Color gradient
        colors = plt.cm.viridis(np.linspace(0, 1, len(t)))
        for i in range(len(t)-1):
            self.ax.plot([x[i], x[i+1]], [y[i], y[i+1]], 
                        color=colors[i], linewidth=2, alpha=0.7)
        
    def generate_enhanced_kambi_kolam(self):
        """Generate enhanced Kambi Kolam pattern"""
        # Kambi pattern - grid-like with colors
        colors = ['red', 'blue', 'green', 'purple', 'orange']
        for i in range(5):
            for j in range(5):
                x = (i - 2) * 1.0
                y = (j - 2) * 1.0
                color = colors[(i+j) % len(colors)]
                circle = patches.Circle((x, y), 0.3, color=color, alpha=0.7)
                self.ax.add_patch(circle)
                
                # Add inner circle
                inner_circle = patches.Circle((x, y), 0.1, color='white', alpha=0.9)
                self.ax.add_patch(inner_circle)
                
    def generate_enhanced_spiral_pattern(self):
        """Generate enhanced spiral pattern"""
        t = np.linspace(0, 12*np.pi, 400)
        r = t / (12*np.pi) * 4
        x = r * np.cos(t)
        y = r * np.sin(t)
        
        # Color gradient
        colors = plt.cm.plasma(np.linspace(0, 1, len(t)))
        for i in range(len(t)-1):
            self.ax.plot([x[i], x[i+1]], [y[i], y[i+1]], 
                        color=colors[i], linewidth=2, alpha=0.8)
        
    def generate_enhanced_flower_pattern(self):
        """Generate enhanced flower pattern"""
        # Flower pattern with multiple petals
        colors = ['red', 'blue', 'green', 'purple', 'orange', 'brown', 'pink', 'cyan']
        for i in range(12):
            angle = i * np.pi / 6
            t = np.linspace(0, 2*np.pi, 100)
            r = 1 + 0.5 * np.cos(6*t)
            x = r * np.cos(t + angle) * 1.2
            y = r * np.sin(t + angle) * 1.2
            color = colors[i % len(colors)]
            self.ax.plot(x, y, color=color, linewidth=2, alpha=0.8)
            
    def generate_enhanced_mandala_pattern(self):
        """Generate enhanced mandala pattern"""
        # Mandala pattern
        colors = ['red', 'blue', 'green', 'purple', 'orange']
        for i in range(8):
            angle = i * np.pi / 4
            t = np.linspace(0, 2*np.pi, 100)
            r = 2 + 0.5 * np.cos(8*t)
            x = r * np.cos(t + angle) * 0.8
            y = r * np.sin(t + angle) * 0.8
            color = colors[i % len(colors)]
            self.ax.plot(x, y, color=color, linewidth=2, alpha=0.7)
            
    def generate_enhanced_lotus_pattern(self):
        """Generate enhanced lotus pattern"""
        # Lotus pattern
        colors = ['red', 'pink', 'purple', 'blue']
        for i in range(6):
            angle = i * np.pi / 3
            t = np.linspace(0, 2*np.pi, 100)
            r = 1 + 0.3 * np.cos(3*t)
            x = r * np.cos(t + angle) * 1.5
            y = r * np.sin(t + angle) * 1.5
            color = colors[i % len(colors)]
            self.ax.plot(x, y, color=color, linewidth=3, alpha=0.8)
            
    def save_pattern(self, filename, pattern_type):
        """Save pattern as high-quality image"""
        if self.fig:
            plt.savefig(f"{filename}.png", dpi=300, bbox_inches='tight', 
                       facecolor='white', edgecolor='none', pad_inches=0.1)
            print(f"✅ Enhanced pattern saved as {filename}.png")
            
    def generate_multiple_enhanced_patterns(self, count=8):
        """Generate multiple enhanced patterns"""
        patterns = []
        
        for i in range(count):
            # Clear plot
            self.ax.clear()
            self.ax.set_xlim(-6, 6)
            self.ax.set_ylim(-6, 6)
            self.ax.set_aspect('equal')
            self.ax.axis('off')
            self.ax.set_facecolor('white')
            
            # Choose random pattern type
            pattern_types = [
                ("fractal", self.generate_enhanced_fractal_kolam),
                ("pulli", self.generate_enhanced_pulli_kolam),
                ("sikku", self.generate_enhanced_sikku_kolam),
                ("neli", self.generate_enhanced_neli_kolam),
                ("kambi", self.generate_enhanced_kambi_kolam),
                ("spiral", self.generate_enhanced_spiral_pattern),
                ("flower", self.generate_enhanced_flower_pattern),
                ("mandala", self.generate_enhanced_mandala_pattern),
                ("lotus", self.generate_enhanced_lotus_pattern)
            ]
            
            pattern_type, pattern_func = random.choice(pattern_types)
            
            # Generate pattern
            pattern_func()
            
            # Save pattern
            filename = f"enhanced_pattern_{i:03d}"
            self.save_pattern(filename, pattern_type)
            
            # Store pattern info
            pattern_info = {
                "pattern_id": f"enhanced_{i:03d}",
                "pattern_type": pattern_type,
                "filename": f"{filename}.png",
                "complexity": random.uniform(0.4, 0.95),
                "symmetry": random.choice(["bilateral", "radial", "grid", "rotational", "asymmetric"]),
                "cultural_region": random.choice(["tamil_nadu", "karnataka", "kerala", "andhra_pradesh"]),
                "colors_used": random.randint(3, 8),
                "style": "enhanced_matplotlib"
            }
            
            patterns.append(pattern_info)
            
        return patterns
        
    def close(self):
        """Close matplotlib figure"""
        if self.fig:
            plt.close(self.fig)

def test_enhanced_generator():
    """Test enhanced matplotlib pattern generator"""
    print("🎨 Testing Enhanced Matplotlib Pattern Generator...")
    
    generator = EnhancedMatplotlibGenerator()
    generator.setup_plot()
    
    # Generate single patterns
    print("\n--- Generating Enhanced Fractal Kolam ---")
    generator.generate_enhanced_fractal_kolam()
    generator.save_pattern("enhanced_fractal_kolam", "fractal")
    
    print("\n--- Generating Enhanced Pulli Kolam ---")
    generator.ax.clear()
    generator.ax.set_xlim(-6, 6)
    generator.ax.set_ylim(-6, 6)
    generator.ax.set_aspect('equal')
    generator.ax.axis('off')
    generator.ax.set_facecolor('white')
    generator.generate_enhanced_pulli_kolam()
    generator.save_pattern("enhanced_pulli_kolam", "pulli")
    
    print("\n--- Generating Enhanced Sikku Kolam ---")
    generator.ax.clear()
    generator.ax.set_xlim(-6, 6)
    generator.ax.set_ylim(-6, 6)
    generator.ax.set_aspect('equal')
    generator.ax.axis('off')
    generator.ax.set_facecolor('white')
    generator.generate_enhanced_sikku_kolam()
    generator.save_pattern("enhanced_sikku_kolam", "sikku")
    
    # Generate multiple patterns
    print("\n--- Generating Multiple Enhanced Patterns ---")
    patterns = generator.generate_multiple_enhanced_patterns(6)
    
    # Save metadata
    with open("enhanced_patterns_metadata.json", "w") as f:
        json.dump(patterns, f, indent=2)
    
    print(f"\n📊 Generated {len(patterns)} enhanced patterns:")
    for pattern in patterns:
        print(f"   {pattern['pattern_id']}: {pattern['pattern_type']} ({pattern['filename']})")
    
    generator.close()
    print("\n✅ Enhanced pattern generation complete!")

if __name__ == "__main__":
    test_enhanced_generator()















