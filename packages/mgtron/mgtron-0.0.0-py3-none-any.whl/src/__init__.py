"""Global variables and functions for the package."""

from .globals.helpers import version_getter

__version__ = version_getter()

__all__ = ["__version__"]
