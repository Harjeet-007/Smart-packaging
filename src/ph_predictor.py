"""pH Prediction Engine - Color to pH correlation"""

import numpy as np
from typing import Tuple, Dict
from src.config import CALIBRATION_POINTS, FRESHNESS_THRESHOLDS, FRESHNESS_CONFIG


class PHPredictor:
    """Predicts pH from RGB values using calibration model."""
    
    def __init__(self, calibration_points: Dict[float, Tuple[int, int, int]] = None):
        """
        Initialize predictor with calibration points.
        
        Args:
            calibration_points: Dict mapping pH values to RGB tuples
        """
        self.calibration_points = calibration_points or CALIBRATION_POINTS
        self.thresholds = FRESHNESS_THRESHOLDS
        self.freshness_config = FRESHNESS_CONFIG
    
    def predict_ph(self, rgb: Tuple[int, int, int]) -> float:
        """
        Predict pH from RGB values using nearest neighbor.
        
        Args:
            rgb: Tuple of (R, G, B) values (0-255)
            
        Returns:
            Predicted pH value
        """
        target_vector = np.array(rgb, dtype=float)
        min_distance = float('inf')
        predicted_ph = None
        
        for ph, cal_rgb in self.calibration_points.items():
            cal_vector = np.array(cal_rgb, dtype=float)
            distance = np.linalg.norm(target_vector - cal_vector)
            
            if distance < min_distance:
                min_distance = distance
                predicted_ph = ph
        
        return predicted_ph
    
    def predict_ph_with_confidence(
        self, rgb: Tuple[int, int, int]
    ) -> Tuple[float, float, float]:
        """
        Predict pH with confidence score and distance.
        
        Args:
            rgb: Tuple of (R, G, B) values
            
        Returns:
            Tuple of (predicted_pH, confidence, distance)
        """
        target_vector = np.array(rgb, dtype=float)
        distances = {}
        
        # Calculate distances to all calibration points
        for ph, cal_rgb in self.calibration_points.items():
            cal_vector = np.array(cal_rgb, dtype=float)
            distance = np.linalg.norm(target_vector - cal_vector)
            distances[ph] = distance
        
        # Find nearest point
        min_distance = min(distances.values())
        predicted_ph = min(distances, key=distances.get)
        
        # Calculate confidence (inverse of normalized distance)
        # Normalize distance to 0-100 range
        max_possible_distance = np.linalg.norm(np.array([255, 255, 255]))
        normalized_distance = (min_distance / max_possible_distance) * 100
        confidence = 1 / (1 + normalized_distance / 100)
        
        return predicted_ph, confidence, min_distance
    
    def predict_ph_with_interpolation(
        self, rgb: Tuple[int, int, int]
    ) -> Tuple[float, float, float]:
        """
        Predict pH with linear interpolation between two nearest points.
        More accurate than nearest neighbor.
        
        Args:
            rgb: Tuple of (R, G, B) values
            
        Returns:
            Tuple of (predicted_pH, confidence, distance)
        """
        target_vector = np.array(rgb, dtype=float)
        distances = {}
        
        # Calculate distances to all calibration points
        for ph, cal_rgb in self.calibration_points.items():
            cal_vector = np.array(cal_rgb, dtype=float)
            distance = np.linalg.norm(target_vector - cal_vector)
            distances[ph] = distance
        
        # Get two nearest points
        sorted_distances = sorted(distances.items(), key=lambda x: x[1])
        ph1, dist1 = sorted_distances[0]
        ph2, dist2 = sorted_distances[1]
        min_distance = dist1
        
        # Linear interpolation
        if dist1 + dist2 > 0:
            # Inverse distance weighting
            weight1 = (dist2) / (dist1 + dist2)
            weight2 = (dist1) / (dist1 + dist2)
            predicted_ph = (ph1 * weight1) + (ph2 * weight2)
        else:
            predicted_ph = ph1
        
        # Calculate confidence
        max_possible_distance = np.linalg.norm(np.array([255, 255, 255]))
        normalized_distance = (min_distance / max_possible_distance) * 100
        confidence = 1 / (1 + normalized_distance / 100)
        
        return predicted_ph, confidence, min_distance
    
    def get_freshness_status(self, ph: float) -> Dict:
        """
        Determine freshness status based on pH value.
        
        Args:
            ph: Predicted pH value
            
        Returns:
            Dict with status, icon, color, and advice
        """
        if ph <= self.thresholds['fresh_max_ph']:
            status = 'FRESH'
        elif ph <= self.thresholds['caution_max_ph']:
            status = 'CAUTION'
        else:
            status = 'ALERT'
        
        return {
            'status': status,
            'label': self.freshness_config[status]['label'],
            'icon': self.freshness_config[status]['icon'],
            'color': self.freshness_config[status]['color'],
            'advice': self.freshness_config[status]['advice']
        }
    
    def analyze_rgb(
        self, rgb: Tuple[int, int, int], use_interpolation: bool = True
    ) -> Dict:
        """
        Complete analysis of RGB values.
        
        Args:
            rgb: Tuple of (R, G, B) values
            use_interpolation: Whether to use interpolation (True) or nearest neighbor (False)
            
        Returns:
            Dict with complete analysis results
        """
        if use_interpolation:
            ph, confidence, distance = self.predict_ph_with_interpolation(rgb)
        else:
            ph, confidence, distance = self.predict_ph_with_confidence(rgb)
        
        freshness = self.get_freshness_status(ph)
        
        return {
            'rgb': rgb,
            'predicted_ph': round(ph, 2),
            'confidence': round(confidence, 4),
            'distance': round(distance, 2),
            'freshness_status': freshness['status'],
            'freshness_label': freshness['label'],
            'freshness_icon': freshness['icon'],
            'freshness_color': freshness['color'],
            'advice': freshness['advice']
        }


# Singleton instance
_predictor = None

def get_predictor() -> PHPredictor:
    """Get or create singleton predictor instance."""
    global _predictor
    if _predictor is None:
        _predictor = PHPredictor()
    return _predictor


def predict_ph(rgb: Tuple[int, int, int]) -> float:
    """Quick function to predict pH."""
    predictor = get_predictor()
    return predictor.predict_ph(rgb)


def predict_ph_with_confidence(
    rgb: Tuple[int, int, int]
) -> Tuple[float, float, float]:
    """Quick function to predict pH with confidence."""
    predictor = get_predictor()
    return predictor.predict_ph_with_confidence(rgb)


def analyze_rgb(rgb: Tuple[int, int, int]) -> Dict:
    """Quick function for complete RGB analysis."""
    predictor = get_predictor()
    return predictor.analyze_rgb(rgb, use_interpolation=True)
