from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from Bot.database import DB
from config import WATERMARK_POSITIONS
from flask import Flask, render_template, request

app = Flask(__name__)

def register_handlers(bot: Client):
    @bot.on_message(filters.command("settings"))
    async def settings_command(client: Client, message: Message):
        user_id = message.from_user.id
        username = message.from_user.username or message.from_user.first_name
        user_data = await DB.get_user(user_id)

        if user_data:
            crf = user_data.get("crf")
            watermark = user_data.get("watermark")
            codec = user_data.get("codec")
            audio_codec = user_data.get("audio_codec")
            quality = user_data.get("quality")
            auto_rename = user_data.get("auto_rename")
            auto_rename_format = user_data.get("auto_rename_format")
            caption_format = user_data.get("caption_format")
            thumbnail = user_data.get("thumbnail")
            metadata = user_data.get("metadata")
            watermark_position = user_data.get("watermark_position")

            settings_text = f"""
            Settings for user: {username}

            Crf: {crf if crf else "None"}
            Watermark: {watermark if watermark else "None"}
            Codec: {codec if codec else "None"}
            Audio Codec: {audio_codec if audio_codec else "None"}
            Quality: {quality if quality else "None"}
            Auto Rename: {auto_rename if auto_rename is not None else "False"}
            Auto Rename Format: {auto_rename_format if auto_rename_format else "None"}
            Caption Format: {caption_format if caption_format else "None"}
            Thumbnail: {thumbnail if thumbnail else "None"}
            Metadata: {metadata if metadata else "None"}
            Watermark Position: {watermark_position if watermark_position else "None"}
            """

            keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton("Edit Settings", url=f"http://localhost:5000/settings/{user_id}")]
            ])

            await message.reply_text(settings_text, reply_markup=keyboard)
        else:
            await message.reply_text("No settings found. Please configure your settings.")

@app.route('/settings/<int:user_id>', methods=['GET', 'POST'])
async def settings_page(user_id):
    user_data = await DB.get_user(user_id)
    if request.method == 'POST':
        crf = request.form.get('crf')
        watermark = request.form.get('watermark')
        codec = request.form.get('codec')
        audio_codec = request.form.get('audio_codec')
        quality = request.form.get('quality')
        auto_rename = request.form.get('auto_rename') == 'true'
        auto_rename_format = request.form.get('auto_rename_format')
        caption_format = request.form.get('caption_format')
        thumbnail = request.form.get('thumbnail') == 'true'
        metadata = request.form.get('metadata') == 'true'
        watermark_position = request.form.get('watermark_position')

        await DB.update_user(user_id, crf, watermark, codec, audio_codec, quality, auto_rename, auto_rename_format, caption_format, thumbnail, metadata, watermark_position)

        return "Settings updated successfully!"

    return render_template('settings.html', user_data=user_data, watermark_positions=WATERMARK_POSITIONS)

@app.route('/')
def home():
    return "Encoding Bot Settings"

# Start the Flask app
#if __name__ == '__main__':
#    app.run(debug=True)
