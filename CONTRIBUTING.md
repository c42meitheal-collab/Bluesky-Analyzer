# Contributing to Bluesky Post Analyzer

Thank you for your interest in contributing to the Bluesky Post Analyzer! This document provides guidelines and information for contributors.

## 🤝 Ways to Contribute

- **🐛 Bug Reports** - Report issues you encounter
- **✨ Feature Requests** - Suggest new functionality
- **📝 Documentation** - Improve guides and examples
- **🔧 Code Contributions** - Submit bug fixes or new features
- **🧪 Testing** - Help test new releases and features

## 🚀 Getting Started

### Development Setup

1. **Fork and clone the repository:**
```bash
git clone https://github.com/yourusername/bluesky-analyzer.git
cd bluesky-analyzer
```

2. **Create a virtual environment:**
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt  # If available
```

4. **Test the installation:**
```bash
python src/bluesky_analyzer_debug.py
```

### Project Structure

```
bluesky-analyzer/
├── src/
│   ├── bluesky_analyzer.py      # Main analyzer class
│   ├── bluesky_analyzer_debug.py # Debug/troubleshooting tool
│   └── __init__.py
├── examples/
│   └── example_usage.py         # Usage examples
├── docs/                        # Additional documentation
├── tests/                       # Test files (future)
├── requirements.txt             # Dependencies
├── setup.py                     # Package setup
└── README.md
```

## 📋 Contribution Guidelines

### Code Style

- **Python Style:** Follow PEP 8 guidelines
- **Docstrings:** Use clear, descriptive docstrings for all functions
- **Type Hints:** Include type hints where appropriate
- **Comments:** Comment complex logic and API interactions

### Example Code Style:

```python
def fetch_posts(self, limit: Optional[int] = None) -> List[Dict[str, Any]]:
    """
    Fetch posts from the authenticated user's timeline.
    
    Args:
        limit: Maximum number of posts to fetch. If None, fetches all posts.
        
    Returns:
        List of post dictionaries containing metadata and content.
        
    Raises:
        Exception: If not authenticated or API request fails.
    """
```

### Commit Messages

Use clear, descriptive commit messages:

- **feat:** Add new feature
- **fix:** Bug fix
- **docs:** Documentation changes
- **style:** Code style changes
- **refactor:** Code refactoring
- **test:** Add or update tests
- **chore:** Maintenance tasks

**Examples:**
```
feat: add sentiment analysis to post content
fix: handle empty response from AT Protocol API
docs: update authentication troubleshooting guide
```

## 🐛 Bug Reports

When reporting bugs, please include:

1. **Clear description** of the issue
2. **Steps to reproduce** the problem
3. **Expected vs actual behavior**
4. **Environment details:**
   - Python version
   - Operating system
   - Package versions
5. **Error messages** or logs
6. **Sample data** (if applicable and non-sensitive)

### Bug Report Template:

```markdown
**Description:**
Brief description of the issue

**Steps to Reproduce:**
1. Step one
2. Step two
3. Step three

**Expected Behavior:**
What should happen

**Actual Behavior:**
What actually happens

**Environment:**
- Python version: 3.x.x
- OS: Windows/macOS/Linux
- Package version: x.x.x

**Error Messages:**
```
Paste any error messages here
```

**Additional Context:**
Any other relevant information
```

## ✨ Feature Requests

For new features, please:

1. **Check existing issues** to avoid duplicates
2. **Describe the use case** and problem being solved
3. **Provide examples** of how the feature would work
4. **Consider implementation complexity**
5. **Suggest API design** if applicable

## 🔧 Code Contributions

### Before You Start

1. **Check existing issues** for similar work
2. **Open an issue** to discuss major changes
3. **Fork the repository** and create a feature branch
4. **Keep changes focused** - one feature per PR

### Pull Request Process

1. **Create a feature branch:**
```bash
git checkout -b feature/your-feature-name
```

2. **Make your changes** following the style guidelines

3. **Test your changes:**
```bash
python src/bluesky_analyzer_debug.py  # Basic functionality test
python src/bluesky_analyzer.py        # Full test with small dataset
```

4. **Update documentation** if needed

5. **Commit and push:**
```bash
git add .
git commit -m "feat: add your feature description"
git push origin feature/your-feature-name
```

6. **Open a Pull Request** with:
   - Clear title and description
   - Link to related issues
   - Screenshots/examples if applicable
   - Checklist of changes made

### Pull Request Checklist

- [ ] Code follows project style guidelines
- [ ] Changes are well documented
- [ ] No breaking changes (or clearly marked)
- [ ] Tests pass (when available)
- [ ] Documentation updated if needed
- [ ] Commit messages are clear and descriptive

## 🧪 Testing

Currently, testing is manual. Future improvements:

- **Unit tests** for core functions
- **Integration tests** for API interactions
- **Automated testing** with GitHub Actions

## 📚 Documentation

Help improve documentation:

- **Fix typos** and unclear explanations
- **Add examples** for complex features
- **Update screenshots** and outputs
- **Translate** to other languages
- **Create tutorials** for common use cases

## 🔒 Security

If you discover security vulnerabilities:

1. **Don't open public issues** for security problems
2. **Contact maintainers directly** via email
3. **Provide detailed information** about the vulnerability
4. **Allow time for fixes** before public disclosure

## 💡 Ideas for Contributions

Some areas where contributions would be valuable:

### New Features
- **Sentiment analysis** of post content
- **Network analysis** of mentions and replies
- **Advanced filtering** options
- **Interactive web dashboard**
- **Export to additional formats** (PDF reports, Excel)
- **Scheduled analysis** and monitoring

### Improvements
- **Performance optimization** for large datasets
- **Better error handling** and user feedback
- **More visualization types**
- **Configuration file support**
- **Caching** for repeated analysis

### Documentation
- **Video tutorials**
- **Use case examples**
- **API reference**
- **Troubleshooting guides**

## 🏆 Recognition

Contributors will be recognized in:

- **README.md** acknowledgments section
- **CHANGELOG.md** for each release
- **GitHub contributors** page

## ❓ Questions?

- **Open an issue** for general questions
- **Check existing documentation** first
- **Join discussions** for feature ideas
- **Contact maintainers** for other inquiries

## 📜 Code of Conduct

This project follows a simple code of conduct:

- **Be respectful** and inclusive
- **Help others learn** and grow
- **Focus on constructive feedback**
- **Assume good intentions**
- **Keep discussions professional**

---

Thank you for contributing to the Bluesky Post Analyzer! Your efforts help make social media analysis more accessible to everyone. 🚀✨
