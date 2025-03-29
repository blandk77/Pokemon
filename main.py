import asyncio
import logging
import os
from pyrogram import Client
from pyrogram.types import BotCommand

from config import API_ID, API_HASH, BOT_TOKEN
from Bot.commands import start, help, settings, encode
from Bot.callbacks import crf_callback, codec_callback
from webapp import app  # Import Flask app
import threading

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

LOGGER = logging.getLogger(__name__)

# Initialize Pyrogram Client
bot = Client(
    "VideoEncoderBot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# Register commands
start.register_handlers(bot)
help.register_handlers(bot)
settings.register_handlers(bot)
encode.register_handlers(bot)

# Register Callback queries
crf_callback.register_handlers(bot)
codec_callback.register_handlers(bot)

async def main():
    try:
        await bot.start()
        LOGGER.info("Bot started successfully!")

        # Set bot commands
        await bot.set_bot_commands([
            BotCommand("start", "Start the bot"),
            BotCommand("help", "Get help"),
            BotCommand("settings", "Configure encoding settings"),
            BotCommand("encode", "Encode your video")
        ])

        # Get bot information
        me = await bot.get_me()
        LOGGER.info(f"Bot username: {me.username}")

        # Keep the bot running (idle)
        await asyncio.idle()
    except Exception as e:
        LOGGER.error(f"An error occurred: {e}")
    finally:
        await bot.stop()
        LOGGER.info("Bot stopped.")

if __name__ == "__main__":
    # Start Flask app in a separate thread
    flask_thread = threading.Thread(target=app.run, kwargs={'host': '0.0.0.0', 'port': int(os.environ.get("PORT", 5000))})
    flask_thread.start()
    asyncio.run(main())
