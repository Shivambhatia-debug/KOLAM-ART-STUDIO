#!/usr/bin/env python3
"""
Quick Start Script for Kolam Analysis System
===========================================

This script provides a simple way to run the Kolam analysis system
for the AICTE problem statement 25107.

Usage:
    python run_kolam_analysis.py [option]

Options:
    basic     - Run basic pattern generation and analysis
    advanced  - Run advanced analysis with L-Systems and cultural significance
    demo      - Run complete demonstration
    all       - Run all analyses (default)
"""

import sys
import os

def check_dependencies():
    """Check if required dependencies are installed"""
    try:
        import numpy
        import matplotlib
        print("✓ Dependencies check passed")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("Please install dependencies with: pip install -r requirements.txt")
        return False

def run_basic_analysis():
    """Run basic Kolam analysis"""
    print("🎨 Running Basic Kolam Analysis...")
    print("=" * 40)
    
    try:
        from kolam_analyzer import main as basic_main
        basic_main()
    except Exception as e:
        print(f"Error in basic analysis: {e}")

def run_advanced_analysis():
    """Run advanced Kolam analysis"""
    print("\n🔬 Running Advanced Kolam Analysis...")
    print("=" * 40)
    
    try:
        from advanced_kolam_analysis import main as advanced_main
        advanced_main()
    except Exception as e:
        print(f"Error in advanced analysis: {e}")

def run_complete_demo():
    """Run complete demonstration"""
    print("\n🎭 Running Complete Demonstration...")
    print("=" * 40)
    
    try:
        from demo_kolam_system import main as demo_main
        demo_main()
    except Exception as e:
        print(f"Error in demo: {e}")

def show_help():
    """Show help information"""
    print("""
🎨 Kolam Design Analyzer and Generator
=====================================

AICTE Problem Statement 25107
Indian Knowledge Systems (IKS)

This system analyzes and generates traditional Indian Kolam designs
by identifying their mathematical principles and design patterns.

USAGE:
    python run_kolam_analysis.py [option]

OPTIONS:
    basic     - Generate and analyze basic Kolam patterns
    advanced  - Run advanced analysis with L-Systems and cultural significance
    demo      - Run complete demonstration with all features
    all       - Run all analyses (default)
    help      - Show this help message

EXAMPLES:
    python run_kolam_analysis.py basic
    python run_kolam_analysis.py advanced
    python run_kolam_analysis.py demo
    python run_kolam_analysis.py all

FEATURES:
    ✓ Symmetry detection (radial, bilateral, rotational)
    ✓ Fractal analysis and generation
    ✓ L-System based pattern generation
    ✓ Cultural significance analysis
    ✓ Pattern classification
    ✓ Comprehensive visualization
    ✓ Mathematical principle identification

FILES GENERATED:
    - kolam_analyzer.py (Main analysis module)
    - advanced_kolam_analysis.py (Advanced features)
    - demo_kolam_system.py (Complete demonstration)
    - requirements.txt (Dependencies)
    - README.md (Documentation)
    - kolam_comprehensive_report.json (Analysis results)

For more information, see README.md
""")

def main():
    """Main function"""
    print("🎨 Kolam Design Analyzer and Generator")
    print("AICTE Problem Statement 25107")
    print("=" * 50)
    
    # Check dependencies
    if not check_dependencies():
        return
    
    # Get command line argument
    option = sys.argv[1] if len(sys.argv) > 1 else "all"
    
    if option == "help":
        show_help()
    elif option == "basic":
        run_basic_analysis()
    elif option == "advanced":
        run_advanced_analysis()
    elif option == "demo":
        run_complete_demo()
    elif option == "all":
        print("🚀 Running Complete Kolam Analysis System...")
        run_basic_analysis()
        run_advanced_analysis()
        run_complete_demo()
    else:
        print(f"❌ Unknown option: {option}")
        print("Use 'python run_kolam_analysis.py help' for usage information")
        return
    
    print("\n✅ Analysis complete!")
    print("Check the generated visualizations and reports.")

if __name__ == "__main__":
    main()

