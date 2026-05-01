"""
Discord Markdown formatter.
Mirrors Telegram adapter with Discord-specific escaping and rules.
"""

import re
from .base import BaseAdapter


class DiscordAdapter(BaseAdapter):
    """Adapter for Discord messages (Markdown)."""

    MAX_LENGTH = 2000

    # Discord markdown special chars that need escaping when not used as formatting
    ESCAPE_CHARS = '*_~`|>'

    def escape(self, text: str) -> str:
        for char in self.ESCAPE_CHARS:
            text = text.replace(char, f'\\{char}')
        return text

    def escape_url(self, url: str) -> str:
        """Escape minimal set for URLs."""
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
            key = f"HF{kind.upper()}{idx[0]}"
            idx[0] += 1
            protected[key] = (kind, data)
            return key

        # 1. Code blocks → inline code (Discord supports code blocks but we preserve as inline for consistency? 
        # Actually Discord supports ```blocks, so we could keep them. Let's keep them as blocks.
        # We'll protect them but re-insert as is.
        def protect_code_block(m):
            lang = m.group(1)
            code = m.group(2).strip()
            return ph("CODEBLOCK", (lang, code))

        message = re.sub(r'```(\w*)\n(.*?)```', protect_code_block, message, flags=re.DOTALL)

        # 2. Inline code
        def protect_inline(m):
            return ph("INLINE", m.group(1))

        message = re.sub(r'`([^`]+)`', protect_inline, message)

        # 3. Markdown: **bold** (Discord supports **)
        def protect_bold(m):
            return ph("BOLD", m.group(1))

        def protect_italic(m):
            return ph("ITALIC", m.group(1))

        def protect_strike(m):
            return ph("STRIKE", m.group(1))

        message = re.sub(r'\*\*(.+?)\*\*', protect_bold, message)
        message = re.sub(r'\*(?!\*)(.+?)\*', protect_italic, message)
        message = re.sub(r'~~(.+?)~~', protect_strike, message)

        # 4. Links [text](url)
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
                # Keep as fenced code block
                replacement = f"```{lang}\n{code}```" if lang else f"```{code}```"
            elif kind == "INLINE":
                replacement = f"`{data}`"
            elif kind == "BOLD":
                replacement = f"**{self.escape(data)}**"
            elif kind == "ITALIC":
                replacement = f"*{self.escape(data)}*"
            elif kind == "STRIKE":
                replacement = f"~~{self.escape(data)}~~"
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
        # Close unpaired markdown
        if truncated.count('**') % 2 == 1:
            truncated += '**'
        if truncated.count('`') % 2 == 1:
            truncated += '`'
        if truncated.count('*') % 2 == 1:
            truncated += '*'
        return truncated
