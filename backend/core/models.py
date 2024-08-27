from django.db import models
from accounts.models import User
from django.core.exceptions import ValidationError
from datetime import timedelta
from django.utils import timezone

class ChannelsModel(models.Model):
    is_active = models.BooleanField(default=False)
    chat_id = models.BigIntegerField(unique=True)
    name = models.CharField(max_length=28)
    bots = models.ManyToManyField('BotsModel' , related_name='channel' )
    creation = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.name
    
    class Meta :
        verbose_name = "Channels"
        verbose_name_plural = "Channels"



class FileChannelModel(models.Model):
    message_id = models.PositiveIntegerField()
    channel = models.ForeignKey(ChannelsModel, related_name='filechannel', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('message_id', 'channel')

    def __str__(self) -> str:
        return f'{str(self.message_id)} - {self.channel}'





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

    channel = models.ManyToManyField(FileChannelModel, related_name='files')
    user = models.ForeignKey(User, related_name='files', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    quality = models.CharField(max_length=5, choices=QUALITY_CHOICES, blank=True)
    media_type = models.CharField(max_length=50, blank=True)
    size = models.PositiveBigIntegerField(default=0)
    duration = models.PositiveBigIntegerField(default=0 )
    unique_id_hash = models.CharField(max_length=64, unique=True)
    unique_url_path = models.CharField(max_length=64, unique=True)
    subtitle_status = models.CharField(max_length=10, choices=SUBTITLE_STATUS_CHOICES , null=True , blank=True)
    creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Files"
        verbose_name_plural = "Files"



class ServersModel(models.Model):
    is_active = models.BooleanField(default=False)
    web_url = models.CharField(default='http://127.0.0.0:8000' , max_length=128)
    ip = models.CharField(max_length=128, unique=True)
    username = models.CharField(max_length=128)
    password = models.CharField(max_length=128)
    port = models.PositiveBigIntegerField(default=80)
    user_auth_token = models.CharField(max_length=256 , default='your authentiaction toke user')
    bots = models.ManyToManyField('BotsModel', related_name='server')
    channels = models.ManyToManyField('ChannelsModel', related_name='server')
    allowed_traffic = models.PositiveBigIntegerField()
    traffic_usage = models.FloatField(default=0.0)
    cpu_usage = models.FloatField(default=0.0)
    memory_usage = models.FloatField(default=0.0)
    renew_day = models.PositiveBigIntegerField(default=30)
    expiry = models.DateTimeField(null=True , blank=True)

    class Meta:
        verbose_name = "Servers"
        verbose_name_plural = "Servers"

    def save(self, *args, **kwargs):

        self.expiry = timezone.now() + timedelta(days=self.renew_day)
        
        if self.traffic_usage >= self.allowed_traffic:
            self.is_active = False

        super().save(*args, **kwargs)






class SettingModel(models.Model):
    admin_bot = models.OneToOneField('BotsModel' , related_name='setting' , on_delete=models.CASCADE)
    website_url = models.CharField(max_length=256 )
    backup_channel = models.ForeignKey(ChannelsModel , related_name='setting' , on_delete=models.CASCADE , blank=True , null=True)
    
    class Meta :
        verbose_name = "Setting"
        verbose_name_plural = "Setting"




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