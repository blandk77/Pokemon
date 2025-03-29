from pyrogram import Client, filters
from pyrogram.types import CallbackQuery
from Bot.database import DB

def register_handlers(bot: Client):
    @bot.on_callback_query(filters.regex("^position_"))
    async def position_callback(client: Client, callback_query: CallbackQuery):
        position = callback_query.data.split("_")[1]
        user_id = callback_query.from_user.id
        await DB.update_user(user_id, watermark_position=position)
        await callback_query.answer(f"Watermark position set to: {position}")
        await callback_query.message.edit_text(f"Watermark position updated to {position}.")
