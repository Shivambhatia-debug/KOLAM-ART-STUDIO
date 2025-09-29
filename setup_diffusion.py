#!/usr/bin/env python3
"""
Setup Script for Kolam Diffusion Integration
===========================================

This script installs the diffusion dependencies for the Kolam Art project.
"""

import subprocess
import sys
import os
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

def install_diffusion_dependencies():
    """Install diffusion dependencies"""
    print("\n🎨 Installing AI Diffusion Dependencies...")
    
    # Install PyTorch first (with CUDA support if available)
    print("\n📦 Installing PyTorch...")
    if not run_command("pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118", "Installing PyTorch with CUDA support"):
        print("⚠️  CUDA PyTorch failed, trying CPU version...")
        if not run_command("pip install torch torchvision", "Installing PyTorch CPU version"):
            return False
    
    # Install other diffusion dependencies
    dependencies = [
        "diffusers>=0.21.0",
        "transformers>=4.30.0", 
        "accelerate>=0.20.0",
        "opencv-python>=4.8.0",
        "xformers>=0.0.20"
    ]
    
    for dep in dependencies:
        if not run_command(f"pip install {dep}", f"Installing {dep}"):
            print(f"⚠️  Failed to install {dep}, continuing...")
    
    return True

def test_diffusion_imports():
    """Test if diffusion libraries can be imported"""
    print("\n🧪 Testing diffusion imports...")
    
    try:
        import torch
        print(f"✅ PyTorch {torch.__version__} imported successfully")
        
        if torch.cuda.is_available():
            print(f"✅ CUDA available: {torch.cuda.get_device_name(0)}")
        else:
            print("⚠️  CUDA not available, will use CPU")
        
        import diffusers
        print(f"✅ Diffusers {diffusers.__version__} imported successfully")
        
        import transformers
        print(f"✅ Transformers {transformers.__version__} imported successfully")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def create_outputs_directory():
    """Create outputs directory for generated images"""
    outputs_dir = Path("outputs")
    outputs_dir.mkdir(exist_ok=True)
    print(f"✅ Created outputs directory: {outputs_dir}")

def main():
    """Main setup function"""
    print("🎨 Kolam AI Diffusion Setup")
    print("=" * 40)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Create outputs directory
    create_outputs_directory()
    
    # Install dependencies
    if not install_diffusion_dependencies():
        print("\n❌ Setup failed during dependency installation")
        sys.exit(1)
    
    # Test imports
    if not test_diffusion_imports():
        print("\n⚠️  Some dependencies may not be working correctly")
        print("   The system will still work but AI diffusion will be disabled")
    
    print("\n🎉 Setup completed successfully!")
    print("\n📋 Next steps:")
    print("1. Start your production backend:")
    print("   python production_backend.py")
    print("2. Open your React frontend:")
    print("   npm start")
    print("3. Navigate to /ai-diffusion to use the AI generator!")
    
    print("\n🔧 Troubleshooting:")
    print("- If you get CUDA errors, the system will fallback to CPU")
    print("- First generation may take 5-10 minutes to download models")
    print("- Check the backend logs for detailed error messages")

if __name__ == "__main__":
    main()












