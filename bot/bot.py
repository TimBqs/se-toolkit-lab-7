#!/usr/bin/env python3
"""LMS Telegram Bot - Entry point with --test mode."""

import argparse
import logging
import sys

from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command, CommandStart
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from config import settings
from handlers import (handle_health, handle_help, handle_labs, handle_scores,
                      handle_start)
from handlers.intent_router import route_intent

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


def get_main_keyboard() -> InlineKeyboardMarkup:
    """Create inline keyboard with common actions."""
    keyboard = [
        [
            InlineKeyboardButton(text="🏥 Health", callback_data="health"),
            InlineKeyboardButton(text="📚 Labs", callback_data="labs"),
        ],
        [
            InlineKeyboardButton(text="📊 Scores", callback_data="scores"),
            InlineKeyboardButton(text="❓ Help", callback_data="help"),
        ],
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def handle_message(text: str) -> str:
    """Handle plain text message with LLM intent routing."""
    # Check if it looks like a command without slash
    if text.startswith("/"):
        command, args = parse_command(text)
        return run_command(command, args)
    
    # Use LLM intent router for plain text
    return route_intent(text)


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
        response = handle_message(args.test)
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
        await message.answer(handle_start(), reply_markup=get_main_keyboard())

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

    # Handle callback queries from inline buttons
    @dp.callback_query(lambda c: c.data)
    async def process_callback_query(callback_query: types.CallbackQuery):
        data = callback_query.data
        if data == "health":
            response = handle_health()
        elif data == "labs":
            response = handle_labs()
        elif data == "help":
            response = handle_help()
        elif data == "scores":
            response = "Send me a lab number (e.g., 'lab-04') to see scores"
        else:
            response = "Unknown action"
        await callback_query.message.answer(response)
        await callback_query.answer()

    # Handle plain text messages with LLM intent routing
    @dp.message()
    async def handle_text(message: types.Message):
        response = handle_message(message.text or "")
        await message.answer(response)

    # Run polling
    dp.run_polling(bot)
    return 0


if __name__ == "__main__":
    sys.exit(main())
