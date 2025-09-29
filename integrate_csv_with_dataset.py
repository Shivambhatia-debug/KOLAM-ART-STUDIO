#!/usr/bin/env python3
"""
CSV Dataset Integration Script
=============================

This script integrates the CSV Kolam data with the existing dataset structure.
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
import shutil

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class CSVDatasetIntegrator:
    def __init__(self, csv_dir="kolam_dataset/csv_files", dataset_dir="kolam_dataset"):
        self.csv_dir = Path(csv_dir)
        self.dataset_dir = Path(dataset_dir)
        self.integrated_data = {}
        
    def load_csv_data(self):
        """Load and process CSV data"""
        logger.info("Loading CSV data...")
        
        csv_files = list(self.csv_dir.glob("*.csv"))
        logger.info(f"Found {len(csv_files)} CSV files")
        
        for csv_file in csv_files:
            try:
                logger.info(f"Processing {csv_file.name}...")
                
                # Read CSV with limited rows for processing
                df = pd.read_csv(csv_file, nrows=10)
                
                # Extract coordinate pairs
                coordinates = self.extract_coordinate_pairs(df)
                
                # Generate Kolam image
                image_path = self.generate_kolam_image(csv_file.stem, coordinates)
                
                # Create annotation
                annotation = self.create_annotation(csv_file.stem, coordinates, image_path)
                
                # Store data
                self.integrated_data[csv_file.stem] = {
                    'coordinates': coordinates,
                    'image_path': image_path,
                    'annotation': annotation,
                    'source': 'csv_data'
                }
                
                logger.info(f"  Processed {len(coordinates)} coordinate sets")
                
            except Exception as e:
                logger.error(f"Error processing {csv_file.name}: {e}")
        
        logger.info(f"Successfully processed {len(self.integrated_data)} CSV files")
        return self.integrated_data
    
    def extract_coordinate_pairs(self, df):
        """Extract coordinate pairs from dataframe"""
        coordinates = []
        
        # Find x and y columns
        x_cols = [col for col in df.columns if 'x-kolam' in col.lower()]
        y_cols = [col for col in df.columns if 'y-kolam' in col.lower()]
        
        logger.info(f"  Found {len(x_cols)} x-columns and {len(y_cols)} y-columns")
        
        # Extract coordinate pairs for each row
        for i in range(len(df)):
            row_coords = []
            for j in range(min(len(x_cols), len(y_cols))):
                x_val = df.iloc[i][x_cols[j]]
                y_val = df.iloc[i][y_cols[j]]
                
                if pd.notna(x_val) and pd.notna(y_val):
                    row_coords.append((float(x_val), float(y_val)))
            
            if row_coords:
                coordinates.append(row_coords)
        
        return coordinates
    
    def generate_kolam_image(self, kolam_name, coordinates, size=400):
        """Generate Kolam image from coordinates"""
        # Create output directory
        output_dir = self.dataset_dir / "csv_images"
        output_dir.mkdir(exist_ok=True)
        
        # Create image
        img = Image.new('RGB', (size, size), 'white')
        draw = ImageDraw.Draw(img)
        
        if not coordinates:
            logger.warning(f"No coordinates for {kolam_name}")
            return None
        
        # Find coordinate bounds
        all_x = []
        all_y = []
        for coord_set in coordinates:
            for coord in coord_set:
                all_x.append(coord[0])
                all_y.append(coord[1])
        
        if not all_x:
            return None
        
        # Scale coordinates to image size
        min_x, max_x = min(all_x), max(all_x)
        min_y, max_y = min(all_y), max(all_y)
        
        scale_x = (size - 40) / (max_x - min_x) if max_x != min_x else 1
        scale_y = (size - 40) / (max_y - min_y) if max_y != min_y else 1
        scale = min(scale_x, scale_y)
        
        offset_x = (size - (max_x - min_x) * scale) / 2
        offset_y = (size - (max_y - min_y) * scale) / 2
        
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
                    draw.ellipse([coord[0]-2, coord[1]-2, coord[0]+2, coord[1]+2], 
                               fill=color, outline=color)
        
        # Save image
        image_path = output_dir / f"{kolam_name}_generated.png"
        img.save(image_path)
        
        logger.info(f"  Generated image: {image_path}")
        return str(image_path)
    
    def create_annotation(self, kolam_name, coordinates, image_path):
        """Create annotation for the Kolam"""
        # Analyze pattern characteristics
        all_x = []
        all_y = []
        for coord_set in coordinates:
            for coord in coord_set:
                all_x.append(coord[0])
                all_y.append(coord[1])
        
        # Determine pattern characteristics
        pattern_type = self.classify_pattern_type(coordinates, all_x, all_y)
        symmetry_type = self.detect_symmetry(coordinates, all_x, all_y)
        cultural_region = self.infer_cultural_region(kolam_name)
        complexity_score = self.calculate_complexity_score(coordinates)
        
        annotation = {
            "kolam_type": pattern_type,
            "symmetry_type": symmetry_type,
            "cultural_region": cultural_region,
            "coordinates": coordinates,
            "complexity_score": complexity_score,
            "eulerian_path": True,  # Assume all patterns have Eulerian paths
            "confidence": 0.8,
            "features": {
                "num_coordinate_sets": len(coordinates),
                "total_points": sum(len(coord_set) for coord_set in coordinates),
                "x_range": [min(all_x), max(all_x)] if all_x else [0, 0],
                "y_range": [min(all_y), max(all_y)] if all_y else [0, 0]
            },
            "metadata": {
                "source": "csv_data",
                "image_path": image_path,
                "generation_method": "coordinate_extraction"
            }
        }
        
        return annotation
    
    def classify_pattern_type(self, coordinates, all_x, all_y):
        """Classify pattern type"""
        if not coordinates:
            return "unknown"
        
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
        """Infer cultural region from filename"""
        if "19" in kolam_name:
            return "tamil_nadu"
        elif "29" in kolam_name:
            return "karnataka"
        elif "109" in kolam_name:
            return "kerala"
        else:
            return "unknown"
    
    def calculate_complexity_score(self, coordinates):
        """Calculate complexity score"""
        if not coordinates:
            return 0.0
        
        num_sets = len(coordinates)
        total_points = sum(len(coord_set) for coord_set in coordinates)
        avg_points = total_points / num_sets if num_sets > 0 else 0
        
        complexity = min(1.0, (num_sets * avg_points) / 1000)
        return round(complexity, 3)
    
    def integrate_with_existing_dataset(self):
        """Integrate CSV data with existing dataset structure"""
        logger.info("Integrating with existing dataset...")
        
        # Create directories for CSV data
        csv_train_dir = self.dataset_dir / "csv_train"
        csv_val_dir = self.dataset_dir / "csv_val"
        csv_test_dir = self.dataset_dir / "csv_test"
        
        for dir_path in [csv_train_dir, csv_val_dir]:
            dir_path.mkdir(exist_ok=True)
            (dir_path / "images").mkdir(exist_ok=True)
            (dir_path / "annotations").mkdir(exist_ok=True)
        
        # Split data (simple 80-20 split)
        kolam_names = list(self.integrated_data.keys())
        train_size = int(len(kolam_names) * 0.8)
        train_names = kolam_names[:train_size]
        val_names = kolam_names[train_size:]
        
        # Copy files to appropriate directories
        for split, names in [("csv_train", train_names), ("csv_val", val_names)]:
            for kolam_name in names:
                if kolam_name in self.integrated_data:
                    data = self.integrated_data[kolam_name]
                    
                    # Copy image
                    if data['image_path']:
                        src_img = Path(data['image_path'])
                        dst_img = self.dataset_dir / split / "images" / f"{kolam_name}.png"
                        shutil.copy2(src_img, dst_img)
                    
                    # Save annotation
                    annotation_path = self.dataset_dir / split / "annotations" / f"{kolam_name}.json"
                    with open(annotation_path, 'w') as f:
                        json.dump(data['annotation'], f, indent=2)
        
        logger.info(f"Integrated {len(train_names)} files to csv_train")
        logger.info(f"Integrated {len(val_names)} files to csv_val")
    
    def create_integration_report(self):
        """Create integration report"""
        logger.info("Creating integration report...")
        
        report = {
            "integration_summary": {
                "total_csv_files": len(self.integrated_data),
                "successful_integrations": len([d for d in self.integrated_data.values() if d['image_path']]),
                "failed_integrations": len([d for d in self.integrated_data.values() if not d['image_path']])
            },
            "pattern_analysis": {
                "pattern_types": {},
                "symmetry_types": {},
                "cultural_regions": {}
            },
            "files_processed": list(self.integrated_data.keys())
        }
        
        # Analyze patterns
        for kolam_name, data in self.integrated_data.items():
            annotation = data['annotation']
            
            pattern_type = annotation['kolam_type']
            symmetry_type = annotation['symmetry_type']
            cultural_region = annotation['cultural_region']
            
            report["pattern_analysis"]["pattern_types"][pattern_type] = \
                report["pattern_analysis"]["pattern_types"].get(pattern_type, 0) + 1
            report["pattern_analysis"]["symmetry_types"][symmetry_type] = \
                report["pattern_analysis"]["symmetry_types"].get(symmetry_type, 0) + 1
            report["pattern_analysis"]["cultural_regions"][cultural_region] = \
                report["pattern_analysis"]["cultural_regions"].get(cultural_region, 0) + 1
        
        # Save report
        report_path = self.dataset_dir / "csv_integration_report.json"
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2)
        
        logger.info(f"Integration report saved: {report_path}")
        return report

def main():
    """Main integration function"""
    logger.info("Starting CSV Dataset Integration...")
    
    # Initialize integrator
    integrator = CSVDatasetIntegrator()
    
    # Load CSV data
    integrated_data = integrator.load_csv_data()
    
    if not integrated_data:
        logger.error("No CSV data loaded. Please check the CSV files directory.")
        return
    
    # Integrate with existing dataset
    integrator.integrate_with_existing_dataset()
    
    # Create integration report
    report = integrator.create_integration_report()
    
    # Print summary
    logger.info("\n" + "="*60)
    logger.info("CSV DATASET INTEGRATION SUMMARY")
    logger.info("="*60)
    logger.info(f"Total CSV files processed: {report['integration_summary']['total_csv_files']}")
    logger.info(f"Successful integrations: {report['integration_summary']['successful_integrations']}")
    logger.info(f"Failed integrations: {report['integration_summary']['failed_integrations']}")
    
    logger.info("\nPattern Analysis:")
    for pattern_type, count in report['pattern_analysis']['pattern_types'].items():
        logger.info(f"  {pattern_type}: {count}")
    
    logger.info("\nSymmetry Analysis:")
    for symmetry_type, count in report['pattern_analysis']['symmetry_types'].items():
        logger.info(f"  {symmetry_type}: {count}")
    
    logger.info("\nCultural Regions:")
    for region, count in report['pattern_analysis']['cultural_regions'].items():
        logger.info(f"  {region}: {count}")
    
    logger.info("="*60)
    logger.info("CSV integration completed successfully!")

if __name__ == "__main__":
    main()


