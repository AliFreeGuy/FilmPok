from django.db.models.signals import post_save , pre_save
from django.dispatch import receiver
from core import models , tasks
from .models import ChannelsModel





@receiver(pre_save, sender=ChannelsModel)
def check_backup_status(sender, instance, **kwargs):
    if not instance.pk:
        if instance.backup_status :
            tasks.backup_channel_task.delay_on_commit(instance.id)
        return

    previous_instance = ChannelsModel.objects.get(pk=instance.pk)
    if not previous_instance.backup_status and instance.backup_status:
        tasks.backup_channel_task.delay_on_commit(instance.id)
    return
