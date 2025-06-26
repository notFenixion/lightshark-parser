"""
LightShark Parser - A Python library for parsing LightShark show files.
"""

__version__ = "1.0.0"

from lightshark_parser.main import parse_file_bytes
from lightshark_parser.classes import Lightshow

__all__ = ["parse_file_bytes", "Lightshow"]
