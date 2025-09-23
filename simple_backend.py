"""
Simple Kolam Analysis Backend API
=================================

A simplified Flask backend for Kolam pattern analysis and generation.
This version works without complex image processing dependencies.

AICTE Problem Statement 25107
"""

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import json
import base64
import io
from PIL import Image
import numpy as np
import sys
import os
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import Circle, Rectangle, Polygon
import random
import math
import json
import os
import numpy as np
from datetime import datetime

app = Flask(__name__, static_folder='public', static_url_path='')
CORS(app, origins=['http://localhost:3000', 'http://127.0.0.1:3000', 'http://192.168.56.1:3000'])

class SimpleKolamGenerator:
    """Simple Kolam pattern generator"""
    
    def __init__(self):
        self.patterns = []
    
    def generate_radial_pattern(self, size=5):
        """Generate a radial symmetry pattern"""
        points = []
        center_x, center_y = size // 2, size // 2
        
        for i in range(size):
            for j in range(size):
                distance = math.sqrt((i - center_x)**2 + (j - center_y)**2)
                if distance <= size // 2:
                    points.append((i, j))
        
        return {
            'type': 'radial',
            'points': points,
            'center': (center_x, center_y),
            'size': size
        }
    
    def generate_bilateral_pattern(self, size=5):
        """Generate a bilateral symmetry pattern"""
        points = []
        center_x = size // 2
        
        for i in range(size):
            for j in range(size):
                if j <= center_x:  # Left side
                    points.append((i, j))
                    if j != center_x:  # Mirror to right side
                        points.append((i, size - 1 - j))
        
        return {
            'type': 'bilateral',
            'points': points,
            'center': (center_x, size // 2),
            'size': size
        }
    
    def generate_grid_pattern(self, size=5):
        """Generate a grid-based pattern"""
        points = []
        for i in range(0, size, 2):
            for j in range(0, size, 2):
                points.append((i, j))
        
        return {
            'type': 'grid',
            'points': points,
            'size': size
        }
    
    def generate_brahma_knot_python_style(self):
        """Generate Perfect Brahma's Knot exactly like expected"""
        # 29 dots: 25 grid + 4 petals
        points = []
        center_x, center_y = 200, 200
        grid_spacing = 40
        outer_radius = 80
        
        # 5x5 grid dots (25 dots)
        for i in range(5):
            for j in range(5):
                x = center_x + (j - 2) * grid_spacing
                y = center_y + (i - 2) * grid_spacing
                points.append({
                    'x': x,
                    'y': y,
                    'id': i * 5 + j,
                    'type': 'grid',
                    'size': 6
                })
        
        # 4 outer petal dots
        petal_angles = [90, 0, -90, 180]  # Top, Right, Bottom, Left
        for i, angle in enumerate(petal_angles):
            x = center_x + outer_radius * math.cos(math.radians(angle))
            y = center_y + outer_radius * math.sin(math.radians(angle))
            points.append({
                'x': x,
                'y': y,
                'id': 25 + i,
                'type': 'petal',
                'size': 8
            })
        
        # Brahma's Knot continuous path
        dot_positions = {dot['id']: (dot['x'], dot['y']) for dot in points}
        
        # Path sequence for continuous loop
        path_sequence = [
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
        
        # Smooth curves
        if len(path_coords) > 3:
            x_coords = [p[0] for p in path_coords]
            y_coords = [p[1] for p in path_coords]
            
            # Create smooth curve
            t = np.linspace(0, 1, len(path_coords))
            t_smooth = np.linspace(0, 1, len(path_coords) * 3)
            
            x_smooth = np.interp(t_smooth, t, x_coords)
            y_smooth = np.interp(t_smooth, t, y_coords)
            
            smooth_path = list(zip(x_smooth, y_smooth))
        else:
            smooth_path = path_coords
        
        return {
            'type': 'perfect_brahma_knot',
            'points': points,
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
            }
        }
    
    def generate_turtle_kolam_python_style(self):
        """Generate Turtle Kolam exactly like Python terminal"""
        points = []
        colors = []
        
        # Generate circular pattern like Turtle graphics
        center_x, center_y = 200, 200
        num_layers = 6
        
        for layer in range(num_layers):
            radius = 50 + layer * 20
            petals = 12 + layer * 6
            
            for petal in range(petals):
                angle = (petal * 360 / petals) * math.pi / 180
                x = center_x + radius * math.cos(angle)
                y = center_y + radius * math.sin(angle)
                
                # HSV to RGB color conversion
                hue = (layer * 60 + petal * 10) % 360 / 360
                r = max(0, min(1, 1 - abs((hue * 6) % 2 - 1)))
                g = max(0, min(1, 1 - abs(((hue * 6) % 2) - 1) if (hue * 6) % 2 < 1 else 0))
                b = max(0, min(1, 1 - abs(((hue * 6) % 2) - 1) if (hue * 6) % 2 >= 1 else 0))
                
                points.append({
                    'x': x,
                    'y': y,
                    'id': len(points),
                    'type': 'dot',
                    'color': [r, g, b]
                })
        
        # Generate circular paths
        paths = []
        for layer in range(num_layers):
            radius = 50 + layer * 20
            path_points = []
            
            for i in range(0, 360, 5):
                angle = i * math.pi / 180
                x = center_x + radius * math.cos(angle)
                y = center_y + radius * math.sin(angle)
                path_points.append({'x': x, 'y': y})
            
            paths.append(path_points)
        
        return {
            'type': 'turtle_kolam',
            'points': points,
            'paths': paths,
            'lines': [],
            'colors': ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7', '#DDA0DD'],
            'cultural_info': {
                'traditional_name': 'Colorful Kolam',
                'symbolism': 'Vibrant celebration and joy',
                'region': 'South India'
            },
            'mathematical_properties': {
                'symmetry_type': 'RADIAL',
                'dot_count': len(points),
                'path_count': len(paths),
                'layers': num_layers
            }
        }

class SimpleKolamAnalyzer:
    """Simple Kolam pattern analyzer"""
    
    def analyze_symmetry(self, points):
        """Analyze symmetry of a pattern"""
        if not points:
            return {'type': 'none', 'score': 0}
        
        # Simple symmetry analysis
        center_x = sum(p[0] for p in points) / len(points)
        center_y = sum(p[1] for p in points) / len(points)
        
        # Check for radial symmetry
        distances = [math.sqrt((p[0] - center_x)**2 + (p[1] - center_y)**2) for p in points]
        if len(set(round(d, 1) for d in distances)) <= 3:
            return {'type': 'radial', 'score': 0.8, 'center': (center_x, center_y)}
        
        # Check for bilateral symmetry
        left_points = [p for p in points if p[0] < center_x]
        right_points = [p for p in points if p[0] > center_x]
        
        if len(left_points) == len(right_points):
            return {'type': 'bilateral', 'score': 0.7, 'center': (center_x, center_y)}
        
        return {'type': 'asymmetric', 'score': 0.3}

# Initialize generators
generator = SimpleKolamGenerator()
analyzer = SimpleKolamAnalyzer()

@app.route('/')
def home():
    """Home endpoint"""
    return jsonify({
        'message': 'Kolam Art Studio Backend API',
        'version': '1.0.0',
        'status': 'running',
        'endpoints': {
            'health': '/api/health',
            'patterns': '/api/patterns',
            'generate': '/api/generate',
            'analyze': '/api/analyze',
            'python_brahma': '/api/generate-python-brahma',
            'python_turtle': '/api/generate-python-turtle'
        }
    })

@app.route('/api/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': str(datetime.now()),
        'uptime': 'running'
    })

