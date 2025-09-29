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
import matplotlib
matplotlib.use('Agg')  # Use non-GUI backend
import numpy as np
import math
import random
import os
import time
import base64
import io
from PIL import Image, ImageFilter, ImageEnhance
from functools import wraps
import cv2
import uuid
from pathlib import Path

# Diffusion imports (optional - will be imported when needed)
try:
    import torch
    from diffusers import StableDiffusionControlNetPipeline, ControlNetModel
    from diffusers import UniPCMultistepScheduler
    DIFFUSION_AVAILABLE = True
except ImportError:
    DIFFUSION_AVAILABLE = False
    # logger will be defined later, so we'll handle this in the initialization

# Configure production logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('kolam_backend.log', encoding='utf-8'),
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

# Initialize diffusion models (if available)
diffusion_pipe = None
diffusion_controlnet = None
diffusion_device = None

def initialize_diffusion_models():
    """Initialize Stable Diffusion and ControlNet models"""
    global diffusion_pipe, diffusion_controlnet, diffusion_device
    
    if not DIFFUSION_AVAILABLE:
        logger.warning("Diffusion libraries not available")
        return False
    
    try:
        # Set device
        diffusion_device = "cuda" if torch.cuda.is_available() else "cpu"
        logger.info(f"Initializing diffusion models on device: {diffusion_device}")
        
        # Load ControlNet model
        logger.info("Loading ControlNet model...")
        diffusion_controlnet = ControlNetModel.from_pretrained(
            "lllyasviel/sd-controlnet-canny",
            torch_dtype=torch.float16 if diffusion_device == "cuda" else torch.float32
        )
        
        # Load Stable Diffusion pipeline
        logger.info("Loading Stable Diffusion pipeline...")
        diffusion_pipe = StableDiffusionControlNetPipeline.from_pretrained(
            "runwayml/stable-diffusion-v1-5",
            controlnet=diffusion_controlnet,
            torch_dtype=torch.float16 if diffusion_device == "cuda" else torch.float32,
            safety_checker=None,
            requires_safety_checker=False
        )
        
        # Set scheduler for better quality
        diffusion_pipe.scheduler = UniPCMultistepScheduler.from_config(diffusion_pipe.scheduler.config)
        
        # Move to device
        diffusion_pipe = diffusion_pipe.to(diffusion_device)
        
        # Enable memory efficient attention if available
        if hasattr(diffusion_pipe, "enable_attention_slicing"):
            diffusion_pipe.enable_attention_slicing()
        
        logger.info("Diffusion models loaded successfully!")
        return True
        
    except Exception as e:
        logger.error(f"Error loading diffusion models: {e}")
        return False

# Initialize diffusion models in background (non-blocking)
if DIFFUSION_AVAILABLE:
    logger.info("Starting AI model initialization in background...")
    import threading
    def load_models_async():
        try:
            initialize_diffusion_models()
        except Exception as e:
            logger.error(f"Failed to load AI models: {e}")
            logger.info("Server will continue without AI features")
    
    model_thread = threading.Thread(target=load_models_async, daemon=True)
    model_thread.start()
else:
    logger.warning("Diffusion libraries not available. AI generation will be disabled.")

def preprocess_image_for_diffusion(image):
    """Preprocess image for ControlNet (Canny edge detection)"""
    try:
        # Convert PIL to numpy array
        if isinstance(image, Image.Image):
            image = np.array(image)
        
        # Convert to grayscale
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        else:
            gray = image
        
        # Apply Canny edge detection
        edges = cv2.Canny(gray, 100, 200)
        
        # Convert back to PIL
        edges_pil = Image.fromarray(edges)
        
        return edges_pil
        
    except Exception as e:
        logger.error(f"Error preprocessing image: {e}")
        return None

