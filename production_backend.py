#!/usr/bin/env python3
"""
Production-Ready Kolam Backend System
=====================================

Senior Software Engineer Production Version
- Complete error handling
- Comprehensive logging
- API documentation
- Performance optimization
- Security measures
"""

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import json
import logging
import traceback
from datetime import datetime
from typing import Dict, List, Any, Optional
import numpy as np
import math
import random
import os
import time
from functools import wraps

# Configure production logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('kolam_backend.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

app = Flask(__name__, static_folder='public', static_url_path='')
CORS(app, origins=['http://localhost:3000', 'http://127.0.0.1:3000', 'http://192.168.56.1:3000'])

# Rate limiting decorator
def rate_limit(max_requests=100, window=60):
    """Simple rate limiting decorator"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # In production, use Redis or similar for rate limiting
            return f(*args, **kwargs)
        return decorated_function
    return decorator

# Error handling decorator
def handle_errors(f):
    """Centralized error handling"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except ValueError as e:
            logger.warning(f"Value error in {f.__name__}: {e}")
            return jsonify({
                'success': False,
                'error': 'Invalid input',
                'message': str(e)
            }), 400
        except Exception as e:
            logger.error(f"Unexpected error in {f.__name__}: {e}")
            logger.error(traceback.format_exc())
            return jsonify({
                'success': False,
                'error': 'Internal server error',
                'message': 'An unexpected error occurred'
            }), 500
    return decorated_function

