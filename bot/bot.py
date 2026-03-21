#!/usr/bin/env python3
"""LMS Telegram Bot - Entry point with --test mode."""

import argparse
import logging
import sys

from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command, CommandStart
from config import settings
from handlers import (handle_health, handle_help, handle_labs, handle_scores,
                      handle_start)

logging.basicConfig(level=logging.INFO)


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

    # Telegram mode: start the bot
    if not settings.bot_token:
        logging.error("BOT_TOKEN is not set in .env.bot.secret")
        return 1

    logging.info("Starting bot in Telegram mode...")
    
    # Create bot and dispatcher
    bot = Bot(token=settings.bot_token)
    dp = Dispatcher()

    # Register handlers
    @dp.message(CommandStart())
    async def cmd_start(message: types.Message):
        await message.answer(handle_start())

    @dp.message(Command("help"))
    async def cmd_help(message: types.Message):
        await message.answer(handle_help())

    @dp.message(Command("health"))
    async def cmd_health(message: types.Message):
        await message.answer(handle_health())

    @dp.message(Command("labs"))
    async def cmd_labs(message: types.Message):
        await message.answer(handle_labs())

    @dp.message(Command("scores"))
    async def cmd_scores(message: types.Message):
        # Get args after /scores command
        args_text = message.text.split(maxsplit=1)
        args_text = args_text[1] if len(args_text) > 1 else ""
        await message.answer(handle_scores(args_text))

    # Run polling
    dp.run_polling(bot)
    return 0


if __name__ == "__main__":
    sys.exit(main())
