"""
Utility functions used across the formatter.
"""

import textwrap


def truncate_smart(text: str, max_length: int, break_chars: str = "\n. ") -> -> str:
    """
    Truncate text at a safe boundary.
    Prefers breaking at break characters (newline, period, space).
    """
    if len(text) <= max_length:
        return text

    # Look for last break character within limit
    slice_point = text[:max_length]
    for char in break_chars:
        pos = slice_point.rfind(char)
        if pos > 0:
            return text[:pos].rstrip()

    # Hard break if no good break point
    return text[:max_length].rstrip()


def escape_html(text: str) -> str:
    """Escape HTML special characters."""
    text = text.replace('&', '&amp;')
    text = text.replace('<', '&lt;')
    text = text.replace('>', '&gt;')
    text = text.replace('"', '&quot;')
    return text


def wrap_text(text: str, width: int = 80) -> str:
    """Wrap text to specified width."""
    return textwrap.fill(text, width=width, break_long_words=False, replace_whitespace=False)


def split_paragraphs(text: str) -> list[str]:
    """Split text into paragraphs (blank line separated)."""
    raw_paragraphs = text.split('\n\n')
    return [p.strip() for p in raw_paragraphs if p.strip()]
