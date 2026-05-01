"""Emphasis formatting rules (bold, italic, strikethrough)."""

import re


def normalize_bold(text: str) -> str:
    """Ensure **bold** markers are properly paired."""
    # Count asterisks
    stars = text.count('*')
    # If odd number, might be unclosed
    if stars % 2 == 1:
        # Heuristic: add closing star at end of last paragraph
        pass  # left to adapter-specific handling
    return text


def strip_emphasis(text: str) -> str:
    """Remove all emphasis markers, keep content."""
    text = re.sub(r'\*\*(.+?)\*\*', r'\1', text)
    text = re.sub(r'\*(.+?)\*', r'\1', text)
    text = re.sub(r'~~(.+?)~~', r'\1', text)
    return text
