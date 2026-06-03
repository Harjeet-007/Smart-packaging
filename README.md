# 📦 Smart Packaging System

## Intelligent Biopolymer Monitoring & Real-Time Freshness Analytics

### Overview

**Smart Packaging** is an intelligent packaging management system that uses **color-to-pH correlation** to detect product freshness and spoilage risk in real-time. The system monitors biopolymer indicator films and provides actionable insights through a professional dashboard.

### 🎯 Key Features

- **📊 Real-Time pH Prediction**: Converts RGB color values to pH levels using a calibrated 3-point model
- **🎨 Dual Color Input**: Manual RGB sliders or automatic extraction from uploaded film photos
- **📅 Shelf-Life Tracking**: Monitors packaging date, elapsed time, and expiration status
- **🚨 Freshness Classification**: Automated status determination (FRESH, CAUTION, ALERT)
- **💾 Data Persistence**: SQLite database for scan history and analytics
- **📈 Batch Processing**: Analyze multiple packages in one session
- **📊 Export Reports**: Generate CSV and PDF reports
- **🔐 Confidence Scoring**: Quantifies prediction reliability
- **🎭 Professional UI**: Dark-themed dashboard with real-time updates
- **📱 Mobile-Ready**: Responsive Streamlit interface

### 🏗️ Architecture

```
┌─────────────────────────────────────────────┐
│          Streamlit Dashboard (UI)           │
├─────────────────────────────────────────────┤
│  Color Input → Image Processor → pH Engine  │
├─────────────────────────────────────────────┤
│   Status Logic → Database → Export Module   │
├─────────────────────────────────────────────┤
│         SQLite Database (Persistence)       │
└─────────────────────────────────────────────┘
```

### 📋 System Components

#### 1. **Core Algorithm**
- **Calibration Model**: 3-point RGB-to-pH mapping
- **Distance Metric**: Euclidean norm
- **Prediction Method**: Nearest neighbor with interpolation
- **Confidence**: Inverse distance weighting

#### 2. **Freshness States**

| pH Range | Status | Icon | Action |
|----------|--------|------|--------|
| ≤ 6.0 | FRESH — OPTIMAL | 🟢 | Keep consuming |
| 6.0–6.8 | CAUTION — EARLY SHIFT | 🟡 | Prompt consumption |
| > 6.8 | ALERT — SPOILAGE RISK | 🔴 | Discard safely |

#### 3. **Calibration Points**
```python
PH 5.5 → RGB (165, 175, 75)   # Fresh/Optimal
PH 6.5 → RGB (170, 160, 110)  # Early shift
PH 7.5 → RGB (175, 180, 155)  # Spoilage risk
```

### 🚀 Quick Start

#### Prerequisites
- Python 3.8+
- pip or conda

#### Installation

```bash
# Clone repository
git clone https://github.com/Harjeet-007/Smart-packaging.git
cd Smart-packaging

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

#### Running Locally

```bash
# Run the Streamlit app
streamlit run app.py

# Access at http://localhost:8501
```

#### Running Tests

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=src --cov-report=html
```

### 📁 Project Structure

```
Smart-packaging/
├── app.py                      # Main Streamlit application
├── requirements.txt            # Python dependencies
├── README.md                   # Project documentation
├── .gitignore                  # Git ignore rules
├── src/
│   ├── __init__.py
│   ├── image_processor.py     # Image RGB extraction
│   ├── ph_predictor.py        # pH prediction engine
│   ├── database.py            # SQLite operations
│   ├── utils.py               # Helper functions
│   ├── config.py              # Configuration constants
│   └── ui_components.py       # Reusable UI elements
├── tests/
│   ├── __init__.py
│   ├── test_ph_predictor.py
│   ├── test_image_processor.py
│   ├── test_database.py
│   ├── test_utils.py
│   └── conftest.py            # Pytest fixtures
├── data/
│   └── calibration_points.json # Calibration model data
├── .github/
│   └── workflows/
│       └── tests.yml          # CI/CD pipeline
└── docs/
    ├── architecture.md        # System design
    ├── api.md                 # API documentation
    └── deployment.md          # Deployment guide
```

