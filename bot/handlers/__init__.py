"""Command handlers - pure functions, no Telegram dependency."""

from .commands import (handle_health, handle_help, handle_labs, handle_scores,
                       handle_start)
from .intent_router import route_intent

__all__ = [
    "handle_start",
    "handle_help",
    "handle_health",
    "handle_labs",
    "handle_scores",
    "route_intent",
]
