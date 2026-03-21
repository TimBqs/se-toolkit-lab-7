#!/usr/bin/env python3
"""LMS Telegram Bot - Entry point with --test mode."""

import argparse
import sys

from handlers import (
    handle_start,
    handle_help,
    handle_health,
    handle_labs,
    handle_scores,
)


def parse_command(text: str) -> tuple[str, str]:
    """Parse command text into (command, args)."""
    parts = text.strip().split(maxsplit=1)
    if not parts:
        return "", ""
    command = parts[0]
    args = parts[1] if len(parts) > 1 else ""
    return command, args


def run_command(command: str, args: str) -> str:
    """Route command to handler and return response."""
    if command == "/start":
        return handle_start()
    elif command == "/help":
        return handle_help()
    elif command == "/health":
        return handle_health()
    elif command == "/labs":
        return handle_labs()
    elif command == "/scores":
        return handle_scores(args)
    else:
        return f"Unknown command: {command}. Use /help for available commands."


def main() -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(description="LMS Telegram Bot")
    parser.add_argument(
        "--test",
        type=str,
        metavar="TEXT",
        help="Test mode: process TEXT as input and print response to stdout",
    )
    args = parser.parse_args()

    if args.test:
        # Test mode: call handlers directly
        command, cmd_args = parse_command(args.test)
        response = run_command(command, cmd_args)
        print(response)
        return 0

    # Telegram mode: start the bot (to be implemented in Task 2)
    print("Starting bot in Telegram mode... (not yet implemented)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