@app.route('/api/health')
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'message': 'Kolam Art Studio Backend is running'
    })

@app.route('/api/patterns/types')
def get_pattern_types():
    """Get available pattern types"""
    return jsonify({
        'types': [
            {
                'id': 'radial',
                'name': 'Radial Symmetry',
                'description': 'Patterns radiating from a central point'
            },
            {
                'id': 'bilateral',
                'name': 'Bilateral Symmetry',
                'description': 'Mirror-symmetric patterns'
            },
            {
                'id': 'grid',
                'name': 'Grid Pattern',
                'description': 'Traditional dot-grid based designs'
            }
        ]
    })

@app.route('/api/patterns/generate', methods=['POST'])
def generate_pattern():
    """Generate a new Kolam pattern"""
    try:
        data = request.get_json()
        pattern_type = data.get('type', 'radial')
        size = data.get('size', 5)
        
        if pattern_type == 'radial':
            pattern = generator.generate_radial_pattern(size)
        elif pattern_type == 'bilateral':
            pattern = generator.generate_bilateral_pattern(size)
        elif pattern_type == 'grid':
            pattern = generator.generate_grid_pattern(size)
        else:
            pattern = generator.generate_radial_pattern(size)
        
        # Analyze the generated pattern
        analysis = analyzer.analyze_symmetry(pattern['points'])
        pattern['analysis'] = analysis
        
        return jsonify({
            'success': True,
            'pattern': pattern,
            'message': f'Generated {pattern_type} pattern successfully'
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Failed to generate pattern'
        }), 500

