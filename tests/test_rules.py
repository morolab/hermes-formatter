"""Tests for formatting rules."""

import pytest
from hermes_formatter.rules import (
    normalize_emoji,
    extract_urls,
    is_url,
    EMOJI_MAP,
    extract_code_blocks,
    extract_inline_code,
)


class TestEmojiNormalization:
    """Test emoji normalization."""

    def test_replace_emoji(self):
        text = "Task :rocket: complete!"
        result = normalize_emoji(text)
        assert "🚀" in result

    def test_unknown_emoji_unchanged(self):
        text = "Unknown :foo: emoji"
        result = normalize_emoji(text)
        assert result == text

    def test_has_emoji(self):
        from hermes_formatter.rules import has_emoji
        assert has_emoji("Hello 🚀") == True
        assert has_emoji("Hello world") == False


class TestURLRules:
    """Test URL extraction and detection."""

    def test_extract_urls(self):
        text = "Check https://example.com and http://test.org"
        urls = extract_urls(text)
        assert len(urls) == 2
        assert "https://example.com" in urls

    def test_is_url(self):
        assert is_url("https://example.com") == True
        assert is_url("not a url") == False

    def test_url_with_path(self):
        text = "See https://example.com/path/to/page?query=1"
        urls = extract_urls(text)
        assert len(urls) == 1


class TestCodeRules:
    """Test code block extraction."""

    def test_extract_code_blocks(self):
        text = "```python\nprint('hello')\n```"
        blocks = extract_code_blocks(text)
        assert len(blocks) == 1
        lang, code = blocks[0]
        assert lang == "python"
        assert "print('hello')" in code

    def test_extract_inline_code(self):
        text = "Use `print()` function"
        codes = extract_inline_code(text)
        assert codes == ["print()"]

    def test_protect_and_restore(self):
        from hermes_formatter.rules.code import protect_code, restore_code
        text = "```py\ncode1``` and ```js\ncode2```"
        protected, placeholders = protect_code(text)
        assert "__CODE_BLOCK_0__" in protected
        restored = restore_code(protected, placeholders)
        assert "```py" in restored
        assert "code1" in restored
        assert "```js" in restored
        assert "code2" in restored
