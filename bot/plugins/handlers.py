from pyrogram import Client, filters
from utils import logger , cache  , utils
from utils import filters as f
from config import con
import json



@Client.on_message(filters.private &f.is_admin ,group=0 )
async def admin_panel_handler(bot, msg):

    user_chat_id = msg.from_user.id
    file_ids = await utils.get_file_ids(msg)
    unique_id_hash = utils.get_hash(msg)
    name = utils.get_name(msg)
    mime_type = file_ids.mime_type if file_ids.mime_type else file_ids.file_type

    data = con.file(
                        channel_chat_id=-1002181514673 ,
                        user_chat_id=user_chat_id ,
                        ext='kkkkk',
                        name=name  ,
                        message_id=333 ,
                        media_type = mime_type  ,
                        raw_message=repr(msg) ,
                        unique_id_hash=unique_id_hash ,
                        size=file_ids.file_size,
                        duration=file_ids.duration,
                        
                 )
    

    print(data)