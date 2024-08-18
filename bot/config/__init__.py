# Bot Configs

from dotenv import load_dotenv
from utils.connection import Connection
load_dotenv(override = True)
from utils.cache import *
from utils.logger import logger
from os import environ as env


API_KEY = env.get('API_KEY')
API_URL = env.get('API_URL')
con = Connection(api_key=API_KEY, api_url=API_URL)
setting = con.setting

logger.info(f'bot username : {setting.admin_bot.username}')
logger.info(f'website url : {setting.website_url}')
API_ID = setting.admin_bot.api_id
API_HASH = setting.admin_bot.api_hash
BOT_TOKEN = setting.admin_bot.bot_token
BOT_USERNAME = setting.admin_bot.username
WORK_DIR = env.get('WORK_DIR') or '/tmp'
PROXY = {"scheme": env.get("PROXY_SCHEME"),
         "hostname": env.get("PROXY_HOSTNAME"),
         "port": int(env.get("PROXY_PORT"))}
DEBUG = env.get('BOT_DEBUG')
REDIS_HOST = env.get('REDIS_HOST')
REDIS_PORT = env.get('REDIS_PORT')
REDIS_DB= env.get('REDIS_DB')
REDIS_PASS = env.get('REDIS_PASS')