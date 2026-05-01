# -*- coding: utf-8 -*-
"""
Hermes Universal Formatter
Converts plain text agent output into platform-specific formatted messages.
"""

from .formatter import format, HermesFormatter, auto_format
from .adapters import get_adapter

__version__ = "0.1.0"
__author__ = "Hermes Agent"
__all__ = ["format", "HermesFormatter", "auto_format", "get_adapter"]
