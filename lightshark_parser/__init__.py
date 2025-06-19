"""
LightShark Parser - A Python library for parsing LightShark show files.
"""

__version__ = "1.0.0"

# Import the main parsing function to make it available at the package level
from .main import parse_file_bytes, Lightshow

__all__ = ["parse_file_bytes", "Lightshow"]
