from celery import shared_task
from core.models import ServersModel
from django.utils import timezone
import logging

logger = logging.getLogger('core')


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
