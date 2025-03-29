import motor.motor_asyncio

from config import MONGO_URL, DATABASE_NAME

class Database:
    def __init__(self):
        self._client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URL)
        self.db = self._client[DATABASE_NAME]
        self.users = self.db["users"]

    async def add_user(self, user_id, username, name):
        user_data = {"user_id": user_id, "username": username, "name": name}
        await self.users.insert_one(user_data)

    async def get_user(self, user_id):
        user = await self.users.find_one({"user_id": user_id})
        return user

    async def update_user(self, user_id, crf=None, watermark=None, codec=None, audio_codec=None, quality=None, auto_rename=None, auto_rename_format=None, caption_format=None, thumbnail=None, metadata=None, watermark_position=None):
        update_data = {}
        if crf is not None:
            update_data["crf"] = crf
        if watermark is not None:
            update_data["watermark"] = watermark
        if codec is not None:
            update_data["codec"] = codec
        if audio_codec is not None:
            update_data["audio_codec"] = audio_codec
        if quality is not None:
            update_data["quality"] = quality
        if auto_rename is not None:
            update_data["auto_rename"] = auto_rename
        if auto_rename_format is not None:
            update_data["auto_rename_format"] = auto_rename_format
        if caption_format is not None:
            update_data["caption_format"] = caption_format
        if thumbnail is not None:
            update_data["thumbnail"] = thumbnail
        if metadata is not None:
            update_data["metadata"] = metadata
        if watermark_position is not None:
            update_data["watermark_position"] = watermark_position

        await self.users.update_one({"user_id": user_id}, {"$set": update_data}, upsert=True)

DB = Database()
