"""Command handlers - pure functions, no Telegram dependency."""


def handle_start() -> str:
    """Handle /start command."""
    return "Welcome to the LMS Bot! Use /help to see available commands."


def handle_help() -> str:
    """Handle /help command."""
    return """Available commands:
/start - Welcome message
/help - Show this help
/health - Check backend connection
/labs - List available labs
/scores - View your scores"""


def handle_health() -> str:
    """Handle /health command."""
    return "Health check: OK (placeholder)"


def handle_labs() -> str:
    """Handle /labs command."""
    return "Labs: No labs available yet (placeholder)"


def handle_scores(query: str = "") -> str:
    """Handle /scores command."""
    return f"Scores for '{query}': No data yet (placeholder)"
