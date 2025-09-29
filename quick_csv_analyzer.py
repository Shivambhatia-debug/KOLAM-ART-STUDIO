#!/usr/bin/env python3
"""
Quick CSV Kolam Data Analyzer
============================

A simplified and faster version to analyze CSV Kolam data.
"""

import os
import pandas as pd
import numpy as np
import json
import matplotlib.pyplot as plt
from pathlib import Path
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def analyze_csv_files(csv_dir="kolam_dataset/csv_files"):
    """Quick analysis of CSV files"""
    csv_path = Path(csv_dir)
    
    if not csv_path.exists():
        logger.error(f"CSV directory not found: {csv_dir}")
        return
    
    csv_files = list(csv_path.glob("*.csv"))
    logger.info(f"Found {len(csv_files)} CSV files")
    
    results = {}
    
    for csv_file in csv_files[:3]:  # Process only first 3 files for speed
        logger.info(f"Analyzing {csv_file.name}...")
        
        try:
            # Read only first few rows to understand structure
            df = pd.read_csv(csv_file, nrows=5)
            
            # Basic analysis
            analysis = {
                'filename': csv_file.name,
                'shape': df.shape,
                'columns': len(df.columns),
                'sample_data': df.iloc[0].values[:10].tolist() if len(df) > 0 else [],
                'data_types': str(df.dtypes.iloc[0]) if len(df.columns) > 0 else 'unknown'
            }
            
            results[csv_file.stem] = analysis
            
            logger.info(f"  Shape: {df.shape}")
            logger.info(f"  Columns: {len(df.columns)}")
            logger.info(f"  Sample: {analysis['sample_data']}")
            
        except Exception as e:
            logger.error(f"Error processing {csv_file.name}: {e}")
            results[csv_file.stem] = {'error': str(e)}
    
    return results

def create_simple_visualization(csv_dir="kolam_dataset/csv_files"):
    """Create simple visualizations"""
    csv_path = Path(csv_dir)
    csv_files = list(csv_path.glob("*.csv"))
    
    if not csv_files:
        logger.error("No CSV files found")
        return
    
    # Create output directory
    output_dir = Path("kolam_dataset/csv_analysis")
    output_dir.mkdir(exist_ok=True)
    
    # Analyze first file in detail
    first_file = csv_files[0]
    logger.info(f"Creating detailed analysis for {first_file.name}")
    
    try:
        # Read limited data
        df = pd.read_csv(first_file, nrows=20)
        
        # Create visualization
        fig, axes = plt.subplots(2, 2, figsize=(12, 10))
        fig.suptitle(f'CSV Kolam Analysis: {first_file.name}', fontsize=14)
        
        # Plot 1: Data structure
        ax1 = axes[0, 0]
        ax1.text(0.1, 0.9, f"File: {first_file.name}\nShape: {df.shape}\nColumns: {len(df.columns)}", 
                transform=ax1.transAxes, fontsize=10, verticalalignment='top')
        ax1.set_title('File Information')
        ax1.axis('off')
        
        # Plot 2: Sample data heatmap
        ax2 = axes[0, 1]
        if len(df) > 0 and len(df.columns) > 0:
            # Take first 10 columns and 10 rows for heatmap
            sample_data = df.iloc[:min(10, len(df)), :min(10, len(df.columns))]
            im = ax2.imshow(sample_data.values, cmap='viridis', aspect='auto')
            ax2.set_title('Sample Data Heatmap')
            ax2.set_xlabel('Columns')
            ax2.set_ylabel('Rows')
            plt.colorbar(im, ax=ax2)
        
        # Plot 3: Column statistics
        ax3 = axes[1, 0]
        if len(df.columns) > 0:
            # Calculate basic stats for first few columns
            stats_data = []
            for i, col in enumerate(df.columns[:10]):
                if df[col].dtype in ['int64', 'float64']:
                    stats_data.append({
                        'column': f'Col_{i}',
                        'mean': df[col].mean(),
                        'std': df[col].std(),
                        'min': df[col].min(),
                        'max': df[col].max()
                    })
            
            if stats_data:
                means = [s['mean'] for s in stats_data]
                ax3.plot(means, 'o-')
                ax3.set_title('Column Means (First 10)')
                ax3.set_xlabel('Column Index')
                ax3.set_ylabel('Mean Value')
                ax3.grid(True, alpha=0.3)
        
        # Plot 4: Data distribution
        ax4 = axes[1, 1]
        if len(df) > 0 and len(df.columns) > 0:
            # Flatten all data and create histogram
            all_values = df.values.flatten()
            all_values = all_values[~np.isnan(all_values)]  # Remove NaN values
            
            if len(all_values) > 0:
                ax4.hist(all_values, bins=20, alpha=0.7, edgecolor='black')
                ax4.set_title('Data Value Distribution')
                ax4.set_xlabel('Value')
                ax4.set_ylabel('Frequency')
                ax4.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        # Save plot
        output_path = output_dir / f"{first_file.stem}_analysis.png"
        plt.savefig(output_path, dpi=150, bbox_inches='tight')
        plt.close()
        
        logger.info(f"Saved visualization: {output_path}")
        
    except Exception as e:
        logger.error(f"Error creating visualization: {e}")

def generate_summary_report(results, output_path="kolam_dataset/csv_summary.json"):
    """Generate summary report"""
    summary = {
        "total_files_analyzed": len(results),
        "files": list(results.keys()),
        "analysis_results": results,
        "summary": {
            "successful_files": len([r for r in results.values() if 'error' not in r]),
            "failed_files": len([r for r in results.values() if 'error' in r])
        }
    }
    
    # Save report
    with open(output_path, 'w') as f:
        json.dump(summary, f, indent=2)
    
    logger.info(f"Summary report saved: {output_path}")
    return summary

def main():
    """Main function"""
    logger.info("Starting Quick CSV Analysis...")
    
    # Analyze CSV files
    results = analyze_csv_files()
    
    if not results:
        logger.error("No results generated")
        return
    
    # Create visualization
    create_simple_visualization()
    
    # Generate summary
    summary = generate_summary_report(results)
    
    # Print results
    logger.info("\n" + "="*50)
    logger.info("QUICK ANALYSIS RESULTS")
    logger.info("="*50)
    logger.info(f"Files analyzed: {summary['total_files_analyzed']}")
    logger.info(f"Successful: {summary['summary']['successful_files']}")
    logger.info(f"Failed: {summary['summary']['failed_files']}")
    
    for filename, result in results.items():
        if 'error' not in result:
            logger.info(f"  {filename}: {result['shape']} shape, {result['columns']} columns")
        else:
            logger.info(f"  {filename}: ERROR - {result['error']}")
    
    logger.info("="*50)
    logger.info("Quick analysis completed!")

if __name__ == "__main__":
    main()


