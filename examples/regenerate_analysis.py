#!/usr/bin/env python3
"""
Quick script to regenerate analysis JSON from existing CSV data
"""

import pandas as pd
import json
from collections import Counter
import sys
import os

# Add src directory to path
sys.path.append('src')
from bluesky_analyzer import BlueskyAnalyzer

def regenerate_analysis():
    """Regenerate analysis from existing CSV"""
    
    # Check if CSV exists
    if not os.path.exists("bluesky_analysis_posts.csv"):
        print("❌ CSV file not found. Please run the full analyzer first.")
        return
    
    print("📊 Regenerating analysis from existing data...")
    
    # Load the CSV data
    df = pd.read_csv("bluesky_analysis_posts.csv")
    
    # Convert created_at back to datetime
    df["created_at"] = pd.to_datetime(df["created_at"])
    
    # Convert hashtags back to lists (they were saved as strings)
    df["hashtags"] = df["hashtags"].apply(lambda x: eval(x) if pd.notna(x) and x != '[]' else [])
    
    # Create analyzer instance and run analysis
    analyzer = BlueskyAnalyzer()
    analysis = analyzer.analyze_posts(df)
    
    # Save the corrected analysis
    with open("bluesky_analysis_analysis.json", "w") as f:
        json.dump(analysis, f, indent=2, default=str)
    
    # Print summary
    analyzer.print_summary(analysis)
    
    print(f"\n✅ Fixed analysis saved to bluesky_analysis_analysis.json")

if __name__ == "__main__":
    regenerate_analysis()
