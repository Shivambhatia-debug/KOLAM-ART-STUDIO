#!/usr/bin/env python3
"""
Manual Model Downloader for Kolam Diffusion
===========================================

Downloads AI models with better timeout settings and retry logic.
"""

import os
import time
from huggingface_hub import snapshot_download
from pathlib import Path

def download_models():
    """Download AI models with better settings"""
    print("🎨 Starting AI Model Download...")
    print("=" * 50)
    
    # Create cache directory
    cache_dir = Path.home() / ".cache" / "huggingface" / "hub"
    cache_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"📁 Cache directory: {cache_dir}")
    
    try:
        # Download Stable Diffusion v1.5
        print("\n📥 Downloading Stable Diffusion v1.5...")
        print("   This may take 10-30 minutes depending on network...")
        
        sd_path = snapshot_download(
            repo_id="runwayml/stable-diffusion-v1-5",
            cache_dir=cache_dir,
            resume_download=True,
            local_files_only=False,
            max_workers=1,  # Reduce concurrent downloads
            ignore_patterns=["*.bin"]  # Skip .bin files, use .safetensors
        )
        
        print(f"✅ Stable Diffusion downloaded to: {sd_path}")
        
        # Download ControlNet Canny
        print("\n📥 Downloading ControlNet Canny...")
        
        controlnet_path = snapshot_download(
            repo_id="lllyasviel/sd-controlnet-canny",
            cache_dir=cache_dir,
            resume_download=True,
            local_files_only=False,
            max_workers=1
        )
        
        print(f"✅ ControlNet downloaded to: {controlnet_path}")
        
        print("\n🎉 All models downloaded successfully!")
        print("\n📋 Next steps:")
        print("1. Restart the backend: python production_backend.py")
        print("2. The AI models will be loaded automatically")
        print("3. You can now generate AI Kolam variants!")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Download failed: {e}")
        print("\n🔧 Troubleshooting:")
        print("- Check your internet connection")
        print("- Try again later when network is stable")
        print("- The system will work without AI models")
        return False

if __name__ == "__main__":
    download_models()











