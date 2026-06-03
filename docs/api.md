# 📚 API Documentation

## pH Predictor API

### PHPredictor Class

```python
from src.ph_predictor import PHPredictor

predictor = PHPredictor()
```

#### Methods

##### `predict_ph(rgb: Tuple[int, int, int]) -> float`

Predict pH from RGB values using nearest neighbor algorithm.

**Parameters**:
- `rgb` (Tuple[int, int, int]): RGB values (0-255)

**Returns**:
- `float`: Predicted pH value

**Example**:
```python
ph = predictor.predict_ph((170, 160, 110))
print(ph)  # Output: 6.5
```

---

##### `predict_ph_with_confidence(rgb) -> Tuple[float, float, float]`

Predict pH with confidence score and Euclidean distance.

**Parameters**:
- `rgb` (Tuple[int, int, int]): RGB values

**Returns**:
- `Tuple[float, float, float]`: (predicted_pH, confidence_score, distance)

**Example**:
```python
ph, confidence, distance = predictor.predict_ph_with_confidence((170, 160, 110))
print(f"pH: {ph}, Confidence: {confidence:.2%}, Distance: {distance:.2f}")
# Output: pH: 6.5, Confidence: 95.24%, Distance: 0.00
```

---

##### `predict_ph_with_interpolation(rgb) -> Tuple[float, float, float]`

Predict pH using linear interpolation between two nearest points (more accurate).

**Parameters**:
- `rgb` (Tuple[int, int, int]): RGB values

**Returns**:
- `Tuple[float, float, float]`: (predicted_pH, confidence_score, distance)

**Example**:
```python
ph, confidence, distance = predictor.predict_ph_with_interpolation((172, 168, 132))
print(f"pH: {ph}, Confidence: {confidence:.2%}")
# Output: pH: 7.0, Confidence: 92.15%
```

---

##### `get_freshness_status(ph: float) -> Dict`

Determine freshness status based on pH value.

**Parameters**:
- `ph` (float): pH value

**Returns**:
- `Dict`: Status dictionary with keys:
  - `status` (str): 'FRESH', 'CAUTION', or 'ALERT'
  - `label` (str): Human-readable label
  - `icon` (str): Status emoji
  - `color` (str): Hex color code
  - `advice` (str): Actionable advice

**Example**:
```python
status = predictor.get_freshness_status(6.5)
print(status)
# Output:
# {
#     'status': 'CAUTION',
#     'label': 'CAUTION — EARLY SHIFT',
#     'icon': '🟡',
#     'color': '#ffab00',
#     'advice': 'Minor pH adjustment detected...'
# }
```

---

##### `analyze_rgb(rgb, use_interpolation=True) -> Dict`

Complete RGB analysis pipeline.

**Parameters**:
- `rgb` (Tuple[int, int, int]): RGB values
- `use_interpolation` (bool): Use interpolation (default: True)

**Returns**:
- `Dict`: Complete analysis with all metrics

**Example**:
```python
analysis = predictor.analyze_rgb((170, 160, 110))
print(analysis)
# Output:
# {
#     'rgb': (170, 160, 110),
#     'predicted_ph': 6.5,
#     'confidence': 1.0,
#     'distance': 0.0,
#     'freshness_status': 'CAUTION',
#     'freshness_label': 'CAUTION — EARLY SHIFT',
#     'freshness_icon': '🟡',
#     'freshness_color': '#ffab00',
#     'advice': '...'
# }
```

---

## Image Processor API

### ImageProcessor Class

```python
from src.image_processor import ImageProcessor

processor = ImageProcessor()
```

#### Methods

##### `extract_rgb_from_image(image_file) -> Tuple[bool, Optional[Tuple], str]`

Extract RGB from image using mean-based approach.

**Parameters**:
- `image_file`: PIL Image, bytes, or file object

**Returns**:
- `Tuple[bool, Optional[Tuple], str]`: (success, rgb_tuple, message)

**Example**:
```python
from PIL import Image

img = Image.open('film_photo.jpg')
success, rgb, msg = processor.extract_rgb_from_image(img)
if success:
    print(f"Extracted RGB: {rgb}")
else:
    print(f"Error: {msg}")
```

---

##### `extract_rgb_histogram(image_file) -> Tuple[bool, Optional[Tuple], str]`

