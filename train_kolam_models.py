#!/usr/bin/env python3
"""
Kolam Dataset Training Script
============================

This script trains machine learning models using the kolam_dataset folder.
It includes:
- Image feature extraction
- Multi-task learning (kolam type, symmetry, cultural region)
- Model evaluation and validation
- Model saving and loading
"""

import os
import json
import numpy as np
import cv2
from PIL import Image
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.preprocessing import StandardScaler, LabelEncoder
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class KolamDatasetTrainer:
    def __init__(self, dataset_path="kolam_dataset"):
        self.dataset_path = Path(dataset_path)
        self.models = {}
        self.scalers = {}
        self.label_encoders = {}
        self.feature_names = []
        
        # Create models directory
        os.makedirs("models", exist_ok=True)
        
    def load_dataset(self):
        """Load the kolam dataset from the folder structure"""
        logger.info("Loading kolam dataset...")
        
        train_data = self._load_split("train")
        val_data = self._load_split("val")
        test_data = self._load_split("test")
        
        # Combine all data
        all_data = train_data + val_data + test_data
        
        logger.info(f"Loaded {len(all_data)} samples total")
        logger.info(f"Train: {len(train_data)}, Val: {len(val_data)}, Test: {len(test_data)}")
        
        return all_data, train_data, val_data, test_data
    
    def _load_split(self, split_name):
        """Load data from a specific split (train/val/test)"""
        split_path = self.dataset_path / split_name
        data = []
        
        if not split_path.exists():
            logger.warning(f"Split {split_name} not found")
            return data
        
        # Load images and annotations
        images_path = split_path / "images"
        annotations_path = split_path / "annotations"
        
        if not images_path.exists() or not annotations_path.exists():
            logger.warning(f"Images or annotations not found for {split_name}")
            return data
        
        # Get all image files
        image_files = list(images_path.glob("*.png"))
        
        for img_file in image_files:
            # Find corresponding annotation
            ann_file = annotations_path / f"{img_file.stem}.json"
            
            if ann_file.exists():
                try:
                    # Load image
                    image = cv2.imread(str(img_file))
                    if image is None:
                        continue
                    
                    # Load annotation
                    with open(ann_file, 'r') as f:
                        annotation = json.load(f)
                    
                    data.append({
                        'image': image,
                        'annotation': annotation,
                        'filename': img_file.name,
                        'split': split_name
                    })
                    
                except Exception as e:
                    logger.error(f"Error loading {img_file}: {e}")
                    continue
        
        logger.info(f"Loaded {len(data)} samples from {split_name}")
        return data
    
    def extract_features(self, image):
        """Extract comprehensive features from kolam image"""
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
        
        # 7. Texture features (Local Binary Pattern approximation)
        # Calculate local variance
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
    
    def prepare_training_data(self, data):
        """Prepare training data with features and labels"""
        logger.info("Extracting features and preparing training data...")
        
        X = []
        y_kolam_type = []
        y_symmetry_type = []
        y_cultural_region = []
        
        for i, sample in enumerate(data):
            if i % 10 == 0:
                logger.info(f"Processing sample {i+1}/{len(data)}")
            
            # Extract features
            features = self.extract_features(sample['image'])
            X.append(features)
            
            # Extract labels
            ann = sample['annotation']
            y_kolam_type.append(ann['kolam_type'])
            y_symmetry_type.append(ann['symmetry_type'])
            y_cultural_region.append(ann['cultural_region'])
        
        X = np.array(X)
        logger.info(f"Feature matrix shape: {X.shape}")
        
        # Store feature names for later use
        self.feature_names = [
            'mean_intensity', 'std_intensity', 'min_intensity', 'max_intensity', 'median_intensity',
            'peak_intensity', 'dark_pixels', 'bright_pixels', 'mid_tone_pixels',
            'edge_pixels', 'edge_density',
            'num_contours', 'avg_contour_area', 'max_contour_area', 'total_contour_area',
            'num_circles', 'avg_circle_radius', 'circle_radius_std',
            'h_symmetry', 'v_symmetry', 'd_symmetry',
            'texture_mean', 'texture_std',
            'aspect_ratio', 'center_x', 'center_y'
        ]
        
        return X, y_kolam_type, y_symmetry_type, y_cultural_region
    
    def train_models(self, X, y_kolam_type, y_symmetry_type, y_cultural_region):
        """Train models for different classification tasks"""
        logger.info("Training models...")
        
        # Scale features
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        self.scalers['main'] = scaler
        
        # Train-test split
        X_train, X_test, y_kolam_train, y_kolam_test = train_test_split(
            X_scaled, y_kolam_type, test_size=0.2, random_state=42, stratify=y_kolam_type
        )
        
        # 1. Kolam Type Classification
        logger.info("Training Kolam Type classifier...")
        kolam_encoder = LabelEncoder()
        y_kolam_encoded = kolam_encoder.fit_transform(y_kolam_type)
        y_kolam_train_encoded = kolam_encoder.transform(y_kolam_train)
        y_kolam_test_encoded = kolam_encoder.transform(y_kolam_test)
        
        self.label_encoders['kolam_type'] = kolam_encoder
        
        # Try different models for kolam type
        models_to_try = {
            'random_forest': RandomForestClassifier(n_estimators=100, random_state=42),
            'svm': SVC(kernel='rbf', random_state=42),
            'mlp': MLPClassifier(hidden_layer_sizes=(100, 50), random_state=42, max_iter=500)
        }
        
        best_kolam_model = None
        best_kolam_score = 0
        
        for name, model in models_to_try.items():
            logger.info(f"Training {name} for kolam type...")
            model.fit(X_train, y_kolam_train_encoded)
            score = model.score(X_test, y_kolam_test_encoded)
            logger.info(f"{name} accuracy: {score:.3f}")
            
            if score > best_kolam_score:
                best_kolam_score = score
                best_kolam_model = model
        
        self.models['kolam_type'] = best_kolam_model
        logger.info(f"Best kolam type model accuracy: {best_kolam_score:.3f}")
        
        # 2. Symmetry Type Classification
        logger.info("Training Symmetry Type classifier...")
        symmetry_encoder = LabelEncoder()
        y_symmetry_encoded = symmetry_encoder.fit_transform(y_symmetry_type)
        
        self.label_encoders['symmetry_type'] = symmetry_encoder
        
        X_train_sym, X_test_sym, y_sym_train, y_sym_test = train_test_split(
            X_scaled, y_symmetry_encoded, test_size=0.2, random_state=42, stratify=y_symmetry_encoded
        )
        
        best_symmetry_model = None
        best_symmetry_score = 0
        
        for name, model in models_to_try.items():
            logger.info(f"Training {name} for symmetry type...")
            model = type(model)(**model.get_params())  # Create new instance
            model.fit(X_train_sym, y_sym_train)
            score = model.score(X_test_sym, y_sym_test)
            logger.info(f"{name} accuracy: {score:.3f}")
            
            if score > best_symmetry_score:
                best_symmetry_score = score
                best_symmetry_model = model
        
        self.models['symmetry_type'] = best_symmetry_model
        logger.info(f"Best symmetry type model accuracy: {best_symmetry_score:.3f}")
        
        # 3. Cultural Region Classification
        logger.info("Training Cultural Region classifier...")
        cultural_encoder = LabelEncoder()
        y_cultural_encoded = cultural_encoder.fit_transform(y_cultural_region)
        
        self.label_encoders['cultural_region'] = cultural_encoder
        
        X_train_cult, X_test_cult, y_cult_train, y_cult_test = train_test_split(
            X_scaled, y_cultural_encoded, test_size=0.2, random_state=42, stratify=y_cultural_encoded
        )
        
        best_cultural_model = None
        best_cultural_score = 0
        
        for name, model in models_to_try.items():
            logger.info(f"Training {name} for cultural region...")
            model = type(model)(**model.get_params())  # Create new instance
            model.fit(X_train_cult, y_cult_train)
            score = model.score(X_test_cult, y_cult_test)
            logger.info(f"{name} accuracy: {score:.3f}")
            
            if score > best_cultural_score:
                best_cultural_score = score
                best_cultural_model = model
        
        self.models['cultural_region'] = best_cultural_model
        logger.info(f"Best cultural region model accuracy: {best_cultural_score:.3f}")
        
        return {
            'kolam_type': best_kolam_score,
            'symmetry_type': best_symmetry_score,
            'cultural_region': best_cultural_score
        }
    
    def evaluate_models(self, test_data):
        """Evaluate models on test data"""
        logger.info("Evaluating models on test data...")
        
        X_test, y_kolam_test, y_symmetry_test, y_cultural_test = self.prepare_training_data(test_data)
        X_test_scaled = self.scalers['main'].transform(X_test)
        
        results = {}
        
        for task, model in self.models.items():
            logger.info(f"Evaluating {task} model...")
            
            # Get predictions
            y_pred = model.predict(X_test_scaled)
            y_true = self.label_encoders[task].transform([test_data[i]['annotation'][task] for i in range(len(test_data))])
            
            # Calculate metrics
            accuracy = accuracy_score(y_true, y_pred)
            results[task] = {
                'accuracy': accuracy,
                'predictions': y_pred,
                'true_labels': y_true
            }
            
            # Print classification report
            logger.info(f"\n{task.upper()} Classification Report:")
            unique_labels = np.unique(np.concatenate([y_true, y_pred]))
            target_names = [self.label_encoders[task].classes_[i] for i in unique_labels]
            logger.info(classification_report(y_true, y_pred, 
                                            labels=unique_labels,
                                            target_names=target_names))
        
        return results
    
    def save_models(self):
        """Save trained models and encoders"""
        logger.info("Saving models...")
        
        for task, model in self.models.items():
            model_path = f"models/{task}_model.pkl"
            joblib.dump(model, model_path)
            logger.info(f"Saved {task} model to {model_path}")
        
        # Save scalers and encoders
        joblib.dump(self.scalers, "models/scalers.pkl")
        joblib.dump(self.label_encoders, "models/label_encoders.pkl")
        joblib.dump(self.feature_names, "models/feature_names.pkl")
        
        logger.info("All models saved successfully!")
    
    def load_models(self):
        """Load pre-trained models"""
        logger.info("Loading pre-trained models...")
        
        try:
            for task in ['kolam_type', 'symmetry_type', 'cultural_region']:
                model_path = f"models/{task}_model.pkl"
                if os.path.exists(model_path):
                    self.models[task] = joblib.load(model_path)
                    logger.info(f"Loaded {task} model")
            
            self.scalers = joblib.load("models/scalers.pkl")
            self.label_encoders = joblib.load("models/label_encoders.pkl")
            self.feature_names = joblib.load("models/feature_names.pkl")
            
            logger.info("All models loaded successfully!")
            return True
            
        except Exception as e:
            logger.error(f"Error loading models: {e}")
            return False
    
    def predict(self, image):
        """Make predictions on a new image"""
        if not self.models:
            logger.error("No models loaded. Please train or load models first.")
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

