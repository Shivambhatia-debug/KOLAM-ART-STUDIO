#!/usr/bin/env python3
"""
AI Model Loading Monitor
========================

Monitors the progress of AI model loading in the background.
"""

import requests
import time
import json

def monitor_model_loading():
    """Monitor AI model loading progress"""
    print("🔍 Monitoring AI Model Loading Progress...")
    print("=" * 50)
    
    for i in range(10):
        try:
            response = requests.get('http://localhost:5000/api/diffusion/status', timeout=5)
            if response.status_code == 200:
                status = response.json()
                print(f"⏱️  Check {i+1}/10:")
                print(f"   🤖 Models loaded: {status['models_loaded']}")
                print(f"   📱 Device: {status['device']}")
                print(f"   🔧 Pipeline loaded: {status['pipeline_loaded']}")
                print(f"   🎯 ControlNet loaded: {status['controlnet_loaded']}")
                
                if status['models_loaded']:
                    print("🎉 AI Models are ready!")
                    return True
                else:
                    print("⏳ Still loading...")
                    time.sleep(30)  # Wait 30 seconds
            else:
                print(f"❌ Status check failed: {response.status_code}")
                break
        except Exception as e:
            print(f"❌ Error: {e}")
            break
    
    print()
    print("💡 Tip: Models download in background while you use other features!")
    return False

if __name__ == "__main__":
    monitor_model_loading()










