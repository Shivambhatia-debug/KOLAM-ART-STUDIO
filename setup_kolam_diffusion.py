#!/usr/bin/env python3
"""
Setup Script for Kolam Diffusion API
=====================================

This script helps set up the Kolam Diffusion API with all required dependencies.
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"\n🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        print(f"Error output: {e.stderr}")
        return False

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8+ is required. Current version:", f"{version.major}.{version.minor}")
        return False
    print(f"✅ Python version {version.major}.{version.minor} is compatible")
    return True

def check_cuda():
    """Check CUDA availability"""
    try:
        import torch
        if torch.cuda.is_available():
            print(f"✅ CUDA is available: {torch.cuda.get_device_name(0)}")
            return True
        else:
            print("⚠️  CUDA not available, will use CPU (slower)")
            return False
    except ImportError:
        print("⚠️  PyTorch not installed yet, will check after installation")
        return None

def install_requirements():
    """Install Python requirements"""
    requirements_file = "diffusion_requirements.txt"
    if not Path(requirements_file).exists():
        print(f"❌ Requirements file {requirements_file} not found")
        return False
    
    # Install requirements
    return run_command(f"pip install -r {requirements_file}", "Installing Python requirements")

def create_directories():
    """Create necessary directories"""
    directories = ["outputs", "models", "logs"]
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"✅ Created directory: {directory}")

def create_startup_script():
    """Create a startup script"""
    script_content = '''#!/bin/bash
# Kolam Diffusion API Startup Script

echo "🎨 Starting Kolam Diffusion API..."

# Check if virtual environment exists
if [ -d "venv" ]; then
    echo "Activating virtual environment..."
    source venv/bin/activate
fi

# Start the Flask API
python kolam_diffusion_api.py
'''
    
    with open("start_kolam_diffusion.sh", "w") as f:
        f.write(script_content)
    
    # Make it executable on Unix systems
    if platform.system() != "Windows":
        os.chmod("start_kolam_diffusion.sh", 0o755)
    
    print("✅ Created startup script: start_kolam_diffusion.sh")

def create_windows_batch():
    """Create Windows batch file"""
    batch_content = '''@echo off
echo 🎨 Starting Kolam Diffusion API...

REM Check if virtual environment exists
if exist "venv\\Scripts\\activate.bat" (
    echo Activating virtual environment...
    call venv\\Scripts\\activate.bat
)

REM Start the Flask API
python kolam_diffusion_api.py
pause
'''
    
    with open("start_kolam_diffusion.bat", "w") as f:
        f.write(batch_content)
    
    print("✅ Created Windows batch file: start_kolam_diffusion.bat")

def main():
    """Main setup function"""
    print("🎨 Kolam Diffusion API Setup")
    print("=" * 40)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Create directories
    create_directories()
    
    # Install requirements
    if not install_requirements():
        print("\n❌ Setup failed during requirements installation")
        sys.exit(1)
    
    # Check CUDA after installation
    cuda_available = check_cuda()
    
    # Create startup scripts
    create_startup_script()
    create_windows_batch()
    
    print("\n🎉 Setup completed successfully!")
    print("\n📋 Next steps:")
    print("1. Start the API server:")
    if platform.system() == "Windows":
        print("   start_kolam_diffusion.bat")
    else:
        print("   ./start_kolam_diffusion.sh")
    print("2. Open kolam_diffusion_test.html in your browser")
    print("3. Upload a Kolam image and generate variants!")
    
    if cuda_available:
        print("\n⚡ CUDA is available - generation will be faster!")
    else:
        print("\n⚠️  CUDA not available - generation will be slower but still functional")
    
    print("\n🔧 Troubleshooting:")
    print("- If you get memory errors, try reducing image size")
    print("- For CPU-only systems, generation may take 3-5 minutes")
    print("- Check the console for detailed error messages")

if __name__ == "__main__":
    main()












