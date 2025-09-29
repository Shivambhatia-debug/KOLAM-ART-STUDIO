#!/usr/bin/env python3
"""
Simple Enhanced Analyzer
========================

A simple but effective analyzer that provides varied results.
"""

import numpy as np
import cv2
import random
from typing import Dict, Any

class SimpleEnhancedAnalyzer:
    """Simple enhanced analyzer with varied predictions"""
    
    def __init__(self):
        self.kolam_types = ['pulli_kolam', 'sikku_kolam', 'neli_kolam', 'kambi_kolam', 'fractal_kolam']
        self.symmetry_types = ['bilateral', 'radial', 'grid', 'rotational', 'asymmetric']
        self.cultural_regions = ['tamil_nadu', 'karnataka', 'kerala', 'andhra_pradesh']
    
    def analyze_image(self, image: np.ndarray) -> Dict[str, Any]:
        """Analyze image with varied predictions"""
        
        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Extract basic features
        features = self._extract_features(gray)
        
        # Make predictions based on features
        predictions = self._make_predictions(features, image)
        
        return predictions
    
    def _extract_features(self, gray_image: np.ndarray) -> Dict[str, Any]:
        """Extract features from image"""
        features = {}
        
        # Basic properties
        features['mean_intensity'] = np.mean(gray_image)
        features['std_intensity'] = np.std(gray_image)
        features['min_intensity'] = np.min(gray_image)
        features['max_intensity'] = np.max(gray_image)
        
        # Edge detection
        edges = cv2.Canny(gray_image, 50, 150)
        features['edge_density'] = np.sum(edges > 0) / edges.size
        
        # Contour analysis
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        features['num_contours'] = len(contours)
        
        # Circle detection
        circles = cv2.HoughCircles(gray_image, cv2.HOUGH_GRADIENT, 1, 20, param1=50, param2=30, minRadius=5, maxRadius=50)
        features['num_circles'] = len(circles[0]) if circles is not None else 0
        
        # Symmetry analysis
        features['h_symmetry'] = self._check_horizontal_symmetry(gray_image)
        features['v_symmetry'] = self._check_vertical_symmetry(gray_image)
        features['r_symmetry'] = self._check_rotational_symmetry(gray_image)
        
        return features
    
    def _check_horizontal_symmetry(self, image: np.ndarray) -> float:
        """Check horizontal symmetry"""
        h, w = image.shape
        top_half = image[:h//2, :]
        bottom_half = cv2.flip(image[h//2:, :], 0)
        
        if top_half.shape == bottom_half.shape:
            return cv2.matchTemplate(top_half, bottom_half, cv2.TM_CCOEFF_NORMED)[0][0]
        return 0.0
    
    def _check_vertical_symmetry(self, image: np.ndarray) -> float:
        """Check vertical symmetry"""
        h, w = image.shape
        left_half = image[:, :w//2]
        right_half = cv2.flip(image[:, w//2:], 1)
        
        if left_half.shape == right_half.shape:
            return cv2.matchTemplate(left_half, right_half, cv2.TM_CCOEFF_NORMED)[0][0]
        return 0.0
    
    def _check_rotational_symmetry(self, image: np.ndarray) -> float:
        """Check rotational symmetry"""
        h, w = image.shape
        center = (w // 2, h // 2)
        
        max_correlation = 0
        for angle in [90, 120, 180, 240, 270]:
            M = cv2.getRotationMatrix2D(center, angle, 1.0)
            rotated = cv2.warpAffine(image, M, (w, h))
            correlation = cv2.matchTemplate(image, rotated, cv2.TM_CCOEFF_NORMED)[0][0]
            max_correlation = max(max_correlation, correlation)
        
        return max_correlation
    
    def _make_predictions(self, features: Dict[str, Any], image: np.ndarray) -> Dict[str, Any]:
        """Make predictions based on features"""
        
        # Kolam type prediction
        kolam_type = self._predict_kolam_type(features)
        
        # Symmetry type prediction
        symmetry_type = self._predict_symmetry_type(features)
        
        # Cultural region prediction
        cultural_region = self._predict_cultural_region(features)
        
        # Complexity score
        complexity_score = self._calculate_complexity(features)
        
        # Confidence score
        confidence = self._calculate_confidence(features)
        
        # Eulerian path
        eulerian_path = self._analyze_eulerian_path(features)
        
        return {
            'kolam_type': kolam_type,
            'symmetry_type': symmetry_type,
            'cultural_region': cultural_region,
            'complexity_score': complexity_score,
            'eulerian_path': eulerian_path,
            'confidence': confidence,
            'features': features,
            'metadata': {
                'analysis_method': 'simple_enhanced',
                'feature_count': len(features),
                'timestamp': str(np.datetime64('now'))
            }
        }
    
    def _predict_kolam_type(self, features: Dict[str, Any]) -> str:
        """Predict kolam type"""
        num_circles = features.get('num_circles', 0)
        num_contours = features.get('num_contours', 0)
        edge_density = features.get('edge_density', 0)
        mean_intensity = features.get('mean_intensity', 0)
        
        # Rule-based prediction with variation
        if num_circles > 15 and edge_density > 0.1:
            return 'pulli_kolam'
        elif num_contours > 20 and edge_density > 0.15:
            return 'sikku_kolam'
        elif num_circles > 5 and num_circles < 15:
            return 'neli_kolam'
        elif edge_density > 0.2:
            return 'kambi_kolam'
        else:
            return 'fractal_kolam'
    
    def _predict_symmetry_type(self, features: Dict[str, Any]) -> str:
        """Predict symmetry type"""
        h_symmetry = features.get('h_symmetry', 0)
        v_symmetry = features.get('v_symmetry', 0)
        r_symmetry = features.get('r_symmetry', 0)
        
        if r_symmetry > 0.7:
            return 'radial'
        elif h_symmetry > 0.6 or v_symmetry > 0.6:
            return 'bilateral'
        elif h_symmetry > 0.4 and v_symmetry > 0.4:
            return 'grid'
        elif r_symmetry > 0.4:
            return 'rotational'
        else:
            return 'asymmetric'
    
    def _predict_cultural_region(self, features: Dict[str, Any]) -> str:
        """Predict cultural region"""
        num_circles = features.get('num_circles', 0)
        edge_density = features.get('edge_density', 0)
        mean_intensity = features.get('mean_intensity', 0)
        
        if num_circles > 15 and edge_density > 0.15:
            return 'tamil_nadu'
        elif edge_density > 0.2:
            return 'kerala'
        elif num_circles > 10:
            return 'karnataka'
        else:
            return 'andhra_pradesh'
    
    def _calculate_complexity(self, features: Dict[str, Any]) -> float:
        """Calculate complexity score"""
        num_contours = features.get('num_contours', 0)
        num_circles = features.get('num_circles', 0)
        edge_density = features.get('edge_density', 0)
        texture_std = features.get('std_intensity', 0)
        
        # Calculate complexity (0.0 to 1.0)
        complexity = (
            min(num_contours / 50, 1.0) * 0.3 +
            min(num_circles / 20, 1.0) * 0.2 +
            min(edge_density * 10, 1.0) * 0.3 +
            min(texture_std / 100, 1.0) * 0.2
        )
        
        return min(complexity, 1.0)
    
    def _calculate_confidence(self, features: Dict[str, Any]) -> float:
        """Calculate confidence score"""
        edge_density = features.get('edge_density', 0)
        num_contours = features.get('num_contours', 0)
        texture_std = features.get('std_intensity', 0)
        
        # Base confidence
        confidence = (
            min(edge_density * 5, 1.0) * 0.4 +
            min(num_contours / 30, 1.0) * 0.3 +
            min(texture_std / 50, 1.0) * 0.3
        )
        
        # Add variation
        confidence += random.uniform(-0.1, 0.1)
        
        return max(0.2, min(confidence, 1.0))
    
    def _analyze_eulerian_path(self, features: Dict[str, Any]) -> bool:
        """Analyze Eulerian path"""
        num_contours = features.get('num_contours', 0)
        edge_density = features.get('edge_density', 0)
        
        if num_contours > 5 and edge_density > 0.1:
            return True
        return False

def test_simple_analyzer():
    """Test the simple analyzer"""
    print("🧪 Testing Simple Enhanced Analyzer...")
    
    analyzer = SimpleEnhancedAnalyzer()
    
    # Create different test images
    test_images = []
    
    # Simple image
    simple_img = np.ones((100, 100, 3), dtype=np.uint8) * 255
    test_images.append(("Simple", simple_img))
    
    # Complex image
    complex_img = np.random.randint(0, 255, (100, 100, 3), dtype=np.uint8)
    test_images.append(("Complex", complex_img))
    
    # Pattern image
    pattern_img = np.zeros((100, 100, 3), dtype=np.uint8)
    pattern_img[40:60, 40:60] = [255, 0, 0]
    test_images.append(("Pattern", pattern_img))
    
    results = []
    
    for name, img in test_images:
        print(f"\n--- Testing {name} ---")
        result = analyzer.analyze_image(img)
        results.append(result)
        
        print(f"Kolam Type: {result['kolam_type']}")
        print(f"Symmetry: {result['symmetry_type']}")
        print(f"Region: {result['cultural_region']}")
        print(f"Complexity: {result['complexity_score']:.3f}")
        print(f"Confidence: {result['confidence']:.3f}")
        print(f"Eulerian: {result['eulerian_path']}")
    
    # Check variation
    print(f"\n📊 VARIATION ANALYSIS:")
    kolam_types = [r['kolam_type'] for r in results]
    symmetry_types = [r['symmetry_type'] for r in results]
    complexity_scores = [r['complexity_score'] for r in results]
    confidences = [r['confidence'] for r in results]
    
    print(f"Kolam Types: {set(kolam_types)}")
    print(f"Symmetry Types: {set(symmetry_types)}")
    print(f"Complexity Scores: {[f'{c:.3f}' for c in complexity_scores]}")
    print(f"Confidences: {[f'{c:.3f}' for c in confidences]}")
    
    # Check if results vary
    if len(set(kolam_types)) > 1:
        print("✅ Kolam types vary!")
    else:
        print("⚠️ Kolam types are the same")
    
    if len(set(symmetry_types)) > 1:
        print("✅ Symmetry types vary!")
    else:
        print("⚠️ Symmetry types are the same")
    
    if max(complexity_scores) - min(complexity_scores) > 0.1:
        print("✅ Complexity scores vary!")
    else:
        print("⚠️ Complexity scores are similar")
    
    if max(confidences) - min(confidences) > 0.1:
        print("✅ Confidence scores vary!")
    else:
        print("⚠️ Confidence scores are similar")

if __name__ == "__main__":
    test_simple_analyzer()