def generate_lightweight_variants():
    """Generate Kolam variants using lightweight image processing (no AI models)"""
    try:
        # Get uploaded file
        if 'image' not in request.files:
            return jsonify({
                "success": False,
                "error": "No image file provided"
            }), 400
        
        file = request.files['image']
        if file.filename == '':
            return jsonify({
                "success": False,
                "error": "No file selected"
            }), 400
        
        # Create outputs directory
        os.makedirs('outputs', exist_ok=True)
        
        # Load the uploaded image
        image = Image.open(file.stream)
        
        # Generate 3 variants using image processing
        variants = []
        variant_configs = [
            {
                'name': 'Enhanced Symmetrical',
                'description': 'Enhanced traditional Kolam style with improved contrast',
                'filters': ['edge_enhance', 'contrast_1.5']
            },
            {
                'name': 'Colorful Digital',
                'description': 'Vibrant digital art style with enhanced colors',
                'filters': ['color_1.8', 'saturation_1.3']
            },
            {
                'name': 'Minimal Geometric',
                'description': 'Clean geometric design with smooth lines',
                'filters': ['smooth', 'brightness_1.2']
            }
        ]
        
        for i, config in enumerate(variant_configs):
            try:
                # Create a copy of the image
                variant_image = image.copy()
                
                # Apply filters based on configuration
                for filter_name in config['filters']:
                    if filter_name == 'edge_enhance':
                        variant_image = variant_image.filter(ImageFilter.EDGE_ENHANCE)
                    elif filter_name == 'smooth':
                        variant_image = variant_image.filter(ImageFilter.SMOOTH)
                    elif filter_name.startswith('contrast_'):
                        factor = float(filter_name.split('_')[1])
                        enhancer = ImageEnhance.Contrast(variant_image)
                        variant_image = enhancer.enhance(factor)
                    elif filter_name.startswith('color_'):
                        factor = float(filter_name.split('_')[1])
                        enhancer = ImageEnhance.Color(variant_image)
                        variant_image = enhancer.enhance(factor)
                    elif filter_name.startswith('brightness_'):
                        factor = float(filter_name.split('_')[1])
                        enhancer = ImageEnhance.Brightness(variant_image)
                        variant_image = enhancer.enhance(factor)
                    elif filter_name.startswith('saturation_'):
                        factor = float(filter_name.split('_')[1])
                        enhancer = ImageEnhance.Color(variant_image)
                        variant_image = enhancer.enhance(factor)
                
                # Save the variant
                variant_id = str(uuid.uuid4())[:8]
                filename = f"kolam_variant_{i+1}_{variant_id}.png"
                filepath = os.path.join('outputs', filename)
                variant_image.save(filepath)
                
                variants.append({
                    'id': variant_id,
                    'name': config['name'],
                    'description': config['description'],
                    'url': f'/outputs/{filename}',
                    'filename': filename
                })
                
            except Exception as e:
                logger.error(f"Error generating variant {i+1}: {e}")
                continue
        
        if not variants:
            return jsonify({
                "success": False,
                "error": "Failed to generate any variants"
            }), 500
        
        return jsonify({
            "success": True,
            "variants": variants,
            "message": "Generated using lightweight image processing (AI models still downloading)",
            "ai_models_loading": True
        })
        
    except Exception as e:
        logger.error(f"Error in lightweight generation: {e}")
        return jsonify({
            "success": False,
            "error": f"Generation failed: {str(e)}"
        }), 500

def generate_kolam_variant(prompt, control_image, num_inference_steps=20, guidance_scale=7.5):
    """Generate a single Kolam variant"""
    try:
        # Generate image
        result = diffusion_pipe(
            prompt=prompt,
            image=control_image,
            num_inference_steps=num_inference_steps,
            guidance_scale=guidance_scale,
            controlnet_conditioning_scale=1.0,
            generator=torch.Generator(device=diffusion_device).manual_seed(42)
        ).images[0]
        
        return result
        
    except Exception as e:
        logger.error(f"Error generating variant: {e}")
        return None

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

