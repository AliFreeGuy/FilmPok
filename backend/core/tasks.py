from celery import shared_task
from core.models import ServersModel
from django.utils import timezone
import logging
from django.conf import settings
import random
import paramiko
import os
from core.utils import ServerMonitoring , ServerStreamManager



logger = logging.getLogger('tasks')

@shared_task
def deactivate_expired_servers():
    logger.info('Starting task to deactivate expired servers.')
    now = timezone.now()
    try:
        expired_servers = ServersModel.objects.filter(expiry__lte=now, is_active=True)
        count = expired_servers.count()
        expired_servers.update(is_active=False)
        logger.info(f'Deactivated {count} expired servers.')
    except Exception as e:
        logger.error('An error occurred while deactivating expired servers: %s', str(e))







@shared_task
def server_monitor_runner(server_id):
    server = ServersModel.objects.filter(id=server_id).first()

    logger.info(f'Starting task for run server monitoring with ID {server_id}.')
    HOSTNAME = server.ip
    SSH_PORT = 22
    USERNAME = server.username
    PASSWORD = server.password
    IP_SERVER = server.ip
    AUTH_TOKEN = server.user_auth_token
    API_URL = f'{settings.SITE_URL}/api/server-monitoring/' 
    SERVER_MONITOR_FILE_PATH = os.path.join(settings.STATIC_ROOT, 'server_monitor.zip')
    server_manager = ServerMonitoring(HOSTNAME, SSH_PORT, USERNAME, PASSWORD, SERVER_MONITOR_FILE_PATH, IP_SERVER, API_URL, AUTH_TOKEN , server)
    server_manager.setup()
    server_manager.disconnect()
    logger.info(f'Restarting server with ID {server_id}.')




    # Define constants for server connection and file paths
 
    DOCKER_PORT = server.port
    FQDN = server.ip
    HAS_SSL = 'False'
    SERVER_STREAMER_FILE_PATH = os.path.join(settings.STATIC_ROOT, 'server_streamer.zip')
    main_bot = random.choice(server.bots.all())
    API_ID = main_bot.api_id
    API_HASH = main_bot.api_hash
    BOT_TOKEN = main_bot.bot_token
    MULTI_TOKENS = [bot.bot_token for bot in server.bots.all()]
    BACKUP_CHANNELS = [str(channel.chat_id) for channel in server.channels.all()]
    BIN_CHANNEL = BACKUP_CHANNELS[0]

    server_stream_manager = ServerStreamManager(
        HOSTNAME, SSH_PORT, USERNAME, PASSWORD, SERVER_STREAMER_FILE_PATH,
        API_ID, API_HASH, BOT_TOKEN, MULTI_TOKENS, BACKUP_CHANNELS, BIN_CHANNEL,
        DOCKER_PORT, FQDN, HAS_SSL ,server
    )
    server_stream_manager.setup()
    server_stream_manager.disconnect()








