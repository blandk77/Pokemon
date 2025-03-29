# Telegram Encoding Bot

A Telegram bot that encodes media files using FFmpeg with customizable settings.

## Setup
1. Install Docker or Python 3.9+.
2. Get a Telegram Bot Token from `@BotFather`.
3. Replace `YOUR_BOT_TOKEN_HERE` in `config.py` with your token.
4. Set `DUMP_CHANNEL_ID` in `config.py` (optional).
5. Install dependencies: `pip install -r requirements.txt`.
6. Install FFmpeg: `apt-get install ffmpeg` (or equivalent).
7. Run the bot: `python main.py`.

## Docker
```bash
docker build -t telegram-encoding-bot .
docker run -e BOT_TOKEN="your_token" -e DUMP_CHANNEL_ID="-1001234567890" telegram-encoding-bot