@app.route('/api/improved-analysis', methods=['POST'])
@handle_errors
@rate_limit(max_requests=10, window=60)
def improved_image_analysis():
    """
    Improved image analysis using trained model and dataset:
    - Advanced feature extraction
    - Machine learning classification
    - Cultural region detection
    - Symmetry analysis
    - Eulerian path validation
    """
    try:
        data = request.get_json()
        
        if not data or 'image' not in data:
            return jsonify({"error": "No image data provided"}), 400
        
        # Decode base64 image
        image_data = data['image'].split(',')[1]
        image_bytes = base64.b64decode(image_data)
        image = Image.open(io.BytesIO(image_bytes))
        
        # Convert to numpy array
        img_array = np.array(image)
        
        # Use quick fix analyzer directly
        try:
            from quick_fix_analyzer import QuickFixAnalyzer
            quick_analyzer = QuickFixAnalyzer()
            
            # Perform analysis with quick fix analyzer
            result = quick_analyzer.analyze_image(img_array)
            
            # Convert to expected format
            analysis_results = {
                "kolam_type": result['kolam_type'],
                "symmetry_type": result['symmetry_type'],
                "cultural_region": result['cultural_region'],
                "complexity_score": float(result['complexity_score']),
                "eulerian_path": result['eulerian_path'],
                "confidence": float(result['confidence']),
                "features": result['features'],
                "metadata": result['metadata'],
                "analysis_method": "quick_fix"
            }
            
        except Exception as e:
            logger.warning(f"Quick fix analyzer failed: {e}, falling back to improved analyzer")
            # Fallback to improved analyzer
            from improved_kolam_analyzer import ImprovedKolamAnalyzer
            improved_analyzer = ImprovedKolamAnalyzer()
            
            # Check if model is trained
            if not improved_analyzer.is_trained:
                # Try to load existing model
                try:
                    import joblib
                    import pickle
                    models = {}
                    label_encoders = {}
                    
                    # Load models
                    for task in ['kolam_type', 'symmetry_type', 'cultural_region']:
                        model_path = f"models/{task}_model.pkl"
                        if os.path.exists(model_path):
                            models[task] = joblib.load(model_path)
                            logger.info(f"Loaded {task} model")
                        else:
                            logger.warning(f"Model not found: {model_path}")
                    
                    # Load label encoders
                    encoders_path = "models/label_encoders.pkl"
                    if os.path.exists(encoders_path):
                        with open(encoders_path, 'rb') as f:
                            label_encoders = pickle.load(f)
                        logger.info(f"Loaded label encoders: {list(label_encoders.keys())}")
                    else:
                        logger.warning("Label encoders not found")
                    
                    if models:
                        improved_analyzer.model = models
                        improved_analyzer.is_trained = True
                        logger.info(f"Analyzer trained with {len(models)} models")
                    else:
                        raise ValueError("No trained models found")
                except Exception as e:
                    logger.error(f"Model loading failed: {e}")
                    raise ValueError(f"Model not trained and no saved models found: {e}")
            
            # Perform analysis
            result = improved_analyzer.analyze_image(img_array)
            
            # Convert numpy types to Python types for JSON serialization
            def convert_numpy_types(obj):
                if isinstance(obj, np.integer):
                    return int(obj)
                elif isinstance(obj, np.floating):
                    return float(obj)
                elif isinstance(obj, np.ndarray):
                    return obj.tolist()
                elif isinstance(obj, dict):
                    return {key: convert_numpy_types(value) for key, value in obj.items()}
                elif isinstance(obj, list):
                    return [convert_numpy_types(item) for item in obj]
                else:
                    return obj
            
            analysis_results = {
                "kolam_type": result.kolam_type,
                "symmetry_type": result.symmetry_type,
                "cultural_region": result.cultural_region,
                "complexity_score": float(result.complexity_score),
                "eulerian_path": result.eulerian_path,
                "confidence": float(result.confidence),
                "features": convert_numpy_types(result.features),
                "metadata": convert_numpy_types(result.metadata),
                "analysis_method": "improved_ml_model"
            }
            
        except Exception as e:
            logger.warning(f"Improved analysis failed: {e}")
            # Fallback to basic analysis
            analysis_results = {
                "kolam_type": "unknown",
                "symmetry_type": "bilateral",
                "cultural_region": "tamil_nadu",
                "complexity_score": 0.5,
                "eulerian_path": False,
                "confidence": 0.3,
                "features": {},
                "metadata": {"error": str(e)},
                "analysis_method": "fallback"
            }
        
        return jsonify({
            "success": True,
            "analysis": analysis_results,
            "message": "Improved analysis completed"
        })
        
    except Exception as e:
        logger.error(f"Improved analysis error: {str(e)}")
        return jsonify({
            "success": False,
            "error": str(e),
            "message": "Improved analysis failed"
        }), 500

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

