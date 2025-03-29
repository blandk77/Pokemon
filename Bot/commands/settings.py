from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from Bot.database import DB
from config import WATERMARK_POSITIONS

def register_handlers(bot: Client):
    @bot.on_message(filters.command("settings"))
    async def settings_command(client: Client, message: Message):
        user_id = message.from_user.id
        user_settings = await DB.get_user_settings(user_id)

        crf = user_settings.get("crf", None)
        video_codec = user_settings.get("video_codec", None)
        audio_codec = user_settings.get("audio_codec", None)
        watermark_text = user_settings.get("watermark_text", None)
        watermark_position = user_settings.get("watermark_position", None)
        auto_rename = user_settings.get("auto_rename", False)
        auto_rename_format = user_settings.get("auto_rename_format", None)
        caption_format = user_settings.get("caption_format", None)
        thumbnail = user_settings.get("thumbnail", None)
        metadata = user_settings.get("metadata", None)

        settings_text = f"""
**Settings for user:** {message.from_user.username}

**CRF:** {crf if crf else "None"}
**Video Codec:** {video_codec if video_codec else "None"}
**Audio Codec:** {audio_codec if audio_codec else "None"}
**Watermark:** {watermark_text if watermark_text else "None"}
**Watermark Position:** {watermark_position if watermark_position else "None"}
**Auto Rename:** {auto_rename}
**Auto Rename Format:** {auto_rename_format if auto_rename_format else "None"}
**Caption Format:** {caption_format if caption_format else "None"}
**Thumbnail:** {thumbnail if thumbnail else "None"}
**Metadata:** {metadata if metadata else "None"}
"""

        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("Set CRF", callback_data="set_crf")],
            [InlineKeyboardButton("Set Video Codec", callback_data="set_video_codec")],
            [InlineKeyboardButton("Set Audio Codec", callback_data="set_audio_codec")],
            [InlineKeyboardButton("Set Watermark Text", callback_data="set_watermark_text")],
            [InlineKeyboardButton("Set Watermark Position", callback_data="set_watermark_position")],
            [InlineKeyboardButton("Toggle Auto Rename", callback_data="toggle_auto_rename")],
            [InlineKeyboardButton("Set Auto Rename Format", callback_data="set_auto_rename_format")],
            [InlineKeyboardButton("Set Caption Format", callback_data="set_caption_format")],
            [InlineKeyboardButton("Set Thumbnail", callback_data="set_thumbnail")],
            [InlineKeyboardButton("Set Metadata", callback_data="set_metadata")]
        ])

        await message.reply_text(settings_text, reply_markup=keyboard)
