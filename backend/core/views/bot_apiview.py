from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework import status, permissions
from core import serializers, models

class SettingAPIView(APIView):
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        setting = models.SettingModel.objects.first()
        setting_data = serializers.SettingSerializer(setting).data
        return Response(setting_data, status=status.HTTP_200_OK)