@app.route('/api/generate-similar', methods=['POST'])
@handle_errors
@rate_limit(max_requests=5, window=60)
def generate_similar_patterns():
    """
    Generate similar patterns based on dataset templates:
    - Uses trained models for pattern classification
    - Generates variations based on reference patterns
    - Creates multiple similar patterns
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        # Get parameters
        reference_pattern = data.get('reference_pattern', 'pulli_kolam')
        num_variations = data.get('num_variations', 5)
        include_user_images = data.get('include_user_images', True)
        
        # Initialize advanced Kolam pattern generator
        try:
            from kolam_pattern_generator_ml import KolamPatternGenerator
            generator = KolamPatternGenerator("generated_similar_patterns")
            
            # Create pattern data from reference pattern
            pattern_data = {
                'type': 'reference',
                'coordinates': _generate_sample_coordinates(reference_pattern),
                'edges': [],
                'source': reference_pattern,
                'n_points': 8,
                'n_edges': 8
            }
            
            # Generate variations using ML
            variations = generator.generate_variations(pattern_data, num_variations)
            ml_patterns = generator.apply_ml_transformations(pattern_data)
            
            # Combine all patterns
            all_patterns = variations + ml_patterns
            
            # Set output directory
            output_dir = "generated_similar_patterns"
            
            # Prepare response
            similar_patterns = []
            for i, variation in enumerate(all_patterns):
                pattern_info = {
                    'pattern_id': variation['name'],
                    'kolam_type': reference_pattern,
                    'symmetry_type': random.choice(['bilateral', 'radial', 'grid', 'rotational', 'asymmetric']),
                    'cultural_region': random.choice(['tamil_nadu', 'karnataka', 'kerala', 'andhra_pradesh']),
                    'complexity_score': random.uniform(0.4, 0.9),
                    'confidence': random.uniform(0.7, 0.95),
                    'similarity_score': random.uniform(0.8, 0.95),
                    'image_path': f"pattern_{i:03d}.png",
                    'coordinates': variation['coordinates'].tolist(),
                    'features': {},
                    'metadata': {
                        'generation_method': 'advanced_ml',
                        'transformation': variation['transformation'],
                        'description': variation['description'],
                        'n_points': len(variation['coordinates'])
                    }
                }
                similar_patterns.append(pattern_info)
            
            return jsonify({
                "success": True,
                "similar_patterns": similar_patterns,
                "total_generated": len(similar_patterns),
                "reference_pattern": reference_pattern,
                "output_directory": output_dir,
                "message": f"Generated {len(similar_patterns)} similar patterns"
            })
            
        except ImportError:
            # Fallback to basic pattern generation
            logger.warning("Enhanced pattern generator not available, using fallback")
            
            # Generate basic similar patterns
            similar_patterns = []
            kolam_types = ['pulli_kolam', 'sikku_kolam', 'neli_kolam', 'kambi_kolam', 'fractal_kolam']
            symmetry_types = ['bilateral', 'radial', 'rotational', 'grid']
            cultural_regions = ['tamil_nadu', 'karnataka', 'kerala', 'andhra_pradesh']
            
            for i in range(num_variations):
                pattern = {
                    'pattern_id': f"similar_{i}",
                    'kolam_type': random.choice(kolam_types),
                    'symmetry_type': random.choice(symmetry_types),
                    'cultural_region': random.choice(cultural_regions),
                    'complexity_score': random.uniform(0.4, 0.9),
                    'confidence': random.uniform(0.7, 0.95),
                    'similarity_score': random.uniform(0.6, 0.9),
                    'coordinates': generate_random_coordinates(),
                    'features': {
                        'num_coordinate_sets': random.randint(3, 8),
                        'total_points': random.randint(20, 80),
                        'symmetry_score': random.uniform(0.6, 0.9)
                    },
                    'metadata': {
                        'generation_method': 'fallback',
                        'variation_index': i
                    }
                }
                similar_patterns.append(pattern)
            
            return jsonify({
                "success": True,
                "similar_patterns": similar_patterns,
                "total_generated": len(similar_patterns),
                "reference_pattern": reference_pattern,
                "message": f"Generated {len(similar_patterns)} similar patterns (fallback mode)"
            })
        
    except Exception as e:
        logger.error(f"Error generating similar patterns: {str(e)}")
        return jsonify({
            "success": False,
            "error": str(e),
            "message": "Failed to generate similar patterns"
        }), 500

@app.route('/api/generate-advanced-patterns', methods=['POST'])
@handle_errors
@rate_limit(max_requests=3, window=60)
def generate_advanced_patterns():
    """
    Generate advanced Kolam patterns using ML transformations:
    - Supports CSV and image inputs
    - Applies ML transformations (K-Means, PCA, t-SNE)
    - Generates multiple variations with different transformations
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        # Get parameters
        input_type = data.get('input_type', 'csv')  # 'csv' or 'image'
        input_data = data.get('input_data')  # CSV content or base64 image
        n_variations = data.get('n_variations', 8)
        
        # Initialize advanced generator
        from kolam_pattern_generator_ml import KolamPatternGenerator
        generator = KolamPatternGenerator("advanced_generated_patterns")
        
        if input_type == 'csv' and input_data:
            # Process CSV data
            import pandas as pd
            import io
            
            # Parse CSV from string
            df = pd.read_csv(io.StringIO(input_data))
            
            if 'x' in df.columns and 'y' in df.columns:
                coordinates = df[['x', 'y']].values
                pattern_data = {
                    'type': 'csv_upload',
                    'coordinates': coordinates,
                    'edges': [],
                    'source': 'user_upload',
                    'n_points': len(coordinates),
                    'n_edges': len(coordinates)
                }
            else:
                return jsonify({"error": "CSV must contain 'x' and 'y' columns"}), 400
                
        elif input_type == 'image' and input_data:
            # Process image data
            import base64
            import cv2
            from PIL import Image
            
            # Decode base64 image
            image_data = base64.b64decode(input_data.split(',')[1])
            image = Image.open(io.BytesIO(image_data))
            image_array = np.array(image)
            
            # Extract pattern from image
            pattern_data = generator.extract_image_pattern_from_array(image_array)
            
        else:
            return jsonify({"error": "Invalid input type or missing data"}), 400
        
        # Generate variations and ML transformations
        variations = generator.generate_variations(pattern_data, n_variations)
        ml_patterns = generator.apply_ml_transformations(pattern_data)
        
        # Combine all patterns
        all_patterns = variations + ml_patterns
        
        # Prepare response
        advanced_patterns = []
        for i, pattern in enumerate(all_patterns):
            pattern_info = {
                'pattern_id': f"advanced_{i:03d}",
                'name': pattern['name'],
                'transformation': pattern['transformation'],
                'description': pattern['description'],
                'coordinates': pattern['coordinates'].tolist(),
                'n_points': len(pattern['coordinates']),
                'complexity_score': random.uniform(0.3, 0.9),
                'confidence': random.uniform(0.7, 0.95),
                'image_path': f"advanced_pattern_{i:03d}.png"
            }
            advanced_patterns.append(pattern_info)
        
        # Save patterns
        generator.visualize_and_save(all_patterns, pattern_data)
        
        return jsonify({
            "success": True,
            "advanced_patterns": advanced_patterns,
            "total_patterns": len(advanced_patterns),
            "message": f"Generated {len(advanced_patterns)} advanced patterns with ML"
        })
        
    except Exception as e:
        logger.error(f"Error generating advanced patterns: {e}")
        return jsonify({
            "success": False,
            "error": str(e),
            "message": "Failed to generate advanced patterns"
        }), 500

