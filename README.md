# Kolam Design Analyzer and Generator

A comprehensive Python program to analyze and generate traditional Indian Kolam designs by identifying their mathematical principles and design patterns.

## Overview

This project addresses the AICTE problem statement (ID: 25107) for developing computer programs to identify design principles behind Kolam designs and recreate them. Kolams are traditional Indian art forms that combine cultural heritage with mathematical concepts like symmetry, fractals, and geometric patterns.

## Key Features

### 🔍 Analysis Capabilities
- **Symmetry Detection**: Identifies radial, bilateral, and rotational symmetry
- **Fractal Analysis**: Calculates fractal dimensions and self-similarity
- **Pattern Recognition**: Analyzes geometric relationships and complexity
- **Grid Analysis**: Studies dot patterns and spatial reasoning

### 🎨 Generation Features
- **Multiple Symmetry Types**: Generate patterns with different symmetry properties
- **Fractal Kolams**: Create self-similar patterns using iterative transformations
- **Grid-based Patterns**: Generate traditional dot-grid based designs
- **Customizable Parameters**: Control grid size, complexity, and symmetry

### 📊 Visualization
- **Interactive Plots**: Visualize patterns with analysis overlays
- **Pattern Comparison**: Side-by-side comparison of different designs
- **Mathematical Metrics**: Display fractal dimensions and complexity measures

## Mathematical Principles Identified

1. **Grid-based Dot Patterns (Pulli)**: Traditional foundation using equidistant points
2. **Symmetry Types**:
   - Radial symmetry (circular patterns)
   - Bilateral symmetry (mirror patterns)
   - Rotational symmetry (n-fold rotation)
3. **Geometric Shapes**: Circles, squares, triangles, and curves
4. **Fractal Properties**: Self-similarity and recursive patterns
5. **Continuous Line Patterns**: Sikku Kolam with unbroken lines
6. **Spatial Reasoning**: Mathematical relationships between points

## Installation

### Option 1: Full System (Python + React)
1. Clone or download the project files
2. Install Python dependencies:
```bash
pip install -r requirements.txt
```
3. Install React dependencies:
```bash
npm install
```
4. Start the backend API:
```bash
python backend/app.py
```
5. Start the React frontend:
```bash
npm start
```

### Option 2: Python Only
1. Install Python dependencies:
```bash
pip install -r requirements.txt
```
2. Run the Python analysis:
```bash
python kolam_analyzer.py
```

## Usage

### Web Application (Recommended)
1. Start the backend: `python backend/app.py`
2. Start the frontend: `npm start`
3. Open `http://localhost:3000` in your browser
4. Use the interactive Kolam Studio to create and analyze patterns

### Python Command Line
```python
python kolam_analyzer.py
```

### Programmatic Usage
```python
from kolam_analyzer import KolamGenerator, KolamAnalyzer, KolamVisualizer

# Generate a pattern
generator = KolamGenerator()
pattern = generator.generate_grid_pattern((5, 5), SymmetryType.RADIAL)

# Analyze the pattern
analyzer = KolamAnalyzer()
symmetry = analyzer.analyze_symmetry(pattern.points)
fractal_props = analyzer.analyze_fractal_properties(pattern)

# Visualize
visualizer = KolamVisualizer()
visualizer.visualize_pattern(pattern, "My Kolam Pattern")
```

## Generated Patterns

The program generates four types of patterns:

1. **Radial Symmetry**: Patterns radiating from a central point
2. **Bilateral Symmetry**: Mirror-symmetric patterns
3. **Rotational Symmetry**: Patterns with n-fold rotation
4. **Fractal Patterns**: Self-similar recursive designs

## Analysis Results

The program provides detailed analysis including:
- Symmetry type classification
- Fractal dimension calculation
- Self-similarity detection
- Complexity assessment
- Point and line count statistics

## Technical Implementation

### Core Classes
- `KolamAnalyzer`: Analyzes patterns for mathematical properties
- `KolamGenerator`: Creates new patterns based on identified principles
- `KolamVisualizer`: Renders patterns and analysis results
- `KolamPattern`: Data structure representing a complete pattern

### Algorithms
- **Symmetry Detection**: Geometric analysis of point distributions
- **Fractal Dimension**: Box-counting method for fractal analysis
- **Pattern Generation**: Rule-based generation using symmetry principles
- **Self-Similarity**: Recursive pattern analysis

## Cultural Significance

Kolams represent a unique intersection of:
- **Art and Mathematics**: Beautiful patterns with deep mathematical foundations
- **Cultural Heritage**: Traditional Indian art form
- **Spatial Reasoning**: Complex geometric relationships
- **Fractal Geometry**: Natural self-similar patterns

## Future Enhancements

- Machine learning-based pattern recognition
- 3D Kolam generation
- Interactive web interface
- Mobile app development
- Integration with traditional Kolam drawing tools

## References

- AICTE Problem Statement 25107
- Indian Knowledge Systems (IKS)
- Traditional Kolam art principles
- Mathematical symmetry theory
- Fractal geometry concepts

## License

This project is developed for educational and research purposes as part of the AICTE challenge.

---

**Organization**: AICTE - Indian Knowledge Systems (IKS)  
**Category**: Software  
**Theme**: Heritage & Culture  
**Problem Statement ID**: 25107
