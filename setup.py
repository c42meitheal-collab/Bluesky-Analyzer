#!/usr/bin/env python3
"""
Setup script for Bluesky Analyzer
"""

from setuptools import setup, find_packages
import os

# Read README file
def read_readme():
    with open("README.md", "r", encoding="utf-8") as fh:
        return fh.read()

# Read requirements
def read_requirements():
    with open("requirements.txt", "r", encoding="utf-8") as fh:
        return [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="bluesky-analyzer",
    version="1.0.0",
    author="Bluesky Analyzer Contributors",
    author_email="contributors@example.com",
    description="A comprehensive tool to analyze your Bluesky posts using the AT Protocol API",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/bluesky-analyzer",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Communications :: Chat",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content :: Message Boards",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Topic :: Scientific/Engineering :: Visualization",
        "Topic :: Sociology",
    ],
    python_requires=">=3.7",
    install_requires=read_requirements(),
    entry_points={
        "console_scripts": [
            "bluesky-analyzer=bluesky_analyzer:main",
        ],
    },
    keywords=[
        "bluesky", "social media", "analysis", "visualization", "at protocol",
        "data analysis", "social network", "posting patterns", "content analysis"
    ],
    project_urls={
        "Bug Reports": "https://github.com/yourusername/bluesky-analyzer/issues",
        "Source": "https://github.com/yourusername/bluesky-analyzer",
        "Documentation": "https://github.com/yourusername/bluesky-analyzer#readme",
        "Changelog": "https://github.com/yourusername/bluesky-analyzer/blob/main/CHANGELOG.md",
    },
    include_package_data=True,
    zip_safe=False,
)
