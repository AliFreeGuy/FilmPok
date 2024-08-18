from pyrogram import filters
import config



async def is_admin(_ , cli , msg ):
    admins  = [int(admin.chat_id) for admin in config.con.setting.admin_users]
    if msg.from_user.id in admins :
        return True
    return False



is_admin = filters.create(is_admin)