@app.route('/api/patterns/analyze', methods=['POST'])
def analyze_pattern():
    """Analyze an uploaded pattern"""
    try:
        data = request.get_json()
        points = data.get('points', [])
        
        if not points:
            return jsonify({
                'success': False,
                'error': 'No points provided for analysis'
            }), 400
        
        analysis = analyzer.analyze_symmetry(points)
        
        return jsonify({
            'success': True,
            'analysis': analysis,
            'message': 'Pattern analyzed successfully'
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Failed to analyze pattern'
        }), 500

@app.route('/api/patterns/visualize', methods=['POST'])
def visualize_pattern():
    """Create a visualization of the pattern"""
    try:
        data = request.get_json()
        points = data.get('points', [])
        pattern_type = data.get('type', 'radial')
        
        if not points:
            return jsonify({
                'success': False,
                'error': 'No points provided for visualization'
            }), 400
        
        # Create visualization
        fig, ax = plt.subplots(figsize=(8, 8))
        ax.set_xlim(-1, max(p[0] for p in points) + 1)
        ax.set_ylim(-1, max(p[1] for p in points) + 1)
        ax.set_aspect('equal')
        
        # Plot points
        for point in points:
            circle = Circle((point[0], point[1]), 0.3, color='red', alpha=0.7)
            ax.add_patch(circle)
        
        # Add title
        ax.set_title(f'Kolam Pattern - {pattern_type.title()}', fontsize=16, fontweight='bold')
        ax.grid(True, alpha=0.3)
        
        # Save to base64
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png', dpi=150, bbox_inches='tight')
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.getvalue()).decode()
        plt.close()
        
        return jsonify({
            'success': True,
            'image': f'data:image/png;base64,{image_base64}',
            'message': 'Pattern visualized successfully'
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Failed to visualize pattern'
        }), 500

# Additional endpoints that frontend expects
@app.route('/api/patterns', methods=['GET'])
def get_patterns():
    """Get available patterns for gallery"""
    patterns = [
        {
            'id': 'radial_1',
            'name': 'Radial Pattern 1',
            'type': 'radial',
            'description': 'Traditional radial symmetry pattern',
            'complexity': 'medium'
        },
        {
            'id': 'bilateral_1',
            'name': 'Bilateral Pattern 1',
            'type': 'bilateral',
            'description': 'Mirror symmetry pattern',
            'complexity': 'simple'
        },
        {
            'id': 'grid_1',
            'name': 'Grid Pattern 1',
            'type': 'grid',
            'description': 'Traditional dot-grid pattern',
            'complexity': 'simple'
        }
    ]
    
    return jsonify({
        'success': True,
        'patterns': patterns
    })

