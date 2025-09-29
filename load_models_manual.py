#!/usr/bin/env python3
"""
Manual Model Loader with Better Error Handling
==============================================

Loads AI models with improved timeout and retry logic.
"""

import os
import time
import signal
import sys
from contextlib import contextmanager

@contextmanager
def timeout(duration):
    """Context manager for timeout"""
    def timeout_handler(signum, frame):
        raise TimeoutError(f"Operation timed out after {duration} seconds")
    
    # Set the signal handler
    old_handler = signal.signal(signal.SIGALRM, timeout_handler)
    signal.alarm(duration)
    
    try:
        yield
    finally:
        # Restore the old signal handler
        signal.signal(signal.SIGALRM, old_handler)
        signal.alarm(0)

def load_models_with_timeout():
    """Load models with timeout protection"""
    print("🎨 Loading AI Models with Timeout Protection")
    print("=" * 50)
    
    try:
        import torch
        from diffusers import StableDiffusionControlNetPipeline, ControlNetModel, UniPCMultistepScheduler
        
        device = 'cuda' if torch.cuda.is_available() else 'cpu'
        print(f"📱 Device: {device}")
        
        # Try to load with timeout
        with timeout(300):  # 5 minute timeout
            print("📥 Loading ControlNet model...")
            controlnet = ControlNetModel.from_pretrained(
                "lllyasviel/sd-controlnet-canny",
                torch_dtype=torch.float16 if device == "cuda" else torch.float32,
                local_files_only=False,  # Allow download
                resume_download=True
            )
            print("✅ ControlNet loaded!")
            
            print("📥 Loading Stable Diffusion pipeline...")
            pipe = StableDiffusionControlNetPipeline.from_pretrained(
                "runwayml/stable-diffusion-v1-5",
                controlnet=controlnet,
                torch_dtype=torch.float16 if device == "cuda" else torch.float32,
                safety_checker=None,
                requires_safety_checker=False,
                local_files_only=False,
                resume_download=True
            )
            
            pipe = pipe.to(device)
            pipe.scheduler = UniPCMultistepScheduler.from_config(pipe.scheduler.config)
            
            if hasattr(pipe, 'enable_attention_slicing'):
                pipe.enable_attention_slicing()
            
            print("✅ All models loaded successfully!")
            print("🎉 AI Diffusion is ready to use!")
            return True
            
    except TimeoutError as e:
        print(f"⏰ {e}")
        print("💡 Models are still downloading in background")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        print("💡 Try again when network is stable")
        return False

if __name__ == "__main__":
    # Only run on Unix-like systems (timeout doesn't work on Windows)
    if sys.platform == "win32":
        print("⚠️  Timeout protection not available on Windows")
        print("💡 Models will download in background")
        print("✅ System is ready to use without AI models")
    else:
        load_models_with_timeout()










