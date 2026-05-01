"""Rules package – preprocessing transforms applied to all messages."""

from .url import extract_urls, is_url
from .emphasis import normalize_bold, strip_emphasis
from .code import extract_code_blocks, extract_inline_code, protect_code, restore_code
from .emoji import normalize_emoji, has_emoji, EMOJI_MAP

import re


def apply_all_rules(text: str, platform: str) -> str:
    """
    Apply all preprocessing rules in order.

    Args:
        text: Raw message
        platform: Target platform (some rules platform-dependent)

    Returns:
        Processed text ready for adapter
    """
    text = normalize_emoji(text)
    text = normalize_urls(text)
    text = detect_code_blocks(text)
    text = process_emphasis(text)
    return text


def normalize_urls(text: str) -> str:
    """Detect and prepare URLs for platform-specific formatting."""
    return text


def detect_code_blocks(text: str) -> str:
    """Normalize code fence styles."""
    return text


def process_emphasis(text: str) -> str:
    """Ensure emphasis markers are well-formed."""
    return text


__all__ = [
    "extract_urls",
    "is_url",
    "normalize_bold",
    "strip_emphasis",
    "extract_code_blocks",
    "extract_inline_code",
    "protect_code",
    "restore_code",
    "normalize_emoji",
    "has_emoji",
    "EMOJI_MAP",
    "apply_all_rules",
    "normalize_urls",
    "detect_code_blocks",
    "process_emphasis",
]
