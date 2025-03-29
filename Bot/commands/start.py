from pyrogram import Client, filters
from pyrogram.types import Message

def register_handlers(bot: Client):
    @bot.on_message(filters.command("start"))
    async def start_command(client: Client, message: Message):
        await message.reply_text("Welcome! Use /help to see available commands.")