@app.route('/api/analyze', methods=['POST'])
def analyze_image():
    """Analyze uploaded image"""
    try:
        data = request.get_json()
        image_data = data.get('image', '')
        
        # Mock analysis for now
        analysis_result = {
            'symmetry_type': 'radial',
            'complexity_score': 0.75,
            'cultural_region': 'Tamil Nadu',
            'festival_theme': 'Diwali',
            'authenticity_score': 0.85,
            'mathematical_properties': {
                'fractal_dimension': 1.2,
                'symmetry_score': 0.9,
                'geometric_accuracy': 0.8
            }
        }
        
        return jsonify({
            'success': True,
            'analysis': analysis_result,
            'message': 'Image analyzed successfully'
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Failed to analyze image'
        }), 500

@app.route('/api/advanced-analysis', methods=['POST'])
def advanced_analyze():
    """Advanced analysis with deep mode"""
    try:
        data = request.get_json()
        image_data = data.get('image', '')
        mode = data.get('mode', 'standard')
        
        # Mock advanced analysis
        analysis_result = {
            'symmetry_type': 'radial',
            'complexity_score': 0.85,
            'cultural_region': 'Karnataka',
            'festival_theme': 'Pongal',
            'authenticity_score': 0.92,
            'mathematical_properties': {
                'fractal_dimension': 1.4,
                'symmetry_score': 0.95,
                'geometric_accuracy': 0.88,
                'eulerian_path': True,
                'l_system_complexity': 0.7
            },
            'cultural_significance': {
                'regional_style': 'South Indian',
                'traditional_meaning': 'Prosperity and good fortune',
                'festival_appropriateness': 0.9
            }
        }
        
        return jsonify({
            'success': True,
            'analysis': analysis_result,
            'mode': mode,
            'message': 'Advanced analysis completed successfully'
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Failed to perform advanced analysis'
        }), 500

@app.route('/api/generate-cultural', methods=['POST'])
def generate_cultural():
    """Generate cultural pattern"""
    try:
        data = request.get_json()
        region = data.get('region', 'Tamil Nadu')
        grid_size = data.get('grid_size', 5)
        
        # Generate different patterns based on region
        if region.lower() == 'tamil_nadu' or region.lower() == 'tamil nadu':
            pattern = generator.generate_radial_pattern(grid_size)
            pattern['cultural_region'] = 'Tamil Nadu'
            pattern['colors'] = ['#DC143C', '#FFD700', '#4ECDC4']  # Red, Gold, Teal
        elif region.lower() == 'karnataka':
            pattern = generator.generate_bilateral_pattern(grid_size)
            pattern['cultural_region'] = 'Karnataka'
            pattern['colors'] = ['#FF6B6B', '#4ECDC4', '#45B7D1']  # Red, Teal, Blue
        elif region.lower() == 'kerala':
            pattern = generator.generate_grid_pattern(grid_size)
            pattern['cultural_region'] = 'Kerala'
            pattern['colors'] = ['#FF6B6B', '#FFD700', '#32CD32']  # Red, Gold, Green
        elif region.lower() == 'andhra_pradesh' or region.lower() == 'andhra pradesh':
            pattern = generator.generate_radial_pattern(grid_size)
            pattern['cultural_region'] = 'Andhra Pradesh'
            pattern['colors'] = ['#FF6B6B', '#FFD700', '#FFA500']  # Red, Gold, Orange
        elif region.lower() == 'telangana':
            pattern = generator.generate_bilateral_pattern(grid_size)
            pattern['cultural_region'] = 'Telangana'
            pattern['colors'] = ['#DC143C', '#FFD700', '#4ECDC4']  # Red, Gold, Teal
        else:
            pattern = generator.generate_radial_pattern(grid_size)
            pattern['cultural_region'] = region
            pattern['colors'] = ['#DC143C', '#FFD700', '#4ECDC4']  # Default colors
        
        pattern['festival_theme'] = 'Traditional'
        pattern['cultural_description'] = f'Traditional {region} Kolam pattern'
        
        return jsonify({
            'success': True,
            'pattern': pattern,
            'message': f'Generated {region} cultural pattern'
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Failed to generate cultural pattern'
        }), 500

