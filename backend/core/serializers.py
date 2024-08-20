from rest_framework import serializers
from .models import SettingModel, BotsModel, FilesModel ,ChannelsModel
from accounts.models import User
import uuid

class BotsSerializer(serializers.ModelSerializer):
    class Meta:
        model = BotsModel
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class ChannelsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChannelsModel
        fields = '__all__'



class SettingSerializer(serializers.ModelSerializer):
    admin_bot = BotsSerializer(read_only=True)
    admin_users = serializers.SerializerMethodField()
    backup_channels = serializers.SerializerMethodField()
    backup_channel = serializers.SerializerMethodField()

    class Meta:
        model = SettingModel
        fields = ['admin_bot', 'website_url', 'admin_users', 'backup_channels', 'backup_channel']  

    def get_admin_users(self, obj):
        admin_users = User.objects.filter(is_admin=True)  
        return UserSerializer(admin_users, many=True).data

    def get_backup_channels(self, obj):
        backup_channels = ChannelsModel.objects.filter(is_active=True)
        return ChannelsSerializer(backup_channels, many=True).data

    def get_backup_channel(self, obj):
        backup_channel = obj.backup_channel
        if backup_channel:
            return ChannelsSerializer(backup_channel).data
        return None








class FilesSerializer(serializers.ModelSerializer):
    unique_url_path = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = FilesModel
        fields = '__all__'

    def save(self, **kwargs):
        # بررسی اینکه آیا شیء جدید است یا موجود
        if not self.instance:
            # شیء جدید است، بنابراین مقدار unique_url_path را تولید می‌کنیم
            if not self.validated_data.get('unique_url_path'):
                self.validated_data['unique_url_path'] = str(uuid.uuid4())
        else:
            # شیء موجود است، مقدار unique_url_path تغییر نمی‌کند
            if 'unique_url_path' in self.validated_data:
                del self.validated_data['unique_url_path']
        
        # صدا زدن متد save والد
        return super().save(**kwargs)