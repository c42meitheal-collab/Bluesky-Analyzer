#!/usr/bin/env python3
"""
Example usage of the Bluesky Analyzer

This example shows how to use the BlueskyAnalyzer class programmatically
instead of using the interactive command-line interface.
"""

import sys
import os

# Add src directory to path to import the analyzer
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from bluesky_analyzer import BlueskyAnalyzer


def analyze_posts_programmatically():
    """
    Example of using BlueskyAnalyzer programmatically
    """
    
    # Initialize the analyzer
    analyzer = BlueskyAnalyzer()
    
    # Credentials (in a real app, use environment variables or secure input)
    handle = "your_handle.bsky.social"
    password = "your_password"
    
    # Authenticate
    if not analyzer.authenticate(handle, password):
        print("Failed to authenticate")
        return
    
    # Fetch posts (limit to 100 for this example)
    raw_posts = analyzer.fetch_posts(limit=100)
    
    if not raw_posts:
        print("No posts found")
        return
    
    # Parse posts into DataFrame
    df = analyzer.parse_posts(raw_posts)
    
    # Perform analysis
    analysis = analyzer.analyze_posts(df)
    
    # Create visualizations
    analyzer.create_visualizations(df, save_dir="example_output")
    
    # Save results
    analyzer.save_results(df, analysis, filename="example_analysis")
    
    # Print summary
    analyzer.print_summary(analysis)
    
    # You can now work with the DataFrame for custom analysis
    print(f"\nCustom analysis:")
    print(f"Posts with hashtags: {df['hashtag_count'].sum()}")
    print(f"Average engagement indicators: {df['mention_count'].mean():.2f} mentions per post")
    
    # Find your most active posting hour
    if 'posting_patterns' in analysis:
        patterns = analysis['posting_patterns']
        print(f"You're most active at {patterns['busiest_hour']}:00")


if __name__ == "__main__":
    # Note: Replace the credentials above with your actual credentials
    # or set up environment variables for security
    print("This is an example - please update credentials before running!")
    # analyze_posts_programmatically()
