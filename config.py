import os

# Telegram API Configuration
API_ID = int(os.environ.get("API_ID", ""))
API_HASH = os.environ.get("API_HASH", "")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "")

# MongoDB Configuration
MONGODB_URL = os.environ.get("MONGODB_URL", "")
DATABASE_NAME = os.environ.get("DATABASE_NAME", "VideoEncoderBot")

# User Channel to add a new user
USER_CHANNEL = int(os.environ.get("USER_CHANNEL", ""))

# Dump Channel to dump the encoded files
DUMP_CHANNEL = int(os.environ.get("DUMP_CHANNEL", ""))

# FFmpeg Settings (Defaults - Can be overridden by user)
DEFAULT_CRF = "30"
DEFAULT_VIDEO_CODEC = "libx264"
DEFAULT_AUDIO_CODEC = "aac"

# Watermark Positions
WATERMARK_POSITIONS = {
    "top_left": "x=10:y=10",
    "top_right": "x=main_w-text_w-10:y=10",
    "bottom_left": "x=10:y=main_h-text_h-10",
    "bottom_right": "x=main_w-text_w-10:y=main_h-text_h-10",
    "center": "x=(main_w-text_w)/2:y=(main_h-text_h)/2"
}

# System Stats Update Interval (seconds)
STATS_UPDATE_INTERVAL = 5

# Auto Rename Defaults
DEFAULT_AUTO_RENAME = False
