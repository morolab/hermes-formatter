"""
Email formatter — generates HTML + plain-text versions.
Returns a dict with 'html' and 'text' keys for multipart emails.
"""

import re
from .base import BaseAdapter


class EmailAdapter(BaseAdapter):
    """
    Adapter for email messages.

    Output format: dict with 'html' and 'text' keys.
    Use: formatter.format(message, platform="email") → {"html": ..., "text": ...}
    """

    MAX_LENGTH = None

    # Simple HTML style for email
    STYLE = """
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; line-height: 1.6; color: #333; max-width: 600px; margin: 0 auto; padding: 20px; }
        h1 { color: #1a73e8; font-size: 1.5em; border-bottom: 2px solid #1a73e8; padding-bottom: 10px; }
        h2 { color: #1a73e8; font-size: 1.2em; margin-top: 24px; }
        .success { color: #0d9f4c; font-weight: bold; }
        .error { color: #d93025; font-weight: bold; }
        .warning { color: #f9ab00; font-weight: bold; }
        .info { color: #1a73e8; }
        code { background: #f5f5f5; padding: 2px 6px; border-radius: 3px; font-family: 'Monaco', 'Consolas', monospace; font-size: 0.9em; }
        pre { background: #f5f5f5; padding: 16px; border-radius: 5px; overflow-x: auto; }
        pre code { background: none; padding: 0; }
        .url { color: #1a73e8; text-decoration: none; }
        .url:hover { text-decoration: underline; }
        ul { padding-left: 20px; }
        li { margin: 4px 0; }
        .footer { margin-top: 30px; font-size: 0.8em; color: #777; border-top: 1px solid #eee; padding-top: 10px; }
        .highlight { background: #fff8e1; padding: 12px; border-left: 3px solid #f9ab00; margin: 10px 0; }
    </style>
    """

    def escape(self, text: str) -> str:
        """Escape HTML entities."""
        text = text.replace('&', '&amp;')
        text = text.replace('<', '&lt;')
        text = text.replace('>', '&gt;')
        return text

    def render(self, message: str, **kwargs) -> dict:
        """
        Convert plain text to HTML email + plain text fallback.

        Returns:
            {"html": "...", "text": "..."}
        """
        plain = self._clean_for_plain(message)

        html = self._convert_to_html(message)

        return {"html": html, "text": plain}

    def _clean_for_plain(self, message: str) -> str:
        """Strip markdown, keep plain readable text."""
        plain = message
        # Remove code fences but keep content
        plain = re.sub(r'```.*?\n(.*?)```', r'\1', plain, flags=re.DOTALL)
        # Remove inline code markers
        plain = re.sub(r'`([^`]+)`', r'\1', plain)
        # Remove bold/italic markers but keep text
        plain = re.sub(r'\*\*(.+?)\*\*', r'\1', plain)
        plain = re.sub(r'\*(.+?)\*', r'\1', plain)
        plain = re.sub(r'~~(.+?)~~', r'\1', plain)
        # Keep URLs as-is
        return plain.strip()

    def _convert_to_html(self, message: str) -> str:
        """Convert markdown-like syntax to HTML."""
        html = message

        # Escape HTML in original text (before we add our tags)
        html = self.escape(html)

        # Code blocks: ```lang\ncode``` → <pre><code class="lang">code</code></pre>
        def code_block_to_html(match):
            lang = match.group(1) or ""
            code = match.group(2)
            class_attr = f' class="language-{lang}"' if lang else ''
            return f'<pre><code{class_attr}>\n{code}\n</code></pre>'

        html = re.sub(r'```(\w*)\n(.*?)```', code_block_to_html, html, flags=re.DOTALL)

        # Inline code: `code` → <code>code</code>
        html = re.sub(r'`([^`]+)`', r'<code>\1</code>', html)

        # Bold: **text** → <strong>text</strong>
        html = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', html)

        # Italic: *text* → <em>text</em>
        html = re.sub(r'\*(?!\*)(.+?)\*', r'<em>\1</em>', html)

        # Strikethrough: ~~text~~ → <del>text</del>
        html = re.sub(r'~~(.+?)~~', r'<del>\1</del>', html)

        # Headers: # → h1, ## → h2
        html = re.sub(r'^# (.+)$', r'<h1>\1</h1>', html, flags=re.MULTILINE)
        html = re.sub(r'^## (.+)$', r'<h2>\1</h2>', html, flags=re.MULTILINE)

        # Lists: • item → <ul><li>item</li></ul> (simplified)
        # For now just wrap lines starting with • or - in <li>
        html = re.sub(r'^[\s]*[•\-\*]\s+(.+)$', r'<li>\1</li>', html, flags=re.MULTILINE)
        # Wrap consecutive <li> in <ul> — this is naive, but works for simple cases
        html = re.sub(r'(<li>.+?</li>\n?)+', r'<ul>\g<0></ul>', html)

        # URLs: convert to clickable links
        url_pattern = r'(https?://[^\s<>]+)'
        html = re.sub(url_pattern, r'<a href="\1" class="url">\1</a>', html)

        # Success/error highlighting
        html = html.replace('✅', '<span class="success">✅</span>')
        html = html.replace('❌', '<span class="error">❌</span>')
        html = html.replace('⚠️', '<span class="warning">⚠️</span>')

        # Wrap in full HTML doc
        full_html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Agent Report</title>
    {self.STYLE}
</head>
<body>
{html}
<div class="footer">
    Generated by Hermes Agent Formatter
</div>
</body>
</html>"""
        return full_html