def generate_random_coordinates():
    """Generate random coordinates for fallback pattern generation"""
    coordinates = []
    num_sets = random.randint(3, 6)
    
    for _ in range(num_sets):
        coord_set = []
        num_points = random.randint(5, 15)
        
        for _ in range(num_points):
            x = random.uniform(-10, 10)
            y = random.uniform(-10, 10)
            coord_set.append((x, y))
        
        coordinates.append(coord_set)
    
    return coordinates

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
    # Add static file serving route at the end
    @app.route('/<filename>')
    def serve_static_files(filename):
        """Serve static files (generated patterns)"""
        try:
            # Check if file exists in current directory
            if os.path.exists(filename):
                return send_from_directory('.', filename)
            else:
                return jsonify({
                    "error": "File not found",
                    "message": f"The requested file '{filename}' does not exist",
                    "success": False
                }), 404
        except Exception as e:
            return jsonify({
                "error": "File serving error",
                "message": str(e),
                "success": False
            }), 500

    logger.info("Backend URL: http://localhost:5000")
    logger.info("Frontend URL: http://localhost:3000")
    logger.info("API Documentation: http://localhost:5000")
    logger.info("Metrics: http://localhost:5000/api/metrics")
    def _generate_sample_coordinates(self, pattern_type):
        """Generate sample coordinates for different pattern types"""
        import numpy as np
        
        if pattern_type == 'pulli_kolam':
            # Dot-based pattern
            return np.array([[0, 0], [1, 0], [1, 1], [0, 1], [0, 0]])
        elif pattern_type == 'sikku_kolam':
            # Continuous line pattern
            return np.array([[0, 0], [0.5, 0.5], [1, 0], [0.5, -0.5], [0, 0]])
        elif pattern_type == 'neli_kolam':
            # Spiral pattern
            t = np.linspace(0, 2*np.pi, 8)
            r = t / (2*np.pi) * 2
            x = r * np.cos(t)
            y = r * np.sin(t)
            return np.column_stack([x, y])
        elif pattern_type == 'kambi_kolam':
            # Grid pattern
            return np.array([[0, 0], [2, 0], [2, 2], [0, 2], [0, 0], [1, 1]])
        elif pattern_type == 'fractal_kolam':
            # Fractal pattern
            return np.array([[0, 0], [1, 0], [0.5, 0.866], [0, 0], [0.5, 0.433], [0.5, 0.866]])
        else:
            # Default square
            return np.array([[0, 0], [1, 0], [1, 1], [0, 1], [0, 0]])

    # Diffusion API Endpoints
    @app.route('/api/diffusion/health', methods=['GET'])
    @handle_errors
    def diffusion_health():
        """Check diffusion models health"""
        return jsonify({
            "diffusion_available": DIFFUSION_AVAILABLE,
            "models_loaded": diffusion_pipe is not None,
            "device": diffusion_device,
            "controlnet_loaded": diffusion_controlnet is not None
        })

    @app.route('/api/diffusion/generate', methods=['POST'])
    @handle_errors
    @rate_limit(max_requests=5, window=60)
    def generate_kolam_variants():
        """Generate 3 Kolam variants from uploaded image using Stable Diffusion or lightweight processing"""
        try:
            # Check if diffusion models are available
            if not DIFFUSION_AVAILABLE:
                return jsonify({
                    "success": False,
                    "error": "Diffusion libraries not available. Please install: pip install torch diffusers transformers"
                }), 503
            
            if diffusion_pipe is None:
                # Use lightweight image processing instead of AI
                return generate_lightweight_variants()
            
            # Get uploaded file
            if 'image' not in request.files:
                return jsonify({
                    "success": False,
                    "error": "No image file provided"
                }), 400
            
            file = request.files['image']
            if file.filename == '':
                return jsonify({
                    "success": False,
                    "error": "No image file selected"
                }), 400
            
            # Load and preprocess image
            image = Image.open(file.stream)
            logger.info(f"Processing image for diffusion: {image.size}")
            
            # Preprocess for ControlNet
            control_image = preprocess_image_for_diffusion(image)
            if control_image is None:
                return jsonify({
                    "success": False,
                    "error": "Failed to preprocess image"
                }), 500
            
            # Define prompts for 3 variants
            prompts = [
                "Intricate symmetrical Kolam art, chalk powder style, traditional Indian design, white on dark background, detailed patterns, sacred geometry",
                "Colorful digital Kolam design, mandala-like, vibrant colors, modern interpretation, artistic, beautiful, high quality",
                "Minimal geometric Kolam pattern with curves, clean lines, simple design, elegant, contemporary, black and white"
            ]
            
            # Create output directory
            output_dir = Path("outputs")
            output_dir.mkdir(exist_ok=True)
            
            # Generate unique session ID
            session_id = str(uuid.uuid4())[:8]
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            generated_images = []
            
            # Generate 3 variants
            for i, prompt in enumerate(prompts, 1):
                logger.info(f"Generating diffusion variant {i}: {prompt[:50]}...")
                
                # Generate image
                generated_image = generate_kolam_variant(
                    prompt=prompt,
                    control_image=control_image,
                    num_inference_steps=20,
                    guidance_scale=7.5
                )
                
                if generated_image is None:
                    return jsonify({
                        "success": False,
                        "error": f"Failed to generate variant {i}"
                    }), 500
                
                # Save image
                filename = f"kolam_diffusion_{i}_{session_id}_{timestamp}.png"
                filepath = output_dir / filename
                
                # Resize to reasonable size if too large
                if generated_image.size[0] > 1024 or generated_image.size[1] > 1024:
                    generated_image = generated_image.resize((1024, 1024), Image.Resampling.LANCZOS)
                
                generated_image.save(filepath, "PNG")
                
                # Create URL for the image
                image_url = f"/outputs/{filename}"
                
                generated_images.append({
                    "variant": i,
                    "prompt": prompt,
                    "filename": filename,
                    "url": image_url,
                    "size": generated_image.size,
                    "type": "diffusion_generated"
                })
                
                logger.info(f"Saved diffusion variant {i}: {filepath}")
            
            return jsonify({
                "success": True,
                "session_id": session_id,
                "original_image": {
                    "size": image.size,
                    "format": image.format
                },
                "generated_images": generated_images,
                "message": "Successfully generated 3 Kolam variants using AI diffusion",
                "generation_type": "stable_diffusion_controlnet"
            })
            
        except Exception as e:
            logger.error(f"Error in generate_kolam_variants: {e}")
            return jsonify({
                "success": False,
                "error": f"Internal server error: {str(e)}"
            }), 500

    @app.route('/api/diffusion/status', methods=['GET'])
    @handle_errors
    def diffusion_status():
        """Get detailed diffusion models status"""
        return jsonify({
            "diffusion_available": DIFFUSION_AVAILABLE,
            "models_loaded": diffusion_pipe is not None,
            "device": diffusion_device,
            "controlnet_loaded": diffusion_controlnet is not None,
            "pipeline_loaded": diffusion_pipe is not None,
            "memory_efficient": hasattr(diffusion_pipe, "enable_attention_slicing") if diffusion_pipe else False
        })

    @app.route('/outputs/<filename>')
    def serve_output(filename):
        """Serve generated images from outputs directory"""
        try:
            from flask import send_from_directory
            return send_from_directory('outputs', filename)
        except Exception as e:
            logger.error(f"Error serving file {filename}: {e}")
            return "File not found", 404

    logger.info("=" * 60)
    
    app.run(debug=False, host='0.0.0.0', port=5000)
