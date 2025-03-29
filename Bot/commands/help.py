from pyrogram import Client, filters
from pyrogram.types import Message

HELP_MESSAGE = """
**Available Commands:**

- /start: Starts the bot.
- /help: Shows this help message.
- /settings: Configure your encoding settings (CRF, codec, watermark, etc.).
- /encode: Send a video file to start encoding.

**Settings Variables:**

- **CRF**: Constant Rate Factor (0-51, lower is better quality).
- **Video Codec**:  The video encoding codec (e.g., libx264, libx265).
- **Audio Codec**: The audio encoding codec (e.g., aac, libmp3lame).
- **Watermark Text**: Text to overlay on the video.
- **Watermark Position**: Where to place the watermark (top_left, top_right, bottom_left, bottom_right, center).
- **Auto Rename**: Enable/disable auto renaming of the encoded file.
- **Auto Rename Format**:  The format for auto renaming. Use variables: {episode}, {season}, {quality}, {audio}.
- **Caption Format**: The format for the caption. Use variables: {filename}, {filesize}, {audio}, {quality}.
- **Thumbnail**: Path to a custom thumbnail file.
- **Metadata**:  FFmpeg-compatible metadata string.

**Important:**

- You must set a CRF and video codec via /settings *before* encoding.
"""

def register_handlers(bot: Client):
    @bot.on_message(filters.command("help"))
    async def help_command(client: Client, message: Message):
        await message.reply_text(HELP_MESSAGE)
