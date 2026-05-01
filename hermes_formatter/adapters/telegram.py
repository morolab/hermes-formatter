"""
Telegram MarkdownV2 formatter.
Converts simple markdown-like agent output to Telegram MarkdownV2.
"""

import re
from .base import BaseAdapter


class TelegramAdapter(BaseAdapter):
    """Adapter for Telegram Bot API (MarkdownV2 formatting)."""

    MAX_LENGTH = 4096

    ESCAPE_CHARS = r'_*[]()~>#+-=|{}.!'

    def escape(self, text: str) -> str:
        """Escape MarkdownV2 special characters for regular text."""
        for char in self.ESCAPE_CHARS:
            text = text.replace(char, f'\\{char}')
        return text

    def escape_url(self, url: str) -> str:
        """Escape only characters that would break link syntax."""
        # Escape backslash and parentheses/brackets that appear in URL
        url = url.replace('\\', '\\\\')
        url = url.replace('(', '\\(')
        url = url.replace(')', '\\)')
        url = url.replace('[', '\\[')
        url = url.replace(']', '\\]')
        return url

    def render(self, message: str, **kwargs) -> str:
        protected = {}
        idx = [0]

        def ph(kind, data):
            key = f"HERMES{kind.upper()}{idx[0]}"
            idx[0] += 1
            protected[key] = (kind, data)
            return key

        # 1. Protect code blocks
        def protect_code_block(m):
            code = m.group(2).strip()
            return ph("CODE", code)

        message = re.sub(r'```(\w*)\n(.*?)```', protect_code_block, message, flags=re.DOTALL)

        # 2. Protect inline code
        def protect_inline(m):
            code = m.group(1)
            return ph("INLINE", code)

        message = re.sub(r'`([^`]+)`', protect_inline, message)

        # 3. Protect markdown patterns
        def protect_bold(m):
            return ph("BOLD", m.group(1))

        def protect_italic(m):
            return ph("ITALIC", m.group(1))

        def protect_strike(m):
            return ph("STRIKE", m.group(1))

        message = re.sub(r'\*\*(.+?)\*\*', protect_bold, message)
        message = re.sub(r'\*(?!\*)(.+?)\*', protect_italic, message)
        message = re.sub(r'~~(.+?)~~', protect_strike, message)

        # 4. Protect explicit links [text](url)
        def protect_link(m):
            return ph("LINK", (m.group(1), m.group(2)))

        message = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', protect_link, message)

        # 5. Protect bare URLs
        url_pattern = r'(https?://[^\s<>]+)'
        urls = re.findall(url_pattern, message)
        for i, url in enumerate(urls):
            key = f"HERMESURL{i}"
            protected[key] = ("URL", url)
            message = message.replace(url, key, 1)

        # 6. Escape everything else
        message = self.escape(message)

        # 7. Restore protected elements
        for key, (kind, data) in protected.items():
            if kind == "CODE":
                replacement = f"`{data}`"
            elif kind == "INLINE":
                replacement = f"`{data}`"
            elif kind == "BOLD":
                content = self.escape(data)
                replacement = f"**{content}**"
            elif kind == "ITALIC":
                content = self.escape(data)
                replacement = f"_{content}_"
            elif kind == "STRIKE":
                content = self.escape(data)
                replacement = f"~{content}~"
            elif kind == "LINK":
                text, url = data
                text_esc = self.escape(text)
                url_esc = self.escape_url(url)
                replacement = f"[{text_esc}]({url_esc})"
            elif kind == "URL":
                url = data
                domain = re.sub(r'https?://', '', url).split('/')[0][:25]
                domain_esc = self.escape(domain)
                url_esc = self.escape_url(url)
                replacement = f"[{domain_esc}]({url_esc})"
            else:
                replacement = str(data)

            message = message.replace(key, replacement)

        # 8. Truncate
        if len(message) > self.MAX_LENGTH:
            message = self.truncate(message, self.MAX_LENGTH)

        return message

    def truncate(self, message: str, max_length: int) -> str:
        if len(message) <= max_length:
            return message

        cut_at = message[:max_length - 3].rfind('\n')
        if cut_at == -1:
            cut_at = message[:max_length - 3].rfind(' ')
        if cut_at == -1:
            cut_at = max_length - 3

        truncated = message[:cut_at].rstrip() + "..."

        if truncated.count('**') % 2 == 1:
            truncated += '**'
        if truncated.count('`') % 2 == 1:
            truncated += '`'
        if truncated.count('_') % 2 == 1:
            truncated += '_'
        if truncated.count('~') % 2 == 1:
            truncated += '~'

        return truncated
