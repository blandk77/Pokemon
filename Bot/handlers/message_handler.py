
import os
import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from config import DEFAULT_CRF, DEFAULT_CODEC, DEFAULT_AUDIO_CODEC, DUMP_CHANNEL_ID
from Bot.database import DB
from Bot.utils import ffmpeg_utils, helpers

def register_handlers(bot: Client):
    @bot.on_message(filters.document | filters.video)
    async def handle_media(client: Client, message: Message):
        user_id = message.from_user.id
        user_data = await DB.get_user(user_id)

        # Check if user has set required settings
        if not user_data or not all(key in user_data for key in ("crf", "codec", "audio_codec")):
            await message.reply_text("Please use /settings and configure CRF, Codec and Audio Codec before sending files.")
            return

        crf = user_data.get("crf") or DEFAULT_CRF
        codec = user_data.get("codec") or DEFAULT_CODEC
        audio_codec = user_data.get("audio_codec") or DEFAULT_AUDIO_CODEC
        quality = user_data.get("quality")
        watermark = user_data.get("watermark")
        watermark_position = user_data.get("watermark_position")
        auto_rename = user_data.get("auto_rename")
        auto_rename_format = user_data.get("auto_rename_format")
        caption_format = user_data.get("caption_format")
        thumbnail = user_data.get("thumbnail")
        metadata = user_data.get("metadata")

        file_name = message.document.file_name if message.document else message.video.file_name
        file_size = message.document.file_size if message.document else message.video.file_size
        file_id = message.document.file_id if message.document else message.video.file_id

        # Download the file
        download_location = f"./downloads/{user_id}/{file_name}"
        os.makedirs(f"./downloads/{user_id}", exist_ok=True)

        start_time = asyncio.get_event_loop().time()  # Get current time

        # Function to report progress
        async def progress(current, total):
            time_diff = asyncio.get_event_loop().time() - start_time
            speed = current / time_diff if time_diff > 0 else 0  # Bytes per second
            speed_str = helpers.format_file_size(speed) + "/s"

            percentage = current * 100 / total
            system_stats = helpers.get_system_stats()

            progress_message = f"""
            Downloading: {file_name}
            Progress: {percentage:.2f}%
            Speed: {speed_str}
            CPU: {system_stats['cpu']}% | Memory: {system_stats['memory']}% | Disk: {system_stats['disk']}%
            """
            try:
                await status_message.edit_text(progress_message)
            except:
                pass

        # Send a message to indicate download starting
        status_message = await message.reply_text(f"Downloading {file_name}...")
        await client.download_media(
            message,
            file_name=download_location,
            progress=progress
        )
        download_end_time = asyncio.get_event_loop().time()
        download_time = download_end_time - start_time

        # Get video info
        video_info = ffmpeg_utils.get_video_info(download_location)
        if not video_info:
            await status_message.edit_text("Failed to get video information.  Encoding aborted.")
            return

        # Auto Rename
        if auto_rename:
            episode = helpers.get_episode_number(file_name)
            season = helpers.get_season_number(file_name)
            quality = user_data.get("quality")
            audio_count = video_info["audio_count"]
            audio = helpers.get_audio_type(audio_count)

            new_file_name = auto_rename_format.format(
                filename=file_name,
                episodes=episode if episode else "",
                season=season if season else "",
                quality=quality if quality else "",
                audio=audio
            )

            # Add the original extension to the new filename
            original_extension = os.path.splitext(file_name)[1]
            new_file_name = new_file_name + original_extension

        else:
            new_file_name = file_name

        output_location = f"./encoded/{user_id}/{new_file_name}"
        os.makedirs(f"./encoded/{user_id}", exist_ok=True)

        # Encoding Progress
        async def encoding_progress(current, total):
            percentage = current * 100 / total if total > 0 else 0
            system_stats = helpers.get_system_stats()
            encoding_message = f"""
            Encoding: {new_file_name}
            Progress: {percentage:.2f}%
            CPU: {system_stats['cpu']}% | Memory: {system_stats['memory']}% | Disk: {system_stats['disk']}%
            """
            try:
                await status_message.edit_text(encoding_message)
            except:
                pass

        # Run encoding
        await status_message.edit_text(f"Encoding {new_file_name}...")
        encode_start_time = asyncio.get_event_loop().time()  # Get current time
        if ffmpeg_utils.encode_video(download_location, output_location, crf, codec, audio_codec, quality, watermark, watermark_position, metadata):
            encode_end_time = asyncio.get_event_loop().time()
            encode_time = encode_end_time - encode_start_time
            file_size = os.path.getsize(output_location)  # File size in bytes
            size_str = helpers.format_file_size(file_size)
            await status_message.edit_text(f"Encoding Complete! {size_str}")
            # Upload to Telegram
            await status_message.edit_text(f"Uploading {new_file_name}...")

            start_upload_time = asyncio.get_event_loop().time()  # Get current time

            async def upload_progress(current, total):
                time_diff = asyncio.get_event_loop().time() - start_upload_time
                speed = current / time_diff if time_diff > 0 else 0  # Bytes per second
                speed_str = helpers.format_file_size(speed) + "/s"

                percentage = current * 100 / total
                system_stats = helpers.get_system_stats()

                upload_message = f"""
                Uploading: {new_file_name}
                Progress: {percentage:.2f}%
                Speed: {speed_str}
                CPU: {system_stats['cpu']}% | Memory: {system_stats['memory']}% | Disk: {system_stats['disk']}%
                """
                try:
                    await status_message.edit_text(upload_message)
                except:
                    pass
            try:
                await client.send_document(
                    chat_id=message.chat.id,
                    document=output_location,
                    file_name=new_file_name,
                    caption=f"Filename: {new_file_name}\nFilesize: {size_str}",
                    progress=upload_progress
                )
                await client.send_document(
                    chat_id=DUMP_CHANNEL_ID,
                    document=output_location,
                    file_name=new_file_name,
                    caption=f"Filename: {new_file_name}\nFilesize: {size_str}"
                )
            except Exception as e:
                print(e)
                await status_message.edit_text(f"Upload failed: {e}")
            finally:
                # Clean up files
                try:
                    os.remove(download_location)
                    os.remove(output_location)
                    os.rmdir(f"./downloads/{user_id}")
                    os.rmdir(f"./encoded/{user_id}")
                except Exception as e:
                    print(f"Error cleaning up files: {e}")
        else:
            await status_message.edit_text("Encoding failed. Check logs for errors.")