def main():
    """Main training function"""
    logger.info("Starting Kolam Dataset Training...")
    
    # Initialize trainer
    trainer = KolamDatasetTrainer()
    
    # Load dataset
    all_data, train_data, val_data, test_data = trainer.load_dataset()
    
    if not all_data:
        logger.error("No data loaded. Please check dataset path.")
        return
    
    # Prepare training data
    X, y_kolam, y_symmetry, y_cultural = trainer.prepare_training_data(all_data)
    
    # Train models
    scores = trainer.train_models(X, y_kolam, y_symmetry, y_cultural)
    
    # Evaluate on test data
    if test_data:
        test_results = trainer.evaluate_models(test_data)
        logger.info("Test Results:")
        for task, result in test_results.items():
            logger.info(f"{task}: {result['accuracy']:.3f}")
    
    # Save models
    trainer.save_models()
    
    logger.info("Training completed successfully!")
    
    # Print summary
    logger.info("\n" + "="*50)
    logger.info("TRAINING SUMMARY")
    logger.info("="*50)
    logger.info(f"Total samples: {len(all_data)}")
    logger.info(f"Feature dimensions: {X.shape[1]}")
    logger.info("Model accuracies:")
    for task, score in scores.items():
        logger.info(f"  {task}: {score:.3f}")
    logger.info("="*50)

if __name__ == "__main__":
    main()
