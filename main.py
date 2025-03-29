import asyncio
import logging
import os

from pyrogram import Client
from pyrogram.types import BotCommand

from config import API_ID, API_HASH, BOT_TOKEN
from Bot.commands import start, help, settings
from Bot.handlers import message_handler

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

# Create pyrogram client
bot = Client("EncodingBot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

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
    await asyncio.idle()
    await bot.stop()

if __name__ == "__main__":
    asyncio.run(main())
