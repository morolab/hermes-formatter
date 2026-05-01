"""Adapter package."""

from .base import BaseAdapter
from .telegram import TelegramAdapter
from .discord import DiscordAdapter
from .cli import CLIAdapter
from .slack import SlackAdapter
from .generic import GenericAdapter
from .email import EmailAdapter

__all__ = [
    "BaseAdapter",
    "TelegramAdapter",
    "DiscordAdapter",
    "CLIAdapter",
    "SlackAdapter",
    "GenericAdapter",
    "EmailAdapter",
]

# Registry of available adapters
_ADAPTER_REGISTRY = {
    "telegram": TelegramAdapter,
    "discord": DiscordAdapter,
    "cli": CLIAdapter,
    "slack": SlackAdapter,
    "generic": GenericAdapter,
    "email": EmailAdapter,
}


def get_adapter(platform: str, **kwargs):
    """
    Get adapter instance for platform.

    Args:
        platform: Name of platform
        **kwargs: Passed to adapter constructor

    Returns:
        Adapter instance
    """
    platform = platform.lower()
    if platform not in _ADAPTER_REGISTRY:
        raise ValueError(
            f"Unknown platform '{platform}'. "
            f"Available: {', '.join(_ADAPTER_REGISTRY.keys())}"
        )
    return _ADAPTER_REGISTRY[platform](**kwargs)
