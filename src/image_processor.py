"""Image Processing Module - Extract RGB from film images"""

import numpy as np
from typing import Tuple, Optional
from PIL import Image
import io
from src.config import ALLOWED_IMAGE_FORMATS, IMAGE_CROP_RATIO, MAX_IMAGE_SIZE_MB


class ImageProcessor:
    """Processes images to extract RGB values from indicator film patches."""
    
    def __init__(self, crop_ratio: float = IMAGE_CROP_RATIO):
        """
        Initialize image processor.
        
        Args:
            crop_ratio: Ratio of image to crop from center (0.0-1.0)
        """
        self.crop_ratio = crop_ratio
        self.allowed_formats = ALLOWED_IMAGE_FORMATS
    
    @staticmethod
    def validate_image(file_obj) -> Tuple[bool, str]:
        """
        Validate image file format and size.
        
        Args:
            file_obj: File object from upload
            
        Returns:
            Tuple of (is_valid, message)
        """
        # Check file size
        file_obj.seek(0, 2)  # Seek to end
        file_size_mb = file_obj.tell() / (1024 * 1024)
        file_obj.seek(0)  # Reset position
        
        if file_size_mb > MAX_IMAGE_SIZE_MB:
            return False, f"File too large. Max size: {MAX_IMAGE_SIZE_MB}MB"
        
        # Check format
        try:
            img = Image.open(file_obj)
            file_obj.seek(0)  # Reset for reading
            
            if img.format.lower() not in ALLOWED_IMAGE_FORMATS:
                return False, f"Invalid format. Allowed: {', '.join(ALLOWED_IMAGE_FORMATS)}"
            
            return True, "Valid image"
        except Exception as e:
            return False, f"Error reading image: {str(e)}"
    
    def extract_rgb_from_image(
        self, image_file
    ) -> Tuple[bool, Optional[Tuple[int, int, int]], str]:
        """
        Extract dominant RGB from image center region.
        
        Args:
            image_file: PIL Image or file object
            
        Returns:
            Tuple of (success, rgb_tuple, message)
        """
        try:
            # Handle different input types
            if isinstance(image_file, bytes):
                img = Image.open(io.BytesIO(image_file))
            elif hasattr(image_file, 'read'):
                img = Image.open(image_file)
            elif isinstance(image_file, Image.Image):
                img = image_file
            else:
                return False, None, "Invalid image input type"
            
            # Convert to RGB if necessary
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            # Convert to numpy array
            img_array = np.array(img)
            
            # Extract center region
            height, width = img_array.shape[:2]
            crop_h = int(height * self.crop_ratio)
            crop_w = int(width * self.crop_ratio)
            
            start_h = (height - crop_h) // 2
            start_w = (width - crop_w) // 2
            
            center_region = img_array[
                start_h:start_h + crop_h,
                start_w:start_w + crop_w
            ]
            
            # Calculate mean RGB
            avg_rgb = tuple(np.mean(center_region, axis=(0, 1))[:3].astype(int))
            
            return True, avg_rgb, "RGB extracted successfully"
        
        except Exception as e:
            return False, None, f"Error extracting RGB: {str(e)}"
    
    def extract_rgb_histogram(
        self, image_file
    ) -> Tuple[bool, Optional[Tuple[int, int, int]], str]:
        """
        Extract RGB using histogram-based approach (more robust).
        Finds the most common color in center region.
        
        Args:
            image_file: PIL Image or file object
            
        Returns:
            Tuple of (success, rgb_tuple, message)
        """
        try:
            # Load image
            if isinstance(image_file, bytes):
                img = Image.open(io.BytesIO(image_file))
            elif hasattr(image_file, 'read'):
                img = Image.open(image_file)
            else:
                img = image_file
            
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            img_array = np.array(img)
            
            # Extract center region
            height, width = img_array.shape[:2]
            crop_h = int(height * self.crop_ratio)
            crop_w = int(width * self.crop_ratio)
            
            start_h = (height - crop_h) // 2
            start_w = (width - crop_w) // 2
            
            center_region = img_array[
                start_h:start_h + crop_h,
                start_w:start_w + crop_w
            ]
            
            # Reshape to 2D array of pixels
            pixels = center_region.reshape(-1, 3)
            
            # Find most common color using median (robust to outliers)
            rgb = tuple(np.median(pixels, axis=0).astype(int))
            
            return True, rgb, "RGB extracted using histogram method"
        
        except Exception as e:
            return False, None, f"Error in histogram extraction: {str(e)}"
    
    def extract_rgb_hsv_filter(
        self, image_file, saturation_threshold: float = 0.3
    ) -> Tuple[bool, Optional[Tuple[int, int, int]], str]:
        """
        Extract RGB by filtering based on color saturation.
        Useful for removing background and noise.
        
        Args:
            image_file: PIL Image or file object
            saturation_threshold: HSV saturation threshold (0-1)
            
        Returns:
            Tuple of (success, rgb_tuple, message)
        """
        try:
            import cv2
            
            # Load image
            if isinstance(image_file, bytes):
                img_pil = Image.open(io.BytesIO(image_file))
            elif hasattr(image_file, 'read'):
                img_pil = Image.open(image_file)
            else:
                img_pil = image_file
            
            img_array = np.array(img_pil.convert('RGB'))
            img_bgr = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
            img_hsv = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2HSV)
            
            # Extract center region
            height, width = img_array.shape[:2]
            crop_h = int(height * self.crop_ratio)
            crop_w = int(width * self.crop_ratio)
            
            start_h = (height - crop_h) // 2
            start_w = (width - crop_w) // 2
            
            center_region_hsv = img_hsv[
                start_h:start_h + crop_h,
                start_w:start_w + crop_w
            ]
            
            # Filter by saturation
            saturation = center_region_hsv[:, :, 1] / 255.0
            mask = saturation >= saturation_threshold
            
            if not np.any(mask):
                # If no saturated pixels, use all pixels
                center_region_rgb = img_array[
                    start_h:start_h + crop_h,
                    start_w:start_w + crop_w
                ]
            else:
                center_region_rgb = img_array[
                    start_h:start_h + crop_h,
                    start_w:start_w + crop_w
                ][mask]
            
            # Calculate mean RGB
            rgb = tuple(np.mean(center_region_rgb, axis=0)[:3].astype(int))
            
            return True, rgb, "RGB extracted using HSV filtering"
        
        except ImportError:
            return False, None, "OpenCV not installed. Use extract_rgb_from_image instead."
        except Exception as e:
            return False, None, f"Error in HSV extraction: {str(e)}"
    
    def get_image_stats(self, image_file) -> Tuple[bool, Optional[dict], str]:
        """
        Get comprehensive statistics about image.
        
        Args:
            image_file: PIL Image or file object
            
        Returns:
            Tuple of (success, stats_dict, message)
        """
        try:
            if isinstance(image_file, bytes):
                img = Image.open(io.BytesIO(image_file))
            elif hasattr(image_file, 'read'):
                img = Image.open(image_file)
            else:
                img = image_file
            
            img_array = np.array(img.convert('RGB'))
            
            stats = {
                'width': img.width,
                'height': img.height,
                'format': img.format,
                'mode': img.mode,
                'mean_rgb': tuple(np.mean(img_array, axis=(0, 1))[:3].astype(int)),
                'median_rgb': tuple(np.median(img_array, axis=(0, 1))[:3].astype(int)),
                'std_dev': tuple(np.std(img_array, axis=(0, 1))[:3].astype(int)),
                'min_rgb': tuple(np.min(img_array, axis=(0, 1))[:3]),
                'max_rgb': tuple(np.max(img_array, axis=(0, 1))[:3])
            }
            
            return True, stats, "Image statistics calculated"
        
        except Exception as e:
            return False, None, f"Error calculating stats: {str(e)}"


# Singleton instance
_processor = None

def get_processor() -> ImageProcessor:
    """Get or create singleton processor instance."""
    global _processor
    if _processor is None:
        _processor = ImageProcessor()
    return _processor


def extract_rgb_from_image(image_file) -> Tuple[bool, Optional[Tuple[int, int, int]], str]:
    """Quick function to extract RGB from image."""
    processor = get_processor()
    return processor.extract_rgb_from_image(image_file)
