"""Configuration constants for Smart Packaging System"""

import os
from pathlib import Path

# ─────────────────────────────────────────────
# CALIBRATION MODEL
# ─────────────────────────────────────────────
CALIBRATION_POINTS = {
    5.5: (165, 175, 75),    # Fresh/Optimal
    6.5: (170, 160, 110),   # Early shift/Caution
    7.5: (175, 180, 155)    # Spoilage risk/Alert
}

# ─────────────────────────────────────────────
# FRESHNESS THRESHOLDS
# ─────────────────────────────────────────────
FRESHNESS_THRESHOLDS = {
    'fresh_max_ph': 6.0,      # pH <= 6.0 → FRESH
    'caution_max_ph': 6.8,    # 6.0 < pH <= 6.8 → CAUTION
    'alert_max_ph': 8.0       # pH > 6.8 → ALERT
}

FRESHNESS_CONFIG = {
    'FRESH': {
        'label': 'FRESH — OPTIMAL',
        'icon': '🟢',
        'color': '#00c853',
        'advice': 'Biopolymer film environment is stable. Product quality is optimal. No action required.'
    },
    'CAUTION': {
        'label': 'CAUTION — EARLY SHIFT',
        'icon': '🟡',
        'color': '#ffab00',
        'advice': 'Minor pH adjustment detected. Early oxidation kinetics observed. Recommend prompt consumption.'
    },
    'ALERT': {
        'label': 'ALERT — SPOILAGE RISK',
        'icon': '🔴',
        'color': '#ff3d00',
        'advice': 'Critical pH threshold exceeded. Unsafe compound metrics detected. Discard product safely.'
    }
}

# ─────────────────────────────────────────────
# SHELF LIFE CONFIGURATION
# ─────────────────────────────────────────────
SHELF_LIFE_RANGE = (1, 14)  # Days
DEFAULT_SHELF_LIFE = 5      # Days

# ─────────────────────────────────────────────
# DATABASE CONFIGURATION
# ─────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent.parent
DATABASE_PATH = BASE_DIR / 'packaging_scans.db'
DATABASE_PATH_STR = str(DATABASE_PATH)

# ─────────────────────────────────────────────
# IMAGE PROCESSING
# ─────────────────────────────────────────────
ALLOWED_IMAGE_FORMATS = ['jpg', 'jpeg', 'png', 'bmp', 'tiff']
MAX_IMAGE_SIZE_MB = 10
IMAGE_CROP_RATIO = 0.25  # Focus on center 50% of image

# ─────────────────────────────────────────────
# UPLOAD CONFIGURATION
# ─────────────────────────────────────────────
UPLOAD_DIR = BASE_DIR / 'uploads'
UPLOAD_DIR.mkdir(exist_ok=True)

# ─────────────────────────────────────────────
# STREAMLIT UI CONFIGURATION
# ─────────────────────────────────────────────
PAGE_TITLE = "Smart Packaging Dashboard"
PAGE_ICON = "📦"
LAYOUT = "wide"

# ─────────────────────────────────────────────
# EXPORT CONFIGURATION
# ─────────────────────────────────────────────
EXPORT_FORMATS = ['csv', 'json', 'pdf', 'excel']
EXPORT_DIR = BASE_DIR / 'exports'
EXPORT_DIR.mkdir(exist_ok=True)

# ─────────────────────────────────────────────
# LOGGING
# ─────────────────────────────────────────────
LOG_DIR = BASE_DIR / 'logs'
LOG_DIR.mkdir(exist_ok=True)
LOG_LEVEL = 'INFO'

# ─────────────────────────────────────────────
# API CONFIGURATION (for future REST API)
# ─────────────────────────────────────────────
API_VERSION = 'v1'
API_HOST = '0.0.0.0'
API_PORT = 8000
API_DEBUG = False
