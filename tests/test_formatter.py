"""Tests for the main formatter module."""

import pytest
from hermes_formatter import format, HermesFormatter, auto_format


class TestFormatter:
    """Test the main format function."""

    def test_format_telegram_bold(self):
        message = "**Hello World**"
        result = format(message, platform="telegram")
        assert result == "*Hello World*"

    def test_format_telegram_italic(self):
        message = "*italic*"
        result = format(message, platform="telegram")
        assert result == "*italic*"  # Telegram uses same marker

    def test_format_telegram_url(self):
        message = "Check https://example.com"
        result = format(message, platform="telegram")
        assert "[example.com]" in result
        assert "(https://example.com)" in result

    def test_format_discord_bold(self):
        message = "**bold**"
        result = format(message, platform="discord")
        assert result == "**bold**"

    def test_format_generic_strip(self):
        message = "**bold** and *italic*"
        result = format(message, platform="generic", strip_markdown=True)
        assert result == "bold and italic"

    def test_format_cli_ansi_present(self):
        message = "**Success**"
        result = format(message, platform="cli")
        # Should contain ANSI codes if rich is not available
        assert "Success" in result

    def test_auto_detect_telegram(self):
        message = "Hello"
        result = auto_format(message, context={"is_telegram": True})
        assert result is not None

    def test_formatter_instance(self):
        f = HermesFormatter(platform="telegram")
        result = f.format("Test")
        assert "Test" in result


class TestBatchFormat:
    """Test batch formatting."""

    def test_format_batch(self):
        messages = ["msg1", "msg2", "msg3"]
        formatter = HermesFormatter(platform="telegram")
        results = formatter.format_batch(messages)
        assert len(results) == 3
        assert all(isinstance(r, str) for r in results)