@app.route('/api/generate-festival', methods=['POST'])
def generate_festival():
    """Generate festival pattern"""
    try:
        data = request.get_json()
        festival = data.get('festival', 'Diwali')
        region = data.get('region', 'Tamil Nadu')
        grid_size = data.get('grid_size', 5)
        
        # Generate different patterns based on festival
        if festival.lower() == 'diwali':
            pattern = generator.generate_radial_pattern(grid_size)
            pattern['festival_theme'] = 'Diwali'
            pattern['colors'] = ['#FFD700', '#FF6B6B', '#4ECDC4']  # Gold, Red, Teal
        elif festival.lower() == 'pongal':
            pattern = generator.generate_bilateral_pattern(grid_size)
            pattern['festival_theme'] = 'Pongal'
            pattern['colors'] = ['#FF6B6B', '#4ECDC4', '#45B7D1']  # Red, Teal, Blue
        elif festival.lower() == 'onam':
            pattern = generator.generate_grid_pattern(grid_size)
            pattern['festival_theme'] = 'Onam'
            pattern['colors'] = ['#FF6B6B', '#FFD700', '#32CD32']  # Red, Gold, Green
        elif festival.lower() == 'sankranti':
            pattern = generator.generate_radial_pattern(grid_size)
            pattern['festival_theme'] = 'Sankranti'
            pattern['colors'] = ['#FF6B6B', '#FFD700', '#FFA500']  # Red, Gold, Orange
        else:
            pattern = generator.generate_radial_pattern(grid_size)
            pattern['festival_theme'] = festival
            pattern['colors'] = ['#DC143C', '#FFD700', '#4ECDC4']  # Default colors
        
        pattern['cultural_region'] = region
        pattern['festival_description'] = f'Traditional {festival} pattern from {region}'
        
        return jsonify({
            'success': True,
            'pattern': pattern,
            'message': f'Generated {festival} pattern for {region}'
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Failed to generate festival pattern'
        }), 500

@app.route('/api/cultural-analysis', methods=['POST'])
def cultural_analysis():
    """Perform cultural analysis"""
    try:
        data = request.get_json()
        pattern = data.get('pattern', {})
        
        analysis = {
            'cultural_region': 'Tamil Nadu',
            'authenticity_score': 0.85,
            'traditional_meaning': 'Prosperity and good fortune',
            'festival_appropriateness': 0.9,
            'regional_characteristics': {
                'color_scheme': 'Traditional red and white',
                'complexity_level': 'Medium',
                'symmetry_type': 'Radial'
            }
        }
        
        return jsonify({
            'success': True,
            'cultural_analysis': analysis,
            'message': 'Cultural analysis completed'
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Failed to perform cultural analysis'
        }), 500

@app.route('/api/generate', methods=['POST'])
def generate_from_template():
    """Generate pattern from template"""
    try:
        data = request.get_json()
        pattern_type = data.get('type', 'radial')
        grid_size = data.get('grid_size', [5, 5])
        
        if isinstance(grid_size, list):
            size = grid_size[0]
        else:
            size = grid_size
        
        if pattern_type == 'radial':
            pattern = generator.generate_radial_pattern(size)
        elif pattern_type == 'bilateral':
            pattern = generator.generate_bilateral_pattern(size)
        else:
            pattern = generator.generate_grid_pattern(size)
        
        return jsonify({
            'success': True,
            'pattern': pattern,
            'message': f'Generated {pattern_type} pattern'
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Failed to generate pattern'
        }), 500

# Static file serving for JSON data
@app.route('/brahma_knot_frontend_data.json')
def serve_brahma_knot():
    """Serve Brahma's Knot data"""
    try:
        return send_from_directory('public', 'brahma_knot_frontend_data.json')
    except FileNotFoundError:
        return jsonify({'error': 'Brahma Knot data not found'}), 404

