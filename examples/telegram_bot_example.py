"""
Example: Telegram Bot using Hermes Formatter

This shows a minimal Telegram bot that receives tasks,
runs a mock agent, and sends formatted responses.

Prerequisites:
    pip install python-telegram-bot

Set environment variable TELEGRAM_BOT_TOKEN.
"""

import os
import asyncio
from telegram import Update, Bot
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from hermes_formatter import format


# Mock agent — replace with real Hermes agent call
async def run_agent(task: str) -> str:
    """Simulate agent processing."""
    await asyncio.sleep(1)  # pretend agent is thinking
    return f"✅ **Task Complete**\n\nProcessed: {task}\n\nResults:\n• 42 items found\n• Time: 2.3s\n\n_Done!_"


async def handle_task(update: Update, context):
    """Handle /task command."""
    task = " ".join(context.args) if context.args else "default task"
    user = update.effective_user

    # Send "typing" indicator
    await update.message.reply_chat_action("typing")

    # Run agent
    raw_output = await run_agent(task)

    # Format for Telegram
    formatted = format(raw_output, platform="telegram")

    # Send (handle Telegram's 4096 char limit)
    if len(formatted) > 4000:
        formatted = formatted[:3997] + "..."

    await update.message.reply_text(formatted, parse_mode="MarkdownV2")


async def handle_start(update: Update, context):
    """Welcome message."""
    welcome = """🤖 *Hermes Agent Bot*

Send me a task and I'll format the agent's response beautifully for Telegram\.

*Example:*
```
/task scrape https://example.com
```
"""
    await update.message.reply_text(welcome, parse_mode="MarkdownV2")


def main():
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        print("Error: Set TELEGRAM_BOT_TOKEN environment variable")
        return

    app = Application.builder().token(token).build()

    app.add_handler(CommandHandler("start", handle_start))
    app.add_handler(CommandHandler("task", handle_task))

    print("Bot starting... (press Ctrl+C to stop)")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
