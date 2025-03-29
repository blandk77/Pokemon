import os

# Telegram API credentials
API_ID = int(os.environ.get("API_ID", "27394279"))
API_HASH = os.environ.get("API_HASH", "90a9aa4c31afa3750da5fd686c410851")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "7773651775:AAEH1TN8P5700Ni7fluT9A7uE0xUWuZ0slE")

# MongoDB configuration
MONGO_URL = os.environ.get("MONGO_URL", "mongodb+srv://telegramguy21:tnkIwvbNkJ5U3fZ7@botsuse.bpgag.mongodb.net/?retryWrites=true&w=majority&appName=Botsuse")
DATABASE_NAME = "encoding_bot"

# Dump Channel ID
DUMP_CHANNEL_ID = int(os.environ.get("DUMP_CHANNEL_ID", "-1002288135729"))

# User Join Channel
USER_JOIN_CHANNEL = int(os.environ.get("USER_JOIN_CHANNEL", "-1002288135729"))

# Encoding settings (default values)
DEFAULT_CRF = 30
DEFAULT_CODEC = "libx264"
DEFAULT_AUDIO_CODEC = "aac"
DEFAULT_QUALITY = "360p"

# Watermark positions (example)
WATERMARK_POSITIONS = {
    "top-left": "x=10:y=10",
    "top-right": "x=main_w-text_w-10:y=10",
    "bottom-left": "x=10:y=main_h-text_h-10",
    "bottom-right": "x=main_w-text_w-10:y=main_h-text_h-10",
    "center": "x=(main_w-text_w)/2:y=(main_h-text_h)/2"
}

# Auto Rename Options
AUTO_RENAME_DEFAULT = False

# Metadata Default
METADATA_DEFAULT = False

# Thumbnail Default
THUMBNAIL_DEFAULT = False

# Flask Configuration
FLASK_HOST = "0.0.0.0"
FLASK_PORT = int(os.environ.get("PORT", 5000))  # Use PORT env var for Heroku/etc.
