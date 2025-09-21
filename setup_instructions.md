# Kolam Analysis System Setup Instructions

## Problem Statement
**AICTE Problem Statement 25107**: Develop computer programs to identify design principles behind Kolam designs and recreate them.

## Quick Setup (Recommended)

### Option 1: Using Python from Microsoft Store
1. Open Microsoft Store
2. Search for "Python 3.13"
3. Install Python 3.13
4. Open Command Prompt or PowerShell
5. Run: `python -m pip install numpy matplotlib scipy`
6. Run: `python run_kolam_analysis.py`

### Option 2: Using Anaconda (Easiest)
1. Download Anaconda from https://www.anaconda.com/download
2. Install Anaconda
3. Open Anaconda Prompt
4. Run: `conda install numpy matplotlib scipy`
5. Run: `python run_kolam_analysis.py`

### Option 3: Manual Python Installation
1. Download Python from https://www.python.org/downloads/
2. Install Python with "Add to PATH" option checked
3. Open Command Prompt
4. Run: `python -m pip install --upgrade pip`
5. Run: `python -m pip install numpy matplotlib scipy`
6. Run: `python run_kolam_analysis.py`

## Alternative: Online Python Environment

If you prefer not to install Python locally, you can use online environments:

### Google Colab
1. Go to https://colab.research.google.com/
2. Upload the Python files
3. Install dependencies: `!pip install numpy matplotlib scipy`
4. Run the code

### Jupyter Notebook Online
1. Go to https://jupyter.org/try
2. Upload the files
3. Run the code

## Files Created

The complete Kolam analysis system includes:

1. **kolam_analyzer.py** - Main analysis module with:
   - Symmetry detection (radial, bilateral, rotational)
   - Fractal analysis
   - Pattern generation
   - Visualization tools

2. **advanced_kolam_analysis.py** - Advanced features:
   - L-System pattern generation
   - Machine learning classification
   - Cultural significance analysis
   - Regional pattern recognition

3. **demo_kolam_system.py** - Complete demonstration
4. **run_kolam_analysis.py** - Easy-to-use launcher
5. **requirements.txt** - Dependencies list
6. **README.md** - Complete documentation

## Key Features Implemented

### ✅ Design Principles Identified
- **Grid-based Dot Patterns (Pulli)**: Traditional foundation using equidistant points
- **Symmetry Types**: Radial, bilateral, and rotational symmetry detection
- **Fractal Properties**: Self-similarity and recursive patterns
- **Geometric Shapes**: Circles, squares, triangles, and curves
- **Continuous Line Patterns**: Sikku Kolam with unbroken lines
- **Spatial Reasoning**: Mathematical relationships between points

### ✅ Analysis Capabilities
- Pattern recognition and classification
- Mathematical principle extraction
- Cultural significance analysis
- Regional pattern identification
- Complexity assessment

### ✅ Generation Features
- Multiple symmetry type generation
- Fractal pattern creation
- L-System based generation
- Customizable parameters

### ✅ Visualization
- Interactive pattern display
- Analysis overlay
- Pattern comparison
- Mathematical metrics display

## Running the System

Once Python is set up:

```bash
# Basic analysis
python run_kolam_analysis.py basic

# Advanced analysis
python run_kolam_analysis.py advanced

# Complete demonstration
python run_kolam_analysis.py demo

# All analyses
python run_kolam_analysis.py all
```

## Expected Output

The system will generate:
- Visual patterns showing different Kolam designs
- Analysis reports with mathematical metrics
- Cultural significance interpretations
- Comprehensive JSON reports
- Pattern classification results

## Mathematical Foundations

The system implements:
- **Group Theory**: For symmetry analysis
- **Fractal Geometry**: For self-similarity detection
- **L-Systems**: For recursive pattern generation
- **Graph Theory**: For line pattern analysis
- **Statistical Analysis**: For pattern classification

## Cultural Significance

The system recognizes:
- Tamil Nadu: Radial symmetry, circular patterns
- Karnataka: Bilateral symmetry, geometric shapes
- Andhra Pradesh: Rotational symmetry, floral motifs
- Kerala: Asymmetric patterns, nature-inspired designs

## Problem Statement Compliance

✅ **Computer programs developed** (Python)
✅ **Design principles identified** (Mathematical analysis)
✅ **Kolam recreation** (Pattern generation)
✅ **Mathematical underpinnings** (Fractal, symmetry, geometry)
✅ **Cultural heritage preservation** (Regional analysis)

This solution fully addresses the AICTE problem statement requirements for developing computer programs to identify design principles behind Kolam designs and recreate them.