Extract RGB using median (more robust to outliers).

**Parameters**:
- `image_file`: PIL Image, bytes, or file object

**Returns**:
- `Tuple[bool, Optional[Tuple], str]`: (success, rgb_tuple, message)

**Example**:
```python
success, rgb, msg = processor.extract_rgb_histogram(image_file)
```

---

##### `extract_rgb_hsv_filter(image_file, saturation_threshold=0.3) -> Tuple`

Extract RGB after HSV-based filtering.

**Parameters**:
- `image_file`: PIL Image, bytes, or file object
- `saturation_threshold` (float): Saturation threshold (0-1)

**Returns**:
- `Tuple[bool, Optional[Tuple], str]`: (success, rgb_tuple, message)

**Example**:
```python
success, rgb, msg = processor.extract_rgb_hsv_filter(image_file, saturation_threshold=0.4)
```

---

##### `get_image_stats(image_file) -> Tuple[bool, Optional[Dict], str]`

Get comprehensive image statistics.

**Parameters**:
- `image_file`: PIL Image, bytes, or file object

**Returns**:
- `Tuple[bool, Optional[Dict], str]`: (success, stats_dict, message)

**Example**:
```python
success, stats, msg = processor.get_image_stats(image_file)
if success:
    print(f"Mean RGB: {stats['mean_rgb']}")
    print(f"Image size: {stats['width']}x{stats['height']}")
```

---

## Database API

### Database Class

```python
from src.database import Database

db = Database('packaging_scans.db')
```

#### Methods

##### `log_scan(scan_data: Dict) -> Tuple[bool, str, int]`

Log a scan event to database.

**Parameters**:
- `scan_data` (Dict): Scan information

**Returns**:
- `Tuple[bool, str, int]`: (success, message, scan_id)

**Example**:
```python
from datetime import datetime

scan_data = {
    'packaging_date': datetime.now().isoformat(),
    'rgb_values': (170, 160, 110),
    'predicted_ph': 6.5,
    'freshness_status': 'CAUTION',
    'confidence': 0.95,
    'shelf_life_days': 5,
    'advice': 'Recommend prompt consumption'
}

success, msg, scan_id = db.log_scan(scan_data)
print(f"Scan logged: {scan_id}")
```

---

##### `get_all_scans(limit=100, offset=0) -> List[Dict]`

Retrieve all scans with pagination.

**Parameters**:
- `limit` (int): Number of records (default: 100)
- `offset` (int): Offset for pagination (default: 0)

**Returns**:
- `List[Dict]`: List of scan records

**Example**:
```python
scans = db.get_all_scans(limit=50, offset=0)
for scan in scans:
    print(f"ID: {scan['id']}, pH: {scan['predicted_ph']}")
```

---

##### `get_scan_by_id(scan_id: int) -> Optional[Dict]`

Retrieve a specific scan.

**Parameters**:
- `scan_id` (int): Scan ID

**Returns**:
- `Optional[Dict]`: Scan record or None

**Example**:
```python
scan = db.get_scan_by_id(42)
if scan:
    print(f"pH: {scan['predicted_ph']}, Status: {scan['freshness_status']}")
```

---

##### `get_scans_by_status(status: str, limit=100) -> List[Dict]`

Get scans by freshness status.

**Parameters**:
- `status` (str): 'FRESH', 'CAUTION', or 'ALERT'
- `limit` (int): Maximum records (default: 100)

**Returns**:
- `List[Dict]`: Matching scans

**Example**:
```python
alert_scans = db.get_scans_by_status('ALERT')
print(f"Found {len(alert_scans)} spoilage alerts")
```

---

##### `get_statistics() -> Dict`

Get database statistics.

**Returns**:
- `Dict`: Statistics including:
  - `total_scans`: Total scan count
  - `status_counts`: Count per status
  - `average_ph`: Average pH
  - `average_confidence`: Average confidence

**Example**:
```python
stats = db.get_statistics()
print(f"Total scans: {stats['total_scans']}")
print(f"Fresh: {stats['status_counts'].get('FRESH', 0)}")
```

---

##### `export_to_csv(filename=None) -> Tuple[bool, str, Optional[str]]`

Export scans to CSV.

