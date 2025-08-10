"""
Logger utility for lightshark_parser library.

This module provides a centralized logger that can be imported and used
throughout the lightshark_parser codebase. It automatically uses the
named 'lightshark_parser' logger.
"""

import logging

# Create the named logger for the library
logger = logging.getLogger('lightshark_parser')

# Export logging functions for easy use throughout the codebase
debug = logger.debug
info = logger.info
warning = logger.warning
error = logger.error
critical = logger.critical

# Also export the logger itself for advanced usage
__all__ = ['logger', 'debug', 'info', 'warning', 'error', 'critical']
