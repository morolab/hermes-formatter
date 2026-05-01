"""URL detection and processing rules."""

import re


def extract_urls(text: str) -> list:
    """Extract all URLs from text."""
    url_pattern = r'https?://[^\s<>]+'
    return re.findall(url_pattern, text)


def is_url(text: str) -> bool:
    """Check if text looks like a URL."""
    return bool(re.match(r'https?://', text))
