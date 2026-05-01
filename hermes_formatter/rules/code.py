"""Code block detection and processing."""

import re


def extract_code_blocks(text: str) -> list:
    """Extract all fenced code blocks with language info."""
    pattern = r'```(\w*)\n(.*?)```'
    matches = re.findall(pattern, text, re.DOTALL)
    return matches  # list of (language, code)


def extract_inline_code(text: str) -> list:
    """Extract inline code snippets."""
    return re.findall(r'`([^`]+)`', text)


def protect_code(text: str) -> tuple[str, dict]:
    """
    Replace code blocks with placeholders.

    Returns:
        (protected_text, {placeholder: (lang, code)})
    """
    placeholders = {}
    counter = [0]  # mutable for closure

    def replace_block(match):
        lang = match.group(1) or ""
        code = match.group(2)
        key = f"__CODE_BLOCK_{counter[0]}__"
        placeholders[key] = (lang, code)
        counter[0] += 1
        return key

    protected = re.sub(r'```(\w*)\n(.*?)```', replace_block, text, flags=re.DOTALL)
    return protected, placeholders


def restore_code(text: str, placeholders: dict) -> str:
    """Restore code blocks from placeholders."""
    for placeholder, (lang, code) in placeholders.items():
        replacement = f"```{lang}\n{code}```" if lang else f"```{code}```"
        text = text.replace(placeholder, replacement)
    return text
