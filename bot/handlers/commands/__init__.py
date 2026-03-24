"""Command handlers - pure functions, no Telegram dependency."""

from services.lms_client import lms_client


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
/scores <lab> - View pass rates for a lab"""


def handle_health() -> str:
    """Handle /health command."""
    result = lms_client.health_check()
    if result["healthy"]:
        return f"Backend is healthy. {result['item_count']} items available."
    else:
        return f"Backend error: {result['error']}. Check that the services are running."


def handle_labs() -> str:
    """Handle /labs command."""
    labs = lms_client.get_labs()
    if not labs:
        return "No labs available. Check that the backend is running and has data."
    
    lines = ["Available labs:"]
    for lab in labs:
        # Lab structure may vary - adjust based on actual response
        lab_name = lab.get("name", lab.get("title", "Unknown"))
        lab_id = lab.get("id", lab.get("slug", ""))
        # Only show main labs (IDs 1-7), skip tasks
        if isinstance(lab_id, int) and 1 <= lab_id <= 7:
            lines.append(f"- {lab_name}")
    
    return "\n".join(lines)


def handle_scores(query: str = "") -> str:
    """Handle /scores command."""
    if not query:
        return "Usage: /scores <lab> (e.g., /scores lab-04)"
    
    result = lms_client.get_pass_rates(query)
    if "error" in result:
        return f"Backend error: {result['error']}. Check that the lab ID is correct."
    
    if not result:
        return f"No pass rate data found for '{query}'."
    
    # Format the pass rates - backend returns a list of dicts
    lines = [f"Pass rates for {query}:"]
    for item in result:
        task_name = item.get("task", "Unknown task")
        avg_score = item.get("avg_score", 0)
        attempts = item.get("attempts", 0)
        lines.append(f"- {task_name}: {avg_score:.1f}% ({attempts} attempts)")
    
    return "\n".join(lines)
