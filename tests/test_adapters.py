"""Tests for platform adapters."""

import pytest
from hermes_formatter.adapters import get_adapter, TelegramAdapter, DiscordAdapter, CLIAdapter, GenericAdapter


class TestTelegramAdapter:
    """Test Telegram MarkdownV2 adapter."""

    def test_escape_special_chars(self):
        adapter = TelegramAdapter()
        text = "Hello *world* _foo_ [bar]"
        escaped = adapter.escape(text)
        assert r"\*" in escaped
        assert r"\_" in escaped
        assert r"\[" in escaped

    def test_render_url(self):
        adapter = TelegramAdapter()
        message = "Visit https://example.com now"
        result = adapter.render(message)
        assert "[example.com]" in result
        assert "(https://example.com)" in result

    def test_render_code(self):
        adapter = TelegramAdapter()
        message = "Use `print()` function"
        result = adapter.render(message)
        assert "`print()`" in result

    def test_max_length_truncate(self):
        adapter = TelegramAdapter()
        long_text = "x" * 5000
        result = adapter.truncate(long_text, adapter.MAX_LENGTH)
        assert len(result) <= adapter.MAX_LENGTH

    def test_close_unclosed_markdown(self):
        adapter = TelegramAdapter()
        message = "**Bold text"  # unclosed
        result = adapter._close_markdown(message)
        assert result.endswith('**')


class TestDiscordAdapter:
    """Test Discord adapter."""

    def test_render_basic(self):
        adapter = DiscordAdapter()
        message = "**bold** and *italic*"
        result = adapter.render(message)
        assert "**bold**" in result

    def test_code_block_protection(self):
        adapter = DiscordAdapter()
        message = "```python\nprint('hi')\n```"
        result = adapter.render(message)
        assert "```python" in result
        assert "print('hi')" in result


class TestGenericAdapter:
    """Test plain text adapter."""

    def test_render_plain(self):
        adapter = GenericAdapter()
        message = "**bold** *italic*"
        result = adapter.render(message)
        assert "**bold**" in result or "bold" in result

    def test_strip_markdown(self):
        adapter = GenericAdapter()
        message = "**bold**"
        result = adapter.render(message, strip_markdown=True)
        assert result == "bold"


class TestAdapterRegistry:
    """Test adapter registry and get_adapter."""

    def test_get_telegram(self):
        adapter = get_adapter("telegram")
        assert isinstance(adapter, TelegramAdapter)

    def test_get_discord(self):
        adapter = get_adapter("discord")
        assert isinstance(adapter, DiscordAdapter)

    def test_get_unknown_raises(self):
        with pytest.raises(ValueError):
            get_adapter("unknown_platform")
