from pyrogram import Client, filters
from utils import logger , cache 
from utils import filters as f
from config import con






@Client.on_message(
                    filters.private &
                    filters.command('start') &
                    f.is_admin 
                    , group=0 
                )
async def admin_panel_handler(bot, msg):
    await bot.send_message(msg.from_user.id , f'hi user')