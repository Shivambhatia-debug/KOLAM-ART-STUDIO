#!/usr/bin/env python3
"""
Advanced Kolam Pattern Generator with ML
========================================

A comprehensive system for generating Kolam patterns with machine learning
transformations, supporting both image uploads and CSV data sources.

Author: AI Assistant
Date: 2025
Purpose: SIH Presentation - Advanced Pattern Generation
"""

import cv2
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import Circle, Polygon
import networkx as nx
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
from sklearn.preprocessing import StandardScaler
import os
import json
import random
from typing import List, Tuple, Dict, Any, Optional
import argparse
from pathlib import Path

# Set matplotlib backend
import matplotlib
matplotlib.use('Agg')

class KolamPatternGenerator:
    """Advanced Kolam Pattern Generator with ML capabilities"""
    
    def __init__(self, output_dir: str = "generated_kolam_patterns"):
        """Initialize the generator"""
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        # Create subdirectories
        (self.output_dir / "images").mkdir(exist_ok=True)
        (self.output_dir / "csv").mkdir(exist_ok=True)
        (self.output_dir / "metadata").mkdir(exist_ok=True)
        
        self.patterns = []
        self.metadata = {}
        
    def load_csv_pattern(self, csv_path: str) -> Dict[str, Any]:
        """
        Load Kolam pattern from CSV file
        
        Args:
            csv_path: Path to CSV file containing coordinates or edges
            
        Returns:
            Dictionary containing pattern data
        """
        print(f"📊 Loading CSV pattern from: {csv_path}")
        
        try:
            df = pd.read_csv(csv_path)
            print(f"   Columns: {list(df.columns)}")
            print(f"   Shape: {df.shape}")
            
            # Determine if it's coordinates or edges
            if 'x' in df.columns and 'y' in df.columns:
                # Coordinate-based pattern
                coordinates = df[['x', 'y']].values
                pattern_type = "coordinates"
                print(f"   Pattern type: Coordinate-based ({len(coordinates)} points)")
                
                # Create edges by connecting consecutive points
                edges = []
                for i in range(len(coordinates) - 1):
                    edges.append((i, i + 1))
                
                # Close the pattern if first and last points are close
                if np.linalg.norm(coordinates[0] - coordinates[-1]) < 0.1:
                    edges.append((len(coordinates) - 1, 0))
                
            elif 'source' in df.columns and 'target' in df.columns:
                # Edge-based pattern
                edges = [(row['source'], row['target']) for _, row in df.iterrows()]
                pattern_type = "edges"
                print(f"   Pattern type: Edge-based ({len(edges)} edges)")
                
                # Extract unique coordinates from edges
                all_nodes = set()
                for edge in edges:
                    all_nodes.add(edge[0])
                    all_nodes.add(edge[1])
                
                # Generate coordinates for nodes (simple grid layout)
                n_nodes = len(all_nodes)
                side = int(np.ceil(np.sqrt(n_nodes)))
                coordinates = []
                for i in range(n_nodes):
                    x = (i % side) * 2
                    y = (i // side) * 2
                    coordinates.append([x, y])
                
            else:
                raise ValueError("CSV must contain either (x,y) columns or (source,target) columns")
            
            pattern_data = {
                'type': pattern_type,
                'coordinates': np.array(coordinates),
                'edges': edges,
                'source': csv_path,
                'n_points': len(coordinates),
                'n_edges': len(edges)
            }
            
            print(f"✅ Successfully loaded CSV pattern")
            return pattern_data
            
        except Exception as e:
            print(f"❌ Error loading CSV: {e}")
            raise
    
    def extract_image_pattern(self, image_path: str) -> Dict[str, Any]:
        """
        Extract Kolam pattern from uploaded image
        
        Args:
            image_path: Path to uploaded image
            
        Returns:
            Dictionary containing extracted pattern data
        """
        print(f"🖼️ Extracting pattern from image: {image_path}")
        
        try:
            # Load image
            image = cv2.imread(image_path)
            if image is None:
                raise ValueError(f"Could not load image: {image_path}")
            
            # Convert to grayscale
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            
            # Apply threshold
            _, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY_INV)
            
            # Find contours
            contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            if not contours:
                raise ValueError("No contours found in image")
            
            # Get the largest contour
            largest_contour = max(contours, key=cv2.contourArea)
            
            # Simplify contour
            epsilon = 0.02 * cv2.arcLength(largest_contour, True)
            simplified = cv2.approxPolyDP(largest_contour, epsilon, True)
            
            # Extract coordinates
            coordinates = simplified.reshape(-1, 2).astype(float)
            
            # Normalize coordinates
            coordinates = self._normalize_coordinates(coordinates)
            
            # Create edges by connecting consecutive points
            edges = []
            for i in range(len(coordinates) - 1):
                edges.append((i, i + 1))
            
            # Close the pattern
            edges.append((len(coordinates) - 1, 0))
            
            # Skeletonize for motif extraction
            skeleton = self._skeletonize(binary)
            
            pattern_data = {
                'type': 'image_extracted',
                'coordinates': coordinates,
                'edges': edges,
                'source': image_path,
                'n_points': len(coordinates),
                'n_edges': len(edges),
                'original_image': image,
                'processed_image': binary,
                'skeleton': skeleton
            }
            
            print(f"✅ Successfully extracted pattern ({len(coordinates)} points)")
            return pattern_data
            
        except Exception as e:
            print(f"❌ Error extracting image pattern: {e}")
            raise
    
    def _normalize_coordinates(self, coordinates: np.ndarray) -> np.ndarray:
        """Normalize coordinates to unit scale"""
        if len(coordinates) == 0:
            return coordinates
        
        # Center coordinates
        center = np.mean(coordinates, axis=0)
        centered = coordinates - center
        
        # Scale to unit size
        max_dist = np.max(np.linalg.norm(centered, axis=1))
        if max_dist > 0:
            normalized = centered / max_dist
        else:
            normalized = centered
        
        return normalized
    
    def _skeletonize(self, binary_image: np.ndarray) -> np.ndarray:
        """Extract skeleton from binary image"""
        # Use morphological operations for skeletonization
        kernel = np.ones((3,3), np.uint8)
        
        # Erosion and dilation
        eroded = cv2.erode(binary_image, kernel, iterations=1)
        dilated = cv2.dilate(eroded, kernel, iterations=1)
        
        # Skeleton
        skeleton = cv2.subtract(binary_image, dilated)
        
        return skeleton
    
    def generate_variations(self, pattern_data: Dict[str, Any], n_variations: int = 8) -> List[Dict[str, Any]]:
        """
        Generate multiple variations of the pattern
        
        Args:
            pattern_data: Original pattern data
            n_variations: Number of variations to generate
            
        Returns:
            List of variation dictionaries
        """
        print(f"🎨 Generating {n_variations} pattern variations...")
        
        variations = []
        coordinates = pattern_data['coordinates']
        
        # 1. Original pattern
        variations.append({
            'name': 'original',
            'coordinates': coordinates.copy(),
            'transformation': 'none',
            'description': 'Original pattern'
        })
        
        # 2. Rotation variations
        for angle in [90, 180, 270]:
            rotated = self._rotate_coordinates(coordinates, angle)
            variations.append({
                'name': f'rotated_{angle}',
                'coordinates': rotated,
                'transformation': f'rotation_{angle}',
                'description': f'Rotated by {angle}°'
            })
        
        # 3. Reflection variations
        h_reflected = self._reflect_coordinates(coordinates, 'horizontal')
        v_reflected = self._reflect_coordinates(coordinates, 'vertical')
        
        variations.append({
            'name': 'reflected_horizontal',
            'coordinates': h_reflected,
            'transformation': 'reflection_horizontal',
            'description': 'Horizontal reflection'
        })
        
        variations.append({
            'name': 'reflected_vertical',
            'coordinates': v_reflected,
            'transformation': 'reflection_vertical',
            'description': 'Vertical reflection'
        })
        
        # 4. Scaling variations
        scaled_up = self._scale_coordinates(coordinates, 1.5)
        scaled_down = self._scale_coordinates(coordinates, 0.7)
        
        variations.append({
            'name': 'scaled_up',
            'coordinates': scaled_up,
            'transformation': 'scale_1.5',
            'description': 'Scaled up by 1.5x'
        })
        
        variations.append({
            'name': 'scaled_down',
            'coordinates': scaled_down,
            'transformation': 'scale_0.7',
            'description': 'Scaled down by 0.7x'
        })
        
        # 5. Tiling variations
        tiled_2x2 = self._tile_coordinates(coordinates, 2, 2)
        tiled_3x3 = self._tile_coordinates(coordinates, 3, 3)
        
        variations.append({
            'name': 'tiled_2x2',
            'coordinates': tiled_2x2,
            'transformation': 'tile_2x2',
            'description': '2x2 tiling'
        })
        
        variations.append({
            'name': 'tiled_3x3',
            'coordinates': tiled_3x3,
            'transformation': 'tile_3x3',
            'description': '3x3 tiling'
        })
        
        # 6. Random perturbations
        for i in range(3):
            perturbed = self._add_random_perturbation(coordinates, noise_level=0.1)
            variations.append({
                'name': f'perturbed_{i+1}',
                'coordinates': perturbed,
                'transformation': f'perturbation_{i+1}',
                'description': f'Random perturbation {i+1}'
            })
        
        # Limit to requested number
        variations = variations[:n_variations]
        
        print(f"✅ Generated {len(variations)} variations")
        return variations
    
    def _rotate_coordinates(self, coordinates: np.ndarray, angle: float) -> np.ndarray:
        """Rotate coordinates by given angle (in degrees)"""
        angle_rad = np.radians(angle)
        cos_a, sin_a = np.cos(angle_rad), np.sin(angle_rad)
        
        rotation_matrix = np.array([
            [cos_a, -sin_a],
            [sin_a, cos_a]
        ])
        
        return coordinates @ rotation_matrix.T
    
    def _reflect_coordinates(self, coordinates: np.ndarray, axis: str) -> np.ndarray:
        """Reflect coordinates across axis"""
        reflected = coordinates.copy()
        if axis == 'horizontal':
            reflected[:, 1] = -reflected[:, 1]
        elif axis == 'vertical':
            reflected[:, 0] = -reflected[:, 0]
        return reflected
    
    def _scale_coordinates(self, coordinates: np.ndarray, scale_factor: float) -> np.ndarray:
        """Scale coordinates by given factor"""
        return coordinates * scale_factor
    
    def _tile_coordinates(self, coordinates: np.ndarray, rows: int, cols: int) -> np.ndarray:
        """Create tiled pattern"""
        tiled = []
        spacing = 3.0  # Spacing between tiles
        
        for i in range(rows):
            for j in range(cols):
                offset = np.array([j * spacing, i * spacing])
                tiled_coords = coordinates + offset
                tiled.append(tiled_coords)
        
        return np.vstack(tiled)
    
    def _add_random_perturbation(self, coordinates: np.ndarray, noise_level: float = 0.1) -> np.ndarray:
        """Add random noise to coordinates"""
        noise = np.random.normal(0, noise_level, coordinates.shape)
        return coordinates + noise
    
    def apply_ml_transformations(self, pattern_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Apply machine learning transformations to the pattern
        
        Args:
            pattern_data: Original pattern data
            
        Returns:
            List of ML-transformed patterns
        """
        print("🤖 Applying ML transformations...")
        
        ml_patterns = []
        coordinates = pattern_data['coordinates']
        
        if len(coordinates) < 3:
            print("   ⚠️ Not enough points for ML transformations")
            return ml_patterns
        
        # 1. K-Means Clustering
        try:
            n_clusters = min(4, len(coordinates) // 2)
            if n_clusters >= 2:
                kmeans = KMeans(n_clusters=n_clusters, random_state=42)
                cluster_labels = kmeans.fit_predict(coordinates)
                
                # Reorganize by clusters
                clustered_coords = []
                for cluster_id in range(n_clusters):
                    cluster_points = coordinates[cluster_labels == cluster_id]
                    if len(cluster_points) > 0:
                        clustered_coords.append(cluster_points)
                
                if clustered_coords:
                    reorganized = np.vstack(clustered_coords)
                    ml_patterns.append({
                        'name': 'kmeans_reorganized',
                        'coordinates': reorganized,
                        'transformation': 'kmeans_clustering',
                        'description': f'K-Means clustering ({n_clusters} clusters)'
                    })
        except Exception as e:
            print(f"   ⚠️ K-Means failed: {e}")
        
        # 2. PCA Transformation
        try:
            if len(coordinates) >= 2:
                pca = PCA(n_components=2)
                pca_coords = pca.fit_transform(coordinates)
                
                ml_patterns.append({
                    'name': 'pca_transformed',
                    'coordinates': pca_coords,
                    'transformation': 'pca',
                    'description': f'PCA transformation (explained variance: {pca.explained_variance_ratio_.sum():.2f})'
                })
        except Exception as e:
            print(f"   ⚠️ PCA failed: {e}")
        
        # 3. t-SNE Transformation
        try:
            if len(coordinates) >= 4:
                tsne = TSNE(n_components=2, random_state=42, perplexity=min(30, len(coordinates)-1))
                tsne_coords = tsne.fit_transform(coordinates)
                
                ml_patterns.append({
                    'name': 'tsne_transformed',
                    'coordinates': tsne_coords,
                    'transformation': 'tsne',
                    'description': 't-SNE transformation'
                })
        except Exception as e:
            print(f"   ⚠️ t-SNE failed: {e}")
        
        # 4. Hybrid patterns (if we have multiple sources)
        if len(self.patterns) > 1:
            try:
                # Combine patterns from different sources
                all_coords = []
                for pattern in self.patterns[-2:]:  # Last 2 patterns
                    if 'coordinates' in pattern:
                        all_coords.append(pattern['coordinates'])
                
                if len(all_coords) >= 2:
                    # Create hybrid by averaging coordinates
                    min_len = min(len(coords) for coords in all_coords)
                    hybrid_coords = np.zeros((min_len, 2))
                    
                    for coords in all_coords:
                        hybrid_coords += coords[:min_len]
                    
                    hybrid_coords /= len(all_coords)
                    
                    ml_patterns.append({
                        'name': 'hybrid_fusion',
                        'coordinates': hybrid_coords,
                        'transformation': 'hybrid_fusion',
                        'description': 'Hybrid fusion of multiple patterns'
                    })
            except Exception as e:
                print(f"   ⚠️ Hybrid fusion failed: {e}")
        
        print(f"✅ Generated {len(ml_patterns)} ML transformations")
        return ml_patterns
    
    def visualize_and_save(self, patterns: List[Dict[str, Any]], pattern_data: Dict[str, Any]):
        """
        Visualize and save all patterns
        
        Args:
            patterns: List of pattern variations
            pattern_data: Original pattern data
        """
        print("🎨 Visualizing and saving patterns...")
        
        # Create subplot grid
        n_patterns = len(patterns)
        cols = 4
        rows = (n_patterns + cols - 1) // cols
        
        fig, axes = plt.subplots(rows, cols, figsize=(16, 4*rows))
        if rows == 1:
            axes = [axes] if cols == 1 else axes
        else:
            axes = axes.flatten()
        
        # Plot each pattern
        for i, pattern in enumerate(patterns):
            ax = axes[i]
            coords = pattern['coordinates']
            
            # Plot points
            ax.scatter(coords[:, 0], coords[:, 1], c='red', s=50, alpha=0.7, zorder=3)
            
            # Plot lines connecting points
            if len(coords) > 1:
                # Connect consecutive points
                for j in range(len(coords) - 1):
                    ax.plot([coords[j, 0], coords[j+1, 0]], 
                           [coords[j, 1], coords[j+1, 1]], 
                           'b-', linewidth=2, alpha=0.8)
                
                # Close the pattern
                ax.plot([coords[-1, 0], coords[0, 0]], 
                       [coords[-1, 1], coords[0, 1]], 
                       'b-', linewidth=2, alpha=0.8)
            
            # Formatting
            ax.set_title(f"{pattern['name']}\n{pattern['description']}", fontsize=10)
            ax.set_aspect('equal')
            ax.grid(True, alpha=0.3)
            ax.set_xlim(coords[:, 0].min() - 1, coords[:, 0].max() + 1)
            ax.set_ylim(coords[:, 1].min() - 1, coords[:, 1].max() + 1)
        
        # Hide unused subplots
        for i in range(n_patterns, len(axes)):
            axes[i].set_visible(False)
        
        plt.tight_layout()
        
        # Save combined visualization
        combined_path = self.output_dir / "images" / "all_patterns_combined.png"
        plt.savefig(combined_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        # Save individual patterns
        for pattern in patterns:
            self._save_individual_pattern(pattern)
        
        # Save CSV files
        self._save_csv_files(patterns)
        
        # Save metadata
        self._save_metadata(patterns, pattern_data)
        
        print(f"✅ Saved {len(patterns)} patterns to {self.output_dir}")
    
    def _save_individual_pattern(self, pattern: Dict[str, Any]):
        """Save individual pattern as PNG"""
        fig, ax = plt.subplots(figsize=(8, 8))
        coords = pattern['coordinates']
        
        # Plot points
        ax.scatter(coords[:, 0], coords[:, 1], c='red', s=100, alpha=0.8, zorder=3)
        
        # Plot lines
        if len(coords) > 1:
            for j in range(len(coords) - 1):
                ax.plot([coords[j, 0], coords[j+1, 0]], 
                       [coords[j, 1], coords[j+1, 1]], 
                       'b-', linewidth=3, alpha=0.8)
            
            ax.plot([coords[-1, 0], coords[0, 0]], 
                   [coords[-1, 1], coords[0, 1]], 
                   'b-', linewidth=3, alpha=0.8)
        
        ax.set_title(f"{pattern['name']} - {pattern['description']}", fontsize=14)
        ax.set_aspect('equal')
        ax.grid(True, alpha=0.3)
        ax.set_xlim(coords[:, 0].min() - 1, coords[:, 0].max() + 1)
        ax.set_ylim(coords[:, 1].min() - 1, coords[:, 1].max() + 1)
        
        # Save
        filename = f"{pattern['name']}.png"
        filepath = self.output_dir / "images" / filename
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        plt.close()
    
    def _save_csv_files(self, patterns: List[Dict[str, Any]]):
        """Save pattern coordinates as CSV files"""
        for pattern in patterns:
            coords = pattern['coordinates']
            
            # Create DataFrame
            df = pd.DataFrame(coords, columns=['x', 'y'])
            df['point_id'] = range(len(coords))
            
            # Save CSV
            filename = f"{pattern['name']}.csv"
            filepath = self.output_dir / "csv" / filename
            df.to_csv(filepath, index=False)
    
    def _save_metadata(self, patterns: List[Dict[str, Any]], pattern_data: Dict[str, Any]):
        """Save metadata about all patterns"""
        metadata = {
            'source_pattern': {
                'type': pattern_data['type'],
                'source': pattern_data['source'],
                'n_points': pattern_data['n_points'],
                'n_edges': pattern_data['n_edges']
            },
            'generated_patterns': [
                {
                    'name': p['name'],
                    'transformation': p['transformation'],
                    'description': p['description'],
                    'n_points': len(p['coordinates'])
                }
                for p in patterns
            ],
            'total_patterns': len(patterns),
            'output_directory': str(self.output_dir)
        }
        
        # Save as JSON
        metadata_path = self.output_dir / "metadata" / "pattern_metadata.json"
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2)
    
    def process_input(self, input_path: str, input_type: str = 'auto', n_variations: int = 8):
        """
        Main processing function
        
        Args:
            input_path: Path to input file (image or CSV)
            input_type: Type of input ('image', 'csv', or 'auto')
            n_variations: Number of variations to generate
        """
        print("🚀 Starting Kolam Pattern Generation with ML")
        print("=" * 60)
        
        # Determine input type
        if input_type == 'auto':
            if input_path.lower().endswith(('.png', '.jpg', '.jpeg')):
                input_type = 'image'
            elif input_path.lower().endswith('.csv'):
                input_type = 'csv'
            else:
                raise ValueError("Could not determine input type. Please specify 'image' or 'csv'")
        
        # Load pattern
        if input_type == 'image':
            pattern_data = self.extract_image_pattern(input_path)
        elif input_type == 'csv':
            pattern_data = self.load_csv_pattern(input_path)
        else:
            raise ValueError("Input type must be 'image' or 'csv'")
        
        # Store original pattern
        self.patterns.append(pattern_data)
        
        # Generate variations
        variations = self.generate_variations(pattern_data, n_variations)
        
        # Apply ML transformations
        ml_patterns = self.apply_ml_transformations(pattern_data)
        
        # Combine all patterns
        all_patterns = variations + ml_patterns
        
        # Visualize and save
        self.visualize_and_save(all_patterns, pattern_data)
        
        return all_patterns

def create_sample_csv():
    """Create a sample CSV file for testing"""
    print("📝 Creating sample CSV file...")
    
    # Create a simple square pattern
    coordinates = [
        [0, 0], [2, 0], [2, 2], [0, 2], [0, 0]  # Square
    ]
    
    df = pd.DataFrame(coordinates, columns=['x', 'y'])
    df.to_csv('sample_kolam.csv', index=False)
    print("✅ Created sample_kolam.csv")

def create_sample_image():
    """Create a sample image for testing"""
    print("🖼️ Creating sample image...")
    
    # Create a simple pattern image
    fig, ax = plt.subplots(figsize=(6, 6))
    
    # Draw a simple Kolam pattern
    # Outer circle
    circle1 = Circle((0, 0), 2, fill=False, linewidth=3, color='black')
    ax.add_patch(circle1)
    
    # Inner square
    square = Polygon([[-1, -1], [1, -1], [1, 1], [-1, 1]], 
                    fill=False, linewidth=3, color='black')
    ax.add_patch(square)
    
    # Center dot
    center_dot = Circle((0, 0), 0.2, color='black')
    ax.add_patch(center_dot)
    
    ax.set_xlim(-3, 3)
    ax.set_ylim(-3, 3)
    ax.set_aspect('equal')
    ax.axis('off')
    
    plt.savefig('sample_kolam.png', dpi=150, bbox_inches='tight', 
                facecolor='white', edgecolor='none')
    plt.close()
    print("✅ Created sample_kolam.png")

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description='Advanced Kolam Pattern Generator with ML')
    parser.add_argument('--input', '-i', type=str, help='Input file path (image or CSV)')
    parser.add_argument('--type', '-t', type=str, choices=['image', 'csv', 'auto'], 
                       default='auto', help='Input type')
    parser.add_argument('--variations', '-v', type=int, default=8, 
                       help='Number of variations to generate')
    parser.add_argument('--output', '-o', type=str, default='generated_kolam_patterns',
                       help='Output directory')
    parser.add_argument('--create-samples', action='store_true',
                       help='Create sample input files')
    
    args = parser.parse_args()
    
    if args.create_samples:
        create_sample_csv()
        create_sample_image()
        print("\n📁 Sample files created:")
        print("   - sample_kolam.csv (coordinate-based)")
        print("   - sample_kolam.png (image-based)")
        print("\nYou can now run:")
        print("   python kolam_pattern_generator_ml.py --input sample_kolam.csv")
        print("   python kolam_pattern_generator_ml.py --input sample_kolam.png")
        return
    
    if not args.input:
        print("❌ Please provide an input file with --input")
        print("Use --create-samples to create sample files")
        return
    
    if not os.path.exists(args.input):
        print(f"❌ Input file not found: {args.input}")
        return
    
    try:
        # Initialize generator
        generator = KolamPatternGenerator(args.output)
        
        # Process input
        patterns = generator.process_input(args.input, args.type, args.variations)
        
        print("\n🎉 Pattern generation completed successfully!")
        print(f"📊 Generated {len(patterns)} patterns")
        print(f"📁 Output directory: {generator.output_dir}")
        print(f"🖼️ Images saved in: {generator.output_dir}/images/")
        print(f"📄 CSV files saved in: {generator.output_dir}/csv/")
        print(f"📋 Metadata saved in: {generator.output_dir}/metadata/")
        
        # Final note
        print("\n" + "="*60)
        print("🎯 KOLAM PATTERN GENERATION COMPLETE")
        print("="*60)
        print("✅ Successfully generated Kolam patterns with ML transformations")
        print("✅ All patterns saved as high-quality PNG images")
        print("✅ Coordinate data exported as CSV files")
        print("✅ Comprehensive metadata generated")
        print("✅ Ready for SIH presentation!")
        print("="*60)
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()















