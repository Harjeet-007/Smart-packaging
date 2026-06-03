"""Utility functions for Smart Packaging System"""

import numpy as np
from typing import Tuple, List
from datetime import datetime, timedelta


def validate_rgb(rgb: Tuple[int, int, int]) -> Tuple[bool, str]:
    """
    Validate RGB tuple format and values.
    
    Args:
        rgb: RGB tuple (R, G, B)
        
    Returns:
        Tuple of (is_valid, message)
    """
    if not isinstance(rgb, (tuple, list)):
        return False, "RGB must be a tuple or list"
    
    if len(rgb) != 3:
        return False, "RGB must have exactly 3 values"
    
    try:
        r, g, b = [int(x) for x in rgb]
        if not all(0 <= x <= 255 for x in [r, g, b]):
            return False, "RGB values must be between 0 and 255"
        return True, "Valid RGB"
    except (ValueError, TypeError):
        return False, "RGB values must be integers"


def rgb_to_hex(rgb: Tuple[int, int, int]) -> str:
    """
    Convert RGB tuple to hex color string.
    
    Args:
        rgb: RGB tuple
        
    Returns:
        Hex color string (e.g., '#FF00FF')
    """
    valid, _ = validate_rgb(rgb)
    if not valid:
        return "#000000"
    return '#{:02x}{:02x}{:02x}'.format(int(rgb[0]), int(rgb[1]), int(rgb[2]))


def hex_to_rgb(hex_color: str) -> Tuple[int, int, int]:
    """
    Convert hex color string to RGB tuple.
    
    Args:
        hex_color: Hex color string (e.g., '#FF00FF')
        
    Returns:
        RGB tuple
    """
    try:
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    except (ValueError, IndexError):
        return (0, 0, 0)


def calculate_color_distance(rgb1: Tuple[int, int, int], rgb2: Tuple[int, int, int]) -> float:
    """
    Calculate Euclidean distance between two RGB colors.
    
    Args:
        rgb1: First RGB tuple
        rgb2: Second RGB tuple
        
    Returns:
        Euclidean distance
    """
    v1 = np.array(rgb1, dtype=float)
    v2 = np.array(rgb2, dtype=float)
    return float(np.linalg.norm(v1 - v2))


def rgb_to_grayscale(rgb: Tuple[int, int, int]) -> int:
    """
    Convert RGB to grayscale using standard formula.
    
    Args:
        rgb: RGB tuple
        
    Returns:
        Grayscale value (0-255)
    """
    r, g, b = rgb
    return int(0.299 * r + 0.587 * g + 0.114 * b)


def is_similar_color(
    rgb1: Tuple[int, int, int],
    rgb2: Tuple[int, int, int],
    threshold: float = 50.0
) -> bool:
    """
    Check if two colors are similar within threshold.
    
    Args:
        rgb1: First RGB tuple
        rgb2: Second RGB tuple
        threshold: Distance threshold (0-441)
        
    Returns:
        True if colors are similar
    """
    distance = calculate_color_distance(rgb1, rgb2)
    return distance <= threshold


def format_time_delta(delta: timedelta) -> str:
    """
    Format timedelta as readable string.
    
    Args:
        delta: timedelta object
        
    Returns:
        Formatted string (e.g., "5d 3h 22m")
    """
    total_seconds = int(delta.total_seconds())
    
    days = total_seconds // 86400
    hours = (total_seconds % 86400) // 3600
    minutes = (total_seconds % 3600) // 60
    
    parts = []
    if days > 0:
        parts.append(f"{days}d")
    if hours > 0:
        parts.append(f"{hours}h")
    if minutes > 0:
        parts.append(f"{minutes}m")
    
    return " ".join(parts) if parts else "0m"


def calculate_shelf_life_percentage(elapsed: timedelta, total: timedelta) -> int:
    """
    Calculate percentage of shelf life used.
    
    Args:
        elapsed: Time elapsed since packaging
        total: Total shelf life
        
    Returns:
        Percentage used (0-100)
    """
    if total.total_seconds() == 0:
        return 0
    
    percentage = (elapsed.total_seconds() / total.total_seconds()) * 100
    return max(0, min(100, int(percentage)))


def is_expired(expiration_time: datetime) -> bool:
    """
    Check if item is expired.
    
    Args:
        expiration_time: Expiration datetime
        
    Returns:
        True if expired
    """
    return datetime.now() > expiration_time


def get_time_remaining(expiration_time: datetime) -> Tuple[int, int, int]:
    """
    Get time remaining until expiration.
    
    Args:
        expiration_time: Expiration datetime
        
    Returns:
        Tuple of (days, hours, minutes)
    """
    delta = expiration_time - datetime.now()
    
    if delta.total_seconds() <= 0:
        return 0, 0, 0
    
    total_seconds = int(delta.total_seconds())
    days = total_seconds // 86400
    hours = (total_seconds % 86400) // 3600
    minutes = (total_seconds % 3600) // 60
    
    return days, hours, minutes


def get_random_rgb() -> Tuple[int, int, int]:
    """
    Generate random RGB tuple.
    
    Returns:
        Random RGB tuple
    """
    return tuple(np.random.randint(0, 256, 3))


def clamp_rgb(rgb: Tuple[int, int, int]) -> Tuple[int, int, int]:
    """
    Clamp RGB values to valid range (0-255).
    
    Args:
        rgb: RGB tuple (may contain invalid values)
        
    Returns:
        Clamped RGB tuple
    """
    return tuple(max(0, min(255, int(x))) for x in rgb)


def merge_colors(
    colors: List[Tuple[int, int, int]],
    weights: List[float] = None
) -> Tuple[int, int, int]:
    """
    Merge multiple colors with optional weights.
    
    Args:
        colors: List of RGB tuples
        weights: List of weights (must sum to 1)
        
    Returns:
        Merged RGB tuple
    """
    if not colors:
        return (0, 0, 0)
    
    if weights is None:
        weights = [1.0 / len(colors)] * len(colors)
    
    if len(colors) != len(weights):
        raise ValueError("Number of colors must match number of weights")
    
    if abs(sum(weights) - 1.0) > 0.001:
        # Normalize weights
        total = sum(weights)
        weights = [w / total for w in weights]
    
    merged = np.zeros(3, dtype=float)
    for color, weight in zip(colors, weights):
        merged += np.array(color, dtype=float) * weight
    
    return tuple(merged.astype(int))
