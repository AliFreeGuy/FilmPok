from celery import shared_task
from core.models import ServersModel
from django.utils import timezone
import logging
from django.conf import settings
import paramiko
import os
from core.utils import ServerMonitoring



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
    PORT = 22
    USERNAME = server.username
    PASSWORD = server.password
    IP_SERVER = server.ip
    AUTH_TOKEN = server.user_auth_token
    API_URL = f'{settings.SITE_URL}/api/server-monitoring/' 
    SERVER_MONITOR_FILE_PATH = os.path.join(settings.STATIC_ROOT, 'server_monitor.zip')
    server_manager = ServerMonitoring(HOSTNAME, PORT, USERNAME, PASSWORD, SERVER_MONITOR_FILE_PATH, IP_SERVER, API_URL, AUTH_TOKEN , server)
    server_manager.setup()
    server_manager.disconnect()
    logger.info(f'Restarting server with ID {server_id}.')









