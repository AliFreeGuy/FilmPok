from celery import shared_task
import logging
from pyrogram import Client 
from django.conf import settings
from core import models
import time
from pyrogram.errors import FloodWait
import random

logger = logging.getLogger(__name__)


@shared_task
def backup_channel_task(backup_channel_id):
    setting = models.SettingModel.objects.first()
    backup_channel = models.ChannelsModel.objects.filter(id=backup_channel_id).first()
    source_backup_channel = setting.backup_channel
    backup_channel_files = list(source_backup_channel.files.all())
    file_chunks = [backup_channel_files[i:i + setting.backup_files_chunk] for i in range(0, len(backup_channel_files), setting.backup_files_chunk)]

    backup_channel_bots = list(backup_channel.bots.filter(is_active=True))
    num_bots = len(backup_channel_bots)

    bot_file_lists = {bot: [] for bot in backup_channel_bots}
    
    for index, chunk in enumerate(file_chunks):
        bot = backup_channel_bots[index % num_bots] 
        bot_file_lists[bot].append(chunk)
    
    logger.info('Backup operation was started')
    for bot, files in bot_file_lists.items():
        api_id = bot.api_id
        api_hash = bot.api_hash
        bot_token = bot.bot_token
        session_name = f'backup_session_{str(random.randint(0, 10000))}'
        bot = Client(session_name, api_id=api_id, api_hash=api_hash, bot_token=bot_token, proxy=settings.PROXY)

        backup_channel.refresh_from_db()
        if not backup_channel.backup_status:
            logger.warning(f'Backup operation was stopped by the admin. Task is terminating.')
            return 

        for file_pack in files:
            with bot:
                for file in file_pack:
                    backup_channel.refresh_from_db()
                    if not backup_channel.backup_status:
                        logger.warning(f'Backup operation was stopped by the admin. Task is terminating.')
                        return 
                    
                    try:
                        messages = bot.get_messages(chat_id=int(source_backup_channel.chat_id), message_ids=file.message_id)
                        backuped_message = messages.copy(backup_channel.chat_id)
                        file.channel = backup_channel
                        file.message_id = backuped_message.id
                        file.save()
                        backup_channel.remaining_messages = len(source_backup_channel.files.all())
                        backup_channel.save()
                        logger.info(f'Copied the file with message name {file.name} in channel {backup_channel.name}')
                        time.sleep(random.randint(0, 2))
                    
                    except FloodWait as e:
                        logger.warning(f'*** FloodWait: {str(e.value)} SEC ***')
                        time.sleep(e.value)
                
                logger.info(f'*** SLEEP: {str(setting.backup_files_sleep)} ***')
                time.sleep(random.randint(0, setting.backup_files_sleep))
                
    logger.info('Backup operation completed')
