#!/usr/bin/env python3
"""
Test Trained Kolam Models
=========================

This script tests the trained models on sample images from the dataset.
"""

import os
import json
import numpy as np
import cv2
from PIL import Image
import joblib
from pathlib import Path
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class KolamModelTester:
    def __init__(self):
        self.models = {}
        self.scalers = {}
        self.label_encoders = {}
        self.feature_names = []
        
    def load_models(self):
        """Load pre-trained models"""
        logger.info("Loading pre-trained models...")
        
        try:
            # Load models
            for task in ['kolam_type', 'symmetry_type', 'cultural_region']:
                model_path = f"models/{task}_model.pkl"
                if os.path.exists(model_path):
                    self.models[task] = joblib.load(model_path)
                    logger.info(f"Loaded {task} model")
                else:
                    logger.error(f"Model not found: {model_path}")
                    return False
            
            # Load scalers and encoders
            self.scalers = joblib.load("models/scalers.pkl")
            self.label_encoders = joblib.load("models/label_encoders.pkl")
            self.feature_names = joblib.load("models/feature_names.pkl")
            
            logger.info("All models loaded successfully!")
            return True
            
        except Exception as e:
            logger.error(f"Error loading models: {e}")
            return False
    
    def extract_features(self, image):
        """Extract features from image (same as training)"""
        features = []
        
        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # 1. Basic image statistics
        features.extend([
            np.mean(gray),
            np.std(gray),
            np.min(gray),
            np.max(gray),
            np.median(gray)
        ])
        
        # 2. Histogram features
        hist = cv2.calcHist([gray], [0], None, [256], [0, 256])
        features.extend([
            np.argmax(hist),  # Peak intensity
            np.sum(hist[:50]),  # Dark pixels
            np.sum(hist[200:]),  # Bright pixels
            np.sum(hist[50:200])  # Mid-tone pixels
        ])
        
        # 3. Edge detection features
        edges = cv2.Canny(gray, 50, 150)
        features.extend([
            np.sum(edges > 0),  # Total edge pixels
            np.sum(edges > 0) / (edges.shape[0] * edges.shape[1])  # Edge density
        ])
        
        # 4. Contour features
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if contours:
            features.extend([
                len(contours),  # Number of contours
                np.mean([cv2.contourArea(c) for c in contours]),  # Average contour area
                np.max([cv2.contourArea(c) for c in contours]),  # Max contour area
                np.sum([cv2.contourArea(c) for c in contours])  # Total contour area
            ])
        else:
            features.extend([0, 0, 0, 0])
        
        # 5. Hough circle detection (for dots)
        circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 20,
                                 param1=50, param2=30, minRadius=5, maxRadius=50)
        if circles is not None:
            features.extend([
                len(circles[0]),  # Number of circles
                np.mean(circles[0][:, 2]) if len(circles[0]) > 0 else 0,  # Average radius
                np.std(circles[0][:, 2]) if len(circles[0]) > 1 else 0  # Radius std
            ])
        else:
            features.extend([0, 0, 0])
        
        # 6. Symmetry features
        # Horizontal symmetry
        h_symmetry = np.sum(np.abs(gray - np.fliplr(gray))) / (gray.shape[0] * gray.shape[1])
        # Vertical symmetry
        v_symmetry = np.sum(np.abs(gray - np.flipud(gray))) / (gray.shape[0] * gray.shape[1])
        # Diagonal symmetry
        d_symmetry = np.sum(np.abs(gray - np.fliplr(np.flipud(gray)))) / (gray.shape[0] * gray.shape[1])
        
        features.extend([h_symmetry, v_symmetry, d_symmetry])
        
        # 7. Texture features
        kernel = np.ones((3, 3), np.float32) / 9
        local_mean = cv2.filter2D(gray.astype(np.float32), -1, kernel)
        local_variance = cv2.filter2D((gray.astype(np.float32) - local_mean) ** 2, -1, kernel)
        features.extend([
            np.mean(local_variance),
            np.std(local_variance)
        ])
        
        # 8. Geometric features
        # Aspect ratio
        features.append(gray.shape[1] / gray.shape[0])
        
        # Center of mass
        moments = cv2.moments(gray)
        if moments['m00'] != 0:
            cx = moments['m10'] / moments['m00']
            cy = moments['m01'] / moments['m00']
            features.extend([cx / gray.shape[1], cy / gray.shape[0]])  # Normalized
        else:
            features.extend([0.5, 0.5])
        
        return np.array(features)
    
    def predict(self, image):
        """Make predictions on a new image"""
        if not self.models:
            logger.error("No models loaded. Please load models first.")
            return None
        
        # Extract features
        features = self.extract_features(image)
        features_scaled = self.scalers['main'].transform([features])
        
        # Make predictions
        predictions = {}
        for task, model in self.models.items():
            pred_encoded = model.predict(features_scaled)[0]
            pred_label = self.label_encoders[task].inverse_transform([pred_encoded])[0]
            predictions[task] = pred_label
        
        return predictions
    
    def test_on_dataset_samples(self, dataset_path="kolam_dataset"):
        """Test models on sample images from the dataset"""
        logger.info("Testing models on dataset samples...")
        
        dataset_path = Path(dataset_path)
        test_path = dataset_path / "test"
        
        if not test_path.exists():
            logger.error("Test dataset not found")
            return
        
        # Get test images
        images_path = test_path / "images"
        annotations_path = test_path / "annotations"
        
        if not images_path.exists() or not annotations_path.exists():
            logger.error("Test images or annotations not found")
            return
        
        image_files = list(images_path.glob("*.png"))
        
        logger.info(f"Testing on {len(image_files)} test images...")
        
        correct_predictions = {'kolam_type': 0, 'symmetry_type': 0, 'cultural_region': 0}
        total_predictions = len(image_files)
        
        for img_file in image_files:
            # Load image
            image = cv2.imread(str(img_file))
            if image is None:
                continue
            
            # Load ground truth annotation
            ann_file = annotations_path / f"{img_file.stem}.json"
            if not ann_file.exists():
                continue
            
            with open(ann_file, 'r') as f:
                annotation = json.load(f)
            
            # Make predictions
            predictions = self.predict(image)
            
            if predictions:
                logger.info(f"\nTesting: {img_file.name}")
                logger.info(f"Ground Truth:")
                logger.info(f"  Kolam Type: {annotation['kolam_type']}")
                logger.info(f"  Symmetry: {annotation['symmetry_type']}")
                logger.info(f"  Cultural Region: {annotation['cultural_region']}")
                
                logger.info(f"Predictions:")
                logger.info(f"  Kolam Type: {predictions['kolam_type']}")
                logger.info(f"  Symmetry: {predictions['symmetry_type']}")
                logger.info(f"  Cultural Region: {predictions['cultural_region']}")
                
                # Check accuracy
                for task in ['kolam_type', 'symmetry_type', 'cultural_region']:
                    if predictions[task] == annotation[task]:
                        correct_predictions[task] += 1
                
                logger.info(f"Correct: {sum(1 for task in ['kolam_type', 'symmetry_type', 'cultural_region'] if predictions[task] == annotation[task])}/3")
        
        # Print final results
        logger.info("\n" + "="*50)
        logger.info("FINAL TEST RESULTS")
        logger.info("="*50)
        for task, correct in correct_predictions.items():
            accuracy = correct / total_predictions
            logger.info(f"{task}: {correct}/{total_predictions} = {accuracy:.3f}")
        
        overall_accuracy = sum(correct_predictions.values()) / (total_predictions * 3)
        logger.info(f"Overall Accuracy: {overall_accuracy:.3f}")
        logger.info("="*50)

def main():
    """Main testing function"""
    logger.info("Starting Kolam Model Testing...")
    
    # Initialize tester
    tester = KolamModelTester()
    
    # Load models
    if not tester.load_models():
        logger.error("Failed to load models. Please train models first.")
        return
    
    # Test on dataset samples
    tester.test_on_dataset_samples()
    
    logger.info("Testing completed!")

if __name__ == "__main__":
    main()


