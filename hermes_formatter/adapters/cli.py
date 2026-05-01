"""
CLI formatter with ANSI colors using the `rich` library.
Falls back to plain text if rich is not available.
"""

from .base import BaseAdapter

try:
    from rich.console import Console
    from rich.syntax import Syntax
    from rich.markdown import Markdown
    from rich.panel import Panel
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False


class CLIAdapter(BaseAdapter):
    """Adapter for terminal/console output with colors."""

    MAX_LENGTH = None  # No hard limit for CLI

    def escape(self, text: str) -> str:
        """No escaping needed for CLI (we control rendering)."""
        return text

    def render(self, message: str, **kwargs) -> str:
        """
        Render message with ANSI colors.

        If rich is available: use Rich for rich formatting.
        Otherwise: basic ANSI escape codes.
        """
        if RICH_AVAILABLE:
            return self._render_rich(message, **kwargs)
        else:
            return self._render_ansi(message, **kwargs)

    def _render_rich(self, message: str, **kwargs) -> str:
        """Render using Rich library (to_string for capture)."""
        console = Console(force_terminal=True, width=kwargs.get("width", 80))

        # Convert markdown to Rich-compatible render
        # Rich handles **bold**, *italic*, `code`, code blocks natively
        md = Markdown(message)

        # Capture output instead of printing
        from io import StringIO
        buffer = StringIO()
        temp_console = Console(file=buffer, force_terminal=True, width=kwargs.get("width", 80))
        temp_console.print(md)
        return buffer.getvalue()

    def _render_ansi(self, message: str, **kwargs) -> str:
        """Manual ANSI coloring (fallback)."""
        # ANSI color codes
        GREEN = '\033[92m'
        BLUE = '\033[94m'
        YELLOW = '\033[93m'
        RED = '\033[91m'
        CYAN = '\033[96m'
        BOLD = '\033[1m'
        RESET = '\033[0m'

        lines = message.split('\n')
        colored_lines = []

        for line in lines:
            # Title/headings (lines starting with # or all caps)
            if line.startswith('#') or line.isupper():
                colored_lines.append(f"{CYAN}{BOLD}{line}{RESET}")
            # Success indicators
            elif any(word in line.lower() for word in ['✅', 'success', 'complete', 'done']):
                colored_lines.append(f"{GREEN}{line}{RESET}")
            # Errors/ failures
            elif any(word in line.lower() for word in ['❌', 'error', 'failed', 'fatal']):
                colored_lines.append(f"{RED}{line}{RESET}")
            # Warnings/ info
            elif any(word in line.lower() for word in ['⚠️', 'warning', 'note']):
                colored_lines.append(f"{YELLOW}{line}{RESET}")
            # URLs (highlight in blue)
            elif 'http://' in line or 'https://' in line:
                colored_lines.append(f"{BLUE}{line}{RESET}")
            # Code blocks (lines with backticks)
            elif '`' in line:
                colored_lines.append(f"{CYAN}{line}{RESET}")
            else:
                colored_lines.append(line)

        return '\n'.join(colored_lines)

    def render_for_display(self, message: str) -> str:
        """
        Render with visual enhancements (panels, borders).
        Useful for prominent agent summaries.
        """
        if not RICH_AVAILABLE:
            return f"{'='*40}\n{message}\n{'='*40}"

        from rich.panel import Panel
        from io import StringIO
        buffer = StringIO()
        console = Console(file=buffer, force_terminal=True, width=80)
        panel = Panel(Markdown(message), border_style="cyan")
        console.print(panel)
        return buffer.getvalue()