**Parameters**:
- `filename` (str): Output filename (auto-generated if None)

**Returns**:
- `Tuple[bool, str, Optional[str]]`: (success, message, filepath)

**Example**:
```python
success, msg, filepath = db.export_to_csv('scans_export.csv')
if success:
    print(f"Exported to {filepath}")
```

---

##### `export_to_json(filename=None) -> Tuple[bool, str, Optional[str]]`

Export scans to JSON.

**Parameters**:
- `filename` (str): Output filename

**Returns**:
- `Tuple[bool, str, Optional[str]]`: (success, message, filepath)

---

##### `delete_scan(scan_id: int) -> Tuple[bool, str]`

Delete a scan record.

**Parameters**:
- `scan_id` (int): Scan ID

**Returns**:
- `Tuple[bool, str]`: (success, message)

---

## Utility Functions API

### Color Functions

```python
from src.utils import (
    validate_rgb,
    rgb_to_hex,
    hex_to_rgb,
    calculate_color_distance,
    rgb_to_grayscale,
    is_similar_color,
    clamp_rgb,
    merge_colors
)
```

#### `validate_rgb(rgb) -> Tuple[bool, str]`
Validate RGB tuple format and values.

#### `rgb_to_hex(rgb) -> str`
Convert RGB to hex color string.

#### `hex_to_rgb(hex_color) -> Tuple`
Convert hex to RGB tuple.

#### `calculate_color_distance(rgb1, rgb2) -> float`
Calculate Euclidean distance between colors.

#### `rgb_to_grayscale(rgb) -> int`
Convert to grayscale (0-255).

#### `is_similar_color(rgb1, rgb2, threshold) -> bool`
Check if colors are similar within threshold.

#### `merge_colors(colors, weights) -> Tuple`
Merge multiple colors with weights.

---

### Time Functions

```python
from src.utils import (
    format_time_delta,
    calculate_shelf_life_percentage,
    is_expired,
    get_time_remaining
)
```

#### `format_time_delta(delta) -> str`
Format timedelta as readable string (e.g., "5d 3h 22m").

#### `calculate_shelf_life_percentage(elapsed, total) -> int`
Calculate percentage of shelf life used (0-100).

#### `is_expired(expiration_time) -> bool`
Check if expiration time has passed.

#### `get_time_remaining(expiration_time) -> Tuple[int, int, int]`
Get remaining time as (days, hours, minutes).

---

## Quick Start Examples

### Example 1: Full Analysis Pipeline

```python
from src.ph_predictor import PHPredictor
from src.database import Database
from datetime import datetime

# Initialize
predictor = PHPredictor()
db = Database()

# Analyze color
rgb = (170, 160, 110)
analysis = predictor.analyze_rgb(rgb)

# Log to database
scan_data = {
    'packaging_date': datetime.now().isoformat(),
    'rgb_values': rgb,
    'predicted_ph': analysis['predicted_ph'],
    'freshness_status': analysis['freshness_status'],
    'confidence': analysis['confidence'],
    'advice': analysis['advice']
}

success, msg, scan_id = db.log_scan(scan_data)
print(f"Scan {scan_id} logged: {analysis['freshness_label']}")
```

### Example 2: Image Processing + Analysis

```python
from src.image_processor import ImageProcessor
from src.ph_predictor import PHPredictor

processor = ImageProcessor()
predictor = PHPredictor()

# Extract RGB from image
success, rgb, msg = processor.extract_rgb_from_image('film_photo.jpg')

if success:
    # Analyze
    analysis = predictor.analyze_rgb(rgb)
    print(f"Status: {analysis['freshness_status']}")
    print(f"Advice: {analysis['advice']}")
else:
    print(f"Error: {msg}")
```

### Example 3: Batch Analysis

```python
from src.database import Database

db = Database()

# Get all alert scans
alerts = db.get_scans_by_status('ALERT', limit=100)

# Export for review
success, msg, filepath = db.export_to_csv('alerts_export.csv')
print(f"Exported {len(alerts)} alerts to {filepath}")

# Get statistics
stats = db.get_statistics()
print(f"Total scans: {stats['total_scans']}")
print(f"Average pH: {stats['average_ph']}")
```

---

**Version**: 1.0.0  
**Last Updated**: 2026-06-03
