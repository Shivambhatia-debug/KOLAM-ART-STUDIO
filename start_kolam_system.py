#!/usr/bin/env python3
"""
Kolam Art Studio - Complete System Launcher
==========================================

This script launches the complete Kolam analysis system including:
- Python backend API
- React frontend (if available)
- Pattern analysis and generation

AICTE Problem Statement 25107
"""

import subprocess
import sys
import os
import time
import webbrowser
from pathlib import Path

def check_python_dependencies():
    """Check if Python dependencies are installed"""
    try:
        import flask
        import numpy
        import matplotlib
        print("✅ Python dependencies found")
        return True
    except ImportError as e:
        print(f"❌ Missing Python dependency: {e}")
        print("Please install dependencies with: pip install -r requirements.txt")
        return False

def check_node_dependencies():
    """Check if Node.js dependencies are installed"""
    try:
        # Check if node_modules exists
        if os.path.exists("node_modules"):
            print("✅ Node.js dependencies found")
            return True
        else:
            print("⚠️  Node.js dependencies not found")
            print("Run 'npm install' to install React frontend dependencies")
            return False
    except Exception:
        return False

def start_backend():
    """Start the Python backend API"""
    print("\n🚀 Starting Python Backend API...")
    print("=" * 50)
    
    try:
        # Start the Flask backend
        backend_process = subprocess.Popen([
            sys.executable, "backend/app.py"
        ], cwd=os.getcwd())
        
        print("✅ Backend API started on http://localhost:5000")
        return backend_process
    except Exception as e:
        print(f"❌ Failed to start backend: {e}")
        return None

def start_frontend():
    """Start the React frontend"""
    print("\n🎨 Starting React Frontend...")
    print("=" * 50)
    
    try:
        # Start the React development server
        frontend_process = subprocess.Popen([
            "npm", "start"
        ], cwd=os.getcwd())
        
        print("✅ Frontend started on http://localhost:3000")
        return frontend_process
    except Exception as e:
        print(f"❌ Failed to start frontend: {e}")
        print("Make sure Node.js and npm are installed")
        return None

def open_browser():
    """Open browser to the application"""
    print("\n🌐 Opening browser...")
    time.sleep(3)  # Wait for servers to start
    
    try:
        webbrowser.open("http://localhost:3000")
        print("✅ Browser opened to http://localhost:3000")
    except Exception as e:
        print(f"⚠️  Could not open browser automatically: {e}")
        print("Please open http://localhost:3000 manually")

def show_system_info():
    """Show system information and available features"""
    print("\n🎨 KOLAM ART STUDIO - COMPLETE SYSTEM")
    print("=" * 60)
    print("AICTE Problem Statement 25107")
    print("Indian Knowledge Systems (IKS)")
    print("Category: Software | Theme: Heritage & Culture")
    print("=" * 60)
    
    print("\n📋 Available Features:")
    print("✅ Interactive Kolam Design Studio")
    print("✅ Mathematical Pattern Analysis")
    print("✅ Cultural Significance Detection")
    print("✅ Regional Pattern Recognition")
    print("✅ Fractal Dimension Calculation")
    print("✅ Symmetry Detection Algorithms")
    print("✅ Pattern Gallery & Templates")
    print("✅ Export & Download Options")
    
    print("\n🔧 System Components:")
    print("• Python Backend API (Flask)")
    print("• React Frontend (Interactive UI)")
    print("• Mathematical Analysis Engine")
    print("• Cultural Analysis Module")
    print("• Pattern Generation System")
    
    print("\n🌐 Access Points:")
    print("• Frontend: http://localhost:3000")
    print("• Backend API: http://localhost:5000")
    print("• API Documentation: http://localhost:5000")

def main():
    """Main launcher function"""
    show_system_info()
    
    # Check dependencies
    python_ok = check_python_dependencies()
    node_ok = check_node_dependencies()
    
    if not python_ok:
        print("\n❌ Cannot start system without Python dependencies")
        return
    
    # Start backend
    backend_process = start_backend()
    if not backend_process:
        print("\n❌ Cannot start system without backend")
        return
    
    # Start frontend if available
    frontend_process = None
    if node_ok:
        frontend_process = start_frontend()
    else:
        print("\n⚠️  Frontend not available - running backend only")
        print("Access API at: http://localhost:5000")
    
    # Open browser if frontend is running
    if frontend_process:
        open_browser()
    
    print("\n✅ System started successfully!")
    print("=" * 60)
    print("Press Ctrl+C to stop the system")
    
    try:
        # Keep the script running
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n\n🛑 Stopping Kolam Art Studio...")
        
        # Terminate processes
        if backend_process:
            backend_process.terminate()
            print("✅ Backend stopped")
        
        if frontend_process:
            frontend_process.terminate()
            print("✅ Frontend stopped")
        
        print("👋 Goodbye!")

if __name__ == "__main__":
    main()








































