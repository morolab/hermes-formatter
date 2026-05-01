"""
Slack mrkdwn formatter.
Slack's mrkdwn has some differences from standard Markdown.
"""

import re
from .base import BaseAdapter


class SlackAdapter(BaseAdapter):
    """Adapter for Slack messages (mrkdwn format)."""

    MAX_LENGTH = 40000

    # Characters that need escaping in Slack: ` * _ ~ > | & <
    ESCAPE_CHARS = '`*_~>|&<'

    def escape(self, text: str) -> str:
        for char in self.ESCAPE_CHARS:
            text = text.replace(char, f'\\{char}')
        return text

    def escape_url(self, url: str) -> str:
        """Escape URL for Slack mrkdwn link."""
        # Slack uses <url> for auto-link; minimal escaping needed
        url = url.replace('\\', '\\\\')
        url = url.replace('|', '\\|')  # pipe separates url|text in Slack link
        return url

    def render(self, message: str, **kwargs) -> str:
        protected = {}
        idx = [0]

        def ph(kind, data):
            key = f"HF{kind.upper()}{idx[0]}"
            idx[0] += 1
            protected[key] = (kind, data)
            return key

        # 1. Code blocks
        def protect_code_block(m):
            lang = m.group(1)
            code = m.group(2).strip()
            return ph("CODEBLOCK", (lang, code))

        message = re.sub(r'```(\w*)\n(.*?)```', protect_code_block, message, flags=re.DOTALL)

        # 2. Inline code
        def protect_inline(m):
            return ph("INLINE", m.group(1))

        message = re.sub(r'`([^`]+)`', protect_inline, message)

        # 3. Markdown patterns
        def protect_bold(m):
            return ph("BOLD", m.group(1))

        def protect_italic(m):
            return ph("ITALIC", m.group(1))

        def protect_strike(m):
            return ph("STRIKE", m.group(1))

        message = re.sub(r'\*\*(.+?)\*\*', protect_bold, message)   # ** → bold
        message = re.sub(r'\*(?!\*)(.+?)\*', protect_italic, message)  # * → italic
        message = re.sub(r'~~(.+?)~~', protect_strike, message)

        # 4. Links [text](url) → Slack format <url|text>
        def protect_link(m):
            return ph("LINK", (m.group(1), m.group(2)))

        message = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', protect_link, message)

        # 5. Bare URLs
        url_pattern = r'(https?://[^\s<>]+)'
        urls = re.findall(url_pattern, message)
        for i, url in enumerate(urls):
            key = f"HFURL{i}"
            protected[key] = ("URL", url)
            message = message.replace(url, key, 1)

        # 6. Escape everything else
        message = self.escape(message)

        # 7. Restore
        for key, (kind, data) in protected.items():
            if kind == "CODEBLOCK":
                lang, code = data
                replacement = f"```{lang}\n{code}```" if lang else f"```{code}```"
            elif kind == "INLINE":
                replacement = f"`{data}`"
            elif kind == "BOLD":
                replacement = f"*{self.escape(data)}*"
            elif kind == "ITALIC":
                replacement = f"_{self.escape(data)}_"
            elif kind == "STRIKE":
                replacement = f"~{self.escape(data)}~"
            elif kind == "LINK":
                text, url = data
                url_esc = self.escape_url(url)
                # Slack link format: <url|text> or just <url>
                # Avoid escaping text? text should be escaped already at step 6? Wait we escaped globally before restoring pattern.
                # Our text is raw; we need to escape it now because it was inside escaped string? Actually we escaped entire message before restoring, so the text content inside the placeholder data was not escaped because it was replaced with placeholder before escape. Now we need to escape text before inserting. Yes.
                text_esc = self.escape(text)
                replacement = f"<{url_esc}|{text_esc}>"
            elif kind == "URL":
                url = data
                url_esc = self.escape_url(url)
                replacement = f"<{url_esc}>"
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
        return truncated
