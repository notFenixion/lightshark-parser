"""
Custom exception classes for the LightShark Parser.
"""


class MarkerNotFoundError(ValueError):
    """Raised when a required marker/header is not found in the file."""

    pass
