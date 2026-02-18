from aiogram import Bot
from aiogram.types import Message, FSInputFile
import os


async def download_file(bot: Bot, file_id: str, file_type: str, user_id: int) -> str:
    """Download file from Telegram and save locally"""
    # Create downloads directory if it doesn't exist
    os.makedirs("downloads", exist_ok=True)
    
    # Get file info
    file = await bot.get_file(file_id)
    
    # Generate filename
    extension = file.file_path.split('.')[-1] if '.' in file.file_path else file_type
    filename = f"{user_id}_{file_type}_{file_id}.{extension}"
    file_path = os.path.join("downloads", filename)
    
    # Download file
    await bot.download_file(file.file_path, file_path)
    
    return file_path


async def send_file_to_group(bot: Bot, group_id: str, file_path: str, caption: str = ""):
    """Send file to Telegram group"""
    try:
        file = FSInputFile(file_path)
        
        # Determine file type by extension
        ext = file_path.split('.')[-1].lower()
        
        if ext in ['pdf']:
            await bot.send_document(group_id, file, caption=caption)
        elif ext in ['jpg', 'jpeg', 'png', 'gif']:
            await bot.send_photo(group_id, file, caption=caption)
        elif ext in ['mp3', 'ogg', 'wav', 'm4a']:
            await bot.send_audio(group_id, file, caption=caption)
        elif ext in ['mp4', 'mov', 'avi']:
            await bot.send_video(group_id, file, caption=caption)
        else:
            await bot.send_document(group_id, file, caption=caption)
    except Exception as e:
        print(f"Error sending file: {e}")


async def send_media_to_group(bot: Bot, group_id: int, file_id: str, media_type: str, caption: str = ""):
    """Forward media directly to group without downloading
    Args:
        bot: Bot instance
        group_id: Telegram group chat ID (int, required by Telegram API)
        file_id: Telegram file ID
        media_type: Type of media (photo, audio, voice, video, document)
        caption: Optional caption
    """
    try:
        if media_type == "photo":
            await bot.send_photo(group_id, file_id, caption=caption)
        elif media_type == "audio" or media_type == "voice":
            # Voice messages can be sent as voice or audio
            try:
                await bot.send_voice(group_id, file_id, caption=caption)
            except:
                await bot.send_audio(group_id, file_id, caption=caption)
        elif media_type == "video":
            await bot.send_video(group_id, file_id, caption=caption)
        elif media_type == "document":
            await bot.send_document(group_id, file_id, caption=caption)
    except Exception as e:
        print(f"Error sending media: {e}")
