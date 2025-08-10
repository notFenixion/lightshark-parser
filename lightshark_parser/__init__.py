"""
LightShark Parser - A Python library for parsing LightShark show files.
"""

__version__ = "1.0.0"

from lightshark_parser.classes import Lightshow
from lightshark_parser.parsers.file_parser import parse_file_bytes, parse_lshw
from lightshark_parser.parsers.parse_dict import parse_dict_to_lightshow
from lightshark_parser.utils.logger import logger


__all__ = ["parse_file_bytes", "parse_lshw", "parse_dict_to_lightshow", "Lightshow", "logger"]
