from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from flask import Flask
import os
import threading
from config import BOT_TOKEN, WATERMARK_POSITIONS, FLASK_HOST, FLASK_PORT, DUMP_CHANNEL_ID, MONGO_URL
from commands import register_commands
from encoding import encode_file
from pymongo import MongoClient

app = Client("encoding_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
flask_app = Flask(__name__)

# MongoDB client
mongo_client = MongoClient(MONGO_URL)
db = mongo_client.get_default_database()
users_collection = db["users"]

# Flask health check endpoint
@flask_app.route("/health")
def health():
    return "Bot is running", 200

def run_flask():
    flask_app.run(host=FLASK_HOST, port=FLASK_PORT)

# Handle file uploads
@app.on_message(filters.document | filters.video)
async def handle_file(client, message):
    user_id = message.from_user.id
    file = await message.download()

    output_path = f"encoded_{os.path.basename(file)}"
    success, result = encode_file(user_id, file, output_path)

    if not success:
        await message.reply_text(result)
        os.remove(file)
        return

    output_path, caption = result
    await message.reply_document(output_path, caption=caption)
    await client.send_document(DUMP_CHANNEL_ID, output_path, caption=caption)
    os.remove(file)
    os.remove(output_path)

# Handle settings callbacks
@app.on_callback_query()
async def handle_callback(client, query):
    user_id = query.from_user.id
    data = query.data.split("_")

    if data[0] == "set":
        param = data[1]
        if param == "watermark":
            await query.message.reply_text("Send the watermark text:")
            users_collection.update_one({"user_id": user_id}, {"$set": {"pending": "watermark"}})
        elif param == "crf":
            await query.message.reply_text("Send CRF value (0-51):")
            users_collection.update_one({"user_id": user_id}, {"$set": {"pending": "crf"}})
        elif param == "quality":
            await query.message.reply_text("Send quality (e.g., 720p):")
            users_collection.update_one({"user_id": user_id}, {"$set": {"pending": "quality"}})
        elif param == "rename":
            await query.message.reply_text("Send rename pattern (e.g., {season}{episodes}_{quality}):")
            users_collection.update_one({"user_id": user_id}, {"$set": {"pending": "rename_pattern"}})
        elif param == "caption":
            await query.message.reply_text("Send caption pattern (e.g., {filename} | {quality}):")
            users_collection.update_one({"user_id": user_id}, {"$set": {"pending": "caption_pattern"}})
        elif param == "meta":
            await query.message.reply_text("Send metadata (e.g., title=My Video;comment=Test):")
            users_collection.update_one({"user_id": user_id}, {"$set": {"pending": "metadata"}})
        elif param == "thumb":
            await query.message.reply_text("Send an image for thumbnail:")
            users_collection.update_one({"user_id": user_id}, {"$set": {"pending": "thumbnail"}})
    elif data[0] == "toggle":
        current = users_collection.find_one({"user_id": user_id})["auto_rename"]
        users_collection.update_one({"user_id": user_id}, {"$set": {"auto_rename": not current}})
        await query.message.reply_text(f"Auto Rename set to: {not current}")
    elif data[0] == "pos":
        pos = "_".join(data[2:])
        users_collection.update_one({"user_id": user_id}, {"$set": {"watermark_pos": pos}})
        await query.message.reply_text(f"Watermark position set to: {pos}")

# Handle text input for settings
@app.on_message(filters.text & ~filters.command(["start", "settings", "help"]))
async def handle_text(client, message):
    user_id = message.from_user.id
    user_data = users_collection.find_one({"user_id": user_id})
    if user_data and "pending" in user_data:
        pending = user_data["pending"]
        if pending == "watermark":
            users_collection.update_one({"user_id": user_id}, {"$set": {"watermark": message.text}})
            buttons = [[InlineKeyboardButton(pos, callback_data=f"pos_{user_id}_{pos}")] for pos in WATERMARK_POSITIONS]
            await message.reply_text(
                "Choose watermark position:",
                reply_markup=InlineKeyboardMarkup(buttons)
            )
        elif pending in ["crf", "quality", "rename_pattern", "caption_pattern", "metadata"]:
            users_collection.update_one({"user_id": user_id}, {"$set": {pending: message.text}})
            await message.reply_text(f"{pending.capitalize()} set to: {message.text}")
        users_collection.update_one({"user_id": user_id}, {"$unset": {"pending": ""}})

# Handle thumbnail image
@app.on_message(filters.photo)
async def handle_thumbnail(client, message):
    user_id = message.from_user.id
    user_data = users_collection.find_one({"user_id": user_id})
    if user_data and user_data.get("pending") == "thumbnail":
        file = await message.download()
        users_collection.update_one({"user_id": user_id}, {"$set": {"thumbnail": file}})
        await message.reply_text("Thumbnail set!")
        users_collection.update_one({"user_id": user_id}, {"$unset": {"pending": ""}})

if __name__ == "__main__":
    register_commands(app)
    threading.Thread(target=run_flask, daemon=True).start()
    app.run()
