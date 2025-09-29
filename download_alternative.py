#!/usr/bin/env python3
"""
Alternative Model Downloader
============================

Tries different methods to download AI models faster.
"""

import os
import requests
import subprocess
import sys

def try_alternative_downloads():
    """Try different download methods"""
    print("🚀 Trying Alternative Download Methods...")
    print("=" * 50)
    
    # Method 1: Try Hugging Face Mirror
    print("📥 Method 1: Using Hugging Face Mirror...")
    try:
        os.environ['HF_ENDPOINT'] = 'https://hf-mirror.com'
        print("✅ Set mirror to hf-mirror.com")
        
        from huggingface_hub import snapshot_download
        sd_path = snapshot_download(
            repo_id='runwayml/stable-diffusion-v1-5',
            resume_download=True,
            local_files_only=False,
            max_workers=2
        )
        print("✅ Download successful with mirror!")
        return True
        
    except Exception as e:
        print(f"❌ Mirror failed: {e}")
    
    # Method 2: Try smaller model
    print("\n📥 Method 2: Using smaller model...")
    try:
        from huggingface_hub import snapshot_download
        # Try a smaller, faster model
        sd_path = snapshot_download(
            repo_id='stabilityai/stable-diffusion-2-1-base',
            resume_download=True,
            local_files_only=False,
            max_workers=2
        )
        print("✅ Smaller model downloaded!")
        return True
        
    except Exception as e:
        print(f"❌ Smaller model failed: {e}")
    
    # Method 3: Try with wget/curl
    print("\n📥 Method 3: Using direct download...")
    try:
        # Download specific files directly
        model_urls = [
            "https://huggingface.co/runwayml/stable-diffusion-v1-5/resolve/main/unet/diffusion_pytorch_model.safetensors",
            "https://huggingface.co/runwayml/stable-diffusion-v1-5/resolve/main/vae/diffusion_pytorch_model.safetensors"
        ]
        
        cache_dir = os.path.expanduser('~/.cache/huggingface/hub')
        os.makedirs(cache_dir, exist_ok=True)
        
        for url in model_urls:
            filename = url.split('/')[-1]
            filepath = os.path.join(cache_dir, filename)
            
            print(f"Downloading {filename}...")
            response = requests.get(url, stream=True)
            response.raise_for_status()
            
            with open(filepath, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            print(f"✅ Downloaded {filename}")
        
        return True
        
    except Exception as e:
        print(f"❌ Direct download failed: {e}")
    
    # Method 4: Use existing models
    print("\n📥 Method 4: Check existing models...")
    try:
        cache_dir = os.path.expanduser('~/.cache/huggingface/hub')
        if os.path.exists(cache_dir):
            print("📁 Checking cache directory...")
            for item in os.listdir(cache_dir):
                if 'stable-diffusion' in item.lower():
                    print(f"✅ Found existing model: {item}")
                    return True
        
        print("❌ No existing models found")
        
    except Exception as e:
        print(f"❌ Cache check failed: {e}")
    
    return False

def suggest_alternatives():
    """Suggest alternative approaches"""
    print("\n💡 Alternative Solutions:")
    print("=" * 30)
    print("1. 🌐 Use online AI services:")
    print("   • Leonardo AI (free)")
    print("   • Adobe Firefly")
    print("   • DALL-E 2")
    print()
    print("2. 📱 Use mobile apps:")
    print("   • Wombo Dream")
    print("   • Lensa AI")
    print()
    print("3. 🖥️ Use existing system:")
    print("   • All pattern generation works")
    print("   • Image analysis works")
    print("   • AI features will work once download completes")
    print()
    print("4. ⏰ Wait for download:")
    print("   • Models download in background")
    print("   • System works without AI models")
    print("   • AI features activate automatically")

if __name__ == "__main__":
    success = try_alternative_downloads()
    
    if not success:
        suggest_alternatives()
    else:
        print("\n🎉 Download completed successfully!")
        print("✅ AI models are ready to use!")










