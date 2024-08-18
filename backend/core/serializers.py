from rest_framework import serializers
from .models import SettingModel, BotsModel
from accounts.models import User

class BotsSerializer(serializers.ModelSerializer):
    class Meta:
        model = BotsModel
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class SettingSerializer(serializers.ModelSerializer):
    admin_bot = BotsSerializer(read_only=True)
    admin_users = serializers.SerializerMethodField()

    class Meta:
        model = SettingModel
        fields = '__all__'

    def get_admin_users(self, obj):
        admin_users = User.objects.filter(is_admin=True)  
        return UserSerializer(admin_users, many=True).data
