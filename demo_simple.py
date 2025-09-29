#!/usr/bin/env python3
"""
Simple Demo for Kolam Pattern Generator
======================================

Quick demonstration of the system capabilities.
"""

from kolam_pattern_generator_ml import KolamPatternGenerator, create_sample_csv, create_sample_image

def main():
    print("🎨 KOLAM PATTERN GENERATOR - SIMPLE DEMO")
    print("=" * 50)
    
    # Create sample files
    print("Creating sample files...")
    create_sample_csv()
    create_sample_image()
    
    # Demo 1: CSV Processing
    print("\n📊 Demo 1: CSV Pattern Processing")
    generator1 = KolamPatternGenerator("demo_csv_output")
    patterns1 = generator1.process_input("sample_kolam.csv", "csv", 6)
    print(f"✅ Generated {len(patterns1)} patterns from CSV")
    
    # Demo 2: Image Processing  
    print("\n🖼️ Demo 2: Image Pattern Processing")
    generator2 = KolamPatternGenerator("demo_image_output")
    patterns2 = generator2.process_input("sample_kolam.png", "image", 6)
    print(f"✅ Generated {len(patterns2)} patterns from image")
    
    # Cleanup
    import os
    os.remove("sample_kolam.csv")
    os.remove("sample_kolam.png")
    
    print("\n🎉 Demo completed successfully!")
    print("Check the demo_*_output directories for results!")

if __name__ == "__main__":
    main()















