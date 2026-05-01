"""
Base adapter class that all platform adapters inherit from.
"""

from abc import ABC, abstractmethod
from typing import Any


class BaseAdapter(ABC):
    """Abstract base class for platform adapters."""

    @abstractmethod
    def render(self, message: str, **kwargs) -> str:
        """Convert processed message to platform-specific format."""
        pass

    @abstractmethod
    def escape(self, text: str) -> str:
        """Escape special characters for this platform."""
        pass

    def truncate(self, message: str, max_length: int) -> str:
        """
        Truncate message safely without breaking formatting.
        Default: simple truncation with ellipsis.
        Override per platform for smart breaks.
        """
        if len(message) <= max_length:
            return message
        return message[: max_length - 3] + "..."

    def _safe_split(self, text: str, max_len: int) -> str:
        """Split at word boundary to avoid breaking mid-word."""
        if len(text) <= max_len:
            return text
        # Find last space before limit
        split_at = text[:max_len].rfind(" ")
        if split_at == -1:
            split_at = max_len
        return text[:split_at].rstrip()