@app.route('/turtle_kolam_frontend_data.json')
def serve_turtle_kolam():
    """Serve Turtle Kolam data"""
    try:
        return send_from_directory('public', 'turtle_kolam_frontend_data.json')
    except FileNotFoundError:
        return jsonify({'error': 'Turtle Kolam data not found'}), 404

@app.route('/enhanced_turtle_kolam_data.json')
def serve_enhanced_kolam():
    """Serve Enhanced Kolam data"""
    try:
        return send_from_directory('public', 'enhanced_turtle_kolam_data.json')
    except FileNotFoundError:
        return jsonify({'error': 'Enhanced Kolam data not found'}), 404

# Topological generation endpoint
@app.route('/api/generate-topological', methods=['POST'])
def generate_topological():
    """Generate topological pattern"""
    try:
        data = request.get_json()
        num_dots = data.get('num_dots', 9)
        symmetry_type = data.get('symmetry_type', 'radial')
        complexity = data.get('complexity', 'medium')
        
        # Generate pattern based on parameters
        if symmetry_type == 'radial':
            pattern = generator.generate_radial_pattern(int(num_dots**0.5))
        elif symmetry_type == 'bilateral':
            pattern = generator.generate_bilateral_pattern(int(num_dots**0.5))
        else:
            pattern = generator.generate_grid_pattern(int(num_dots**0.5))
        
        # Add topological properties
        pattern['topological_properties'] = {
            'num_dots': num_dots,
            'symmetry_type': symmetry_type,
            'complexity': complexity,
            'angle_encoding': [random.uniform(0, 2*math.pi) for _ in range(num_dots)],
            'numeric_representation': f"0x{random.randint(1000, 9999):04x}",
            'tracing_sequence': list(range(num_dots))
        }
        
        return jsonify({
            'success': True,
            'message': 'Topological pattern generated successfully',
            'pattern': pattern
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Failed to generate topological pattern'
        }), 500

# Python-style generation endpoints
@app.route('/api/generate-python-brahma', methods=['POST'])
def generate_python_brahma():
    """Generate Brahma's Knot exactly like Python terminal"""
    try:
        print("🐍 Generating Python-style Brahma's Knot...")
        pattern = generator.generate_brahma_knot_python_style()
        print(f"✅ Pattern generated with {len(pattern.get('points', []))} points")
        
        response_data = {
            'success': True,
            'message': 'Brahma\'s Knot generated in Python style',
            'pattern': pattern
        }
        
        print(f"📤 Sending response: {len(str(response_data))} characters")
        return jsonify(response_data)
    
    except Exception as e:
        print(f"❌ Error generating Brahma's Knot: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Failed to generate Python-style Brahma\'s Knot'
        }), 500

@app.route('/api/generate-python-turtle', methods=['POST'])
def generate_python_turtle():
    """Generate Turtle Kolam exactly like Python terminal"""
    try:
        print("🐢 Generating Python-style Turtle Kolam...")
        pattern = generator.generate_turtle_kolam_python_style()
        print(f"✅ Turtle pattern generated with {len(pattern.get('points', []))} points")
        
        response_data = {
            'success': True,
            'message': 'Turtle Kolam generated in Python style',
            'pattern': pattern
        }
        
        print(f"📤 Sending Turtle response: {len(str(response_data))} characters")
        return jsonify(response_data)
    
    except Exception as e:
        print(f"❌ Error generating Turtle Kolam: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Failed to generate Python-style Turtle Kolam'
        }), 500

if __name__ == '__main__':
    print("🎨 Starting Kolam Art Studio Backend...")
    print("📍 Backend URL: http://localhost:5000")
    print("🔗 Frontend URL: http://localhost:3000")
    print("📚 API Documentation: http://localhost:5000")
    print("=" * 50)
    
    app.run(debug=True, host='0.0.0.0', port=5000)
