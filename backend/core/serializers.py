from rest_framework import serializers
from .models import SettingModel, BotsModel, FilesModel ,ChannelsModel ,FileChannelModel
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





class FilesModelSerializer(serializers.ModelSerializer):
    user = serializers.CharField(write_only=True)  
    class Meta:
        model = FilesModel
        fields = '__all__'
        extra_kwargs = {
            'user': {'write_only': True},
            'unique_url_path': {'read_only': True}  
        }

    def validate_user(self, value):
        try:
            user = User.objects.get(chat_id=value)
        except User.DoesNotExist:
            raise serializers.ValidationError("User with this chat_id does not exist.")
        return user

    def create(self, validated_data):
        validated_data['unique_url_path'] = str(uuid.uuid4())
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        return super().update(instance, validated_data)





class FileChannelModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileChannelModel
        fields = ['id', 'message_id', 'channel']  # اضافه کردن فیلد 'id'