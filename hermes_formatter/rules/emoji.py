"""Emoji normalization rules."""

# Common emoji mappings (textual → unicode)
EMOJI_MAP = {
    ":smile:": "😊",
    ":grinning:": "😀",
    ":wink:": "😉",
    ":thinking:": "🤔",
    ":rocket:": "🚀",
    ":fire:": "🔥",
    ":white_check_mark:": "✅",
    ":heavy_check_mark:": "✔️",
    ":x:": "❌",
    ":cross_mark:": "✖️",
    ":warning:": "⚠️",
    ":information_source:": "ℹ️",
    ":bulb:": "💡",
    ":gear:": "⚙️",
    ":hourglass:": "⏳",
    ":bell:": "🔔",
    ":hammer:": "🔨",
    ":wrench:": "🔧",
    ":package:": "📦",
    ":chart_with_upwards_trend:": "📈",
    ":chart_with_downwards_trend:": "📉",
    ":bar_chart:": "📊",
    ":memo:": "📝",
    ":email:": "📧",
    ":link:": "🔗",
    ":key:": "🔑",
    ":lock:": "🔒",
    ":unlock:": "🔓",
    ":globe_with_meridians:": "🌐",
    ":computer:": "💻",
    ":iphone:": "📱",
    ":page_facing_up:": "📄",
    ":floppy_disk:": "💾",
    ":cd:": "💿",
    ":mag:": "🔍",
    ":warning_sign:": "⚠",  # older variant
}


def normalize_emoji(text: str) -> str:
    """
    Replace textual emoji codes with actual Unicode emoji.
    """
    for textual, emoji_char in EMOJI_MAP.items():
        text = text.replace(textual, emoji_char)
    return text


def has_emoji(text: str) -> bool:
    """Check if text contains any of our mapped emoji."""
    return any(emoji in text for emoji in EMOJI_MAP.values())
