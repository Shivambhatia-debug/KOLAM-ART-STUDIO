#!/usr/bin/env python3
"""
Demo Kolam Image Generator
=========================

Creates a simple demo Kolam image for testing the diffusion API.
"""

import numpy as np
from PIL import Image, ImageDraw
import math

def create_demo_kolam(size=512):
    """Create a simple demo Kolam pattern"""
    # Create white background
    img = Image.new('RGB', (size, size), 'white')
    draw = ImageDraw.Draw(img)
    
    center = size // 2
    radius = size // 3
    
    # Draw a simple radial pattern
    for i in range(8):
        angle = i * math.pi / 4
        x1 = center + radius * math.cos(angle)
        y1 = center + radius * math.sin(angle)
        x2 = center + (radius * 0.5) * math.cos(angle)
        y2 = center + (radius * 0.5) * math.sin(angle)
        
        # Draw lines
        draw.line([(center, center), (x1, y1)], fill='black', width=3)
        draw.line([(center, center), (x2, y2)], fill='black', width=2)
    
    # Draw circles
    for r in [radius * 0.3, radius * 0.6, radius * 0.9]:
        draw.ellipse([center-r, center-r, center+r, center+r], outline='black', width=2)
    
    # Add some dots
    for i in range(12):
        angle = i * math.pi / 6
        x = center + (radius * 0.8) * math.cos(angle)
        y = center + (radius * 0.8) * math.sin(angle)
        draw.ellipse([x-3, y-3, x+3, y+3], fill='black')
    
    return img

def main():
    """Create and save demo Kolam"""
    print("🎨 Creating demo Kolam image...")
    
    # Create demo image
    demo_img = create_demo_kolam(512)
    
    # Save it
    demo_img.save("demo_kolam.png", "PNG")
    print("✅ Demo Kolam saved as 'demo_kolam.png'")
    
    # Show some info
    print(f"📏 Image size: {demo_img.size}")
    print(f"🎨 Image mode: {demo_img.mode}")
    print("\n💡 You can now use this image to test the diffusion API!")

if __name__ == "__main__":
    main()












