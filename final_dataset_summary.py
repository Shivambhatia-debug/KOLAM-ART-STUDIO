#!/usr/bin/env python3
"""
Final Dataset Summary
====================

Comprehensive summary of the entire Kolam dataset including:
- Original generated dataset
- CSV integrated data
- Training models status
- System capabilities
"""

import os
import json
import logging
from pathlib import Path
import pandas as pd

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class DatasetSummaryGenerator:
    def __init__(self, dataset_dir="kolam_dataset"):
        self.dataset_dir = Path(dataset_dir)
        self.summary = {}
        
    def generate_comprehensive_summary(self):
        """Generate comprehensive dataset summary"""
        logger.info("Generating comprehensive dataset summary...")
        
        # Original dataset analysis
        original_data = self.analyze_original_dataset()
        
        # CSV data analysis
        csv_data = self.analyze_csv_data()
        
        # Model status
        model_status = self.check_model_status()
        
        # System capabilities
        system_capabilities = self.analyze_system_capabilities()
        
        # Combine all data
        self.summary = {
            "dataset_overview": {
                "total_samples": original_data['total_samples'] + csv_data['total_samples'],
                "original_dataset_samples": original_data['total_samples'],
                "csv_integrated_samples": csv_data['total_samples'],
                "train_split": original_data['train_samples'] + csv_data['train_samples'],
                "val_split": original_data['val_samples'] + csv_data['val_samples'],
                "test_split": original_data['test_samples']
            },
            "original_dataset": original_data,
            "csv_integrated_data": csv_data,
            "model_status": model_status,
            "system_capabilities": system_capabilities,
            "recommendations": self.generate_recommendations()
        }
        
        return self.summary
    
    def analyze_original_dataset(self):
        """Analyze the original generated dataset"""
        logger.info("Analyzing original dataset...")
        
        # Count files in each split
        train_images = len(list((self.dataset_dir / "train" / "images").glob("*.png")))
        val_images = len(list((self.dataset_dir / "val" / "images").glob("*.png")))
        test_images = len(list((self.dataset_dir / "test" / "images").glob("*.png")))
        
        # Read metadata
        metadata_path = self.dataset_dir / "metadata" / "dataset_info.json"
        metadata = {}
        if metadata_path.exists():
            with open(metadata_path, 'r') as f:
                metadata = json.load(f)
        
        return {
            "total_samples": train_images + val_images + test_images,
            "train_samples": train_images,
            "val_samples": val_images,
            "test_samples": test_images,
            "metadata": metadata,
            "kolam_types": metadata.get('kolam_types', {}),
            "symmetry_types": metadata.get('symmetry_types', {}),
            "cultural_regions": metadata.get('cultural_regions', {})
        }
    
    def analyze_csv_data(self):
        """Analyze CSV integrated data"""
        logger.info("Analyzing CSV integrated data...")
        
        # Count CSV data
        csv_train_images = len(list((self.dataset_dir / "csv_train" / "images").glob("*.png")))
        csv_val_images = len(list((self.dataset_dir / "csv_val" / "images").glob("*.png")))
        
        # Read CSV integration report
        csv_report_path = self.dataset_dir / "csv_integration_report.json"
        csv_report = {}
        if csv_report_path.exists():
            with open(csv_report_path, 'r') as f:
                csv_report = json.load(f)
        
        return {
            "total_samples": csv_train_images + csv_val_images,
            "train_samples": csv_train_images,
            "val_samples": csv_val_images,
            "integration_report": csv_report,
            "pattern_analysis": csv_report.get('pattern_analysis', {}),
            "files_processed": csv_report.get('files_processed', [])
        }
    
    def check_model_status(self):
        """Check status of trained models"""
        logger.info("Checking model status...")
        
        models_dir = Path("models")
        model_files = {
            "kolam_type_model": models_dir / "kolam_type_model.pkl",
            "symmetry_type_model": models_dir / "symmetry_type_model.pkl",
            "cultural_region_model": models_dir / "cultural_region_model.pkl",
            "feature_names": models_dir / "feature_names.pkl",
            "label_encoders": models_dir / "label_encoders.pkl",
            "scalers": models_dir / "scalers.pkl"
        }
        
        model_status = {}
        for model_name, model_path in model_files.items():
            model_status[model_name] = {
                "exists": model_path.exists(),
                "size_mb": round(model_path.stat().st_size / (1024*1024), 2) if model_path.exists() else 0
            }
        
        return {
            "models_available": sum(1 for status in model_status.values() if status['exists']),
            "total_models": len(model_files),
            "model_details": model_status,
            "training_complete": all(status['exists'] for status in model_status.values())
        }
    
    def analyze_system_capabilities(self):
        """Analyze system capabilities"""
        logger.info("Analyzing system capabilities...")
        
        # Check backend status
        backend_files = [
            "production_backend.py",
            "enhanced_backend_api.py",
            "research_backend_api.py"
        ]
        
        backend_status = {}
        for backend_file in backend_files:
            backend_path = Path(backend_file)
            backend_status[backend_file] = {
                "exists": backend_path.exists(),
                "size_kb": round(backend_path.stat().st_size / 1024, 2) if backend_path.exists() else 0
            }
        
        # Check frontend status
        frontend_files = [
            "src/App.js",
            "src/pages/ImageAnalysis.js",
            "src/components/ProfessionalHeader.js"
        ]
        
        frontend_status = {}
        for frontend_file in frontend_files:
            frontend_path = Path(frontend_file)
            frontend_status[frontend_file] = {
                "exists": frontend_path.exists(),
                "size_kb": round(frontend_path.stat().st_size / 1024, 2) if frontend_path.exists() else 0
            }
        
        return {
            "backend_apis": backend_status,
            "frontend_components": frontend_status,
            "api_endpoints": [
                "/api/health",
                "/api/analyze",
                "/api/improved-analysis",
                "/api/generate-pattern",
                "/api/cultural-analysis"
            ],
            "features_available": [
                "Image Analysis",
                "Pattern Generation",
                "Cultural Classification",
                "Symmetry Detection",
                "Eulerian Path Validation",
                "ML-based Classification"
            ]
        }
    
    def generate_recommendations(self):
        """Generate recommendations for dataset usage"""
        return {
            "training_recommendations": [
                "Use the combined dataset (original + CSV) for better model performance",
                "Retrain models with the expanded dataset for improved accuracy",
                "Consider data augmentation techniques for CSV coordinate data",
                "Validate model performance on both synthetic and real coordinate data"
            ],
            "usage_recommendations": [
                "Use /api/improved-analysis for ML-based image analysis",
                "Combine pattern generation with cultural analysis for comprehensive results",
                "Leverage the CSV data for coordinate-based pattern reconstruction",
                "Use the trained models for real-time Kolam classification"
            ],
            "next_steps": [
                "Test the complete system with real Kolam images",
                "Fine-tune models based on user feedback",
                "Expand the dataset with more diverse Kolam patterns",
                "Implement advanced visualization features"
            ]
        }
    
    def save_summary_report(self, output_path="kolam_dataset/final_dataset_summary.json"):
        """Save the comprehensive summary report"""
        with open(output_path, 'w') as f:
            json.dump(self.summary, f, indent=2)
        
        logger.info(f"Summary report saved: {output_path}")
        return output_path
    
    def print_summary(self):
        """Print a formatted summary"""
        logger.info("\n" + "="*80)
        logger.info("COMPREHENSIVE KOLAM DATASET SUMMARY")
        logger.info("="*80)
        
        # Dataset Overview
        overview = self.summary['dataset_overview']
        logger.info(f"\n📊 DATASET OVERVIEW:")
        logger.info(f"   Total Samples: {overview['total_samples']}")
        logger.info(f"   ├─ Original Dataset: {overview['original_dataset_samples']}")
        logger.info(f"   └─ CSV Integrated: {overview['csv_integrated_samples']}")
        logger.info(f"   Train Split: {overview['train_split']}")
        logger.info(f"   Validation Split: {overview['val_split']}")
        logger.info(f"   Test Split: {overview['test_split']}")
        
        # Model Status
        model_status = self.summary['model_status']
        logger.info(f"\n🤖 MODEL STATUS:")
        logger.info(f"   Models Available: {model_status['models_available']}/{model_status['total_models']}")
        logger.info(f"   Training Complete: {'✅ Yes' if model_status['training_complete'] else '❌ No'}")
        
        # System Capabilities
        capabilities = self.summary['system_capabilities']
        logger.info(f"\n⚙️ SYSTEM CAPABILITIES:")
        logger.info(f"   API Endpoints: {len(capabilities['api_endpoints'])}")
        logger.info(f"   Features Available: {len(capabilities['features_available'])}")
        
        # Recommendations
        recommendations = self.summary['recommendations']
        logger.info(f"\n💡 RECOMMENDATIONS:")
        for i, rec in enumerate(recommendations['training_recommendations'][:2], 1):
            logger.info(f"   {i}. {rec}")
        
        logger.info("="*80)

def main():
    """Main function"""
    logger.info("Generating Final Dataset Summary...")
    
    # Initialize summary generator
    generator = DatasetSummaryGenerator()
    
    # Generate comprehensive summary
    summary = generator.generate_comprehensive_summary()
    
    # Save summary report
    report_path = generator.save_summary_report()
    
    # Print formatted summary
    generator.print_summary()
    
    logger.info(f"\n✅ Complete dataset summary generated: {report_path}")
    logger.info("🎉 Kolam Analysis System is ready for use!")

if __name__ == "__main__":
    main()


