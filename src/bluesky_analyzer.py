#!/usr/bin/env python3
"""
Bluesky Post Fetcher and Analyzer
Fetches all your posts from Bluesky using AT Protocol and provides analysis
"""

import requests
import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timezone
import re
from collections import Counter
import time
from typing import List, Dict, Any
import os
import getpass

class BlueskyAnalyzer:
    def __init__(self):
        self.base_url = "https://bsky.social"
        self.session = None
        self.access_jwt = None
        self.refresh_jwt = None
        self.did = None
        
    def authenticate(self, handle: str, password: str) -> bool:
        """
        Authenticate with Bluesky using handle and password
        """
        auth_url = f"{self.base_url}/xrpc/com.atproto.server.createSession"
        
        auth_data = {
            "identifier": handle,
            "password": password
        }
        
        try:
            response = requests.post(auth_url, json=auth_data)
            response.raise_for_status()
            
            session_data = response.json()
            self.access_jwt = session_data["accessJwt"]
            self.refresh_jwt = session_data["refreshJwt"] 
            self.did = session_data["did"]
            
            print(f"✅ Successfully authenticated as {handle}")
            return True
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Authentication failed: {e}")
            return False
    
    def get_headers(self) -> Dict[str, str]:
        """Get headers with authentication"""
        return {
            "Authorization": f"Bearer {self.access_jwt}",
            "Content-Type": "application/json"
        }
    
    def fetch_posts(self, limit: int = None) -> List[Dict[str, Any]]:
        """
        Fetch all posts from the authenticated user
        """
        if not self.access_jwt:
            raise Exception("Not authenticated. Call authenticate() first.")
        
        posts = []
        cursor = None
        batch_size = 100  # Max allowed by API
        total_fetched = 0
        
        print("🔄 Fetching posts...")
        
        while True:
            # Construct API URL
            url = f"{self.base_url}/xrpc/com.atproto.repo.listRecords"
            params = {
                "repo": self.did,
                "collection": "app.bsky.feed.post",
                "limit": batch_size
            }
            
            if cursor:
                params["cursor"] = cursor
            
            try:
                response = requests.get(url, params=params, headers=self.get_headers())
                response.raise_for_status()
                
                data = response.json()
                batch_posts = data.get("records", [])
                
                if not batch_posts:
                    break
                
                posts.extend(batch_posts)
                total_fetched += len(batch_posts)
                print(f"   Fetched {total_fetched} posts so far...")
                
                # Check if we have more pages
                cursor = data.get("cursor")
                if not cursor:
                    break
                
                # Check limit
                if limit and total_fetched >= limit:
                    posts = posts[:limit]
                    break
                
                # Rate limiting - be nice to the API
                time.sleep(0.1)
                
            except requests.exceptions.RequestException as e:
                print(f"❌ Error fetching posts: {e}")
                break
        
        print(f"✅ Successfully fetched {len(posts)} posts")
        return posts
    
    def parse_posts(self, raw_posts: List[Dict]) -> pd.DataFrame:
        """
        Parse raw post data into a pandas DataFrame for analysis
        """
        parsed_posts = []
        
        for post in raw_posts:
            try:
                value = post.get("value", {})
                
                # Parse timestamp
                created_at = value.get("createdAt", "")
                if created_at:
                    timestamp = datetime.fromisoformat(created_at.replace("Z", "+00:00"))
                else:
                    timestamp = None
                
                # Extract text content
                text = value.get("text", "")
                
                # Extract facets (links, mentions, hashtags)
                facets = value.get("facets", [])
                mentions = []
                hashtags = []
                links = []
                
                for facet in facets:
                    for feature in facet.get("features", []):
                        if feature.get("$type") == "app.bsky.richtext.facet#mention":
                            mentions.append(feature.get("did", ""))
                        elif feature.get("$type") == "app.bsky.richtext.facet#tag":
                            hashtags.append(feature.get("tag", ""))
                        elif feature.get("$type") == "app.bsky.richtext.facet#link":
                            links.append(feature.get("uri", ""))
                
                # Check for media
                embed = value.get("embed", {})
                has_image = embed.get("$type") == "app.bsky.embed.images"
                has_external = embed.get("$type") == "app.bsky.embed.external"
                
                # Reply information
                reply = value.get("reply", {})
                is_reply = bool(reply)
                
                parsed_post = {
                    "uri": post.get("uri", ""),
                    "cid": post.get("cid", ""),
                    "text": text,
                    "created_at": timestamp,
                    "char_count": len(text),
                    "word_count": len(text.split()) if text else 0,
                    "mentions": mentions,
                    "hashtags": hashtags,
                    "links": links,
                    "mention_count": len(mentions),
                    "hashtag_count": len(hashtags),
                    "link_count": len(links),
                    "has_image": has_image,
                    "has_external": has_external,
                    "is_reply": is_reply,
                    "hour": timestamp.hour if timestamp else None,
                    "day_of_week": timestamp.weekday() if timestamp else None,
                    "date": timestamp.date() if timestamp else None
                }
                
                parsed_posts.append(parsed_post)
                
            except Exception as e:
                print(f"⚠️  Error parsing post: {e}")
                continue
        
        df = pd.DataFrame(parsed_posts)
        print(f"✅ Parsed {len(df)} posts into DataFrame")
        return df
    
    def analyze_posts(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Perform comprehensive analysis of posts
        """
        print("🔬 Analyzing posts...")
        
        analysis = {}
        
        # Basic stats
        analysis["total_posts"] = len(df)
        analysis["date_range"] = {
            "earliest": df["created_at"].min().strftime("%Y-%m-%d") if not df.empty else None,
            "latest": df["created_at"].max().strftime("%Y-%m-%d") if not df.empty else None
        }
        
        # Content analysis
        analysis["content"] = {
            "avg_char_count": df["char_count"].mean(),
            "avg_word_count": df["word_count"].mean(),
            "longest_post": df.loc[df["char_count"].idxmax()]["text"] if not df.empty else "",
            "longest_post_chars": df["char_count"].max(),
            "reply_percentage": (df["is_reply"].sum() / len(df) * 100) if not df.empty else 0,
            "posts_with_images": df["has_image"].sum(),
            "posts_with_links": df["has_external"].sum()
        }
        
        # Hashtag analysis
        all_hashtags = [tag for tags in df["hashtags"] for tag in tags]
        analysis["hashtags"] = {
            "total_used": len(all_hashtags),
            "unique_hashtags": len(set(all_hashtags)),
            "most_common": Counter(all_hashtags).most_common(10)
        }
        
        # Posting patterns
        if not df.empty and df["created_at"].notna().any():
            # Hourly distribution
            hourly_counts = df.groupby("hour").size()
            analysis["posting_patterns"] = {
                "busiest_hour": hourly_counts.idxmax(),
                "busiest_hour_count": hourly_counts.max(),
                "posts_by_hour": hourly_counts.to_dict()
            }
            
            # Daily distribution
            day_names = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
            daily_counts = df.groupby("day_of_week").size()
            analysis["posting_patterns"]["posts_by_day"] = {
                day_names[day]: count for day, count in daily_counts.items()
            }
            
            # Monthly activity (suppress timezone warning)
            monthly_counts = df.groupby(df["created_at"].dt.tz_localize(None).dt.to_period("M")).size()
            # Convert Period objects to strings for JSON serialization
            monthly_activity = {str(period): count for period, count in monthly_counts.items()}
            analysis["posting_patterns"]["monthly_activity"] = monthly_activity
        
        return analysis
    
    def create_visualizations(self, df: pd.DataFrame, save_dir: str = "bluesky_analysis"):
        """
        Create visualization charts
        """
        print("📊 Creating visualizations...")
        
        # Create directory for plots
        os.makedirs(save_dir, exist_ok=True)
        
        # Set style
        plt.style.use('default')
        sns.set_palette("husl")
        
        # 1. Posting frequency over time
        if not df.empty and df["created_at"].notna().any():
            plt.figure(figsize=(12, 6))
            df.set_index("created_at").resample("D").size().plot(kind="line")
            plt.title("Daily Posting Frequency")
            plt.xlabel("Date")
            plt.ylabel("Number of Posts")
            plt.xticks(rotation=45)
            plt.tight_layout()
            plt.savefig(f"{save_dir}/posting_frequency.png", dpi=300, bbox_inches="tight")
            plt.close()
            
            # 2. Hourly posting pattern
            plt.figure(figsize=(10, 6))
            hourly_data = df.groupby("hour").size()
            hourly_data.plot(kind="bar")
            plt.title("Posts by Hour of Day")
            plt.xlabel("Hour")
            plt.ylabel("Number of Posts")
            plt.xticks(rotation=0)
            plt.tight_layout()
            plt.savefig(f"{save_dir}/hourly_pattern.png", dpi=300, bbox_inches="tight")
            plt.close()
            
            # 3. Day of week pattern
            plt.figure(figsize=(10, 6))
            day_names = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
            daily_data = df.groupby("day_of_week").size()
            daily_data.index = [day_names[i] for i in daily_data.index]
            daily_data.plot(kind="bar")
            plt.title("Posts by Day of Week")
            plt.xlabel("Day")
            plt.ylabel("Number of Posts")
            plt.xticks(rotation=45)
            plt.tight_layout()
            plt.savefig(f"{save_dir}/daily_pattern.png", dpi=300, bbox_inches="tight")
            plt.close()
        
        # 4. Character count distribution
        plt.figure(figsize=(10, 6))
        df["char_count"].hist(bins=30, alpha=0.7)
        plt.axvline(df["char_count"].mean(), color="red", linestyle="--", label=f"Mean: {df['char_count'].mean():.1f}")
        plt.title("Distribution of Post Character Counts")
        plt.xlabel("Character Count")
        plt.ylabel("Frequency")
        plt.legend()
        plt.tight_layout()
        plt.savefig(f"{save_dir}/char_count_distribution.png", dpi=300, bbox_inches="tight")
        plt.close()
        
        print(f"✅ Visualizations saved to {save_dir}/")
    
    def save_results(self, df: pd.DataFrame, analysis: Dict, filename: str = "bluesky_analysis"):
        """
        Save results to files
        """
        print("💾 Saving results...")
        
        # Save raw data
        df.to_csv(f"{filename}_posts.csv", index=False)
        
        # Save analysis results
        with open(f"{filename}_analysis.json", "w") as f:
            # Convert any non-serializable objects
            serializable_analysis = json.loads(json.dumps(analysis, default=str))
            json.dump(serializable_analysis, f, indent=2)
        
        print(f"✅ Results saved:")
        print(f"   - Posts data: {filename}_posts.csv")
        print(f"   - Analysis: {filename}_analysis.json")
    
    def print_summary(self, analysis: Dict):
        """
        Print a nice summary of the analysis
        """
        print("\n" + "="*60)
        print("📊 BLUESKY ANALYSIS SUMMARY")
        print("="*60)
        
        print(f"\n📈 BASIC STATS:")
        print(f"   Total posts: {analysis['total_posts']:,}")
        print(f"   Date range: {analysis['date_range']['earliest']} to {analysis['date_range']['latest']}")
        
        content = analysis["content"]
        print(f"\n📝 CONTENT ANALYSIS:")
        print(f"   Average characters per post: {content['avg_char_count']:.1f}")
        print(f"   Average words per post: {content['avg_word_count']:.1f}")
        print(f"   Longest post: {content['longest_post_chars']} characters")
        print(f"   Reply percentage: {content['reply_percentage']:.1f}%")
        print(f"   Posts with images: {content['posts_with_images']}")
        print(f"   Posts with links: {content['posts_with_links']}")
        
        hashtags = analysis["hashtags"]
        print(f"\n🏷️  HASHTAG USAGE:")
        print(f"   Total hashtags used: {hashtags['total_used']}")
        print(f"   Unique hashtags: {hashtags['unique_hashtags']}")
        if hashtags["most_common"]:
            print(f"   Top hashtags:")
            for tag, count in hashtags["most_common"][:5]:
                print(f"      #{tag}: {count} times")
        
        if "posting_patterns" in analysis:
            patterns = analysis["posting_patterns"]
            print(f"\n⏰ POSTING PATTERNS:")
            print(f"   Most active hour: {patterns['busiest_hour']}:00 ({patterns['busiest_hour_count']} posts)")
            
            if "posts_by_day" in patterns:
                busiest_day = max(patterns["posts_by_day"].items(), key=lambda x: x[1])
                print(f"   Most active day: {busiest_day[0]} ({busiest_day[1]} posts)")
        
        print("\n" + "="*60)


def main():
    """
    Main function to run the analysis
    """
    print("🦋 Bluesky Post Analyzer")
    print("="*40)
    
    # Initialize analyzer
    analyzer = BlueskyAnalyzer()
    
    # Get credentials
    handle = input("Enter your Bluesky handle (e.g., username.bsky.social): ").strip()
    password = getpass.getpass("Enter your password: ").strip()
    
    # Authenticate
    if not analyzer.authenticate(handle, password):
        print("❌ Failed to authenticate. Please check your credentials.")
        return
    
    # Ask for post limit
    limit_input = input("Enter max number of posts to fetch (or press Enter for all): ").strip()
    limit = int(limit_input) if limit_input.isdigit() else None
    
    try:
        # Fetch posts
        raw_posts = analyzer.fetch_posts(limit=limit)
        
        if not raw_posts:
            print("❌ No posts found.")
            return
        
        # Parse posts
        df = analyzer.parse_posts(raw_posts)
        
        # Analyze
        analysis = analyzer.analyze_posts(df)
        
        # Create visualizations
        analyzer.create_visualizations(df)
        
        # Save results
        analyzer.save_results(df, analysis)
        
        # Print summary
        analyzer.print_summary(analysis)
        
        print("\n✅ Analysis complete! Check the generated files and visualizations.")
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Analysis interrupted by user.")
    except Exception as e:
        print(f"\n❌ An error occurred: {e}")


if __name__ == "__main__":
    main()
