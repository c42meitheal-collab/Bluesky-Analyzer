# Bluesky Post Analyzer 🦋

[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![GitHub issues](https://img.shields.io/github/issues/yourusername/bluesky-analyzer)](https://github.com/yourusername/bluesky-analyzer/issues)

A comprehensive Python tool to fetch, analyze, and visualize your Bluesky posts using the AT Protocol API. Discover fascinating insights about your posting patterns, content style, and social engagement!

## ✨ Features

- **🔐 Secure Authentication** - Uses Bluesky App Passwords for secure API access
- **📊 Rich Analytics** - Comprehensive analysis of posting patterns, content metrics, and engagement
- **📈 Beautiful Visualizations** - Generate charts showing your activity over time
- **💾 Multiple Export Formats** - CSV, JSON, and PNG outputs for further analysis
- **🔍 Debug Mode** - Troubleshooting tools for authentication issues
- **⚡ Efficient** - Handles rate limiting and large datasets gracefully

## 🎯 What You'll Discover

Real example from a user analysis:

```
📊 BLUESKY ANALYSIS SUMMARY
════════════════════════════════════════════════════════════
📈 BASIC STATS:
   Total posts: 150
   Date range: 2025-08-15 to 2025-08-22

📝 CONTENT ANALYSIS:
   Average characters per post: 127.3
   Average words per post: 21.8
   Reply percentage: 73.0%
   Posts with images: 12
   Posts with links: 8

⏰ POSTING PATTERNS:
   Most active hour: 15:00 (22 posts)
   Most active day: Tuesday (48 posts)
```

## 🚀 Quick Start

### Installation

1. **Clone the repository:**
```bash
git clone https://github.com/yourusername/bluesky-analyzer.git
cd bluesky-analyzer
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

### Authentication Setup

**Important:** You need a Bluesky App Password (not your main password):

1. Go to [bsky.app](https://bsky.app) → **Settings** → **Privacy and Security** → **App Passwords**
2. Click **"Add App Password"** and name it "Post Analyzer"
3. **Save the generated password** - you'll use this with the analyzer

### Basic Usage

```bash
python src/bluesky_analyzer.py
```

Follow the prompts:
- **Handle:** `your-handle.bsky.social`
- **Password:** Your App Password (not main password)
- **Post limit:** Enter a number or leave blank for all posts

## 📊 Analysis Output

### Generated Files

- **`bluesky_analysis_posts.csv`** - Complete dataset of your posts
- **`bluesky_analysis_analysis.json`** - Structured analysis results
- **`bluesky_analysis/`** folder with visualizations:
  - `posting_frequency.png` - Daily posting activity over time
  - `hourly_pattern.png` - Your most active hours
  - `daily_pattern.png` - Which days you post most
  - `char_count_distribution.png` - Post length patterns

### Metrics Analyzed

**Content Analysis:**
- Post frequency and timing patterns
- Character and word count statistics
- Reply vs. original post ratios
- Media usage (images, links)
- Hashtag analysis and trends

**Behavioral Insights:**
- Most active hours and days
- Posting consistency over time
- Conversation engagement levels
- Content style patterns

## 🛠️ Advanced Usage

### Programmatic API

```python
from src.bluesky_analyzer import BlueskyAnalyzer

# Initialize and authenticate
analyzer = BlueskyAnalyzer()
analyzer.authenticate("your-handle.bsky.social", "your-app-password")

# Fetch and analyze posts
posts = analyzer.fetch_posts(limit=100)
df = analyzer.parse_posts(posts)
analysis = analyzer.analyze_posts(df)

# Generate visualizations
analyzer.create_visualizations(df)
analyzer.print_summary(analysis)
```

### Debug Mode

If you're having authentication issues:

```bash
python src/bluesky_analyzer_debug.py
```

This will test different authentication methods and provide detailed troubleshooting.

## 🔧 Troubleshooting

### Common Issues

| Issue | Solution |
|-------|----------|
| **401 Unauthorized** | Use App Password instead of main password |
| **Handle not found** | Try email address or remove @ symbol |
| **Network errors** | Check internet connection and try again |

For detailed troubleshooting, see [AUTHENTICATION_TROUBLESHOOTING.md](AUTHENTICATION_TROUBLESHOOTING.md).

## 📈 Example Insights

The analyzer reveals fascinating patterns:

- **Conversation Enthusiasts:** Users with high reply percentages (70%+)
- **Time Patterns:** Peak activity hours (evenings are popular!)
- **Day Preferences:** Some users heavily favor specific weekdays
- **Content Style:** Long-form vs. short-form posting preferences
- **Media Usage:** Image and link sharing habits

## 🤝 Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📋 Requirements

- Python 3.7+
- Dependencies: `requests`, `pandas`, `matplotlib`, `seaborn`
- Active Bluesky account with App Password

## 🔒 Privacy & Security

- **No credential storage** - Passwords are only used for authentication
- **Local processing** - All analysis happens on your machine
- **Respect rate limits** - Built-in delays to be API-friendly
- **Your data stays yours** - Nothing is uploaded or shared

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built using the [AT Protocol](https://atproto.com/) by Bluesky
- Inspired by the need for social media self-reflection tools
- Thanks to the Bluesky community for API documentation

## 🐛 Issues & Support

- **Bug reports:** [GitHub Issues](https://github.com/yourusername/bluesky-analyzer/issues)
- **Feature requests:** [GitHub Discussions](https://github.com/yourusername/bluesky-analyzer/discussions)
- **Documentation:** Check the [docs/](docs/) folder

---

**Made with ❤️ for the Bluesky community**

*Discover your digital personality through data! 📊✨*
