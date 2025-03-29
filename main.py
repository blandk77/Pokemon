import asyncio
import logging
import os

from pyrogram import Client
from pyrogram.types import BotCommand

from config import API_ID, API_HASH, BOT_TOKEN
from Bot.commands import start, help, settings
from Bot.handlers import message_handler
from flask import Flask, render_template, request
from aiohttp import web

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

# Create pyrogram client
bot = Client("EncodingBot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

async def run_flask_app():
    from Bot.commands import settings  # Import settings here to avoid circular imports
    app = settings.app  # Access the Flask app from settings.py

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', 5000)  # Use config.FLASK_HOST/PORT from config.py
    await site.start()
    print("Flask app started on port 5000")

async def main():
    await bot.start()
    print("Bot started. Connecting to MongoDB...")

    # Set bot commands
    commands = [
        BotCommand("start", "Start the bot"),
        BotCommand("help", "Get help and usage instructions"),
        BotCommand("settings", "Configure encoding settings"),
    ]
    await bot.set_bot_commands(commands)

    # Register handlers
    start.register_handlers(bot)
    help.register_handlers(bot)
    settings.register_handlers(bot)
    message_handler.register_handlers(bot)

    # Get bot's username
    me = await bot.get_me()
    bot_username = me.username

    print(f"@{bot_username} started successfully!")

    flask_task = asyncio.create_task(run_flask_app())

    await asyncio.gather(asyncio.sleep(1), flask_task, bot.idle())

    await bot.stop()

if __name__ == "__main__":
    asyncio.run(main())
