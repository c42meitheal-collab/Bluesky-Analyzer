#!/usr/bin/env python3
"""
Bluesky Post Fetcher and Analyzer - Debug Version
Enhanced with better authentication debugging
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

class BlueskyAnalyzerDebug:
    def __init__(self):
        self.base_url = "https://bsky.social"
        self.session = None
        self.access_jwt = None
        self.refresh_jwt = None
        self.did = None
        
    def clean_handle(self, handle: str) -> str:
        """Clean and normalize the handle"""
        # Remove invisible characters and whitespace
        handle = ''.join(char for char in handle if ord(char) < 127).strip()
        
        # Remove @ if present
        if handle.startswith('@'):
            handle = handle[1:]
        
        # Add .bsky.social if not present and doesn't contain a domain
        if '.' not in handle:
            handle = f"{handle}.bsky.social"
        elif not handle.endswith('.bsky.social') and '@' not in handle:
            # If it has a dot but not .bsky.social and not an email
            if not any(tld in handle for tld in ['.com', '.org', '.net', '.edu', '.gov']):
                handle = f"{handle}.bsky.social"
        
        return handle
        
    def test_authentication_methods(self, identifier: str, password: str) -> bool:
        """Test different authentication methods"""
        
        print("🔍 Testing authentication methods...")
        
        # Clean the identifier
        cleaned_handle = self.clean_handle(identifier)
        print(f"   Original input: '{identifier}'")
        print(f"   Cleaned handle: '{cleaned_handle}'")
        
        auth_url = f"{self.base_url}/xrpc/com.atproto.server.createSession"
        
        # Test methods in order of preference
        test_identifiers = [
            cleaned_handle,
            identifier.strip(),  # Original with just whitespace removed
            identifier.strip().lstrip('@'),  # Remove @ from original
        ]
        
        # If the cleaned handle doesn't look like an email, also try did: format
        if '@' not in cleaned_handle:
            test_identifiers.append(f"did:plc:{cleaned_handle}")
        
        for i, test_id in enumerate(test_identifiers, 1):
            print(f"\n   Method {i}: Testing with identifier '{test_id}'")
            
            auth_data = {
                "identifier": test_id,
                "password": password
            }
            
            try:
                response = requests.post(auth_url, json=auth_data)
                print(f"      Response status: {response.status_code}")
                
                if response.status_code == 200:
                    print("      ✅ Authentication successful!")
                    session_data = response.json()
                    self.access_jwt = session_data["accessJwt"]
                    self.refresh_jwt = session_data["refreshJwt"]
                    self.did = session_data["did"]
                    print(f"      DID: {self.did}")
                    return True
                elif response.status_code == 401:
                    print("      ❌ 401 Unauthorized - Invalid credentials")
                    try:
                        error_data = response.json()
                        if "message" in error_data:
                            print(f"      Error message: {error_data['message']}")
                    except:
                        pass
                else:
                    print(f"      ❌ Unexpected status code: {response.status_code}")
                    try:
                        error_data = response.json()
                        print(f"      Error: {error_data}")
                    except:
                        print(f"      Response text: {response.text}")
                        
            except requests.exceptions.RequestException as e:
                print(f"      ❌ Network error: {e}")
        
        return False
    
    def authenticate(self, handle: str, password: str) -> bool:
        """
        Enhanced authentication with debugging
        """
        print(f"\n🔐 Attempting to authenticate...")
        
        # First try the enhanced method
        if self.test_authentication_methods(handle, password):
            return True
        
        print("\n❌ All authentication methods failed.")
        print("\n🔧 Troubleshooting suggestions:")
        print("   1. Check if you need an App Password:")
        print("      - Go to Settings > Privacy and Security > App Passwords")
        print("      - Create a new app password for this tool")
        print("   2. Try using your email address instead of handle")
        print("   3. Make sure your handle doesn't have extra characters")
        print("   4. Verify your credentials by logging into bsky.app")
        
        return False
    
    def get_headers(self) -> Dict[str, str]:
        """Get headers with authentication"""
        return {
            "Authorization": f"Bearer {self.access_jwt}",
            "Content-Type": "application/json"
        }
    
    def test_api_access(self) -> bool:
        """Test if we can access the API with current auth"""
        if not self.access_jwt:
            print("❌ No access token available")
            return False
        
        print("🔍 Testing API access...")
        
        # Try to get profile info
        url = f"{self.base_url}/xrpc/com.atproto.repo.describeRepo"
        params = {"repo": self.did}
        
        try:
            response = requests.get(url, params=params, headers=self.get_headers())
            if response.status_code == 200:
                print("✅ API access confirmed")
                return True
            else:
                print(f"❌ API test failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ API test error: {e}")
            return False
    
    def fetch_posts_sample(self, limit: int = 5) -> List[Dict[str, Any]]:
        """
        Fetch a small sample of posts for testing
        """
        if not self.access_jwt:
            raise Exception("Not authenticated. Call authenticate() first.")
        
        print(f"🔄 Fetching {limit} sample posts...")
        
        url = f"{self.base_url}/xrpc/com.atproto.repo.listRecords"
        params = {
            "repo": self.did,
            "collection": "app.bsky.feed.post",
            "limit": limit
        }
        
        try:
            response = requests.get(url, params=params, headers=self.get_headers())
            response.raise_for_status()
            
            data = response.json()
            posts = data.get("records", [])
            
            print(f"✅ Successfully fetched {len(posts)} posts")
            return posts
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Error fetching posts: {e}")
            return []


def main():
    """
    Debug version of the main function
    """
    print("🦋 Bluesky Post Analyzer - Debug Mode")
    print("="*50)
    
    # Initialize the analyzer
    analyzer = BlueskyAnalyzerDebug()
    
    # Get credentials with better prompting
    print("\n📝 Enter your Bluesky credentials:")
    print("   💡 Tip: You might need an App Password instead of your main password")
    print("   💡 You can also try your email address instead of handle")
    
    handle = input("\nHandle or email: ").strip()
    password = getpass.getpass("Password (hidden): ").strip()
    
    # Authenticate
    if not analyzer.authenticate(handle, password):
        print("\n❌ Authentication failed. Please check the troubleshooting suggestions above.")
        return
    
    # Test API access
    if not analyzer.test_api_access():
        print("❌ API access test failed.")
        return
    
    # Try to fetch a few sample posts
    sample_posts = analyzer.fetch_posts_sample(5)
    
    if sample_posts:
        print(f"\n✅ Success! Found {len(sample_posts)} posts.")
        print("Sample post data:")
        for i, post in enumerate(sample_posts[:2], 1):
            text = post.get("value", {}).get("text", "")[:100]
            created = post.get("value", {}).get("createdAt", "")
            print(f"   {i}. {created}: {text}...")
        
        print("\n🎉 Authentication and API access working!")
        print("You can now run the full analyzer with: python src/bluesky_analyzer.py")
    else:
        print("❌ No posts found or error fetching posts.")


if __name__ == "__main__":
    main()
