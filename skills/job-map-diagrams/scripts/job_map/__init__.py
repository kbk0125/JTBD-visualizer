"""Core validation, measurement, layout, and Eraser generation for job maps."""

from .eraser import build_diagram
from .model import JobMapSpec
from .validation import validate_spec

__all__ = ["JobMapSpec", "build_diagram", "validate_spec"]
