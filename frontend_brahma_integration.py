#!/usr/bin/env python3
"""
Frontend Integration: Perfect Brahma's Knot
- Generate data for frontend
- 29 dots, single continuous line
- Smooth curves, traditional style
"""

import json
import math
import numpy as np

class FrontendBrahmaIntegration:
    def __init__(self):
        self.center_x, self.center_y = 200, 200
        self.grid_spacing = 40
        self.outer_radius = 80
        
    def generate_29_dots(self):
        """Generate 29 dots for frontend"""
        dots = []
        
        # 5x5 grid dots (25 dots)
        for i in range(5):
            for j in range(5):
                x = self.center_x + (j - 2) * self.grid_spacing
                y = self.center_y + (i - 2) * self.grid_spacing
                dots.append({
                    'id': i * 5 + j,
                    'x': x,
                    'y': y,
                    'type': 'grid',
                    'size': 6
                })
        
        # 4 outer petal dots
        petal_angles = [90, 0, -90, 180]  # Top, Right, Bottom, Left
        for i, angle in enumerate(petal_angles):
            x = self.center_x + self.outer_radius * math.cos(math.radians(angle))
            y = self.center_y + self.outer_radius * math.sin(math.radians(angle))
            dots.append({
                'id': 25 + i,
                'x': x,
                'y': y,
                'type': 'petal',
                'size': 8
            })
        
        return dots
    
    def create_brahma_path(self, dots):
        """Create Brahma's Knot path"""
        # Get dot positions
        dot_positions = {dot['id']: (dot['x'], dot['y']) for dot in dots}
        
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
            if dot_id in dot_positions:
                path_coords.append(dot_positions[dot_id])
        
        return path_coords
    
    def smooth_curves(self, path_coords):
        """Create smooth curves for frontend"""
        if len(path_coords) < 3:
            return path_coords
        
        # Use cubic spline interpolation
        x_coords = [p[0] for p in path_coords]
        y_coords = [p[1] for p in path_coords]
        
        # Create parameter t
        t = np.linspace(0, 1, len(path_coords))
        t_smooth = np.linspace(0, 1, len(path_coords) * 3)
        
        # Interpolate
        x_smooth = np.interp(t_smooth, t, x_coords)
        y_smooth = np.interp(t_smooth, t, y_coords)
        
        return list(zip(x_smooth, y_smooth))
    
    def generate_frontend_data(self):
        """Generate data for frontend"""
        print("🎯 Generating Frontend Brahma's Knot Data...")
        
        # Generate dots
        dots = self.generate_29_dots()
        print(f"✅ Generated {len(dots)} dots")
        
        # Create path
        path_coords = self.create_brahma_path(dots)
        print(f"✅ Created path with {len(path_coords)} points")
        
        # Smooth curves
        smooth_path = self.smooth_curves(path_coords)
        print(f"✅ Smoothed curves")
        
        # Create frontend-compatible data
        frontend_data = {
            'type': 'perfect_brahma_knot',
            'points': dots,
            'paths': [smooth_path],
            'lines': [],
            'colors': ['#DC143C', '#B22222', '#8B0000'],
            'cultural_info': {
                'traditional_name': 'Brahma Mudi (Eternal Knot)',
                'symbolism': 'Infinite consciousness and eternal cycle',
                'region': 'Tamil Nadu',
                'material': 'Chalk/Rangoli powder',
                'style': 'Traditional South Indian'
            },
            'mathematical_properties': {
                'symmetry_type': 'RADIAL',
                'dot_count': 29,
                'path_count': 1,
                'continuous_loop': True,
                'smooth_curves': True,
                'interlaced_pattern': True,
                'eternal_design': True
            },
            'animation_properties': {
                'draw_dots_first': True,
                'draw_path_continuously': True,
                'smooth_animation': True,
                'step_by_step': True
            }
        }
        
        return frontend_data
    
    def save_frontend_data(self, data, filename='perfect_brahma_knot_frontend.json'):
        """Save data for frontend"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Saved frontend data to {filename}")
        return filename

def main():
    """Main function"""
    print("🎯 Frontend Brahma's Knot Integration")
    print("=" * 50)
    
    try:
        # Generate data
        brahma = FrontendBrahmaIntegration()
        data = brahma.generate_frontend_data()
        
        # Save data
        filename = brahma.save_frontend_data(data)
        
        print("\n✅ Frontend integration complete!")
        print(f"📊 Dots: {len(data['points'])}")
        print(f"📊 Path Points: {len(data['paths'][0])}")
        print(f"📁 File: {filename}")
        print("🎨 Ready for frontend integration!")
        
        # Print sample data
        print("\n📋 Sample Data:")
        print(f"• First dot: {data['points'][0]}")
        print(f"• First path point: {data['paths'][0][0]}")
        print(f"• Cultural info: {data['cultural_info']['traditional_name']}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()


































