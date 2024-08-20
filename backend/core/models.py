from django.db import models
from accounts.models import User
import uuid



class ChannelsModel(models.Model):
    chat_id = models.BigIntegerField(unique=True)
    name = models.CharField(max_length=28)
    is_active = models.BooleanField(default=False)
    creation = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.name
    
    class Meta :
        verbose_name = "Channels"
        verbose_name_plural = "Channels"




class ServersModel(models.Model):
    ip = models.CharField(max_length=128 ,unique=True)
    username = models.CharField(max_length=128)
    password = models.CharField(max_length=128)
    bots = models.ManyToManyField('BotsModel' , related_name='server'  )
    allowed_traffic = models.PositiveBigIntegerField()
    traffic_usage = models.FloatField(default=0.0)
    cpu_usage = models.FloatField(default=0.0)
    memory_usage = models.FloatField(default=0.0)
    disk_usage = models.FloatField(default=0.0)
    creation = models.DateTimeField(auto_now_add=True)

    class Meta :
        verbose_name = "Servers"
        verbose_name_plural = "Servers"






class SettingModel(models.Model):
    admin_bot = models.OneToOneField('BotsModel' , related_name='setting' , on_delete=models.CASCADE)
    website_url = models.CharField(max_length=256 )
    backup_channel = models.ForeignKey(ChannelsModel , related_name='setting' , on_delete=models.CASCADE , blank=True , null=True)

    class Meta :
        verbose_name = "Setting"
        verbose_name_plural = "Setting"







class FilesModel(models.Model):
    QUALITY_CHOICES = [
        ('1080p', '1080p'),
        ('720p', '720p'),
        ('480p', '480p'),
        ('360p', '360p'),
        ('240p', '240p'),
        ('144p', '144p'),
    ]

    SUBTITLE_STATUS_CHOICES = [
        ('dubbed', 'Dubbed'),
        ('original', 'Original'), 
        ('hardsub', 'Hardsub'),
    ]

    channel = models.ForeignKey(ChannelsModel, related_name='files', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='files', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    quality = models.CharField(max_length=5, choices=QUALITY_CHOICES, blank=True)
    media_type = models.CharField(max_length=50, blank=True)
    size = models.PositiveBigIntegerField(default=0)
    duration = models.PositiveBigIntegerField(default=0 )
    message_id = models.BigIntegerField()
    unique_id_hash = models.CharField(max_length=64, unique=True)
    unique_url_path = models.CharField(max_length=64, unique=True)
    subtitle_status = models.CharField(max_length=10, choices=SUBTITLE_STATUS_CHOICES , null=True , blank=True)
    raw_message = models.JSONField(null=True, blank=True)
    creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Files"
        verbose_name_plural = "Files"





class BotsModel(models.Model):
    bot_token = models.CharField(max_length=128 , unique=True)
    username = models.CharField(max_length=32, unique=True)
    api_hash = models.CharField(max_length=128)
    api_id = models.PositiveIntegerField()
    is_active  = models.BooleanField(default=True)
    creation = models.DateTimeField(auto_now_add=True)
    
    def __str__(self) -> str:
        return self.username
    
    class Meta :
        verbose_name = "Bots"
        verbose_name_plural = "Bots"