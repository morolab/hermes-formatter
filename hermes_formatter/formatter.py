"""
Universal formatter for Hermes agent messages.
Takes plain text and converts it to platform-specific formats.
"""

import re
from typing import Optional, Dict, Any
from .adapters import get_adapter
from .rules import apply_all_rules


class HermesFormatter:
    """Main formatter class that orchestrates platform-specific rendering."""

    def __init__(self, platform: str, **adapter_kwargs):
        """
        Initialize formatter for a specific platform.

        Args:
            platform: Target platform ('telegram', 'discord', 'cli', 'slack', 'email', 'generic')
            **adapter_kwargs: Additional options passed to the adapter
        """
        self.platform = platform.lower()
        self.adapter = get_adapter(self.platform, **adapter_kwargs)

    def format(self, message: str, **context: Any) -> str:
        """
        Format a message for the target platform.

        Args:
            message: Raw agent output text
            **context: Optional context (max_length, truncate, etc.)

        Returns:
            Formatted string ready to send
        """
        # Step 1: Apply universal rules (URL detection, emoji normalization, etc.)
        processed = apply_all_rules(message, self.platform)

        # Step 2: Platform-specific escaping/formatting
        formatted = self.adapter.render(processed, **context)

        # Step 3: Length truncation if needed
        max_len = context.get("max_length")
        if max_len and len(formatted) > max_len:
            formatted = self.adapter.truncate(formatted, max_len)

        return formatted

    def format_batch(self, messages: list, **context) -> list:
        """Format multiple messages efficiently."""
        return [self.format(msg, **context) for msg in messages]


def format(message: str, platform: str = "generic", **kwargs) -> str:
    """
    Quick one-liner formatter.

    Args:
        message: The agent output to format
        platform: Target platform name
        **kwargs: Adapter-specific options

    Returns:
        Formatted string

    Example:
        >>> format("**Success!**", platform="telegram")
        "*Success!*"
    """
    formatter = HermesFormatter(platform, **kwargs)
    return formatter.format(message, **kwargs)


def auto_format(message: str, context: Optional[Dict[str, Any]] = None) -> str:
    """
    Auto-detect platform from context and format accordingly.

    Context keys:
        - platform: explicit platform name
        - is_telegram: bool
        - is_discord: bool
        - is_slack: bool
        - is_cli: bool
        - max_length: int
    """
    if context is None:
        context = {}

    platform = context.pop("platform", None) or (
        "telegram" if context.get("is_telegram") else
        "discord" if context.get("is_discord") else
        "slack" if context.get("is_slack") else
        "cli" if context.get("is_cli") else
        "generic"
    )

    return format(message, platform=platform, **context)
