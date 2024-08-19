from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework import status, permissions
from core import serializers, models
from accounts.models import User
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from core.models import FilesModel, ChannelsModel
from accounts.models import User
from core.serializers import FilesSerializer




class SettingAPIView(APIView):
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        setting = models.SettingModel.objects.first()
        setting_data = serializers.SettingSerializer(setting).data
        return Response(setting_data, status=status.HTTP_200_OK)









class FileCreateUpdateView(APIView):

    def post(self, request, *args, **kwargs):
        data = request.data.copy()  

        try:
            channel = ChannelsModel.objects.get(chat_id=data.get('channel_chat_id'))
        except ChannelsModel.DoesNotExist:
            return Response({"error": "Channel not found."}, status=status.HTTP_404_NOT_FOUND)

        # جستجوی یوزر با chat_id
        try:
            user = User.objects.get(chat_id=data.get('user_chat_id'))
        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        # افزودن کانال و یوزر به داده‌های ورودی
        data['channel'] = channel.id
        data['user'] = user.id

        # جستجوی فایل با unique_id_hash
        file_instance = FilesModel.objects.filter(unique_id_hash=data.get('unique_id_hash')).first()

        # اگر فایل وجود داشت، به‌روز رسانی شود
        if file_instance:
            serializer = FilesSerializer(file_instance, data=data, partial=True)
        else:
            # اگر فایل وجود نداشت، یک فایل جدید ایجاد شود
            serializer = FilesSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        unique_id_hash = request.data.get('unique_id_hash')

        if not unique_id_hash:
            return Response({"error": "unique_id_hash is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            file_instance = FilesModel.objects.get(unique_id_hash=unique_id_hash)
            file_instance.delete()
            return Response({"message": "File deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
        except FilesModel.DoesNotExist:
            return Response({"error": "File not found."}, status=status.HTTP_404_NOT_FOUND)
