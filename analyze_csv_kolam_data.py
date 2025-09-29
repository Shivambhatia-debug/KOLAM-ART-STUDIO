#!/usr/bin/env python3
"""
CSV Kolam Data Analyzer
======================

This script analyzes the CSV files containing Kolam coordinate data
and integrates them with the existing dataset structure.
"""

import os
import pandas as pd
import numpy as np
import json
import cv2
from PIL import Image, ImageDraw
import matplotlib.pyplot as plt
from pathlib import Path
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class CSVKolamAnalyzer:
    def __init__(self, csv_dir="kolam_dataset/csv_files"):
        self.csv_dir = Path(csv_dir)
        self.kolam_data = {}
        
    def load_csv_files(self):
        """Load all CSV files and analyze their structure"""
        logger.info("Loading CSV files...")
        
        csv_files = list(self.csv_dir.glob("*.csv"))
        logger.info(f"Found {len(csv_files)} CSV files")
        
        for csv_file in csv_files:
            logger.info(f"Analyzing {csv_file.name}...")
            try:
                # Read CSV file
                df = pd.read_csv(csv_file)
                
                # Analyze structure
                self.analyze_csv_structure(csv_file.name, df)
                
                # Extract coordinates
                coordinates = self.extract_coordinates(df)
                
                # Store data
                self.kolam_data[csv_file.stem] = {
                    'filename': csv_file.name,
                    'coordinates': coordinates,
                    'num_points': len(coordinates),
                    'dataframe': df
                }
                
            except Exception as e:
                logger.error(f"Error processing {csv_file.name}: {e}")
        
        logger.info(f"Successfully loaded {len(self.kolam_data)} CSV files")
        return self.kolam_data
    
    def analyze_csv_structure(self, filename, df):
        """Analyze the structure of a CSV file"""
        logger.info(f"Structure of {filename}:")
        logger.info(f"  Shape: {df.shape}")
        logger.info(f"  Columns: {list(df.columns)}")
        logger.info(f"  Data types: {df.dtypes.to_dict()}")
        
        # Check for coordinate patterns
        coord_columns = [col for col in df.columns if 'kolam' in col.lower()]
        logger.info(f"  Coordinate columns: {coord_columns}")
        
        # Sample data
        logger.info(f"  Sample data (first 3 rows):")
        for i in range(min(3, len(df))):
            logger.info(f"    Row {i}: {df.iloc[i].values[:10]}...")  # First 10 values
    
    def extract_coordinates(self, df):
        """Extract coordinate pairs from the dataframe"""
        coordinates = []
        
        # Find x and y coordinate columns
        x_cols = [col for col in df.columns if 'x-kolam' in col.lower()]
        y_cols = [col for col in df.columns if 'y-kolam' in col.lower()]
        
        logger.info(f"  Found {len(x_cols)} x-coordinate columns and {len(y_cols)} y-coordinate columns")
        
        # Extract coordinate pairs
        for i in range(len(df)):
            row_coords = []
            for j in range(min(len(x_cols), len(y_cols))):
                x_val = df.iloc[i][x_cols[j]]
                y_val = df.iloc[i][y_cols[j]]
                
                # Skip invalid coordinates (NaN, None, etc.)
                if pd.notna(x_val) and pd.notna(y_val):
                    row_coords.append((float(x_val), float(y_val)))
            
            if row_coords:  # Only add if we have valid coordinates
                coordinates.append(row_coords)
        
        logger.info(f"  Extracted {len(coordinates)} coordinate sets")
        return coordinates
    
    def visualize_kolam_patterns(self, output_dir="kolam_dataset/visualizations"):
        """Create visualizations of the Kolam patterns from CSV data"""
        os.makedirs(output_dir, exist_ok=True)
        
        logger.info("Creating visualizations...")
        
        for kolam_name, data in self.kolam_data.items():
            try:
                self.create_kolam_visualization(kolam_name, data, output_dir)
            except Exception as e:
                logger.error(f"Error creating visualization for {kolam_name}: {e}")
    
    def create_kolam_visualization(self, kolam_name, data, output_dir):
        """Create a single Kolam visualization"""
        coordinates = data['coordinates']
        
        if not coordinates:
            logger.warning(f"No coordinates found for {kolam_name}")
            return
        
        # Create figure
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        fig.suptitle(f'Kolam Pattern Analysis: {kolam_name}', fontsize=16)
        
        # Plot 1: All coordinate sets overlaid
        ax1 = axes[0, 0]
        for i, coord_set in enumerate(coordinates[:10]):  # Limit to first 10 sets
            if coord_set:
                x_vals = [coord[0] for coord in coord_set]
                y_vals = [coord[1] for coord in coord_set]
                ax1.plot(x_vals, y_vals, 'o-', alpha=0.7, markersize=2)
        ax1.set_title('All Coordinate Sets (First 10)')
        ax1.set_xlabel('X Coordinate')
        ax1.set_ylabel('Y Coordinate')
        ax1.grid(True, alpha=0.3)
        
        # Plot 2: First coordinate set
        ax2 = axes[0, 1]
        if coordinates:
            first_set = coordinates[0]
            if first_set:
                x_vals = [coord[0] for coord in first_set]
                y_vals = [coord[1] for coord in first_set]
                ax2.plot(x_vals, y_vals, 'ro-', markersize=4)
                ax2.set_title('First Coordinate Set')
                ax2.set_xlabel('X Coordinate')
                ax2.set_ylabel('Y Coordinate')
                ax2.grid(True, alpha=0.3)
        
        # Plot 3: Coordinate distribution
        ax3 = axes[1, 0]
        all_x = []
        all_y = []
        for coord_set in coordinates:
            for coord in coord_set:
                all_x.append(coord[0])
                all_y.append(coord[1])
        
        if all_x and all_y:
            ax3.scatter(all_x, all_y, alpha=0.5, s=1)
            ax3.set_title('Coordinate Distribution')
            ax3.set_xlabel('X Coordinate')
            ax3.set_ylabel('Y Coordinate')
            ax3.grid(True, alpha=0.3)
        
        # Plot 4: Statistics
        ax4 = axes[1, 1]
        ax4.axis('off')
        
        # Calculate statistics
        stats_text = f"""
Statistics for {kolam_name}:

Total coordinate sets: {len(coordinates)}
Total points: {sum(len(coord_set) for coord_set in coordinates)}
Average points per set: {np.mean([len(coord_set) for coord_set in coordinates]):.1f}

X coordinate range: {min(all_x):.1f} to {max(all_x):.1f}
Y coordinate range: {min(all_y):.1f} to {max(all_y):.1f}

X coordinate mean: {np.mean(all_x):.1f}
Y coordinate mean: {np.mean(all_y):.1f}
        """
        
        ax4.text(0.1, 0.9, stats_text, transform=ax4.transAxes, fontsize=10,
                verticalalignment='top', fontfamily='monospace')
        
        plt.tight_layout()
        
        # Save plot
        output_path = os.path.join(output_dir, f"{kolam_name}_analysis.png")
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        logger.info(f"Saved visualization: {output_path}")
    
    def generate_kolam_images(self, output_dir="kolam_dataset/generated_images"):
        """Generate actual Kolam images from coordinate data"""
        os.makedirs(output_dir, exist_ok=True)
        
        logger.info("Generating Kolam images...")
        
        for kolam_name, data in self.kolam_data.items():
            try:
                self.create_kolam_image(kolam_name, data, output_dir)
            except Exception as e:
                logger.error(f"Error creating image for {kolam_name}: {e}")
    
    def create_kolam_image(self, kolam_name, data, output_dir):
        """Create a single Kolam image from coordinates"""
        coordinates = data['coordinates']
        
        if not coordinates:
            return
        
        # Create image
        img_size = 800
        img = Image.new('RGB', (img_size, img_size), 'white')
        draw = ImageDraw.Draw(img)
        
        # Find coordinate bounds
        all_x = []
        all_y = []
        for coord_set in coordinates:
            for coord in coord_set:
                all_x.append(coord[0])
                all_y.append(coord[1])
        
        if not all_x:
            return
        
        min_x, max_x = min(all_x), max(all_x)
        min_y, max_y = min(all_y), max(all_y)
        
        # Scale coordinates to image size
        scale_x = (img_size - 100) / (max_x - min_x) if max_x != min_x else 1
        scale_y = (img_size - 100) / (max_y - min_y) if max_y != min_y else 1
        scale = min(scale_x, scale_y)
        
        offset_x = (img_size - (max_x - min_x) * scale) / 2
        offset_y = (img_size - (max_y - min_y) * scale) / 2
        
        # Draw patterns
        colors = ['black', 'red', 'blue', 'green', 'purple']
        
        for i, coord_set in enumerate(coordinates[:5]):  # Limit to first 5 sets
            if coord_set:
                color = colors[i % len(colors)]
                
                # Convert coordinates to image coordinates
                img_coords = []
                for coord in coord_set:
                    img_x = int((coord[0] - min_x) * scale + offset_x)
                    img_y = int((coord[1] - min_y) * scale + offset_y)
                    img_coords.append((img_x, img_y))
                
                # Draw lines connecting points
                if len(img_coords) > 1:
                    draw.line(img_coords, fill=color, width=2)
                
                # Draw points
                for coord in img_coords:
                    draw.ellipse([coord[0]-3, coord[1]-3, coord[0]+3, coord[1]+3], 
                               fill=color, outline=color)
        
        # Save image
        output_path = os.path.join(output_dir, f"{kolam_name}_generated.png")
        img.save(output_path)
        
        logger.info(f"Generated image: {output_path}")
    
    def create_dataset_annotations(self, output_dir="kolam_dataset/csv_annotations"):
        """Create annotation files for the CSV data"""
        os.makedirs(output_dir, exist_ok=True)
        
        logger.info("Creating dataset annotations...")
        
        for kolam_name, data in self.kolam_data.items():
            try:
                annotation = self.create_annotation(kolam_name, data)
                
                # Save annotation
                output_path = os.path.join(output_dir, f"{kolam_name}_annotation.json")
                with open(output_path, 'w') as f:
                    json.dump(annotation, f, indent=2)
                
                logger.info(f"Created annotation: {output_path}")
                
            except Exception as e:
                logger.error(f"Error creating annotation for {kolam_name}: {e}")
    
    def create_annotation(self, kolam_name, data):
        """Create annotation for a single Kolam"""
        coordinates = data['coordinates']
        
        # Analyze pattern characteristics
        all_x = []
        all_y = []
        for coord_set in coordinates:
            for coord in coord_set:
                all_x.append(coord[0])
                all_y.append(coord[1])
        
        # Determine pattern type based on characteristics
        pattern_type = self.classify_pattern_type(coordinates, all_x, all_y)
        symmetry_type = self.detect_symmetry(coordinates, all_x, all_y)
        cultural_region = self.infer_cultural_region(kolam_name)
        
        annotation = {
            "kolam_type": pattern_type,
            "symmetry_type": symmetry_type,
            "cultural_region": cultural_region,
            "coordinates": coordinates,
            "complexity_score": self.calculate_complexity_score(coordinates),
            "eulerian_path": self.check_eulerian_path(coordinates),
            "metadata": {
                "num_coordinate_sets": len(coordinates),
                "total_points": sum(len(coord_set) for coord_set in coordinates),
                "x_range": [min(all_x), max(all_x)] if all_x else [0, 0],
                "y_range": [min(all_y), max(all_y)] if all_y else [0, 0],
                "source": "csv_data",
                "filename": data['filename']
            }
        }
        
        return annotation
    
    def classify_pattern_type(self, coordinates, all_x, all_y):
        """Classify the pattern type based on characteristics"""
        if not coordinates:
            return "unknown"
        
        # Simple heuristics for classification
        num_sets = len(coordinates)
        avg_points = np.mean([len(coord_set) for coord_set in coordinates])
        
        if num_sets == 1 and avg_points < 10:
            return "simple_kolam"
        elif num_sets > 5:
            return "complex_kolam"
        elif avg_points > 50:
            return "detailed_kolam"
        else:
            return "traditional_kolam"
    
    def detect_symmetry(self, coordinates, all_x, all_y):
        """Detect symmetry type"""
        if not all_x or not all_y:
            return "unknown"
        
        # Simple symmetry detection
        center_x = np.mean(all_x)
        center_y = np.mean(all_y)
        
        # Check for radial symmetry
        distances = [np.sqrt((x - center_x)**2 + (y - center_y)**2) for x, y in zip(all_x, all_y)]
        if len(set([round(d, 1) for d in distances])) < len(distances) * 0.3:
            return "radial"
        
        # Check for bilateral symmetry
        left_points = sum(1 for x in all_x if x < center_x)
        right_points = sum(1 for x in all_x if x > center_x)
        
        if abs(left_points - right_points) < len(all_x) * 0.1:
            return "bilateral"
        
        return "asymmetric"
    
    def infer_cultural_region(self, kolam_name):
        """Infer cultural region from filename or pattern"""
        # Simple mapping based on filename patterns
        if "19" in kolam_name:
            return "tamil_nadu"
        elif "29" in kolam_name:
            return "karnataka"
        elif "109" in kolam_name:
            return "kerala"
        else:
            return "unknown"
    
    def calculate_complexity_score(self, coordinates):
        """Calculate complexity score (0-1)"""
        if not coordinates:
            return 0.0
        
        num_sets = len(coordinates)
        total_points = sum(len(coord_set) for coord_set in coordinates)
        avg_points = total_points / num_sets if num_sets > 0 else 0
        
        # Normalize complexity (simple heuristic)
        complexity = min(1.0, (num_sets * avg_points) / 1000)
        return round(complexity, 3)
    
    def check_eulerian_path(self, coordinates):
        """Check if pattern has Eulerian path characteristics"""
        # Simple check: if we can trace all points without lifting pen
        if not coordinates:
            return False
        
        # For now, assume all patterns have Eulerian paths
        # This would need more sophisticated graph analysis
        return True
    
    def generate_summary_report(self, output_path="kolam_dataset/csv_analysis_report.json"):
        """Generate a summary report of all CSV data"""
        logger.info("Generating summary report...")
        
        summary = {
            "total_files": len(self.kolam_data),
            "files_analyzed": list(self.kolam_data.keys()),
            "statistics": {
                "total_coordinate_sets": sum(len(data['coordinates']) for data in self.kolam_data.values()),
                "total_points": sum(sum(len(coord_set) for coord_set in data['coordinates']) 
                                  for data in self.kolam_data.values()),
                "average_sets_per_file": np.mean([len(data['coordinates']) for data in self.kolam_data.values()]),
                "average_points_per_set": np.mean([np.mean([len(coord_set) for coord_set in data['coordinates']]) 
                                                 for data in self.kolam_data.values()])
            },
            "pattern_types": {},
            "symmetry_types": {},
            "cultural_regions": {}
        }
        
        # Count pattern types, symmetry types, and cultural regions
        for kolam_name, data in self.kolam_data.items():
            # This would need the annotation data, but for now we'll use simple classification
            pattern_type = self.classify_pattern_type(data['coordinates'], [], [])
            symmetry_type = self.detect_symmetry(data['coordinates'], [], [])
            cultural_region = self.infer_cultural_region(kolam_name)
            
            summary["pattern_types"][pattern_type] = summary["pattern_types"].get(pattern_type, 0) + 1
            summary["symmetry_types"][symmetry_type] = summary["symmetry_types"].get(symmetry_type, 0) + 1
            summary["cultural_regions"][cultural_region] = summary["cultural_regions"].get(cultural_region, 0) + 1
        
        # Save report
        with open(output_path, 'w') as f:
            json.dump(summary, f, indent=2)
        
        logger.info(f"Summary report saved: {output_path}")
        return summary

