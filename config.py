import os

#Telegram Bot Token (get from BotFather)
BOT_TOKEN = os.getenv("BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")

# MongoDB URL
MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017/encoding_bot")

# Dump Channel ID (where encoded files are sent in addition to the user)
DUMP_CHANNEL_ID = os.getenv("DUMP_CHANNEL_ID", "-1001234567890")

# User Channel ID (where new user notifications are sent)
USER_CHANNEL_ID = os.getenv("USER_CHANNEL_ID", "-1009876543210")

# Flask settings
FLASK_HOST = "0.0.0.0"
FLASK_PORT = 5000

# Default FFmpeg settings (can be overridden by users)
DEFAULT_CRF = None  # Required field
DEFAULT_WATERMARK = None  # Optional
DEFAULT_VIDEO_CODEC = "libx264"
DEFAULT_AUDIO_CODEC = "aac"
DEFAULT_QUALITY = None  # Required field
DEFAULT_METADATA = None  # Optional
DEFAULT_THUMBNAIL = None  # Optional
DEFAULT_AUTO_RENAME = False
DEFAULT_RENAME_PATTERN = "{season}{episodes}_{quality}_{audio}"
DEFAULT_CAPTION_PATTERN = "{filename} | {filesize} | {quality} | {audio}"

# Watermark position options (for UI buttons)
WATERMARK_POSITIONS = {
    "Top-Left": "x=10:y=10",
    "Top-Right": "x=main_w-text_w-10:y=10",
    "Bottom-Left": "x=10:y=main_h-text_h-10",
    "Bottom-Right": "x=main_w-text_w-10:y=main_h-text_h-10",
    "Center": "x=(main_w-text_w)/2:y=(main_h-text_h)/2"
}
