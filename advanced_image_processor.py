"""
Advanced Kolam Image Processing Module
====================================

Implements Steps 2-4 from the comprehensive plan:
- Step 2: Dot Detection with Hough Circle Transform
- Step 3: Line Skeletonization and Edge Extraction  
- Step 4: Graph Analysis for Eulerian Property

Uses OpenCV for image processing and NetworkX for graph analysis.
"""

import cv2
import numpy as np
import networkx as nx
from skimage import morphology, measure
from scipy import ndimage
import json
import math

class AdvancedKolamImageProcessor:
    def __init__(self):
        self.original_image = None
        self.processed_image = None
        self.detected_dots = []
        self.skeleton = None
        self.graph = None
        self.analysis_results = {}
    
    def preprocess_image(self, image_path_or_array, perspective_correction=True):
        """
        Step 1 Enhancement: Advanced Image Preprocessing
        """
        if isinstance(image_path_or_array, str):
            self.original_image = cv2.imread(image_path_or_array)
        else:
            self.original_image = image_path_or_array
        
        # Convert to grayscale
        gray = cv2.cvtColor(self.original_image, cv2.COLOR_BGR2GRAY)
        
        # Noise reduction with Gaussian blur
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        
        # Adaptive thresholding for better binarization
        binary = cv2.adaptiveThreshold(
            blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
            cv2.THRESH_BINARY_INV, 11, 2
        )
        
        # Optional perspective correction
        if perspective_correction:
            binary = self._correct_perspective(binary)
        
        self.processed_image = binary
        return binary
    
    def _correct_perspective(self, image):
        """
        Perspective correction for photos taken at an angle
        """
        # Find contours to detect the main Kolam boundary
        contours, _ = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        if contours:
            # Find the largest contour (assuming it's the Kolam boundary)
            largest_contour = max(contours, key=cv2.contourArea)
            
            # Approximate contour to find corners
            epsilon = 0.02 * cv2.arcLength(largest_contour, True)
            approx = cv2.approxPolyDP(largest_contour, epsilon, True)
            
            # If we found a quadrilateral, apply perspective correction
            if len(approx) == 4:
                # Order the points: top-left, top-right, bottom-right, bottom-left
                rect = self._order_points(approx.reshape(4, 2))
                
                # Compute the width and height of the new image
                (tl, tr, br, bl) = rect
                widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
                widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
                maxWidth = max(int(widthA), int(widthB))
                
                heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
                heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
                maxHeight = max(int(heightA), int(heightB))
                
                # Construct the destination points
                dst = np.array([
                    [0, 0],
                    [maxWidth - 1, 0],
                    [maxWidth - 1, maxHeight - 1],
                    [0, maxHeight - 1]
                ], dtype="float32")
                
                # Compute the perspective transform matrix and apply it
                M = cv2.getPerspectiveTransform(rect, dst)
                image = cv2.warpPerspective(image, M, (maxWidth, maxHeight))
        
        return image
    
    def _order_points(self, pts):
        """
        Order points in the order: top-left, top-right, bottom-right, bottom-left
        """
        rect = np.zeros((4, 2), dtype="float32")
        
        # Top-left point has the smallest sum
        # Bottom-right has the largest sum
        s = pts.sum(axis=1)
        rect[0] = pts[np.argmin(s)]
        rect[2] = pts[np.argmax(s)]
        
        # Top-right has smallest difference
        # Bottom-left has largest difference
        diff = np.diff(pts, axis=1)
        rect[1] = pts[np.argmin(diff)]
        rect[3] = pts[np.argmax(diff)]
        
        return rect
    
    def detect_dots_hough_circles(self, min_radius=3, max_radius=20, param1=50, param2=30):
        """
        Step 2: Advanced Dot Detection using Hough Circle Transform
        """
        if self.processed_image is None:
            raise ValueError("Image must be preprocessed first")
        
        # Invert image for circle detection (circles should be white on black)
        inverted = cv2.bitwise_not(self.processed_image)
        
        # Apply Hough Circle Transform
        circles = cv2.HoughCircles(
            inverted,
            cv2.HOUGH_GRADIENT,
            dp=1,
            minDist=20,
            param1=param1,
            param2=param2,
            minRadius=min_radius,
            maxRadius=max_radius
        )
        
        detected_dots = []
        if circles is not None:
            circles = np.round(circles[0, :]).astype("int")
            
            for (x, y, r) in circles:
                detected_dots.append({
                    'x': int(x),
                    'y': int(y), 
                    'radius': int(r),
                    'confidence': 1.0
                })
        
        # If Hough circles don't work well, fall back to connected component analysis
        if len(detected_dots) < 5:
            detected_dots = self._detect_dots_connected_components()
        
        self.detected_dots = self._sort_dots_to_grid(detected_dots)
        return self.detected_dots
    
    def _detect_dots_connected_components(self):
        """
        Alternative dot detection using Connected Component Analysis
        """
        # Find connected components
        labeled_image = measure.label(self.processed_image)
        regions = measure.regionprops(labeled_image)
        
        detected_dots = []
        for region in regions:
            # Filter by area and eccentricity to find dot-like shapes
            if 10 < region.area < 500 and region.eccentricity < 0.8:
                y, x = region.centroid
                detected_dots.append({
                    'x': int(x),
                    'y': int(y),
                    'radius': int(np.sqrt(region.area / np.pi)),
                    'confidence': 1.0 - region.eccentricity
                })
        
        return detected_dots
    
    def _sort_dots_to_grid(self, dots):
        """
        Sort and map dots into a 2D grid based on their positions
        """
        if not dots:
            return dots
        
        # Sort by y-coordinate first (top to bottom), then x-coordinate (left to right)
        sorted_dots = sorted(dots, key=lambda d: (d['y'], d['x']))
        
        # Try to detect grid structure
        y_positions = [d['y'] for d in sorted_dots]
        unique_y = []
        tolerance = 20  # pixels
        
        for y in y_positions:
            if not any(abs(y - uy) < tolerance for uy in unique_y):
                unique_y.append(y)
        
        unique_y.sort()
        
        # Group dots by rows
        grid_dots = []
        for target_y in unique_y:
            row_dots = [d for d in sorted_dots if abs(d['y'] - target_y) < tolerance]
            row_dots.sort(key=lambda d: d['x'])
            
            # Add grid coordinates
            for i, dot in enumerate(row_dots):
                dot['grid_row'] = len(grid_dots)
                dot['grid_col'] = i
            
            grid_dots.extend(row_dots)
        
        return grid_dots
    
    def skeletonize_lines(self):
        """
        Step 3: Line Skeletonization and Edge Extraction
        """
        if self.processed_image is None:
            raise ValueError("Image must be preprocessed first")
        
        # Create a copy without dots for line skeletonization
        image_without_dots = self.processed_image.copy()
        
        # Remove detected dots from the image
        for dot in self.detected_dots:
            cv2.circle(image_without_dots, (dot['x'], dot['y']), dot['radius'] + 2, 0, -1)
        
        # Apply morphological operations to clean up lines
        kernel = np.ones((3, 3), np.uint8)
        cleaned = cv2.morphologyEx(image_without_dots, cv2.MORPH_CLOSE, kernel)
        
        # Skeletonize the lines
        skeleton = morphology.skeletonize(cleaned > 0)
        self.skeleton = skeleton.astype(np.uint8) * 255
        
        return self.skeleton
    
    def extract_line_graph(self):
        """
        Step 3: Build graph representation from skeleton
        """
        if self.skeleton is None:
            self.skeletonize_lines()
        
        # Find junctions and endpoints in skeleton
        junctions, endpoints = self._find_skeleton_features()
        
        # Create graph
        self.graph = nx.Graph()
        
        # Add dots as nodes
        for i, dot in enumerate(self.detected_dots):
            self.graph.add_node(f"dot_{i}", pos=(dot['x'], dot['y']), type='dot')
        
        # Add junction points as nodes  
        for i, (x, y) in enumerate(junctions):
            self.graph.add_node(f"junction_{i}", pos=(x, y), type='junction')
        
        # Add endpoint nodes
        for i, (x, y) in enumerate(endpoints):
            self.graph.add_node(f"endpoint_{i}", pos=(x, y), type='endpoint')
        
        # Connect nearby nodes with edges
        self._connect_nearby_nodes()
        
        return self.graph
    
    def _find_skeleton_features(self):
        """
        Find junctions and endpoints in the skeleton
        """
        # Create kernels for detecting junctions and endpoints
        junction_kernel = np.array([
            [1, 1, 1],
            [1, 10, 1], 
            [1, 1, 1]
        ])
        
        endpoint_kernel = np.array([
            [1, 1, 1],
            [1, 10, 1],
            [1, 1, 1]
        ])
        
        # Convolve skeleton with kernels
        skeleton_binary = self.skeleton > 0
        convolved = ndimage.convolve(skeleton_binary.astype(int), junction_kernel)
        
        # Find junctions (pixels with 3+ neighbors)
        junction_mask = (convolved >= 13) & skeleton_binary
        junctions = np.column_stack(np.where(junction_mask))[:, [1, 0]]  # (x, y) format
        
        # Find endpoints (pixels with exactly 1 neighbor)
        endpoint_mask = (convolved == 11) & skeleton_binary
        endpoints = np.column_stack(np.where(endpoint_mask))[:, [1, 0]]  # (x, y) format
        
        return junctions.tolist(), endpoints.tolist()
    
    def _connect_nearby_nodes(self, max_distance=50):
        """
        Connect nodes that are close to each other
        """
        nodes = list(self.graph.nodes(data=True))
        
        for i, (node1, data1) in enumerate(nodes):
            for j, (node2, data2) in enumerate(nodes[i+1:], i+1):
                pos1 = data1['pos']
                pos2 = data2['pos']
                
                distance = np.sqrt((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2)
                
                if distance <= max_distance:
                    # Check if there's a line connecting these points in the skeleton
                    if self._line_exists_between_points(pos1, pos2):
                        self.graph.add_edge(node1, node2, weight=distance)
    
    def _line_exists_between_points(self, pos1, pos2):
        """
        Check if a line exists between two points in the skeleton
        """
        x1, y1 = int(pos1[0]), int(pos1[1])
        x2, y2 = int(pos2[0]), int(pos2[1])
        
        # Use Bresenham's line algorithm to sample points along the line
        points = self._bresenham_line(x1, y1, x2, y2)
        
        # Check if most points along the line are part of the skeleton
        skeleton_points = 0
        for x, y in points:
            if 0 <= x < self.skeleton.shape[1] and 0 <= y < self.skeleton.shape[0]:
                if self.skeleton[y, x] > 0:
                    skeleton_points += 1
        
        # If more than 70% of points are on the skeleton, consider it a valid connection
        return skeleton_points / len(points) > 0.7
    
    def _bresenham_line(self, x1, y1, x2, y2):
        """
        Bresenham's line algorithm to get points along a line
        """
        points = []
        dx = abs(x2 - x1)
        dy = abs(y2 - y1)
        sx = 1 if x1 < x2 else -1
        sy = 1 if y1 < y2 else -1
        err = dx - dy
        
        while True:
            points.append((x1, y1))
            
            if x1 == x2 and y1 == y2:
                break
                
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x1 += sx
            if e2 < dx:
                err += dx
                y1 += sy
        
        return points
    
    def analyze_eulerian_properties(self):
        """
        Step 4: Graph Analysis for Eulerian Property
        """
        if self.graph is None:
            self.extract_line_graph()
        
        analysis = {
            'is_eulerian': False,
            'is_semi_eulerian': False,
            'node_count': self.graph.number_of_nodes(),
            'edge_count': self.graph.number_of_edges(),
            'degree_sequence': [],
            'odd_degree_nodes': [],
            'connected_components': 0,
            'euler_path_exists': False,
            'recommendations': []
        }
        
        if self.graph.number_of_nodes() == 0:
            analysis['recommendations'].append("No nodes detected. Check image quality and preprocessing.")
            return analysis
        
        # Calculate degree sequence
        degrees = dict(self.graph.degree())
        analysis['degree_sequence'] = list(degrees.values())
        
        # Find odd degree nodes
        odd_degree_nodes = [node for node, degree in degrees.items() if degree % 2 == 1]
        analysis['odd_degree_nodes'] = odd_degree_nodes
        
        # Check connectivity
        if nx.is_connected(self.graph):
            analysis['connected_components'] = 1
            
            # Eulerian circuit: all nodes have even degree
            if len(odd_degree_nodes) == 0:
                analysis['is_eulerian'] = True
                analysis['euler_path_exists'] = True
                analysis['recommendations'].append("Perfect! This Kolam has an Eulerian circuit - can be drawn without lifting the hand.")
            
            # Eulerian path: exactly 2 nodes have odd degree
            elif len(odd_degree_nodes) == 2:
                analysis['is_semi_eulerian'] = True
                analysis['euler_path_exists'] = True
                analysis['recommendations'].append("This Kolam has an Eulerian path - can be drawn without lifting the hand if you start and end at specific points.")
            
            else:
                analysis['recommendations'].append(f"This Kolam has {len(odd_degree_nodes)} nodes with odd degree. Traditional Kolams should have 0 or 2 such nodes.")
        
        else:
            analysis['connected_components'] = nx.number_connected_components(self.graph)
            analysis['recommendations'].append(f"This design has {analysis['connected_components']} separate components. Traditional Kolams are usually connected.")
        
        return analysis
    
    def calculate_symmetry_score(self, symmetry_type='rotational'):
        """
        Step 5: Enhanced Symmetry Analysis
        """
        if not self.detected_dots:
            return {'score': 0, 'type': 'none', 'details': 'No dots detected'}
        
        # Create point cloud from dots
        points = np.array([(dot['x'], dot['y']) for dot in self.detected_dots])
        
        if symmetry_type == 'rotational':
            return self._calculate_rotational_symmetry(points)
        elif symmetry_type == 'bilateral':
            return self._calculate_bilateral_symmetry(points)
        elif symmetry_type == 'radial':
            return self._calculate_radial_symmetry(points)
        else:
            return {'score': 0, 'type': 'unknown', 'details': 'Unknown symmetry type'}
    
    def _calculate_rotational_symmetry(self, points):
        """
        Calculate rotational symmetry score
        """
        center = np.mean(points, axis=0)
        centered_points = points - center
        
        best_score = 0
        best_fold = 0
        
        # Test 2-fold, 3-fold, 4-fold, 6-fold, 8-fold symmetry
        for fold in [2, 3, 4, 6, 8]:
            angle = 2 * np.pi / fold
            
            # Rotate points by the angle
            cos_a, sin_a = np.cos(angle), np.sin(angle)
            rotation_matrix = np.array([[cos_a, -sin_a], [sin_a, cos_a]])
            rotated_points = centered_points @ rotation_matrix.T
            
            # Calculate overlap score
            score = self._calculate_point_overlap(centered_points, rotated_points)
            
            if score > best_score:
                best_score = score
                best_fold = fold
        
        return {
            'score': best_score,
            'type': f'{best_fold}-fold rotational',
            'fold': best_fold,
            'details': f'Best rotational symmetry: {best_fold}-fold with {best_score:.1%} accuracy'
        }
    
    def _calculate_bilateral_symmetry(self, points):
        """
        Calculate bilateral symmetry score
        """
        center = np.mean(points, axis=0)
        centered_points = points - center
        
        best_score = 0
        best_axis = 'none'
        
        # Test vertical and horizontal symmetry
        for axis, reflection_matrix in [
            ('vertical', np.array([[-1, 0], [0, 1]])),
            ('horizontal', np.array([[1, 0], [0, -1]]))
        ]:
            reflected_points = centered_points @ reflection_matrix.T
            score = self._calculate_point_overlap(centered_points, reflected_points)
            
            if score > best_score:
                best_score = score
                best_axis = axis
        
        return {
            'score': best_score,
            'type': f'bilateral ({best_axis})',
            'axis': best_axis,
            'details': f'Best bilateral symmetry: {best_axis} axis with {best_score:.1%} accuracy'
        }
    
    def _calculate_radial_symmetry(self, points):
        """
        Calculate radial symmetry score (point symmetry through center)
        """
        center = np.mean(points, axis=0)
        centered_points = points - center
        
        # Point reflection through center
        reflected_points = -centered_points
        score = self._calculate_point_overlap(centered_points, reflected_points)
        
        return {
            'score': score,
            'type': 'radial (point)',
            'details': f'Radial symmetry through center: {score:.1%} accuracy'
        }
    
    def _calculate_point_overlap(self, points1, points2, tolerance=10):
        """
        Calculate overlap percentage between two point sets
        """
        if len(points1) == 0 or len(points2) == 0:
            return 0.0
        
        matches = 0
        for p1 in points1:
            distances = np.sqrt(np.sum((points2 - p1)**2, axis=1))
            if np.min(distances) <= tolerance:
                matches += 1
        
        return matches / len(points1)
    
    def generate_comprehensive_analysis(self):
        """
        Generate comprehensive analysis combining all steps
        """
        # Ensure all analysis steps are completed
        if not self.detected_dots:
            self.detect_dots_hough_circles()
        
        if self.skeleton is None:
            self.skeletonize_lines()
        
        if self.graph is None:
            self.extract_line_graph()
        
        eulerian_analysis = self.analyze_eulerian_properties()
        symmetry_analysis = self._analyze_all_symmetries()
        
        # Calculate additional metrics
        metrics = self._calculate_pattern_metrics()
        
        comprehensive_analysis = {
            'image_processing': {
                'dots_detected': len(self.detected_dots),
                'skeleton_generated': self.skeleton is not None,
                'graph_constructed': self.graph is not None
            },
            'geometric_properties': {
                'dot_count': len(self.detected_dots),
                'graph_nodes': eulerian_analysis['node_count'],
                'graph_edges': eulerian_analysis['edge_count'],
                'connected_components': eulerian_analysis['connected_components']
            },
            'eulerian_analysis': eulerian_analysis,
            'symmetry_analysis': symmetry_analysis,
            'pattern_metrics': metrics,
            'cultural_classification': self._classify_cultural_style(),
            'quality_score': self._calculate_quality_score(eulerian_analysis, symmetry_analysis),
            'recommendations': self._generate_recommendations(eulerian_analysis, symmetry_analysis)
        }
        
        return comprehensive_analysis
    
    def _analyze_all_symmetries(self):
        """
        Analyze all types of symmetry
        """
        if not self.detected_dots:
            return {'rotational': {'score': 0}, 'bilateral': {'score': 0}, 'radial': {'score': 0}}
        
        return {
            'rotational': self.calculate_symmetry_score('rotational'),
            'bilateral': self.calculate_symmetry_score('bilateral'),
            'radial': self.calculate_symmetry_score('radial')
        }
    
    def _calculate_pattern_metrics(self):
        """
        Calculate additional pattern metrics
        """
        if not self.detected_dots:
            return {}
        
        points = np.array([(dot['x'], dot['y']) for dot in self.detected_dots])
        
        # Calculate bounding box
        min_x, min_y = np.min(points, axis=0)
        max_x, max_y = np.max(points, axis=0)
        
        # Calculate average distances
        center = np.mean(points, axis=0)
        distances_from_center = np.sqrt(np.sum((points - center)**2, axis=1))
        
        return {
            'bounding_box': {
                'width': int(max_x - min_x),
                'height': int(max_y - min_y),
                'aspect_ratio': float((max_x - min_x) / (max_y - min_y)) if max_y != min_y else 1.0
            },
            'center_point': {'x': float(center[0]), 'y': float(center[1])},
            'radius_stats': {
                'mean_radius': float(np.mean(distances_from_center)),
                'max_radius': float(np.max(distances_from_center)),
                'min_radius': float(np.min(distances_from_center))
            },
            'density': len(self.detected_dots) / ((max_x - min_x) * (max_y - min_y)) if max_x != min_x and max_y != min_y else 0
        }
    
    def _classify_cultural_style(self):
        """
        Classify cultural style based on pattern characteristics
        """
        if not self.detected_dots:
            return {'region': 'unknown', 'confidence': 0.0}
        
        # Simple rule-based classification (can be enhanced with ML)
        symmetry_analysis = self._analyze_all_symmetries()
        metrics = self._calculate_pattern_metrics()
        
        scores = {
            'tamil_nadu': 0.0,
            'karnataka': 0.0,
            'kerala': 0.0,
            'andhra_pradesh': 0.0
        }
        
        # Tamil Nadu: High rotational symmetry, radial patterns
        if symmetry_analysis['rotational']['score'] > 0.7:
            scores['tamil_nadu'] += 0.4
        if symmetry_analysis['radial']['score'] > 0.6:
            scores['tamil_nadu'] += 0.3
        
        # Karnataka: Geometric precision, bilateral symmetry
        if symmetry_analysis['bilateral']['score'] > 0.7:
            scores['karnataka'] += 0.4
        if metrics.get('bounding_box', {}).get('aspect_ratio', 0) > 0.8:  # Square-ish
            scores['karnataka'] += 0.3
        
        # Kerala: Organic, less symmetric
        if all(s['score'] < 0.5 for s in symmetry_analysis.values()):
            scores['kerala'] += 0.5
        
        # Andhra Pradesh: Complex, high dot density
        if len(self.detected_dots) > 20:
            scores['andhra_pradesh'] += 0.4
        if self.graph and self.graph.number_of_edges() > 25:
            scores['andhra_pradesh'] += 0.3
        
        best_region = max(scores, key=scores.get)
        confidence = scores[best_region]
        
        return {
            'region': best_region,
            'confidence': confidence,
            'all_scores': scores
        }
    
    def _calculate_quality_score(self, eulerian_analysis, symmetry_analysis):
        """
        Calculate overall quality score of the Kolam
        """
        score = 0.0
        
        # Eulerian properties (40% weight)
        if eulerian_analysis['is_eulerian']:
            score += 0.4
        elif eulerian_analysis['is_semi_eulerian']:
            score += 0.3
        elif eulerian_analysis['euler_path_exists']:
            score += 0.2
        
        # Symmetry (30% weight)
        max_symmetry = max([s.get('score', 0) for s in symmetry_analysis.values()])
        score += 0.3 * max_symmetry
        
        # Connectivity (20% weight)
        if eulerian_analysis['connected_components'] == 1:
            score += 0.2
        elif eulerian_analysis['connected_components'] <= 3:
            score += 0.1
        
        # Dot count (10% weight) - optimal range is 9-36 dots
        dot_count = len(self.detected_dots)
        if 9 <= dot_count <= 36:
            score += 0.1
        elif 5 <= dot_count <= 50:
            score += 0.05
        
        return min(score, 1.0)  # Cap at 1.0
    
    def _generate_recommendations(self, eulerian_analysis, symmetry_analysis):
        """
        Generate recommendations for improving the Kolam
        """
        recommendations = []
        
        # Eulerian recommendations
        if not eulerian_analysis['euler_path_exists']:
            recommendations.append("Add or remove connections to create an Eulerian path for traditional single-line drawing")
        
        # Symmetry recommendations
        max_symmetry = max([s.get('score', 0) for s in symmetry_analysis.values()])
        if max_symmetry < 0.5:
            recommendations.append("Consider improving symmetry for better visual balance")
        
        # Connectivity recommendations
        if eulerian_analysis['connected_components'] > 1:
            recommendations.append(f"Connect the {eulerian_analysis['connected_components']} separate parts for a unified design")
        
        # Dot count recommendations
        dot_count = len(self.detected_dots)
        if dot_count < 5:
            recommendations.append("Add more dots to create a richer pattern")
        elif dot_count > 50:
            recommendations.append("Consider simplifying the design with fewer dots")
        
        return recommendations
    
    def export_analysis_results(self, output_path):
        """
        Export comprehensive analysis results to JSON
        """
        analysis = self.generate_comprehensive_analysis()
        
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
        
        analysis_serializable = convert_numpy_types(analysis)
        
        with open(output_path, 'w') as f:
            json.dump(analysis_serializable, f, indent=2)
        
        return analysis_serializable

# Example usage and testing
if __name__ == "__main__":
    # Test the advanced image processor
    processor = AdvancedKolamImageProcessor()
    
    print("🎨 Advanced Kolam Image Processor")
    print("=" * 50)
    print("Features:")
    print("✅ Hough Circle Transform for dot detection")
    print("✅ Morphological skeletonization")
    print("✅ NetworkX graph analysis")
    print("✅ Eulerian path detection")
    print("✅ Advanced symmetry analysis")
    print("✅ Cultural classification")
    print("✅ Quality scoring")
    print("=" * 50)


