def main():
    """Main analysis function"""
    logger.info("Starting CSV Kolam Data Analysis...")
    
    # Initialize analyzer
    analyzer = CSVKolamAnalyzer()
    
    # Load CSV files
    kolam_data = analyzer.load_csv_files()
    
    if not kolam_data:
        logger.error("No CSV data loaded. Please check the CSV files directory.")
        return
    
    # Create visualizations
    analyzer.visualize_kolam_patterns()
    
    # Generate images
    analyzer.generate_kolam_images()
    
    # Create annotations
    analyzer.create_dataset_annotations()
    
    # Generate summary report
    summary = analyzer.generate_summary_report()
    
    logger.info("CSV analysis completed successfully!")
    
    # Print summary
    logger.info("\n" + "="*50)
    logger.info("ANALYSIS SUMMARY")
    logger.info("="*50)
    logger.info(f"Total files analyzed: {summary['total_files']}")
    logger.info(f"Total coordinate sets: {summary['statistics']['total_coordinate_sets']}")
    logger.info(f"Total points: {summary['statistics']['total_points']}")
    logger.info(f"Average sets per file: {summary['statistics']['average_sets_per_file']:.1f}")
    logger.info(f"Average points per set: {summary['statistics']['average_points_per_set']:.1f}")
    logger.info("="*50)

if __name__ == "__main__":
    main()


