import hashlib
from pyrogram.types import Message
from pyrogram.file_id import FileId
from typing import Any, Optional, Union
from pyrogram.raw.types.messages import Messages
from datetime import datetime
from pyrogram.types import InlineKeyboardButton , InlineKeyboardMarkup , ReplyKeyboardMarkup , KeyboardButton
import re
from pyrogram import filters
import config




QUALITY_CHOICES = [
    ('1080p', '1080p'),
    ('720p', '720p'),
    ('480p', '480p'),
    ('360p', '360p'),
    ('240p', '240p'),
    ('144p', '144p'),
]

SUBTITLE_STATUS_CHOICES = [
    ('dubbed', 'Dubbed'),
    ('original', 'Original'), 
    ('hardsub', 'Hardsub'),
]



async def is_admin(_ , cli , msg ):
    admins  = [int(admin.chat_id) for admin in config.con.setting.admin_users]
    if msg.from_user.id in admins :return True
    return False
is_admin = filters.create(is_admin)



def file_information_text(file_update , setting):
    message_text = f"""
**File Name:** {file_update.name}
**Subtitle Status:** {file_update.subtitle_status}
**Quality:** {file_update.quality}
**Download Link:** {setting.website_url}/{file_update.unique_url_path}
            """
    return message_text




def file_btn(file_info , setting ):
    unique_id_hash = file_info["unique_id_hash"]
    selected_quality = file_info["quality"]
    selected_subtitle_status = file_info["subtitle_status"]
    quality_btns = []
    subtitle_btns =[]
    buttons = []

    for quality in QUALITY_CHOICES:
            quality_text = f"{'✔️' if quality[0] == selected_quality else ''}{quality[1]}"
            quality_btn = InlineKeyboardButton( text=quality_text.replace('p' , ''),callback_data=f'quality_{quality[0]}:{unique_id_hash}')
            quality_btns.append(quality_btn)

    for subtitle in SUBTITLE_STATUS_CHOICES:
            subtitle_text = f"{'✔️' if subtitle[0] == selected_subtitle_status else ''} {subtitle[1]}"
            subtitle_btn = InlineKeyboardButton(text=subtitle_text,callback_data=f'sub_{subtitle[0]}:{unique_id_hash}')
            subtitle_btns.append(subtitle_btn)

    subtitle_btns.append(InlineKeyboardButton(text='🗂',url=f'{setting.website_url}/admin/core/filesmodel/{file_info.id}/change/'))
    buttons.append(subtitle_btns)
    buttons.append(quality_btns)
    return InlineKeyboardMarkup(buttons)






def analyze_text(text):
    if text :
        duble_pattern = re.compile(r'#دوبله_فارسی|#دوبله\s+فارسی', re.IGNORECASE)
        subtitle_pattern = re.compile(r'#زیرنویس(_چسبیده)?_فارسی', re.IGNORECASE)
        quality_pattern = re.compile(r'\b(1080p|720p|480p|360p|240p|144p)\b', re.IGNORECASE)
        
        if duble_pattern.search(text): content_type = 'dubbed'
        elif subtitle_pattern.search(text):content_type = 'hardsub'
        else:content_type = None  
        
        quality_match = quality_pattern.search(text)
        quality = quality_match.group(0) if quality_match else None
        
        if quality not in dict(QUALITY_CHOICES):quality = None
        if content_type not in dict(SUBTITLE_STATUS_CHOICES):content_type = None
        return {'sub' : content_type ,  'quality' : quality}
    
    return {}





async def parse_file_id(message: "Message") -> Optional[FileId]:
    media = get_media_from_message(message)
    if media:
        return FileId.decode(media.file_id)

async def parse_file_unique_id(message: "Messages") -> Optional[str]:
    media = get_media_from_message(message)
    if media:
        return media.file_unique_id

async def get_file_ids(message : Message) -> Optional[FileId]:
    if message.empty:
        raise None
    media = get_media_from_message(message)
    file_unique_id = await parse_file_unique_id(message)
    file_id = await parse_file_id(message)
    
    setattr(file_id, "file_size", getattr(media, "file_size", 0))
    setattr(file_id, "mime_type", getattr(media, "mime_type", ""))
    setattr(file_id, "file_name", getattr(media, "file_name", ""))
    setattr(file_id, "duration", getattr(media, "duration", ""))
    setattr(file_id, "unique_id", file_unique_id)
    
    return file_id

def get_media_from_message(message: "Message") -> Any:
    media_types = (
        "audio",
        "document",
        "photo",
        "sticker",
        "animation",
        "video",
        "voice",
        "video_note",
    )
    for attr in media_types:
        media = getattr(message, attr, None)
        if media:
            return media


def get_hash(media_msg: Union[str, Message], length: int = 6) -> str:
    if isinstance(media_msg, Message):
        media = get_media_from_message(media_msg)
        unique_id = getattr(media, "file_unique_id", "")
    else:
        unique_id = media_msg
    long_hash = hashlib.sha256(unique_id.encode("UTF-8")).hexdigest()
    return long_hash[:length]




def get_name(media_msg: Union[Message, FileId]) -> str:

    if isinstance(media_msg, Message):
        media = get_media_from_message(media_msg)
        file_name = getattr(media, "file_name", "")

    elif isinstance(media_msg, FileId):
        file_name = getattr(media_msg, "file_name", "")

    if not file_name:
        if isinstance(media_msg, Message) and media_msg.media:
            media_type = media_msg.media.value
        elif media_msg.file_type:
            media_type = media_msg.file_type.name.lower()
        else:
            media_type = "file"

        formats = {
            "photo": "jpg", "audio": "mp3", "voice": "ogg",
            "video": "mp4", "animation": "mp4", "video_note": "mp4",
            "sticker": "webp"
        }

        ext = formats.get(media_type)
        ext = "." + ext if ext else ""

        date = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        file_name = f"{media_type}-{date}{ext}"

    return file_name
