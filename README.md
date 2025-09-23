# 🎨 Kolam Art Studio

> **AI-Powered Interactive Kolam Design and Analysis System for Cultural Heritage Preservation**

[![AICTE Problem Statement 25107](https://img.shields.io/badge/AICTE-Problem%20Statement%2025107-blue)](https://www.aicte-india.org/)
[![React](https://img.shields.io/badge/React-18.2.0-61DAFB?logo=react)](https://reactjs.org/)
[![Flask](https://img.shields.io/badge/Flask-2.3.3-000000?logo=flask)](https://flask.palletsprojects.com/)
[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?logo=python)](https://python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

## 🌟 Overview

Kolam Art Studio is a comprehensive web-based platform that combines traditional Indian Kolam art with modern AI technology. The system generates authentic Kolam patterns using mathematical algorithms, analyzes existing patterns for cultural authenticity, and preserves regional Kolam styles through advanced computer vision and graph theory.

### 🎯 Key Features

- 🎨 **Interactive Design Studio** - Real-time pattern creation with AI assistance
- 🔍 **Advanced Pattern Analysis** - Computer vision and graph theory algorithms  
- 🏛️ **Cultural Authenticity** - Research-based validation of traditional patterns
- 📱 **Multi-platform Support** - Web, mobile-responsive interface
- 🌍 **Regional Classification** - 5 traditional Indian regional styles
- 🧮 **Mathematical Foundation** - Eulerian path algorithms and topology

## 🚀 Quick Start

### Prerequisites
- Node.js 16+ and npm
- Python 3.8+
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Shivambhatia-debug/KOLAM-ART-STUDIO.git
   cd KOLAM-ART-STUDIO
   ```

2. **Frontend Setup**
   ```bash
   # Install dependencies
   npm install
   
   # Start development server
   npm start
   ```

3. **Backend Setup**
   ```bash
   # Create virtual environment
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   
   # Install dependencies
   pip install -r backend/requirements.txt
   
   # Run Flask server
   cd backend
   python app.py
   ```

4. **Access the Application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:5000

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────┐
│              Frontend Layer                     │
│    React 18.2.0 + Styled Components           │
│         Interactive Canvas (Fabric.js)         │
└─────────────────┬───────────────────────────────┘
                  │ HTTP/REST API
┌─────────────────┴───────────────────────────────┐
│              Backend Layer                      │
│     Flask 2.3.3 + Python Libraries            │
│    Mathematical Algorithms & AI Models         │
└─────────────────┬───────────────────────────────┘
                  │
┌─────────────────┴───────────────────────────────┐
│            Processing Layer                     │
│   NumPy | SciPy | OpenCV | NetworkX           │
│       Computer Vision & Graph Theory           │
└─────────────────────────────────────────────────┘
```

## 🧮 Mathematical Algorithms

### Eulerian Path Validation
Validates authentic Kolam drawing (single continuous line) using Hierholzer's algorithm:

```python
def validate_eulerian_properties(dot_matrix, paths):
    """
    Validates if pattern can be drawn in single continuous line
    Uses Hierholzer's algorithm for Eulerian path detection
    """
    graph = create_graph(dot_matrix, paths)
    odd_degree_nodes = [node for node in graph.nodes() 
                       if graph.degree(node) % 2 == 1]
    return len(odd_degree_nodes) in [0, 2]
```

### Symmetry Detection
Multi-type symmetry analysis using geometric transformations:
- **Radial Symmetry** - Equidistant from center
- **Bilateral Symmetry** - Mirror across axis  
- **Rotational Symmetry** - Rotational invariance
- **Point Symmetry** - Central point reflection

### Fractal Dimension Calculation
Box-counting method for complexity analysis using linear regression on log-log plots.

## 🎨 Cultural Features

### Traditional Kolam Types
1. **Pulli Kolam** - Dot-based grid patterns
2. **Sikku Kolam** - Continuous line designs without lifting
3. **Neli Kolam** - Square grid-based patterns
4. **Kambi Kolam** - Line-weaving techniques
5. **Fractal Kolam** - Self-similar recursive patterns

### Regional Styles
- **Tamil Nadu**: Radial patterns with rice flour, daily threshold decoration
- **Karnataka**: Geometric Rangavalli with festival associations
- **Kerala**: Floral Pookalam for Onam celebrations
- **Andhra Pradesh**: Muggulu with protective symbolism
- **Telangana**: Gorintaku with cultural heritage themes

## 📡 API Documentation

### Core Endpoints

#### Pattern Analysis
```http
POST /api/analyze
Content-Type: application/json

{
  "image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAA..."
}
```

#### Cultural Pattern Generation
```http
POST /api/generate-cultural
Content-Type: application/json

{
  "region": "tamil_nadu|karnataka|kerala|andhra_pradesh|telangana",
  "pattern_style": "traditional|modern",
  "grid_size": 5,
  "use_colors": true
}
```

#### Advanced Analysis
```http
POST /api/advanced-analysis
Content-Type: application/json

{
  "image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAA...",
  "mode": "standard|deep"
}
```

## 🛠️ Technology Stack

### Frontend
- **React 18.2.0** - Modern UI framework
- **Fabric.js 5.3.0** - Interactive canvas
- **Styled Components 6.1.0** - CSS-in-JS styling
- **React Router DOM 6.8.0** - Client-side routing
- **Axios 1.6.0** - HTTP client

### Backend
- **Flask 2.3.3** - Web framework
- **NumPy 1.24.3** - Numerical computing
- **SciPy 1.11.1** - Scientific computing
- **Matplotlib 3.7.2** - Data visualization
- **Pillow 10.0.1** - Image processing
- **NetworkX** - Graph algorithms

## 📁 Project Structure

```
KOLAM ART/
├── backend/                          # Flask backend services
│   ├── app.py                       # Main Flask application
│   └── requirements.txt             # Python dependencies
├── src/                             # React frontend source
│   ├── App.js                       # Main React application
│   ├── components/                  # Reusable UI components
│   ├── pages/                       # Main application pages
│   └── styles/                      # Styling and themes
├── public/                          # Static frontend assets
├── kolam_analyzer.py                # Core pattern analysis engine
├── research_based_kolam_analyzer.py # Academic research implementation
├── topological_kolam_generator.py   # 5-step topological method
├── package.json                     # Frontend dependencies
└── requirements.txt                 # Root Python dependencies
```

## 🎯 Usage Guide

### 1. Basic Pattern Creation
1. Navigate to Kolam Studio
2. Select drawing tools (pencil, brush, shapes)
3. Create patterns on interactive canvas
4. Use color palette for styling
5. Export as PNG/SVG

### 2. AI-Assisted Generation
1. Choose generation type (Basic/Cultural/Festival/Topological)
2. Configure parameters (region, style, grid size)
3. Click "Generate Pattern"
4. Customize generated pattern
5. Analyze and validate

### 3. Pattern Analysis
1. Upload image or use canvas pattern
2. Select analysis type (Basic/Advanced)
3. Review analysis results:
   - Symmetry type and mathematical properties
   - Cultural classification and region
   - Authenticity score and recommendations

## 🔬 Research Foundation

This project implements research-based algorithms from:
- Nature Journal publications on Indian geometric art
- arXiv papers on mathematical pattern analysis
- Academic research on traditional Indian knowledge systems
- Imaginary.org mathematical art exhibitions

### Mathematical Principles
- **Euler Path Theory**: Single continuous line drawing validation
- **Graph Theory**: Network analysis of dot-line relationships
- **Symmetry Groups**: Mathematical classification of pattern types
- **Fractal Geometry**: Self-similarity and recursive structures
- **Topology**: Spatial relationship analysis

## 🚀 Deployment

### Production Build
```bash
# Frontend
npm run build

# Backend
pip install -r backend/requirements.txt
python backend/app.py
```

### Docker Deployment
```bash
# Build and run with Docker Compose
docker-compose up --build
```

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **AICTE** for the problem statement and competition framework
- **Traditional Kolam Artists** for preserving this cultural heritage
- **Research Community** for mathematical foundations
- **Open Source Libraries** that made this project possible

## 📞 Contact

**Project Lead**: [Shivam Bhatia](https://github.com/Shivambhatia-debug)

**Project Repository**: [KOLAM-ART-STUDIO](https://github.com/Shivambhatia-debug/KOLAM-ART-STUDIO)

---

<div align="center">

**🎨 Preserving Cultural Heritage Through Technology 🎨**

*Created for AICTE Problem Statement 25107 - AI-Powered Interactive Kolam Design and Analysis System*

[![Made with ❤️ in India](https://img.shields.io/badge/Made%20with%20❤️%20in-India-orange)](https://github.com/Shivambhatia-debug/KOLAM-ART-STUDIO)

</div>
