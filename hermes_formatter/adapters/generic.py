"""
Generic plain-text adapter (fallback).
No formatting, minimal processing.
"""

from .base import BaseAdapter


class GenericAdapter(BaseAdapter):
    """Plain text formatter — no special formatting applied."""

    MAX_LENGTH = None

    def escape(self, text: str) -> str:
        """No escaping for plain text."""
        return text

    def render(self, message: str, **kwargs) -> str:
        """
        Return message as clean plain text.
        Optionally strip markdown hints if requested.
        """
        strip_markdown = kwargs.get("strip_markdown", False)

        if strip_markdown:
            # Remove **bold**, *italic*, `code`, ~~strikethrough~~
            message = re.sub(r'\*\*(.+?)\*\*', r'\1', message)
            message = re.sub(r'\*(.+?)\*', r'\1', message)
            message = re.sub(r'~~(.+?)~~', r'\1', message)
            message = re.sub(r'`(.+?)`', r'\1', message)
            message = re.sub(r'```.*?\n(.*?)```', r'\1', message, flags=re.DOTALL)

        return message
