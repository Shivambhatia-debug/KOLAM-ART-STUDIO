#!/usr/bin/env python3
"""
Improved Kolam Image Analyzer
============================

Enhanced image analysis system that works with proper dataset.
Implements advanced computer vision techniques for Kolam pattern recognition.

Features:
- Dataset-based training and validation
- Advanced feature extraction
- Cultural classification
- Symmetry detection
- Eulerian path analysis
- Performance metrics
"""

import numpy as np
import cv2
import json
import os
import math
from typing import List, Dict, Any, Tuple, Optional
from dataclasses import dataclass
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import train_test_split
import joblib
from pathlib import Path

@dataclass
class AnalysisResult:
    kolam_type: str
    symmetry_type: str
    cultural_region: str
    complexity_score: float
    eulerian_path: bool
    confidence: float
    features: Dict[str, Any]
    metadata: Dict[str, Any]

class ImprovedKolamAnalyzer:
    def __init__(self, dataset_path: str = "kolam_dataset"):
        self.dataset_path = Path(dataset_path)
        self.model = None
        self.feature_scaler = None
        self.is_trained = False
        
        # Analysis parameters
        self.dot_detection_params = {
            'min_radius': 3,
            'max_radius': 20,
            'param1': 50,
            'param2': 30
        }
        
        self.line_detection_params = {
            'threshold1': 50,
            'threshold2': 150,
            'min_line_length': 30,
            'max_line_gap': 10
        }
    
    def load_dataset(self) -> Tuple[List[np.ndarray], List[Dict]]:
        """Load dataset images and annotations"""
        images = []
        annotations = []
        
        images_dir = self.dataset_path / "images"
        annotations_dir = self.dataset_path / "annotations"
        
        if not images_dir.exists() or not annotations_dir.exists():
            raise FileNotFoundError(f"Dataset not found at {self.dataset_path}")
        
        for image_file in images_dir.glob("*.png"):
            # Load image
            image = cv2.imread(str(image_file))
            if image is not None:
                images.append(image)
                
                # Load corresponding annotation
                annotation_file = annotations_dir / f"{image_file.stem}.json"
                if annotation_file.exists():
                    with open(annotation_file, 'r') as f:
                        annotation = json.load(f)
                        annotations.append(annotation)
                else:
                    # Create default annotation if missing
                    annotations.append({
                        'kolam_type': 'unknown',
                        'symmetry_type': 'unknown',
                        'cultural_region': 'unknown',
                        'complexity_score': 0.5,
                        'eulerian_path': False
                    })
        
        print(f"📊 Loaded {len(images)} images and {len(annotations)} annotations")
        return images, annotations
    
    def extract_features(self, image: np.ndarray) -> Dict[str, Any]:
        """Extract comprehensive features from Kolam image - Updated to match 26 expected features"""
        features = {}
        
        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # 1. Basic intensity features (7 features)
        features['mean_intensity'] = np.mean(gray)
        features['std_intensity'] = np.std(gray)
        features['min_intensity'] = np.min(gray)
        features['max_intensity'] = np.max(gray)
        features['median_intensity'] = np.median(gray)
        features['peak_intensity'] = np.percentile(gray, 95)
        
        # 2. Pixel distribution features (3 features)
        features['dark_pixels'] = np.sum(gray < 50) / gray.size
        features['bright_pixels'] = np.sum(gray > 200) / gray.size
        features['mid_tone_pixels'] = np.sum((gray >= 50) & (gray <= 200)) / gray.size
        
        # 3. Edge features (2 features)
        edges = cv2.Canny(gray, 50, 150)
        features['edge_pixels'] = np.sum(edges > 0) / edges.size
        features['edge_density'] = np.sum(edges > 0) / (edges.shape[0] * edges.shape[1])
        
        # 4. Contour features (4 features)
        contours, _ = cv2.findContours(gray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        features['num_contours'] = len(contours)
        if contours:
            areas = [cv2.contourArea(c) for c in contours]
            features['avg_contour_area'] = np.mean(areas)
            features['max_contour_area'] = np.max(areas)
            features['total_contour_area'] = np.sum(areas)
        else:
            features['avg_contour_area'] = 0
            features['max_contour_area'] = 0
            features['total_contour_area'] = 0
        
        # 5. Circle features (3 features)
        circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 20, param1=50, param2=30, minRadius=3, maxRadius=20)
        if circles is not None:
            circles = circles[0]
            features['num_circles'] = len(circles)
            features['avg_circle_radius'] = np.mean(circles[:, 2])
            features['circle_radius_std'] = np.std(circles[:, 2])
        else:
            features['num_circles'] = 0
            features['avg_circle_radius'] = 0
            features['circle_radius_std'] = 0
        
        # 6. Symmetry features (3 features)
        h, w = gray.shape
        # Horizontal symmetry
        top_half = gray[:h//2, :]
        bottom_half = cv2.flip(gray[h//2:, :], 0)
        if top_half.shape == bottom_half.shape:
            features['h_symmetry'] = cv2.matchTemplate(top_half, bottom_half, cv2.TM_CCOEFF_NORMED)[0][0]
        else:
            features['h_symmetry'] = 0
        
        # Vertical symmetry
        left_half = gray[:, :w//2]
        right_half = cv2.flip(gray[:, w//2:], 1)
        if left_half.shape == right_half.shape:
            features['v_symmetry'] = cv2.matchTemplate(left_half, right_half, cv2.TM_CCOEFF_NORMED)[0][0]
        else:
            features['v_symmetry'] = 0
        
        # Diagonal symmetry
        features['d_symmetry'] = self._check_diagonal_symmetry(gray)
        
        # 7. Texture features (2 features)
        features['texture_mean'] = np.mean(gray)
        features['texture_std'] = np.std(gray)
        
        # 8. Geometric features (2 features)
        features['aspect_ratio'] = w / h if h > 0 else 0
        features['center_x'] = w / 2
        features['center_y'] = h / 2
        
        return features
    
    def _check_diagonal_symmetry(self, image: np.ndarray) -> float:
        """Check for diagonal symmetry"""
        h, w = image.shape
        
        # Check main diagonal symmetry
        # Create flipped version along main diagonal
        flipped = cv2.flip(image, -1)  # Flip both horizontally and vertically
        
        # Calculate correlation
        correlation = cv2.matchTemplate(image, flipped, cv2.TM_CCOEFF_NORMED)[0][0]
        return correlation
    
    def _detect_dots(self, gray_image: np.ndarray) -> List[Tuple[int, int, int]]:
        """Detect dots using Hough Circle Transform"""
        # Apply Gaussian blur to reduce noise
        blurred = cv2.GaussianBlur(gray_image, (9, 9), 2)
        
        # Detect circles
        circles = cv2.HoughCircles(
            blurred,
            cv2.HOUGH_GRADIENT,
            dp=1,
            minDist=20,
            param1=self.dot_detection_params['param1'],
            param2=self.dot_detection_params['param2'],
            minRadius=self.dot_detection_params['min_radius'],
            maxRadius=self.dot_detection_params['max_radius']
        )
        
        if circles is not None:
            circles = np.round(circles[0, :]).astype("int")
            return [(x, y, r) for x, y, r in circles]
        
        return []
    
    def _detect_lines(self, gray_image: np.ndarray) -> List[Tuple[int, int, int, int]]:
        """Detect lines using Hough Line Transform"""
        # Apply Canny edge detection
        edges = cv2.Canny(
            gray_image,
            self.line_detection_params['threshold1'],
            self.line_detection_params['threshold2']
        )
        
        # Detect lines
        lines = cv2.HoughLinesP(
            edges,
            rho=1,
            theta=np.pi/180,
            threshold=50,
            minLineLength=self.line_detection_params['min_line_length'],
            maxLineGap=self.line_detection_params['max_line_gap']
        )
        
        if lines is not None:
            return [(x1, y1, x2, y2) for x1, y1, x2, y2 in lines.reshape(-1, 4)]
        
        return []
    
    def _analyze_symmetry(self, gray_image: np.ndarray) -> Dict[str, Any]:
        """Analyze symmetry properties"""
        features = {}
        
        # Rotational symmetry
        features['rotational_symmetry'] = self._check_rotational_symmetry(gray_image)
        
        # Bilateral symmetry
        features['bilateral_symmetry'] = self._check_bilateral_symmetry(gray_image)
        
        # Grid symmetry
        features['grid_symmetry'] = self._check_grid_symmetry(gray_image)
        
        return features
    
    def _check_rotational_symmetry(self, image: np.ndarray) -> float:
        """Check for rotational symmetry"""
        h, w = image.shape
        center = (w // 2, h // 2)
        
        # Test different rotation angles
        max_correlation = 0
        for angle in [90, 120, 180, 240, 270]:
            # Rotate image
            M = cv2.getRotationMatrix2D(center, angle, 1.0)
            rotated = cv2.warpAffine(image, M, (w, h))
            
            # Calculate correlation
            correlation = cv2.matchTemplate(image, rotated, cv2.TM_CCOEFF_NORMED)[0][0]
            max_correlation = max(max_correlation, correlation)
        
        return max_correlation
    
    def _check_bilateral_symmetry(self, image: np.ndarray) -> float:
        """Check for bilateral symmetry"""
        h, w = image.shape
        
        # Check vertical symmetry
        left_half = image[:, :w//2]
        right_half = cv2.flip(image[:, w//2:], 1)
        
        # Resize if necessary
        if left_half.shape != right_half.shape:
            right_half = cv2.resize(right_half, (left_half.shape[1], left_half.shape[0]))
        
        vertical_correlation = cv2.matchTemplate(left_half, right_half, cv2.TM_CCOEFF_NORMED)[0][0]
        
        # Check horizontal symmetry
        top_half = image[:h//2, :]
        bottom_half = cv2.flip(image[h//2:, :], 0)
        
        if top_half.shape != bottom_half.shape:
            bottom_half = cv2.resize(bottom_half, (top_half.shape[1], top_half.shape[0]))
        
        horizontal_correlation = cv2.matchTemplate(top_half, bottom_half, cv2.TM_CCOEFF_NORMED)[0][0]
        
        return max(vertical_correlation, horizontal_correlation)
    
    def _check_grid_symmetry(self, image: np.ndarray) -> float:
        """Check for grid symmetry"""
        h, w = image.shape
        
        # Divide image into grid
        grid_size = 4
        cell_h, cell_w = h // grid_size, w // grid_size
        
        correlations = []
        for i in range(grid_size):
            for j in range(grid_size):
                cell = image[i*cell_h:(i+1)*cell_h, j*cell_w:(j+1)*cell_w]
                
                # Check symmetry with opposite cell
                opp_i, opp_j = grid_size - 1 - i, grid_size - 1 - j
                opp_cell = image[opp_i*cell_h:(opp_i+1)*cell_h, opp_j*cell_w:(opp_j+1)*cell_w]
                
                if cell.shape == opp_cell.shape:
                    correlation = cv2.matchTemplate(cell, opp_cell, cv2.TM_CCOEFF_NORMED)[0][0]
                    correlations.append(correlation)
        
        return np.mean(correlations) if correlations else 0
    
    def _extract_geometric_features(self, gray_image: np.ndarray) -> Dict[str, Any]:
        """Extract geometric features"""
        features = {}
        
        # Find contours
        contours, _ = cv2.findContours(gray_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        if contours:
            # Largest contour
            largest_contour = max(contours, key=cv2.contourArea)
            
            # Area and perimeter
            features['contour_area'] = cv2.contourArea(largest_contour)
            features['contour_perimeter'] = cv2.arcLength(largest_contour, True)
            
            # Aspect ratio
            x, y, w, h = cv2.boundingRect(largest_contour)
            features['aspect_ratio'] = w / h if h > 0 else 0
            
            # Circularity
            features['circularity'] = 4 * np.pi * features['contour_area'] / (features['contour_perimeter'] ** 2) if features['contour_perimeter'] > 0 else 0
            
            # Solidity
            hull = cv2.convexHull(largest_contour)
            hull_area = cv2.contourArea(hull)
            features['solidity'] = features['contour_area'] / hull_area if hull_area > 0 else 0
        
        return features
    
    def _extract_texture_features(self, gray_image: np.ndarray) -> Dict[str, Any]:
        """Extract texture features using Local Binary Patterns"""
        features = {}
        
        # Calculate image moments
        moments = cv2.moments(gray_image)
        features['moment_hu_1'] = moments['m00']
        features['moment_hu_2'] = moments['m10'] / (moments['m00'] + 1e-10)
        features['moment_hu_3'] = moments['m01'] / (moments['m00'] + 1e-10)
        
        # Calculate standard deviation and mean
        features['texture_std'] = np.std(gray_image)
        features['texture_mean'] = np.mean(gray_image)
        
        # Calculate entropy
        hist, _ = np.histogram(gray_image.ravel(), 256, [0, 256])
        hist = hist / hist.sum()
        entropy = -np.sum(hist * np.log2(hist + 1e-10))
        features['texture_entropy'] = entropy
        
        return features
    
    def _analyze_eulerian_properties(self, gray_image: np.ndarray, dots: List, lines: List) -> Dict[str, Any]:
        """Analyze Eulerian path properties"""
        features = {}
        
        # Create graph from dots and lines
        graph = self._create_graph_from_elements(dots, lines)
        
        # Check if graph has Eulerian path
        features['has_eulerian_path'] = self._has_eulerian_path(graph)
        
        # Calculate graph properties
        if graph:
            features['num_vertices'] = len(graph)
            features['num_edges'] = sum(len(neighbors) for neighbors in graph.values()) // 2
            features['graph_density'] = features['num_edges'] / (features['num_vertices'] * (features['num_vertices'] - 1) / 2) if features['num_vertices'] > 1 else 0
        else:
            features['has_eulerian_path'] = False
            features['num_vertices'] = 0
            features['num_edges'] = 0
            features['graph_density'] = 0
        
        return features
    
    def _create_graph_from_elements(self, dots: List, lines: List) -> Dict[int, List[int]]:
        """Create graph from detected dots and lines"""
        graph = {}
        
        # Add vertices (dots)
        for i, (x, y, r) in enumerate(dots):
            graph[i] = []
        
        # Add edges (lines connecting dots)
        for x1, y1, x2, y2 in lines:
            # Find closest dots to line endpoints
            dot1_idx = self._find_closest_dot(x1, y1, dots)
            dot2_idx = self._find_closest_dot(x2, y2, dots)
            
            if dot1_idx is not None and dot2_idx is not None and dot1_idx != dot2_idx:
                if dot2_idx not in graph[dot1_idx]:
                    graph[dot1_idx].append(dot2_idx)
                if dot1_idx not in graph[dot2_idx]:
                    graph[dot2_idx].append(dot1_idx)
        
        return graph
    
    def _find_closest_dot(self, x: int, y: int, dots: List) -> Optional[int]:
        """Find closest dot to given coordinates"""
        min_distance = float('inf')
        closest_idx = None
        
        for i, (dx, dy, r) in enumerate(dots):
            distance = math.sqrt((x - dx) ** 2 + (y - dy) ** 2)
            if distance < min_distance and distance < r * 3:  # Within 3 times radius
                min_distance = distance
                closest_idx = i
        
        return closest_idx
    
    def _has_eulerian_path(self, graph: Dict[int, List[int]]) -> bool:
        """Check if graph has Eulerian path"""
        if not graph:
            return False
        
        # Count vertices with odd degree
        odd_degree_count = 0
        for vertex in graph:
            if len(graph[vertex]) % 2 == 1:
                odd_degree_count += 1
        
        # Eulerian path exists if 0 or 2 vertices have odd degree
        return odd_degree_count == 0 or odd_degree_count == 2
    
    def train_model(self, images: List[np.ndarray], annotations: List[Dict]) -> Dict[str, Any]:
        """Train classification model on dataset"""
        print("🎯 Training Kolam analysis model...")
        
        # Extract features
        X = []
        y_kolam_type = []
        y_symmetry_type = []
        y_cultural_region = []
        
        for i, (image, annotation) in enumerate(zip(images, annotations)):
            if i % 10 == 0:
                print(f"Processing image {i+1}/{len(images)}")
            
            features = self.extract_features(image)
            X.append(list(features.values()))
            
            y_kolam_type.append(annotation.get('kolam_type', 'unknown'))
            y_symmetry_type.append(annotation.get('symmetry_type', 'unknown'))
            y_cultural_region.append(annotation.get('cultural_region', 'unknown'))
        
        X = np.array(X)
        
        # Train models for each classification task
        models = {}
        results = {}
        
        # Kolam type classification
        if len(set(y_kolam_type)) > 1:
            X_train, X_test, y_train, y_test = train_test_split(X, y_kolam_type, test_size=0.2, random_state=42)
            model = RandomForestClassifier(n_estimators=100, random_state=42)
            model.fit(X_train, y_train)
            y_pred = model.predict(X_test)
            
            models['kolam_type'] = model
            results['kolam_type'] = {
                'accuracy': model.score(X_test, y_test),
                'classification_report': classification_report(y_test, y_pred, output_dict=True)
            }
        
        # Symmetry type classification
        if len(set(y_symmetry_type)) > 1:
            X_train, X_test, y_train, y_test = train_test_split(X, y_symmetry_type, test_size=0.2, random_state=42)
            model = RandomForestClassifier(n_estimators=100, random_state=42)
            model.fit(X_train, y_train)
            y_pred = model.predict(X_test)
            
            models['symmetry_type'] = model
            results['symmetry_type'] = {
                'accuracy': model.score(X_test, y_test),
                'classification_report': classification_report(y_test, y_pred, output_dict=True)
            }
        
        # Cultural region classification
        if len(set(y_cultural_region)) > 1:
            X_train, X_test, y_train, y_test = train_test_split(X, y_cultural_region, test_size=0.2, random_state=42)
            model = RandomForestClassifier(n_estimators=100, random_state=42)
            model.fit(X_train, y_train)
            y_pred = model.predict(X_test)
            
            models['cultural_region'] = model
            results['cultural_region'] = {
                'accuracy': model.score(X_test, y_test),
                'classification_report': classification_report(y_test, y_pred, output_dict=True)
            }
        
        self.model = models
        self.is_trained = True
        
        # Save models
        os.makedirs("models", exist_ok=True)
        for task, model in models.items():
            joblib.dump(model, f"models/{task}_model.pkl")
        
        print("✅ Model training complete!")
        return results
    
    def analyze_image(self, image: np.ndarray) -> AnalysisResult:
        """Analyze single Kolam image"""
        if not self.is_trained:
            raise ValueError("Model not trained. Call train_model() first.")
        
        # Extract features
        features = self.extract_features(image)
        feature_vector = np.array(list(features.values())).reshape(1, -1)
        
        # Load label encoders if available
        try:
            import pickle
            with open('models/label_encoders.pkl', 'rb') as f:
                label_encoders = pickle.load(f)
        except:
            label_encoders = {}
        
        # Make predictions
        predictions = {}
        confidences = {}
        
        for task, model in self.model.items():
            prediction = model.predict(feature_vector)[0]
            confidence = model.predict_proba(feature_vector).max()
            
            # Convert numeric prediction back to label if encoder available
            if task in label_encoders:
                try:
                    prediction = label_encoders[task].inverse_transform([prediction])[0]
                except:
                    pass  # Keep numeric if conversion fails
            
            predictions[task] = prediction
            confidences[task] = confidence
        
        # Calculate overall confidence
        overall_confidence = np.mean(list(confidences.values()))
        
        # Calculate dynamic complexity score based on features
        complexity_factors = {
            'num_contours': features.get('num_contours', 0) * 0.1,
            'num_circles': features.get('num_circles', 0) * 0.05,
            'edge_density': features.get('edge_density', 0) * 100,
            'texture_std': features.get('texture_std', 0) / 100,
            'symmetry_complexity': (features.get('h_symmetry', 0) + features.get('v_symmetry', 0) + features.get('d_symmetry', 0)) / 3
        }
        
        # Calculate complexity score (0.0 to 1.0)
        complexity_score = min(1.0, sum(complexity_factors.values()) / 5.0)
        
        # Create analysis result
        result = AnalysisResult(
            kolam_type=predictions.get('kolam_type', 'unknown'),
            symmetry_type=predictions.get('symmetry_type', 'unknown'),
            cultural_region=predictions.get('cultural_region', 'unknown'),
            complexity_score=complexity_score,
            eulerian_path=features.get('has_eulerian_path', False),
            confidence=overall_confidence,
            features=features,
            metadata={
                'analysis_timestamp': str(np.datetime64('now')),
                'model_version': '1.0.0',
                'feature_count': len(features),
                'complexity_factors': complexity_factors
            }
        )
        
        return result
    
    def evaluate_model(self, test_images: List[np.ndarray], test_annotations: List[Dict]) -> Dict[str, Any]:
        """Evaluate model performance on test set"""
        if not self.is_trained:
            raise ValueError("Model not trained. Call train_model() first.")
        
        print("📊 Evaluating model performance...")
        
        predictions = []
        ground_truth = []
        
        for image, annotation in zip(test_images, test_annotations):
            result = self.analyze_image(image)
            predictions.append(result)
            ground_truth.append(annotation)
        
        # Calculate metrics
        metrics = {}
        
        for task in ['kolam_type', 'symmetry_type', 'cultural_region']:
            if task in self.model:
                pred_values = [getattr(p, task) for p in predictions]
                true_values = [gt.get(task, 'unknown') for gt in ground_truth]
                
                accuracy = sum(p == t for p, t in zip(pred_values, true_values)) / len(pred_values)
                metrics[task] = {'accuracy': accuracy}
        
        return metrics

def main():
    """Main function to demonstrate the improved analyzer"""
    print("🎨 Improved Kolam Image Analyzer")
    print("=" * 50)
    
    # Initialize analyzer
    analyzer = ImprovedKolamAnalyzer("kolam_dataset")
    
    try:
        # Load dataset
        images, annotations = analyzer.load_dataset()
        
        if len(images) == 0:
            print("❌ No images found in dataset. Please generate dataset first.")
            return
        
        # Train model
        training_results = analyzer.train_model(images, annotations)
        
        print("\n📊 Training Results:")
        for task, results in training_results.items():
            print(f"   {task}: {results['accuracy']:.3f} accuracy")
        
        # Test on a few images
        print("\n🔍 Testing analysis on sample images...")
        for i in range(min(3, len(images))):
            result = analyzer.analyze_image(images[i])
            print(f"\nImage {i+1}:")
            print(f"   Kolam Type: {result.kolam_type}")
            print(f"   Symmetry: {result.symmetry_type}")
            print(f"   Cultural Region: {result.cultural_region}")
            print(f"   Eulerian Path: {result.eulerian_path}")
            print(f"   Confidence: {result.confidence:.3f}")
        
        print("\n✅ Analysis system ready!")
        
    except FileNotFoundError as e:
        print(f"❌ {e}")
        print("💡 Please run 'python kolam_dataset_generator.py' first to create the dataset.")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()



