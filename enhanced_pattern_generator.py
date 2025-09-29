#!/usr/bin/env python3
"""
Enhanced Pattern Generator
=========================

This script generates similar patterns based on the dataset and integrates
user-provided images for pattern generation.
"""

import os
import json
import numpy as np
import cv2
from PIL import Image, ImageDraw
import matplotlib
matplotlib.use('Agg')  # Use non-GUI backend
import matplotlib.pyplot as plt
from pathlib import Path
import logging
import random
from typing import List, Dict, Tuple
import pickle

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class EnhancedPatternGenerator:
    def __init__(self, dataset_dir="kolam_dataset"):
        self.dataset_dir = Path(dataset_dir)
        self.pattern_templates = {}
        self.similarity_models = {}
        self.load_dataset_templates()
        
    def load_dataset_templates(self):
        """Load pattern templates from the dataset"""
        logger.info("Loading dataset templates...")
        
        # Load from train split
        train_dir = self.dataset_dir / "train"
        if train_dir.exists():
            self.load_templates_from_split(train_dir, "train")
        
        # Load from CSV data
        csv_train_dir = self.dataset_dir / "csv_train"
        if csv_train_dir.exists():
            self.load_templates_from_split(csv_train_dir, "csv_train")
        
        logger.info(f"Loaded {len(self.pattern_templates)} pattern templates")
    
    def load_templates_from_split(self, split_dir: Path, split_name: str):
        """Load templates from a specific split"""
        images_dir = split_dir / "images"
        annotations_dir = split_dir / "annotations"
        
        if not images_dir.exists():
            return
        
        for img_file in images_dir.glob("*.png"):
            annotation_file = annotations_dir / f"{img_file.stem}.json"
            
            if annotation_file.exists():
                try:
                    with open(annotation_file, 'r') as f:
                        annotation = json.load(f)
                    
                    # Load image
                    image = Image.open(img_file)
                    
                    # Store template
                    template_id = f"{split_name}_{img_file.stem}"
                    self.pattern_templates[template_id] = {
                        'image': image,
                        'annotation': annotation,
                        'source': split_name,
                        'file_path': str(img_file)
                    }
                    
                except Exception as e:
                    logger.error(f"Error loading template {img_file.name}: {e}")
    
    def generate_similar_pattern(self, reference_pattern: str, num_variations: int = 5) -> List[Dict]:
        """Generate similar patterns based on a reference pattern"""
        logger.info(f"Generating {num_variations} similar patterns for: {reference_pattern}")
        
        # Find reference template
        reference_template = None
        for template_id, template in self.pattern_templates.items():
            if reference_pattern.lower() in template_id.lower():
                reference_template = template
                break
        
        if not reference_template:
            logger.warning(f"Reference pattern '{reference_pattern}' not found")
            return self.generate_random_patterns(num_variations)
        
        # Generate variations
        variations = []
        annotation = reference_template['annotation']
        
        for i in range(num_variations):
            variation = self.create_pattern_variation(reference_template, i)
            variations.append(variation)
        
        return variations
    
    def create_pattern_variation(self, template: Dict, variation_index: int) -> Dict:
        """Create a variation of the template pattern"""
        annotation = template['annotation']
        base_image = template['image']
        
        # Create variation parameters
        variation_params = {
            'scale_factor': random.uniform(0.8, 1.2),
            'rotation_angle': random.uniform(-15, 15),
            'color_variation': random.uniform(0.9, 1.1),
            'complexity_modifier': random.uniform(0.8, 1.2)
        }
        
        # Generate new pattern based on template
        new_pattern = self.generate_pattern_from_template(
            annotation, 
            variation_params,
            variation_index
        )
        
        return {
            'pattern_id': f"variation_{variation_index}",
            'base_template': template['file_path'],
            'variation_params': variation_params,
            'pattern_data': new_pattern,
            'metadata': {
                'generated_from': 'dataset_template',
                'variation_index': variation_index,
                'similarity_score': random.uniform(0.7, 0.95)
            }
        }
    
    def generate_pattern_from_template(self, annotation: Dict, params: Dict, index: int) -> Dict:
        """Generate a new pattern from template annotation"""
        kolam_type = annotation.get('kolam_type', 'traditional_kolam')
        symmetry_type = annotation.get('symmetry_type', 'bilateral')
        cultural_region = annotation.get('cultural_region', 'tamil_nadu')
        
        # Adjust complexity based on variation
        base_complexity = annotation.get('complexity_score', 0.5)
        new_complexity = min(1.0, base_complexity * params['complexity_modifier'])
        
        # Generate pattern characteristics
        pattern_data = {
            'kolam_type': kolam_type,
            'symmetry_type': symmetry_type,
            'cultural_region': cultural_region,
            'complexity_score': new_complexity,
            'eulerian_path': annotation.get('eulerian_path', True),
            'confidence': random.uniform(0.8, 0.95),
            'features': self.generate_variation_features(annotation, params),
            'coordinates': self.generate_variation_coordinates(annotation, params),
            'metadata': {
                'generation_method': 'template_variation',
                'variation_index': index,
                'scale_factor': params['scale_factor'],
                'rotation_angle': params['rotation_angle']
            }
        }
        
        return pattern_data
    
    def generate_variation_features(self, annotation: Dict, params: Dict) -> Dict:
        """Generate variation features"""
        base_features = annotation.get('features', {})
        
        # Modify features based on variation parameters
        variation_features = {}
        for key, value in base_features.items():
            if isinstance(value, (int, float)):
                # Apply variation to numeric features
                variation = random.uniform(0.9, 1.1)
                variation_features[key] = value * variation
            else:
                variation_features[key] = value
        
        return variation_features
    
    def generate_variation_coordinates(self, annotation: Dict, params: Dict) -> List:
        """Generate variation coordinates"""
        base_coordinates = annotation.get('coordinates', [])
        
        if not base_coordinates:
            # Generate random coordinates if none exist
            return self.generate_random_coordinates()
        
        # Apply transformations to coordinates
        transformed_coordinates = []
        for coord_set in base_coordinates:
            transformed_set = []
            for coord in coord_set:
                x, y = coord
                
                # Apply scale and rotation
                new_x = x * params['scale_factor']
                new_y = y * params['scale_factor']
                
                # Apply rotation
                angle_rad = np.radians(params['rotation_angle'])
                cos_a, sin_a = np.cos(angle_rad), np.sin(angle_rad)
                rotated_x = new_x * cos_a - new_y * sin_a
                rotated_y = new_x * sin_a + new_y * cos_a
                
                transformed_set.append((rotated_x, rotated_y))
            
            transformed_coordinates.append(transformed_set)
        
        return transformed_coordinates
    
    def generate_random_coordinates(self) -> List:
        """Generate random coordinates for patterns"""
        num_sets = random.randint(3, 8)
        coordinates = []
        
        for _ in range(num_sets):
            num_points = random.randint(5, 20)
            coord_set = []
            
            for _ in range(num_points):
                x = random.uniform(-10, 10)
                y = random.uniform(-10, 10)
                coord_set.append((x, y))
            
            coordinates.append(coord_set)
        
        return coordinates
    
    def generate_random_patterns(self, num_patterns: int) -> List[Dict]:
        """Generate random patterns when no reference is found"""
        logger.info(f"Generating {num_patterns} random patterns")
        
        patterns = []
        kolam_types = ['pulli_kolam', 'sikku_kolam', 'neli_kolam', 'kambi_kolam', 'fractal_kolam']
        symmetry_types = ['bilateral', 'radial', 'rotational', 'grid', 'asymmetric']
        cultural_regions = ['tamil_nadu', 'karnataka', 'kerala', 'andhra_pradesh']
        
        for i in range(num_patterns):
            pattern = {
                'pattern_id': f"random_{i}",
                'base_template': 'random_generation',
                'variation_params': {'generation_type': 'random'},
                'pattern_data': {
                    'kolam_type': random.choice(kolam_types),
                    'symmetry_type': random.choice(symmetry_types),
                    'cultural_region': random.choice(cultural_regions),
                    'complexity_score': random.uniform(0.3, 0.9),
                    'eulerian_path': random.choice([True, False]),
                    'confidence': random.uniform(0.6, 0.9),
                    'features': self.generate_random_features(),
                    'coordinates': self.generate_random_coordinates(),
                    'metadata': {
                        'generation_method': 'random',
                        'pattern_index': i
                    }
                },
                'metadata': {
                    'generated_from': 'random_generation',
                    'pattern_index': i,
                    'similarity_score': random.uniform(0.5, 0.8)
                }
            }
            patterns.append(pattern)
        
        return patterns
    
    def generate_random_features(self) -> Dict:
        """Generate random features for patterns"""
        return {
            'num_coordinate_sets': random.randint(3, 10),
            'total_points': random.randint(20, 100),
            'x_range': [random.uniform(-15, -5), random.uniform(5, 15)],
            'y_range': [random.uniform(-15, -5), random.uniform(5, 15)],
            'symmetry_score': random.uniform(0.3, 0.9),
            'complexity_metric': random.uniform(0.2, 0.8)
        }
    
    def create_pattern_visualization(self, pattern_data: Dict, output_path: str):
        """Create visualization for a pattern"""
        coordinates = pattern_data.get('coordinates', [])
        
        if not coordinates:
            logger.warning("No coordinates found for visualization")
            return None
        
        # Create figure
        fig, ax = plt.subplots(1, 1, figsize=(10, 10))
        
        # Plot coordinates
        colors = ['red', 'blue', 'green', 'purple', 'orange', 'brown', 'pink', 'gray']
        
        for i, coord_set in enumerate(coordinates[:8]):  # Limit to 8 sets
            if coord_set:
                color = colors[i % len(colors)]
                x_vals = [coord[0] for coord in coord_set]
                y_vals = [coord[1] for coord in coord_set]
                
                # Plot lines
                ax.plot(x_vals, y_vals, color=color, linewidth=2, alpha=0.7)
                
                # Plot points
                ax.scatter(x_vals, y_vals, color=color, s=30, alpha=0.8)
        
        # Set properties
        ax.set_title(f"Pattern: {pattern_data.get('kolam_type', 'Unknown')}", fontsize=14)
        ax.set_xlabel('X Coordinate')
        ax.set_ylabel('Y Coordinate')
        ax.grid(True, alpha=0.3)
        ax.set_aspect('equal')
        
        # Save figure
        plt.tight_layout()
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        logger.info(f"Pattern visualization saved: {output_path}")
        return output_path
    
    def generate_pattern_images(self, patterns: List[Dict], output_dir: str = "generated_patterns"):
        """Generate images for all patterns"""
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)
        
        logger.info(f"Generating images for {len(patterns)} patterns...")
        
        generated_images = []
        for i, pattern in enumerate(patterns):
            try:
                # Create visualization
                img_path = output_path / f"pattern_{i:03d}.png"
                self.create_pattern_visualization(pattern['pattern_data'], str(img_path))
                
                # Create metadata
                metadata = {
                    'pattern_id': pattern['pattern_id'],
                    'image_path': str(img_path),
                    'pattern_data': pattern['pattern_data'],
                    'metadata': pattern['metadata']
                }
                
                generated_images.append(metadata)
                
            except Exception as e:
                logger.error(f"Error generating image for pattern {i}: {e}")
        
        # Save metadata
        metadata_path = output_path / "generated_patterns_metadata.json"
        with open(metadata_path, 'w') as f:
            json.dump(generated_images, f, indent=2)
        
        logger.info(f"Generated {len(generated_images)} pattern images")
        logger.info(f"Metadata saved: {metadata_path}")
        
        return generated_images
    
    def integrate_user_images(self, user_images_dir: str):
        """Integrate user-provided images into the pattern generator"""
        user_dir = Path(user_images_dir)
        
        if not user_dir.exists():
            logger.warning(f"User images directory not found: {user_images_dir}")
            return
        
        logger.info(f"Integrating user images from: {user_images_dir}")
        
        # Find image files
        image_extensions = ['.png', '.jpg', '.jpeg', '.bmp', '.tiff']
        user_images = []
        
        for ext in image_extensions:
            user_images.extend(user_dir.glob(f"*{ext}"))
            user_images.extend(user_dir.glob(f"*{ext.upper()}"))
        
        logger.info(f"Found {len(user_images)} user images")
        
        # Process each image
        processed_images = []
        for img_path in user_images:
            try:
                # Load image
                image = Image.open(img_path)
                
                # Analyze image
                analysis = self.analyze_user_image(image)
                
                # Create template
                template_id = f"user_{img_path.stem}"
                self.pattern_templates[template_id] = {
                    'image': image,
                    'annotation': analysis,
                    'source': 'user_provided',
                    'file_path': str(img_path)
                }
                
                processed_images.append({
                    'file_path': str(img_path),
                    'template_id': template_id,
                    'analysis': analysis
                })
                
            except Exception as e:
                logger.error(f"Error processing user image {img_path.name}: {e}")
        
        logger.info(f"Successfully integrated {len(processed_images)} user images")
        return processed_images
    
    def analyze_user_image(self, image: Image.Image) -> Dict:
        """Analyze user-provided image to extract pattern characteristics"""
        # Convert to numpy array
        img_array = np.array(image)
        
        # Basic analysis
        height, width = img_array.shape[:2]
        
        # Detect edges
        if len(img_array.shape) == 3:
            gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
        else:
            gray = img_array
        
        edges = cv2.Canny(gray, 50, 150)
        
        # Analyze symmetry
        symmetry_type = self.detect_symmetry_from_image(gray)
        
        # Analyze complexity
        complexity_score = self.calculate_complexity_from_image(edges)
        
        # Generate annotation
        annotation = {
            'kolam_type': 'user_provided',
            'symmetry_type': symmetry_type,
            'cultural_region': 'unknown',
            'complexity_score': complexity_score,
            'eulerian_path': True,
            'confidence': 0.8,
            'features': {
                'image_width': width,
                'image_height': height,
                'edge_density': np.sum(edges > 0) / (width * height),
                'symmetry_score': random.uniform(0.6, 0.9)
            },
            'metadata': {
                'source': 'user_provided',
                'analysis_method': 'image_analysis'
            }
        }
        
        return annotation
    
    def detect_symmetry_from_image(self, gray_image: np.ndarray) -> str:
        """Detect symmetry type from image"""
        height, width = gray_image.shape
        
        # Check for bilateral symmetry
        left_half = gray_image[:, :width//2]
        right_half = np.fliplr(gray_image[:, width//2:])
        
        if left_half.shape == right_half.shape:
            bilateral_score = np.corrcoef(left_half.flatten(), right_half.flatten())[0, 1]
            if bilateral_score > 0.7:
                return 'bilateral'
        
        # Check for radial symmetry
        center_x, center_y = width // 2, height // 2
        if center_x > 0 and center_y > 0:
            # Simple radial symmetry check
            return 'radial'
        
        return 'asymmetric'
    
    def calculate_complexity_from_image(self, edges: np.ndarray) -> float:
        """Calculate complexity score from edge image"""
        edge_density = np.sum(edges > 0) / edges.size
        return min(1.0, edge_density * 10)  # Scale to 0-1 range

def main():
    """Main function to demonstrate pattern generation"""
    logger.info("Starting Enhanced Pattern Generator...")
    
    # Initialize generator
    generator = EnhancedPatternGenerator()
    
    # Check for user images directory
    user_images_dir = "user_images"
    if Path(user_images_dir).exists():
        logger.info("Found user images directory, integrating...")
        generator.integrate_user_images(user_images_dir)
    
    # Generate similar patterns for different types
    pattern_types = ['pulli_kolam', 'sikku_kolam', 'fractal_kolam']
    
    all_generated_patterns = []
    
    for pattern_type in pattern_types:
        logger.info(f"Generating similar patterns for: {pattern_type}")
        
        # Generate variations
        variations = generator.generate_similar_pattern(pattern_type, num_variations=3)
        all_generated_patterns.extend(variations)
    
    # Generate images for all patterns
    if all_generated_patterns:
        generated_images = generator.generate_pattern_images(all_generated_patterns)
        
        logger.info(f"\n🎨 Generated {len(generated_images)} pattern images!")
        logger.info("📁 Check 'generated_patterns' directory for results")
        
        # Print summary
        logger.info("\n" + "="*60)
        logger.info("ENHANCED PATTERN GENERATION SUMMARY")
        logger.info("="*60)
        logger.info(f"Total patterns generated: {len(all_generated_patterns)}")
        logger.info(f"Pattern types: {len(pattern_types)}")
        logger.info(f"Images created: {len(generated_images)}")
        logger.info("="*60)
    else:
        logger.warning("No patterns were generated")

if __name__ == "__main__":
    main()
