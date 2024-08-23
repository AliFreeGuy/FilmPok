from pyrogram import Client, filters
from utils import logger , cache  , utils
from config import con
from pyrogram.errors import MessageNotModified



@Client.on_message(filters.private & utils.is_admin ,group=0 )
async def file_setting_manager(bot, msg):

    if not msg.text :
            
        caption_parser = utils.analyze_text(msg.caption)
        setting = con.setting
        backup_channel = setting.backup_channel
        print(setting)
        if backup_channel :

            message = await msg.copy(backup_channel.chat_id)
            setting = con.setting
            user_chat_id = msg.from_user.id
            file_ids = await utils.get_file_ids(message)
            unique_id_hash = utils.get_hash(message)
            name = utils.get_name(message)
            mime_type = file_ids.mime_type if file_ids.mime_type else file_ids.file_type
            duration = None
            if file_ids.duration:
                try:
                    duration = int(file_ids.duration)
                except ValueError:
                    duration = None


            file_update = con.file(
                channel_chat_id=backup_channel.chat_id,
                user_chat_id=user_chat_id,
                name=name,
                message_id=message.id,
                media_type=mime_type,
                unique_id_hash=unique_id_hash,
                size=file_ids.file_size,
                duration=duration,
                quality=caption_parser.get('quality', None),
                subtitle_status=caption_parser.get('sub', None)
            )
            
           
            await msg.reply_text(
                            utils.file_information_text(setting=setting , file_update=file_update) , 
                            quote = True  ,
                            reply_markup = utils.file_btn(file_update , setting ))

            
        
        
    



@Client.on_callback_query( utils.is_admin,group=0)
async def call_file_setting_manager(bot , call  ):
    setting = con.setting
    status = call.data.split('_')[0]
    unique_id_hash = call.data.split(':')[1]
    data = call.data.split('_')[1].split(':')[0]
    file_data = con.file(unique_id_hash = unique_id_hash  , channel_chat_id=setting.backup_channel.chat_id , user_chat_id=call.from_user.id)



    if file_data :

        if status == 'quality'  :
            file_data = con.file(unique_id_hash = unique_id_hash  ,quality=data , channel_chat_id=setting.backup_channel.chat_id , user_chat_id=call.from_user.id)
            
        elif status == 'sub' :
            file_data = con.file(unique_id_hash = unique_id_hash  ,subtitle_status=data , channel_chat_id=setting.backup_channel.chat_id , user_chat_id=call.from_user.id)
            
        try :

            await bot.edit_message_text(chat_id = call.from_user.id , 
                                            text = utils.file_information_text(file_data , setting),
                                            message_id = call.message.id ,
                                            reply_markup = utils.file_btn(file_data , setting))
            
        except MessageNotModified  as e :logger.info(e)
            
           