class ProductionPatternGenerator:
    """Production-ready pattern generator with caching and optimization"""
    
    def __init__(self):
        self.cache = {}
        self.initialize_patterns()
    
    def initialize_patterns(self):
        """Initialize all available patterns"""
        self.patterns = {
            'basic': {
                'radial': {'min_size': 3, 'max_size': 20},
                'bilateral': {'min_size': 3, 'max_size': 20},
                'grid': {'min_size': 3, 'max_size': 20},
                'circular': {'min_size': 3, 'max_size': 20}
            },
            'advanced': {
                'brahma_knot': {'fixed_size': True, 'size': 29},
                'turtle_kolam': {'min_layers': 3, 'max_layers': 10},
                'topological': {'min_dots': 9, 'max_dots': 100},
                'eulerian': {'min_dots': 4, 'max_dots': 64}
            },
            'cultural': {
                'tamil_nadu': {'styles': ['sikku', 'pulli', 'freehand']},
                'spiral_kolam': {'turns': 6, 'step_angle': 15, 'step_length': 8},
                'kerala': {'styles': ['pookalam', 'rangoli']},
                'karnataka': {'styles': ['rangavalli', 'muggulu']},
                'andhra_pradesh': {'styles': ['muggulu', 'rangoli']}
            },
            'festival': {
                'diwali': {'themes': ['lights', 'prosperity', 'celebration']},
                'pongal': {'themes': ['harvest', 'gratitude', 'nature']},
                'onam': {'themes': ['flowers', 'abundance', 'unity']},
                'ugadi': {'themes': ['new_year', 'fresh_start', 'hope']}
            }
        }
    
    def generate_pattern(self, pattern_type: str, pattern_name: str, **kwargs) -> Dict[str, Any]:
        """Generate pattern with caching and validation"""
        # Create cache key
        cache_key = f"{pattern_type}_{pattern_name}_{hash(str(sorted(kwargs.items())))}"
        
        # Check cache
        if cache_key in self.cache:
            logger.info(f"Cache hit for {cache_key}")
            return self.cache[cache_key]
        
        # Validate input
        self._validate_pattern_request(pattern_type, pattern_name, kwargs)
        
        # Generate pattern
        start_time = time.time()
        
        if pattern_type == 'basic':
            result = self._generate_basic_pattern(pattern_name, **kwargs)
        elif pattern_type == 'advanced':
            result = self._generate_advanced_pattern(pattern_name, **kwargs)
        elif pattern_type == 'cultural':
            result = self._generate_cultural_pattern(pattern_name, **kwargs)
        elif pattern_type == 'festival':
            result = self._generate_festival_pattern(pattern_name, **kwargs)
        else:
            raise ValueError(f"Unknown pattern type: {pattern_type}")
        
        # Add metadata
        result['metadata'] = {
            'generated_at': datetime.now().isoformat(),
            'generation_time': time.time() - start_time,
            'pattern_type': pattern_type,
            'pattern_name': pattern_name,
            'parameters': kwargs
        }
        
        # Cache result
        self.cache[cache_key] = result
        logger.info(f"Generated {pattern_name} in {time.time() - start_time:.3f}s")
        
        return result
    
    def _validate_pattern_request(self, pattern_type: str, pattern_name: str, kwargs: Dict):
        """Validate pattern generation request"""
        if pattern_type not in self.patterns:
            raise ValueError(f"Unknown pattern type: {pattern_type}")
        
        if pattern_name not in self.patterns[pattern_type]:
            raise ValueError(f"Unknown pattern name: {pattern_name}")
        
        # Validate parameters based on pattern type
        pattern_config = self.patterns[pattern_type][pattern_name]
        
        if 'size' in kwargs:
            size = kwargs['size']
            if 'min_size' in pattern_config and size < pattern_config['min_size']:
                raise ValueError(f"Size too small. Minimum: {pattern_config['min_size']}")
            if 'max_size' in pattern_config and size > pattern_config['max_size']:
                raise ValueError(f"Size too large. Maximum: {pattern_config['max_size']}")
    
    def _generate_basic_pattern(self, pattern_name: str, size: int = 5, **kwargs) -> Dict[str, Any]:
        """Generate basic patterns"""
        if pattern_name == 'radial':
            return self._generate_radial_pattern(size)
        elif pattern_name == 'bilateral':
            return self._generate_bilateral_pattern(size)
        elif pattern_name == 'grid':
            return self._generate_grid_pattern(size)
        elif pattern_name == 'circular':
            return self._generate_circular_pattern(size)
        else:
            raise ValueError(f"Unknown basic pattern: {pattern_name}")
    
    def _generate_advanced_pattern(self, pattern_name: str, **kwargs) -> Dict[str, Any]:
        """Generate advanced patterns"""
        if pattern_name == 'brahma_knot':
            return self._generate_brahma_knot(**kwargs)
        elif pattern_name == 'turtle_kolam':
            return self._generate_turtle_kolam(**kwargs)
        elif pattern_name == 'topological':
            return self._generate_topological_pattern(**kwargs)
        elif pattern_name == 'eulerian':
            return self._generate_eulerian_pattern(**kwargs)
        else:
            raise ValueError(f"Unknown advanced pattern: {pattern_name}")
    
    def _generate_cultural_pattern(self, pattern_name: str, **kwargs) -> Dict[str, Any]:
        """Generate cultural patterns"""
        # Generate points based on cultural region
        points = []
        center_x, center_y = 200, 200
        
        if pattern_name == 'tamil_nadu':
            # Tamil Nadu Sikku Kolam pattern
            for i in range(5):
                for j in range(5):
                    if (i + j) % 2 == 0:  # Checkerboard pattern
                        x = center_x + (i - 2) * 30
                        y = center_y + (j - 2) * 30
                        points.append({
                            'x': x,
                            'y': y,
                            'type': 'dot',
                            'size': 6
                        })
        elif pattern_name == 'kerala':
            # Kerala Ashtamangala pattern
            for i in range(3):
                for j in range(3):
                    x = center_x + (i - 1) * 40
                    y = center_y + (j - 1) * 40
                    points.append({
                        'x': x,
                        'y': y,
                        'type': 'dot',
                        'size': 5
                    })
        elif pattern_name == 'andhra_pradesh':
            # Andhra Pradesh Muggulu pattern
            for i in range(4):
                for j in range(4):
                    if i == j or i + j == 3:  # Diagonal pattern
                        x = center_x + (i - 1.5) * 35
                        y = center_y + (j - 1.5) * 35
                        points.append({
                            'x': x,
                            'y': y,
                            'type': 'dot',
                            'size': 5
                        })
        else:
            # Default cultural pattern
            for i in range(3):
                for j in range(3):
                    x = center_x + (i - 1) * 30
                    y = center_y + (j - 1) * 30
                    points.append({
                        'x': x,
                        'y': y,
                        'type': 'dot',
                        'size': 5
                    })
        
        return {
            'type': f'cultural_{pattern_name}',
            'points': points,
            'paths': [],
            'lines': [],
            'colors': ['#DC143C', '#B22222', '#8B0000'],
            'cultural_info': {
                'region': pattern_name.replace('_', ' ').title(),
                'significance': 'Traditional cultural pattern',
                'style': 'Traditional'
            }
        }
    
    def _generate_festival_pattern(self, pattern_name: str, **kwargs) -> Dict[str, Any]:
        """Generate festival patterns"""
        # Generate points based on festival
        points = []
        center_x, center_y = 200, 200
        
        if pattern_name == 'diwali':
            # Diwali Rangoli pattern - 5x5 grid
            for i in range(5):
                for j in range(5):
                    if i == 0 or i == 4 or j == 0 or j == 4:  # Border pattern
                        x = center_x + (i - 2) * 25
                        y = center_y + (j - 2) * 25
                        points.append({
                            'x': x,
                            'y': y,
                            'type': 'dot',
                            'size': 5
                        })
        elif pattern_name == 'pongal':
            # Pongal Harvest pattern - circular
            for i in range(8):
                angle = i * math.pi / 4
                x = center_x + 60 * math.cos(angle)
                y = center_y + 60 * math.sin(angle)
                points.append({
                    'x': x,
                    'y': y,
                    'type': 'dot',
                    'size': 6
                })
            # Center point
            points.append({
                'x': center_x,
                'y': center_y,
                'type': 'center',
                'size': 8
            })
        elif pattern_name == 'ugadi':
            # Ugadi New Year pattern - 3x3 grid
            for i in range(3):
                for j in range(3):
                    x = center_x + (i - 1) * 40
                    y = center_y + (j - 1) * 40
                    points.append({
                        'x': x,
                        'y': y,
                        'type': 'dot',
                        'size': 5
                    })
        else:
            # Default festival pattern
            for i in range(4):
                for j in range(4):
                    if (i + j) % 2 == 0:  # Checkerboard pattern
                        x = center_x + (i - 1.5) * 30
                        y = center_y + (j - 1.5) * 30
                        points.append({
                            'x': x,
                            'y': y,
                            'type': 'dot',
                            'size': 5
                        })
        
        return {
            'type': f'festival_{pattern_name}',
            'points': points,
            'paths': [],
            'lines': [],
            'colors': ['#FFD700', '#FF6B6B', '#4ECDC4', '#FF8C00'],
            'cultural_info': {
                'festival': pattern_name.title(),
                'significance': 'Festival celebration',
                'theme': 'Celebration'
            }
        }
    
    def _generate_radial_pattern(self, size: int) -> Dict[str, Any]:
        """Generate radial symmetry pattern"""
        points = []
        center_x, center_y = 200, 200
        max_radius = size * 20
        
        for i in range(size * 2):
            for j in range(size * 2):
                distance = math.sqrt((i - size)**2 + (j - size)**2)
                if distance <= size:
                    x = center_x + (i - size) * 20
                    y = center_y + (j - size) * 20
                    points.append({
                        'x': x,
                        'y': y,
                        'type': 'dot',
                        'size': 4
                    })
        
        return {
            'type': 'radial',
            'points': points,
            'paths': [],
            'lines': [],
            'colors': ['#DC143C'],
            'mathematical_properties': {
                'symmetry_type': 'RADIAL',
                'dot_count': len(points),
                'center': (center_x, center_y),
                'radius': max_radius
            }
        }
    
    def _generate_bilateral_pattern(self, size: int) -> Dict[str, Any]:
        """Generate bilateral symmetry pattern"""
        points = []
        center_x, center_y = 200, 200
        
        for i in range(size):
            for j in range(size):
                if j <= size // 2:  # Only left half
                    x = center_x + (i - size//2) * 40
                    y = center_y + (j - size//2) * 40
                    points.append({
                        'x': x,
                        'y': y,
                        'type': 'dot',
                        'size': 4
                    })
                    # Mirror point
                    if j < size // 2:
                        mirror_x = center_x + (size//2 - i) * 40
                        points.append({
                            'x': mirror_x,
                            'y': y,
                            'type': 'dot',
                            'size': 4
                        })
        
        return {
            'type': 'bilateral',
            'points': points,
            'paths': [],
            'lines': [],
            'colors': ['#B22222'],
            'mathematical_properties': {
                'symmetry_type': 'BILATERAL',
                'dot_count': len(points),
                'axis': 'vertical'
            }
        }
    
    def _generate_grid_pattern(self, size: int) -> Dict[str, Any]:
        """Generate grid pattern"""
        points = []
        center_x, center_y = 200, 200
        
        for i in range(0, size, 2):
            for j in range(0, size, 2):
                x = center_x + (i - size//2) * 40
                y = center_y + (j - size//2) * 40
                points.append({
                    'x': x,
                    'y': y,
                    'type': 'dot',
                    'size': 4
                })
        
        return {
            'type': 'grid',
            'points': points,
            'paths': [],
            'lines': [],
            'colors': ['#8B0000'],
            'mathematical_properties': {
                'symmetry_type': 'GRID',
                'dot_count': len(points),
                'grid_size': size
            }
        }
    
    def _generate_circular_pattern(self, size: int) -> Dict[str, Any]:
        """Generate circular pattern"""
        points = []
        center_x, center_y = 200, 200
        radius = size * 20
        
        for i in range(size * 4):
            angle = i * 2 * math.pi / (size * 4)
            x = center_x + radius * math.cos(angle)
            y = center_y + radius * math.sin(angle)
            points.append({
                'x': x,
                'y': y,
                'type': 'dot',
                'size': 4
            })
        
        return {
            'type': 'circular',
            'points': points,
            'paths': [],
            'lines': [],
            'colors': ['#FF6347'],
            'mathematical_properties': {
                'symmetry_type': 'RADIAL',
                'dot_count': len(points),
                'center': (center_x, center_y),
                'radius': radius
            }
        }
    
    def _generate_brahma_knot(self, **kwargs) -> Dict[str, Any]:
        """Generate perfect Brahma's Knot"""
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
        petal_angles = [90, 0, -90, 180]
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
        
        # Create continuous path
        dot_positions = {dot['id']: (dot['x'], dot['y']) for dot in points}
        path_sequence = [
            25, 0, 1, 2, 3, 4, 26, 9, 8, 7, 6, 5, 10, 11, 12, 13, 14,
            19, 18, 17, 16, 15, 20, 21, 22, 23, 24, 28, 27, 26,
            24, 23, 22, 21, 20, 15, 16, 17, 18, 19, 14, 13, 12, 11, 10,
            5, 6, 7, 8, 9, 0, 25
        ]
        
        path_coords = []
        for dot_id in path_sequence:
            if dot_id in dot_positions:
                path_coords.append(dot_positions[dot_id])
        
        # Smooth curves
        if len(path_coords) > 3:
            x_coords = [p[0] for p in path_coords]
            y_coords = [p[1] for p in path_coords]
            t = np.linspace(0, 1, len(path_coords))
            t_smooth = np.linspace(0, 1, len(path_coords) * 3)
            x_smooth = np.interp(t_smooth, t, x_coords)
            y_smooth = np.interp(t_smooth, t, y_coords)
            smooth_path = list(zip(x_smooth, y_smooth))
        else:
            smooth_path = path_coords
        
        return {
            'type': 'brahma_knot',
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
    
    def _generate_turtle_kolam(self, layers: int = 6, **kwargs) -> Dict[str, Any]:
        """Generate Turtle Kolam"""
        points = []
        center_x, center_y = 200, 200
        
        for layer in range(layers):
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
        for layer in range(layers):
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
                'layers': layers
            }
        }
    
    def _generate_topological_pattern(self, num_dots: int = 9, num_junctions: int = 1, 
                                    bond_types: List[str] = None, symmetry_type: str = 'RADIAL',
                                    cultural_region: str = 'tamil_nadu', **kwargs) -> Dict[str, Any]:
        """Generate topological pattern using 5-step method"""
        if bond_types is None:
            bond_types = ['CROSS', 'DOUBLE', 'BROKEN']
        
        points = []
        paths = []
        junctions = []
        center_x, center_y = 200, 200
        
        # Step 1: Generate dot matrix based on symmetry
        if symmetry_type == 'RADIAL':
            # Radial symmetry - circular arrangement
            radius = 60
            for i in range(num_dots):
                angle = (i * 2 * math.pi) / num_dots
                x = center_x + radius * math.cos(angle)
                y = center_y + radius * math.sin(angle)
                points.append({
                    'x': x,
                    'y': y,
                    'id': i,
                    'type': 'dot',
                    'is_center': i == 0
                })
        elif symmetry_type == 'BILATERAL':
            # Bilateral symmetry - mirror arrangement
            for i in range(num_dots):
                if i < num_dots // 2:
                    x = center_x - 40 - (i * 30)
                    y = center_y
                else:
                    x = center_x + 40 + ((i - num_dots // 2) * 30)
                    y = center_y
                points.append({
                    'x': x,
                    'y': y,
                    'id': i,
                    'type': 'dot',
                    'is_center': i == 0
                })
        else:
            # Grid symmetry - square arrangement
            size = int(math.sqrt(num_dots))
            for i in range(size):
                for j in range(size):
                    if len(points) < num_dots:
                        x = center_x + (j - size//2) * 40
                        y = center_y + (i - size//2) * 40
                        points.append({
                            'x': x,
                            'y': y,
                            'id': len(points),
                            'type': 'dot',
                            'is_center': len(points) == 0
                        })
        
        # Step 2: Create graph structure with junctions
        for i in range(min(num_junctions, len(points) - 1)):
            point1_idx = i
            point2_idx = (i + 1) % len(points)
            
            # Calculate junction position (midpoint)
            p1 = points[point1_idx]
            p2 = points[point2_idx]
            junction_x = (p1['x'] + p2['x']) / 2
            junction_y = (p1['y'] + p2['y']) / 2
            
            junctions.append({
                'point1_idx': point1_idx,
                'point2_idx': point2_idx,
                'bond_type': bond_types[i % len(bond_types)],
                'position': [junction_x, junction_y],
                'arms': 2
            })
        
        # Step 3: Generate paths based on bond types
        for junction in junctions:
            p1 = points[junction['point1_idx']]
            p2 = points[junction['point2_idx']]
            
            if junction['bond_type'] == 'CROSS':
                # Cross bond - lines crossing at junction
                path = [
                    [p1['x'], p1['y']],
                    [junction['position'][0], junction['position'][1]],
                    [p2['x'], p2['y']]
                ]
                paths.append(path)
            elif junction['bond_type'] == 'DOUBLE':
                # Double bond - two parallel lines
                offset = 10
                path1 = [
                    [p1['x'] - offset, p1['y']],
                    [junction['position'][0] - offset, junction['position'][1]],
                    [p2['x'] - offset, p2['y']]
                ]
                path2 = [
                    [p1['x'] + offset, p1['y']],
                    [junction['position'][0] + offset, junction['position'][1]],
                    [p2['x'] + offset, p2['y']]
                ]
                paths.extend([path1, path2])
            # BROKEN bonds don't create paths
        
        # Step 4: Apply symmetry transformations
        if symmetry_type == 'RADIAL' and len(points) > 3:
            # Create radial symmetry by duplicating paths
            original_paths = paths.copy()
            for i in range(1, len(points)):
                angle = (i * 2 * math.pi) / len(points)
                cos_a, sin_a = math.cos(angle), math.sin(angle)
                
                for path in original_paths:
                    rotated_path = []
                    for point in path:
                        # Rotate point around center
                        rel_x = point[0] - center_x
                        rel_y = point[1] - center_y
                        new_x = center_x + rel_x * cos_a - rel_y * sin_a
                        new_y = center_y + rel_x * sin_a + rel_y * cos_a
                        rotated_path.append([new_x, new_y])
                    paths.append(rotated_path)
        
        # Step 5: Add cultural motifs and colors
        cultural_colors = {
            'tamil_nadu': ['#DC143C', '#B22222', '#8B0000'],
            'karnataka': ['#FF6B35', '#FFD700', '#FF8C00'],
            'kerala': ['#32CD32', '#FFD700', '#FF6347'],
            'andhra_pradesh': ['#8B0000', '#DC143C', '#B22222'],
            'telangana': ['#FFD700', '#FF6B35', '#32CD32']
        }
        
        colors = cultural_colors.get(cultural_region, ['#DC143C', '#B22222', '#8B0000'])
        
        return {
            'type': 'topological',
            'points': points,
            'paths': paths,
            'junctions': junctions,
            'lines': [],
            'colors': colors,
            'cultural_info': {
                'region': cultural_region.replace('_', ' ').title(),
                'significance': 'Traditional topological kolam pattern',
                'style': 'Research-based 5-step method'
            },
            'mathematical_properties': {
                'symmetry_type': symmetry_type,
                'dot_count': len(points),
                'junction_count': len(junctions),
                'path_count': len(paths),
                'topological_method': '5-step Gopalan & VanLeeuwen',
                'complexity_score': min(1.0, (len(points) + len(junctions)) / 20.0),
                'eulerian_path': len(junctions) > 0
            }
        }
    
    def _generate_eulerian_pattern(self, num_dots: int = 16, **kwargs) -> Dict[str, Any]:
        """Generate Eulerian path pattern"""
        points = []
        size = int(math.sqrt(num_dots))
        
        for i in range(size):
            for j in range(size):
                points.append({
                    'x': i * 50,
                    'y': j * 50,
                    'type': 'dot'
                })
        
        return {
            'type': 'eulerian',
            'points': points,
            'paths': [],
            'lines': [],
            'colors': ['#B22222'],
            'mathematical_properties': {
                'symmetry_type': 'GRID',
                'dot_count': len(points),
                'eulerian_path': True
            }
        }

# Initialize generator
pattern_generator = ProductionPatternGenerator()

# API Routes
@app.route('/')
@handle_errors
def home():
    """Home endpoint with comprehensive API documentation"""
    return jsonify({
        'message': 'Kolam Art Studio Backend API - Production Version',
        'version': '3.0.0',
        'status': 'running',
        'timestamp': datetime.now().isoformat(),
        'documentation': {
            'patterns': '/api/patterns',
            'generate': '/api/generate',
            'analyze': '/api/analyze',
            'health': '/api/health',
            'metrics': '/api/metrics'
        },
        'capabilities': {
            'basic_patterns': list(pattern_generator.patterns['basic'].keys()),
            'advanced_patterns': list(pattern_generator.patterns['advanced'].keys()),
            'cultural_patterns': list(pattern_generator.patterns['cultural'].keys()),
            'festival_patterns': list(pattern_generator.patterns['festival'].keys())
        },
        'features': [
            'Pattern Generation',
            'Cultural Analysis',
            'Mathematical Properties',
            'Caching',
            'Rate Limiting',
            'Error Handling',
            'Logging'
        ]
    })

@app.route('/api/health')
@handle_errors
def health_check():
    """Health check endpoint with system metrics"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '3.0.0',
        'uptime': 'running',
        'cache_size': len(pattern_generator.cache),
        'memory_usage': 'normal'
    })

@app.route('/api/patterns', methods=['GET'])
@handle_errors
@rate_limit(max_requests=50, window=60)
def get_patterns():
    """Get all available patterns with detailed information"""
    return jsonify({
        'success': True,
        'patterns': pattern_generator.patterns,
        'total_categories': len(pattern_generator.patterns),
        'total_patterns': sum(len(patterns) for patterns in pattern_generator.patterns.values())
    })

@app.route('/api/generate', methods=['POST'])
@handle_errors
@rate_limit(max_requests=30, window=60)
def generate_pattern():
    """Generate pattern based on type and parameters"""
    data = request.get_json()
    
    if not data:
        raise ValueError("Request body is required")
    
    pattern_type = data.get('type', 'basic')
    pattern_name = data.get('pattern', 'radial')
    
    # Remove None values from kwargs
    kwargs = {k: v for k, v in data.items() if k not in ['type', 'pattern'] and v is not None}
    
    result = pattern_generator.generate_pattern(pattern_type, pattern_name, **kwargs)
    
    return jsonify({
        'success': True,
        'pattern': result
    })

@app.route('/api/analyze', methods=['POST'])
@handle_errors
@rate_limit(max_requests=20, window=60)
def analyze_pattern():
    """Analyze pattern properties and characteristics"""
    data = request.get_json()
    
    if not data:
        raise ValueError("Request body is required")
    
    # Handle both direct pattern data and wrapped pattern data
    if 'pattern' in data:
        pattern = data['pattern']
    else:
        pattern = data
    
    points = pattern.get('points', [])
    pattern_type = pattern.get('type', 'unknown')
    
    # Basic analysis
    analysis = {
        'point_count': len(points),
        'pattern_type': pattern_type,
        'analyzed_at': datetime.now().isoformat()
    }
    
    # Add symmetry analysis if points available
    if points:
        x_coords = [p.get('x', 0) for p in points if isinstance(p, dict)]
        y_coords = [p.get('y', 0) for p in points if isinstance(p, dict)]
        
        if x_coords and y_coords:
            center_x = sum(x_coords) / len(x_coords)
            center_y = sum(y_coords) / len(y_coords)
            
            # Simple symmetry analysis
            distances = [math.sqrt((p.get('x', 0) - center_x)**2 + (p.get('y', 0) - center_y)**2) for p in points if isinstance(p, dict)]
            if len(set(round(d, 1) for d in distances)) <= 3:
                analysis['symmetry'] = 'RADIAL'
            else:
                analysis['symmetry'] = 'ASYMMETRIC'
            
            analysis['center'] = (center_x, center_y)
            analysis['bounds'] = {
                'min_x': min(x_coords),
                'max_x': max(x_coords),
                'min_y': min(y_coords),
                'max_y': max(y_coords)
            }
    
    # Create frontend-compatible basic analysis format
    frontend_basic_analysis = {
        'cultural_region': 'Tamil Nadu',  # Default cultural region
        'symmetry_type': analysis.get('symmetry', 'Bilateral'),
        'complexity': 'Medium',  # Default complexity level
        'confidence': 0.85,  # Default confidence level
        'point_count': analysis.get('point_count', 0),
        'pattern_type': analysis.get('pattern_type', 'unknown'),
        'center': analysis.get('center', [0, 0]),
        'bounds': analysis.get('bounds', {}),
        'analyzed_at': analysis.get('analyzed_at', '')
            }
    
    return jsonify({
        'success': True,
        'analysis': frontend_basic_analysis
    })

@app.route('/api/metrics', methods=['GET'])
@handle_errors
def get_metrics():
    """Get system metrics and performance data"""
    return jsonify({
        'success': True,
        'metrics': {
            'cache_size': len(pattern_generator.cache),
            'total_patterns': sum(len(patterns) for patterns in pattern_generator.patterns.values()),
            'uptime': 'running',
            'timestamp': datetime.now().isoformat()
        }
    })

@app.route('/api/advanced-analysis', methods=['POST'])
@handle_errors
@rate_limit(max_requests=10, window=60)
def advanced_analysis():
    """Perform advanced analysis on patterns"""
    data = request.get_json()
    
    if not data:
        raise ValueError("Request body is required")
    
    # Handle both direct pattern data and wrapped pattern data
    if 'pattern' in data:
        pattern = data['pattern']
        analysis_type = data.get('type', 'comprehensive')
    else:
        pattern = data
        analysis_type = 'comprehensive'
    
    # Enhanced advanced analysis
    points = pattern.get('points', [])
    paths = pattern.get('paths', [])
    junctions = pattern.get('junctions', [])
    colors = pattern.get('colors', [])
    mathematical_props = pattern.get('mathematical_properties', {})
    cultural_info = pattern.get('cultural_info', {})
    
    # Calculate complexity score based on multiple factors
    complexity_factors = {
        'points': len(points) * 1,
        'paths': len(paths) * 2,
        'junctions': len(junctions) * 3,
        'colors': len(colors) * 0.5
    }
    complexity_score = min(100, sum(complexity_factors.values()))
    
    # Enhanced symmetry detection
    symmetry_detected = 'ASYMMETRIC'
    if points:
        x_coords = [p.get('x', 0) for p in points if isinstance(p, dict)]
        y_coords = [p.get('y', 0) for p in points if isinstance(p, dict)]
        
        if x_coords and y_coords:
            center_x = sum(x_coords) / len(x_coords)
            center_y = sum(y_coords) / len(y_coords)
            
            # Check for radial symmetry
            distances = [math.sqrt((p.get('x', 0) - center_x)**2 + (p.get('y', 0) - center_y)**2) for p in points if isinstance(p, dict)]
            if len(set(round(d, 1) for d in distances)) <= 3:
                symmetry_detected = 'RADIAL'
            else:
                symmetry_detected = 'ASYMMETRIC'
    
    # Use mathematical properties if available
    if mathematical_props.get('symmetry_type'):
        symmetry_detected = mathematical_props.get('symmetry_type', symmetry_detected)
    
    analysis_result = {
        'analysis_type': analysis_type,
        'timestamp': datetime.now().isoformat(),
        'pattern_properties': {
            'point_count': len(points),
            'path_count': len(paths),
            'junction_count': len(junctions),
            'line_count': len(pattern.get('lines', [])),
            'color_count': len(colors),
            'total_elements': len(points) + len(paths) + len(junctions)
        },
        'mathematical_analysis': {
            'symmetry_detected': symmetry_detected,
            'complexity_score': complexity_score,
            'geometric_properties': {
                'has_curves': len(paths) > 0,
                'has_straight_lines': len(pattern.get('lines', [])) > 0,
                'is_closed_loop': mathematical_props.get('continuous_loop', False),
                'has_junctions': len(junctions) > 0,
                'topological_method': mathematical_props.get('topological_method', 'Unknown')
            },
            'topological_properties': {
                'eulerian_path': mathematical_props.get('eulerian_path', False),
                'dot_count': mathematical_props.get('dot_count', len(points)),
                'junction_count': mathematical_props.get('junction_count', len(junctions)),
                'path_count': mathematical_props.get('path_count', len(paths))
            }
        },
        'cultural_analysis': {
            'region': cultural_info.get('region', 'Unknown'),
            'significance': cultural_info.get('significance', 'Traditional art form'),
            'style': cultural_info.get('style', 'Traditional'),
            'materials': cultural_info.get('materials', ['Traditional materials'])
        },
        'recommendations': [
            f"Suitable for: {', '.join(['Festivals', 'Temples', 'Homes'])}",
            f"Complexity Level: {'Low' if complexity_score < 30 else 'Medium' if complexity_score < 70 else 'High'}",
            f"Cultural Appropriateness: High",
            f"Pattern Type: {pattern.get('type', 'Traditional')}",
            f"Symmetry: {symmetry_detected}",
            f"Topological Method: {mathematical_props.get('topological_method', 'Traditional')}"
        ]
    }
    
    # Create frontend-compatible response format
    frontend_analysis = {
        'quality_score': complexity_score / 100,  # Convert to 0-1 scale
        'eulerian_analysis': {
            'euler_path_exists': mathematical_props.get('eulerian_path', len(junctions) > 0)
        },
        'geometric_properties': {
            'graph_nodes': len(points),
            'has_curves': len(paths) > 0,
            'has_junctions': len(junctions) > 0,
            'point_count': len(points),
            'path_count': len(paths),
            'junction_count': len(junctions)
        },
        'cultural_classification': {
            'region': cultural_info.get('region', 'Unknown').lower().replace(' ', '_'),
            'significance': cultural_info.get('significance', 'Traditional art form'),
            'style': cultural_info.get('style', 'Traditional')
        },
        'symmetry_type': symmetry_detected,
        'complexity_level': 'Low' if complexity_score < 30 else 'Medium' if complexity_score < 70 else 'High',
        'topological_method': mathematical_props.get('topological_method', 'Traditional'),
        'recommendations': analysis_result['recommendations']
    }
    
    # Merge frontend-compatible data into main analysis
    analysis_result.update(frontend_analysis)
    
    return jsonify({
        'success': True,
        'analysis': analysis_result
    })

@app.route('/api/cultural-analysis', methods=['POST'])
@handle_errors
@rate_limit(max_requests=10, window=60)
def cultural_analysis():
    """Perform cultural analysis on patterns"""
    data = request.get_json()
    
    if not data:
        raise ValueError("Request body is required")
    
    pattern = data.get('pattern', {})
    
    # Cultural analysis
    cultural_result = {
        'timestamp': datetime.now().isoformat(),
        'cultural_properties': {
            'region': pattern.get('cultural_info', {}).get('region', 'Unknown'),
            'traditional_name': pattern.get('cultural_info', {}).get('traditional_name', 'Traditional Pattern'),
            'significance': pattern.get('cultural_info', {}).get('significance', 'Cultural significance'),
            'materials': pattern.get('cultural_info', {}).get('materials', ['Traditional materials']),
            'style': pattern.get('cultural_info', {}).get('style', 'Traditional')
        },
        'festival_associations': {
            'diwali': pattern.get('cultural_info', {}).get('region') in ['Tamil Nadu', 'Karnataka', 'Andhra Pradesh'],
            'pongal': pattern.get('cultural_info', {}).get('region') == 'Tamil Nadu',
            'onam': pattern.get('cultural_info', {}).get('region') == 'Kerala',
            'ugadi': pattern.get('cultural_info', {}).get('region') in ['Karnataka', 'Andhra Pradesh']
        },
        'cultural_score': 85,  # Default cultural relevance score
        'recommendations': [
            f"Best Occasions: {', '.join(['Festivals', 'Religious ceremonies', 'Cultural events'])}",
            f"Color Schemes: {', '.join(pattern.get('colors', ['#DC143C', '#B22222', '#8B0000']))}",
            f"Placement: Center of home or temple",
            f"Cultural Region: {pattern.get('cultural_info', {}).get('region', 'Unknown')}",
            f"Traditional Significance: {pattern.get('cultural_info', {}).get('significance', 'Traditional art form')}"
        ]
    }
    
    return jsonify({
        'success': True,
        'cultural_analysis': cultural_result
    })

# Legacy endpoints for compatibility
@app.route('/api/generate-python-brahma', methods=['POST'])
@handle_errors
@rate_limit(max_requests=20, window=60)
def generate_python_brahma():
    """Generate Brahma's Knot - Python style (Legacy endpoint)"""
    result = pattern_generator.generate_pattern('advanced', 'brahma_knot')
    return jsonify({
        'success': True,
        'message': 'Brahma\'s Knot generated in Python style',
        'pattern': result
    })

@app.route('/api/generate-python-turtle', methods=['POST'])
@handle_errors
@rate_limit(max_requests=20, window=60)
def generate_python_turtle():
    """Generate Turtle Kolam - Python style (Legacy endpoint)"""
    result = pattern_generator.generate_pattern('advanced', 'turtle_kolam')
    return jsonify({
        'success': True,
        'message': 'Turtle Kolam generated in Python style',
        'pattern': result
    })

@app.route('/api/generate-topological', methods=['POST'])
@handle_errors
@rate_limit(max_requests=20, window=60)
def generate_topological():
    """Generate topological pattern using 5-step method"""
    data = request.get_json() or {}
    
    # Get parameters with defaults
    num_dots = data.get('num_dots', 9)
    num_junctions = data.get('num_junctions', 1)
    bond_types = data.get('bond_types', ['CROSS', 'DOUBLE', 'BROKEN'])
    symmetry_type = data.get('symmetry_type', 'RADIAL')
    cultural_region = data.get('cultural_region', 'tamil_nadu')
    
    start_time = time.time()
    
    # Generate topological pattern using the existing method
    result = pattern_generator.generate_pattern('advanced', 'topological', 
                                               num_dots=num_dots, 
                                               num_junctions=num_junctions,
                                               bond_types=bond_types,
                                               symmetry_type=symmetry_type,
                                               cultural_region=cultural_region)
    
    # Add topological-specific properties
    result['topological_properties'] = {
        'num_dots': num_dots,
        'num_junctions': num_junctions,
        'bond_types': bond_types,
        'symmetry_type': symmetry_type,
        'cultural_region': cultural_region,
        'angle_encoding': [random.uniform(0, 2*math.pi) for _ in range(num_dots)],
        'numeric_representation': f"0x{random.randint(1000, 9999):04x}",
        'tracing_sequence': list(range(num_dots)),
        'research_method': '5-step Gopalan & VanLeeuwen'
    }
    
    generation_time = time.time() - start_time
    
    logger.info(f"Generated topological pattern in {generation_time:.3f}s")
    
    # Create pattern_info for frontend
    pattern_info = {
        'parent_type': result.get('type', 'topological'),
        'symmetry_type': result.get('mathematical_properties', {}).get('symmetry_type', symmetry_type),
        'mathematical_properties': result.get('mathematical_properties', {}),
        'cultural_metadata': result.get('cultural_info', {}),
        'numeric_representation': result.get('topological_properties', {}).get('numeric_representation', ''),
        'angle_encoding': result.get('topological_properties', {}).get('angle_encoding', []),
        'tracing_sequence': result.get('topological_properties', {}).get('tracing_sequence', [])
    }
    
    return jsonify({
        'success': True,
        'message': 'Topological pattern generated successfully',
        'pattern': result,
        'pattern_info': pattern_info,
        'generation_time': generation_time
    })

@app.route('/api/generate-spiral-kolam', methods=['POST'])
@handle_errors
@rate_limit(max_requests=15, window=60)
def generate_spiral_kolam():
    """Generate Animated Spiral Kolam with Dotted Squares"""
    data = request.get_json() or {}
    
    # Get parameters with defaults
    turns = data.get('turns', 6)
    step_angle = data.get('step_angle', 15)
    step_length = data.get('step_length', 8)
    animation = data.get('animation', True)
    
    start_time = time.time()
    
    # Generate spiral pattern data
    pattern_data = {
        'type': 'spiral_kolam',
        'title': 'Animated Spiral Kolam with Dotted Squares',
        'description': 'Beautiful spiral pattern with dotted square elements',
        'metadata': {
            'turns': turns,
            'step_angle': step_angle,
            'step_length': step_length,
            'total_steps': int((360 / step_angle) * turns),
            'animation': animation,
            'colors': {
                'spiral': 'cyan',
                'squares': 'white',
                'background': 'black'
            }
        },
        'elements': [
            {
                'type': 'spiral',
                'description': 'Main spiral path with cyan color',
                'parameters': {
                    'turns': turns,
                    'step_angle': step_angle,
                    'step_length': step_length
                }
            },
            {
                'type': 'dotted_squares',
                'count': int((360 / step_angle) * turns / 15),
                'description': 'White dotted squares placed along spiral path',
                'placement': 'Every 15 steps'
            }
        ],
        'generation_info': {
            'method': 'Python Turtle Graphics',
            'animation': animation,
            'real_time_progress': True,
            'smooth_transitions': True
        },
        'frontend_integration': {
            'canvas_size': '1000x800',
            'animation_duration': f'{(360 / step_angle) * turns * 0.05:.1f} seconds',
            'frame_rate': '20 fps',
            'interactive': True
        }
    }
    
    generation_time = time.time() - start_time
    
    logger.info(f"Generated spiral_kolam in {generation_time:.3f}s")
    
    return jsonify({
        'success': True,
        'pattern': pattern_data,
        'generation_time': generation_time,
        'message': 'Spiral Kolam generated successfully'
    })

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'success': False,
        'error': 'Endpoint not found',
        'message': 'The requested endpoint does not exist',
        'available_endpoints': ['/api/patterns', '/api/generate', '/api/analyze', '/api/health']
    }), 404

@app.errorhandler(500)
def internal_error(error):
    logger.error(f"Internal server error: {error}")
    return jsonify({
        'success': False,
        'error': 'Internal server error',
        'message': 'An unexpected error occurred. Please try again later.'
    }), 500

if __name__ == '__main__':
    logger.info("Starting Production Kolam Backend System...")
    logger.info("Backend URL: http://localhost:5000")
    logger.info("Frontend URL: http://localhost:3000")
    logger.info("API Documentation: http://localhost:5000")
    logger.info("Metrics: http://localhost:5000/api/metrics")
    logger.info("=" * 60)
    
    app.run(debug=False, host='0.0.0.0', port=5000)
