"""
Setup script for packaging ImageSequenceScanner.
"""

from setuptools import setup, find_packages
import io

# Read README with explicit UTF-8 encoding
with io.open("README.md", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="image_sequence_scanner",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "PySide6>=6.4.0",
    ],
    entry_points={
        "console_scripts": [
            "image-sequence-scanner=image_sequence_scanner.gui:run_app",
        ],
    },
    author="Your Name",
    author_email="your.email@example.com",
    description="A tool for visualizing and sanity-checking 3D render image sequences",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/ImageSequenceScanner",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Topic :: Multimedia :: Graphics",
    ],
    python_requires=">=3.9",
) 