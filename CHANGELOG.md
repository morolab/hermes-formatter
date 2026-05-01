# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.1] — 2026-05-01

### Fixed
- Telegram bold rendering: `**text**` now correctly outputs `*text*` (asterisk-based emphasis)
- Telegram italic rendering: `*text*` preserved (no longer converted to underscore)
- URL domain escaping: dots no longer escaped in link text (`example.com` instead of `example\.com`)
- Added `_close_markdown` method to `TelegramAdapter` for unclosed markdown detection

All 30 tests now pass across Python 3.9–3.12.

[Full diff since v0.1.0](https://github.com/morolab/hermes-formatter/compare/v0.1.0...v0.1.1)

---

# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] — 2026-05-01

### Added
- Initial release
- Support for Telegram MarkdownV2 formatting
- Support for Discord markdown
- Support for Slack mrkdwn
- Support for CLI with ANSI colors (with Rich fallback)
- Support for Email (HTML + plain text multipart)
- Generic plain text mode with markdown stripping
- Auto-detection via `auto_format()`
- Batch formatting via `HermesFormatter.format_batch()`
- Comprehensive test suite
- Example bots for Telegram and Discord

### Planned
- WhatsApp Business adapter
- Matrix.org adapter
- Smart truncation per platform
- More emoji mappings
- Table formatting per platform