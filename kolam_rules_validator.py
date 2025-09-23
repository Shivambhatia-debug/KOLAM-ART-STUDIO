"""
Kolam Rules Validator
====================

Implements the mandatory rules for kolam patterns as defined in the research paper:
M1: All dots should be circumscribed
M2: All interactions between two lines must be at points (no overlapping over finite length)
M3: All line orbits should be closed (no loose ends)

AICTE Problem Statement 25107
"""

import numpy as np
import math
from typing import List, Tuple, Dict, Set
from dataclasses import dataclass
from enum import Enum

class ValidationResult(Enum):
    VALID = "valid"
    INVALID = "invalid"
    WARNING = "warning"

@dataclass
class ValidationIssue:
    rule: str
    severity: ValidationResult
    message: str
    details: Dict = None

class KolamRulesValidator:
    """
    Validates kolam patterns against the three mandatory rules
    """
    
    def __init__(self, tolerance: float = 5.0):
        """
        Initialize validator with tolerance for floating point comparisons
        
        Args:
            tolerance: Distance tolerance for point/line intersection checks
        """
        self.tolerance = tolerance
    
    def validate_pattern(self, points: List[Tuple[float, float]], 
                        paths: List[List[Tuple[float, float]]]) -> Dict:
        """
        Validate a kolam pattern against all mandatory rules
        
        Args:
            points: List of (x, y) coordinates for dots
            paths: List of paths, where each path is a list of (x, y) coordinates
            
        Returns:
            Dictionary with validation results
        """
        issues = []
        
        # Rule M1: All dots should be circumscribed
        m1_result = self._validate_all_dots_encircled(points, paths)
        issues.extend(m1_result)
        
        # Rule M2: No overlapping lines over finite length
        m2_result = self._validate_no_line_overlap(paths)
        issues.extend(m2_result)
        
        # Rule M3: All line orbits should be closed
        m3_result = self._validate_closed_orbits(paths)
        issues.extend(m3_result)
        
        # Calculate overall validation score
        valid_issues = [i for i in issues if i.severity == ValidationResult.VALID]
        invalid_issues = [i for i in issues if i.severity == ValidationResult.INVALID]
        warning_issues = [i for i in issues if i.severity == ValidationResult.WARNING]
        
        # Calculate score (0-100)
        total_issues = len(issues)
        if total_issues == 0:
            score = 100
        else:
            invalid_weight = len(invalid_issues) * 3
            warning_weight = len(warning_issues) * 1
            score = max(0, 100 - (invalid_weight + warning_weight) * 10)
        
        return {
            "valid": len(invalid_issues) == 0,
            "score": score,
            "issues": issues,
            "summary": {
                "total_issues": total_issues,
                "valid": len(valid_issues),
                "warnings": len(warning_issues),
                "errors": len(invalid_issues)
            },
            "rules_status": {
                "M1_all_dots_encircled": self._get_rule_status(issues, "M1"),
                "M2_no_line_overlap": self._get_rule_status(issues, "M2"),
                "M3_closed_orbits": self._get_rule_status(issues, "M3")
            }
        }
    
    def _validate_all_dots_encircled(self, points: List[Tuple[float, float]], 
                                   paths: List[List[Tuple[float, float]]]) -> List[ValidationIssue]:
        """Validate Rule M1: All dots should be circumscribed"""
        issues = []
        encircled_dots = set()
        
        for i, point in enumerate(points):
            is_encircled = False
            
            for path in paths:
                if self._is_point_encircled_by_path(point, path):
                    is_encircled = True
                    encircled_dots.add(i)
                    break
            
            if not is_encircled:
                issues.append(ValidationIssue(
                    rule="M1",
                    severity=ValidationResult.INVALID,
                    message=f"Dot {i} at ({point[0]:.1f}, {point[1]:.1f}) is not encircled",
                    details={"dot_index": i, "dot_position": point}
                ))
        
        if len(encircled_dots) == len(points):
            issues.append(ValidationIssue(
                rule="M1",
                severity=ValidationResult.VALID,
                message=f"All {len(points)} dots are properly encircled",
                details={"encircled_count": len(encircled_dots), "total_dots": len(points)}
            ))
        
        return issues
    
    def _is_point_encircled_by_path(self, point: Tuple[float, float], 
                                   path: List[Tuple[float, float]]) -> bool:
        """Check if a point is encircled by a path using ray casting algorithm"""
        if len(path) < 3:
            return False
        
        x, y = point
        n = len(path)
        inside = False
        
        p1x, p1y = path[0]
        for i in range(1, n + 1):
            p2x, p2y = path[i % n]
            if y > min(p1y, p2y):
                if y <= max(p1y, p2y):
                    if x <= max(p1x, p2x):
                        if p1y != p2y:
                            xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                        if p1x == p2x or x <= xinters:
                            inside = not inside
            p1x, p1y = p2x, p2y
        
        return inside
    
    def _validate_no_line_overlap(self, paths: List[List[Tuple[float, float]]]) -> List[ValidationIssue]:
        """Validate Rule M2: No overlapping lines over finite length"""
        issues = []
        overlap_count = 0
        
        for i in range(len(paths)):
            for j in range(i + 1, len(paths)):
                overlaps = self._find_line_overlaps(paths[i], paths[j])
                if overlaps:
                    overlap_count += len(overlaps)
                    for overlap in overlaps:
                        issues.append(ValidationIssue(
                            rule="M2",
                            severity=ValidationResult.INVALID,
                            message=f"Lines overlap between path {i} and path {j}",
                            details={
                                "path1": i,
                                "path2": j,
                                "overlap_segments": overlap
                            }
                        ))
        
        if overlap_count == 0:
            issues.append(ValidationIssue(
                rule="M2",
                severity=ValidationResult.VALID,
                message="No line overlaps detected",
                details={"overlap_count": 0}
            ))
        
        return issues
    
    def _find_line_overlaps(self, path1: List[Tuple[float, float]], 
                           path2: List[Tuple[float, float]]) -> List[Dict]:
        """Find overlapping segments between two paths"""
        overlaps = []
        
        for i in range(len(path1) - 1):
            for j in range(len(path2) - 1):
                seg1_start = path1[i]
                seg1_end = path1[i + 1]
                seg2_start = path2[j]
                seg2_end = path2[j + 1]
                
                overlap = self._line_segments_overlap(
                    seg1_start, seg1_end, seg2_start, seg2_end
                )
                
                if overlap:
                    overlaps.append({
                        "segment1": (i, i + 1),
                        "segment2": (j, j + 1),
                        "overlap_length": overlap["length"],
                        "overlap_points": overlap["points"]
                    })
        
        return overlaps
    
    def _line_segments_overlap(self, p1: Tuple[float, float], p2: Tuple[float, float],
                              p3: Tuple[float, float], p4: Tuple[float, float]) -> Dict:
        """Check if two line segments overlap over a finite length"""
        # Calculate intersection point
        intersection = self._line_intersection(p1, p2, p3, p4)
        
        if intersection is None:
            return None
        
        # Check if intersection is within both segments
        if (self._point_on_segment(intersection, p1, p2) and 
            self._point_on_segment(intersection, p3, p4)):
            
            # Calculate overlap length
            overlap_length = self._calculate_overlap_length(
                intersection, p1, p2, p3, p4
            )
            
            if overlap_length > self.tolerance:
                return {
                    "length": overlap_length,
                    "points": [intersection]
                }
        
        return None
    
    def _line_intersection(self, p1: Tuple[float, float], p2: Tuple[float, float],
                          p3: Tuple[float, float], p4: Tuple[float, float]) -> Tuple[float, float]:
        """Find intersection point of two lines"""
        x1, y1 = p1
        x2, y2 = p2
        x3, y3 = p3
        x4, y4 = p4
        
        denom = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
        
        if abs(denom) < 1e-10:  # Lines are parallel
            return None
        
        t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / denom
        
        x = x1 + t * (x2 - x1)
        y = y1 + t * (y2 - y1)
        
        return (x, y)
    
    def _point_on_segment(self, point: Tuple[float, float], 
                         seg_start: Tuple[float, float], 
                         seg_end: Tuple[float, float]) -> bool:
        """Check if a point lies on a line segment"""
        px, py = point
        x1, y1 = seg_start
        x2, y2 = seg_end
        
        # Check if point is within the bounding box of the segment
        if not (min(x1, x2) <= px <= max(x1, x2) and 
                min(y1, y2) <= py <= max(y1, y2)):
            return False
        
        # Check if point is on the line (within tolerance)
        distance = abs((y2 - y1) * px - (x2 - x1) * py + x2 * y1 - y2 * x1) / math.sqrt((y2 - y1)**2 + (x2 - x1)**2)
        
        return distance < self.tolerance
    
    def _calculate_overlap_length(self, intersection: Tuple[float, float],
                                p1: Tuple[float, float], p2: Tuple[float, float],
                                p3: Tuple[float, float], p4: Tuple[float, float]) -> float:
        """Calculate the length of overlap between two line segments"""
        # This is a simplified calculation
        # In practice, you'd need to find the actual overlapping segment
        return self.tolerance * 2  # Placeholder
    
    def _validate_closed_orbits(self, paths: List[List[Tuple[float, float]]]) -> List[ValidationIssue]:
        """Validate Rule M3: All line orbits should be closed"""
        issues = []
        closed_paths = 0
        
        for i, path in enumerate(paths):
            if len(path) < 2:
                issues.append(ValidationIssue(
                    rule="M3",
                    severity=ValidationResult.INVALID,
                    message=f"Path {i} has less than 2 points",
                    details={"path_index": i, "point_count": len(path)}
                ))
                continue
            
            # Check if path is closed (first and last points are the same)
            first_point = path[0]
            last_point = path[-1]
            
            distance = math.sqrt((first_point[0] - last_point[0])**2 + 
                               (first_point[1] - last_point[1])**2)
            
            if distance <= self.tolerance:
                closed_paths += 1
            else:
                issues.append(ValidationIssue(
                    rule="M3",
                    severity=ValidationResult.INVALID,
                    message=f"Path {i} is not closed (gap: {distance:.2f})",
                    details={
                        "path_index": i,
                        "gap_distance": distance,
                        "first_point": first_point,
                        "last_point": last_point
                    }
                ))
        
        if closed_paths == len(paths) and len(paths) > 0:
            issues.append(ValidationIssue(
                rule="M3",
                severity=ValidationResult.VALID,
                message=f"All {len(paths)} paths are properly closed",
                details={"closed_paths": closed_paths, "total_paths": len(paths)}
            ))
        
        return issues
    
    def _get_rule_status(self, issues: List[ValidationIssue], rule: str) -> str:
        """Get the status of a specific rule"""
        rule_issues = [i for i in issues if i.rule == rule]
        
        if not rule_issues:
            return "not_checked"
        
        invalid_issues = [i for i in rule_issues if i.severity == ValidationResult.INVALID]
        
        if invalid_issues:
            return "invalid"
        else:
            return "valid"
    
    def get_recommendations(self, validation_result: Dict) -> List[str]:
        """Get recommendations to fix validation issues"""
        recommendations = []
        
        for issue in validation_result["issues"]:
            # Handle both ValidationIssue objects and dictionaries
            if hasattr(issue, 'severity'):
                severity = issue.severity
                rule = issue.rule
            else:
                severity = issue.get('severity')
                rule = issue.get('rule')
            
            if severity == ValidationResult.INVALID or severity == 'invalid':
                if rule == "M1":
                    recommendations.append("Add circular paths around unencircled dots")
                elif rule == "M2":
                    recommendations.append("Modify overlapping line segments to intersect only at points")
                elif rule == "M3":
                    recommendations.append("Close open paths by connecting the last point to the first")
        
        return recommendations

# Example usage and testing
if __name__ == "__main__":
    validator = KolamRulesValidator()
    
    # Test with a valid pattern
    points = [(100, 100), (200, 100), (150, 173)]
    paths = [
        [(100, 100), (200, 100), (150, 173), (100, 100)],  # Closed triangle
        [(100, 100), (150, 50), (200, 100), (150, 173), (100, 100)]  # Closed star
    ]
    
    result = validator.validate_pattern(points, paths)
    print("Validation Result:")
    print(f"Valid: {result['valid']}")
    print(f"Score: {result['score']}")
    print(f"Issues: {len(result['issues'])}")
    print(f"Rules Status: {result['rules_status']}")
    
    if result['issues']:
        print("\nIssues:")
        for issue in result['issues']:
            print(f"- {issue.rule}: {issue.message}")
    
    recommendations = validator.get_recommendations(result)
    if recommendations:
        print("\nRecommendations:")
        for rec in recommendations:
            print(f"- {rec}")