### 🔧 Configuration

Edit `src/config.py` to customize:

```python
# Calibration Points (pH → RGB)
CALIBRATION_POINTS = {
    5.5: (165, 175, 75),
    6.5: (170, 160, 110),
    7.5: (175, 180, 155)
}

# Freshness Thresholds
FRESHNESS_THRESHOLDS = {
    'fresh_max_ph': 6.0,
    'caution_max_ph': 6.8,
    'alert_max_ph': 8.0
}

# Shelf Life
SHELF_LIFE_RANGE = (1, 14)  # Days

# Database
DATABASE_PATH = 'packaging_scans.db'
```

### 📊 Usage Examples

#### Example 1: Basic Freshness Check

```python
from src.ph_predictor import predict_ph_with_confidence

# Check a sample
rgb = (170, 160, 110)
ph, confidence = predict_ph_with_confidence(rgb)
print(f"pH: {ph}, Confidence: {confidence:.2%}")
# Output: pH: 6.5, Confidence: 95.24%
```

#### Example 2: Image-Based Detection

```python
from src.image_processor import extract_rgb_from_image
from src.ph_predictor import predict_ph_with_confidence

rgb = extract_rgb_from_image('film_photo.jpg')
ph, confidence = predict_ph_with_confidence(rgb)
print(f"Detected pH: {ph}")
```

#### Example 3: Database Logging

```python
from src.database import Database
from datetime import datetime

db = Database()
scan = {
    'timestamp': datetime.now(),
    'packaging_date': datetime.now(),
    'rgb_values': (170, 160, 110),
    'predicted_ph': 6.5,
    'freshness_status': 'CAUTION',
    'confidence': 0.9524
}
db.log_scan(scan)
```

### 🧪 Testing

The project includes comprehensive test coverage:

```bash
# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_ph_predictor.py -v

# Run with coverage report
pytest tests/ --cov=src --cov-report=html

# View coverage
open htmlcov/index.html
```

### 📦 Deployment

#### Option 1: Streamlit Cloud (Recommended)

1. Push code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repository
4. Deploy with one click

#### Option 2: Docker

```bash
# Build image
docker build -t smart-packaging .

# Run container
docker run -p 8501:8501 smart-packaging
```

#### Option 3: AWS/GCP/Azure

See `docs/deployment.md` for detailed instructions.

### 📊 Data Export

The system supports multiple export formats:

```python
from src.database import Database

db = Database()

# Export to CSV
db.export_to_csv('scans_2026-06.csv')

# Export to PDF
db.export_to_pdf('scans_report.pdf')

# Export to JSON
db.export_to_json('scans_data.json')
```

### 🔐 Security

- ✅ Input validation on all user inputs
- ✅ SQL injection prevention (parameterized queries)
- ✅ Environment variable support for sensitive config
- ✅ No hardcoded credentials
- ✅ HTTPS-ready for deployment

### 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### 📝 License

This project is licensed under the MIT License - see LICENSE file for details.

### 👨‍💻 Author

**Harjeet Singh** (@Harjeet-007)

### 📞 Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Contact: [your-email]
- Documentation: See `docs/` folder

### 🗺️ Roadmap

- [ ] ML-based pH prediction model
- [ ] Multi-point calibration system
- [ ] Mobile app (React Native)
- [ ] REST API with FastAPI
- [ ] Cloud database integration (PostgreSQL)
- [ ] Real-time monitoring dashboard
- [ ] Integration with IoT sensors
- [ ] Batch QR code generation
- [ ] Analytics & reporting engine
- [ ] Multi-language support

### 📚 References

- [Streamlit Documentation](https://docs.streamlit.io)
- [NumPy Documentation](https://numpy.org/doc)
- [OpenCV Documentation](https://docs.opencv.org)
- [SQLite Documentation](https://www.sqlite.org/docs.html)

---

**Made with ❤️ for sustainable packaging solutions**
