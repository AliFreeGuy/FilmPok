from rest_framework.authentication import TokenAuthentication
from rest_framework import status, permissions
from core import serializers, models
from django.http import JsonResponse
from accounts.models import User
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from core.models import FilesModel, ChannelsModel
from accounts.models import User




class SettingAPIView(APIView):
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        setting = models.SettingModel.objects.first()
        setting_data = serializers.SettingSerializer(setting).data
        return Response(setting_data, status=status.HTTP_200_OK)





class FileCreateOrUpdateAPIView(APIView):
    def post(self, request):
        unique_id_hash = request.data.get('unique_id_hash')
        try:
            file_instance = FilesModel.objects.get(unique_id_hash=unique_id_hash)
            serializer = serializers.FilesModelSerializer(file_instance, data=request.data, partial=True)
        except FilesModel.DoesNotExist:
            serializer = serializers.FilesModelSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK if 'file_instance' in locals() else status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FileChannelAPIView(APIView):
    def post(self, request):
        channel_id = request.data.get('channel')
        message_id = request.data.get('message_id')

        if not channel_id or not message_id:
            return Response({'error': 'channel and message_id are required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            channel = ChannelsModel.objects.get(id=channel_id)
        except ChannelsModel.DoesNotExist:
            return Response({'error': 'Channel not found.'}, status=status.HTTP_400_BAD_REQUEST)

        # بررسی وجود نمونه
        if models.FileChannelModel.objects.filter(message_id=message_id, channel=channel).exists():
            return Response({'error': 'FileChannelModel instance already exists.'}, status=status.HTTP_400_BAD_REQUEST)






class FileChannelAPIView(APIView):
    def post(self, request):
        chat_id = request.data.get('chat_id')
        message_id = request.data.get('message_id')

        if not chat_id or not message_id:
            return Response({'error': 'chat_id and message_id are required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            channel = ChannelsModel.objects.get(chat_id=chat_id)
        except ChannelsModel.DoesNotExist:
            return Response({'error': 'Channel with the provided chat_id not found.'}, status=status.HTTP_400_BAD_REQUEST)

        if models.FileChannelModel.objects.filter(message_id=message_id, channel=channel).exists():
            return Response({'error': 'FileChannelModel instance already exists.'}, status=status.HTTP_400_BAD_REQUEST)

        data = {
            'message_id': message_id,
            'channel': channel.id  
        }
        serializer = serializers.FileChannelModelSerializer(data=data)

        if serializer.is_valid():
            file_channel_instance = serializer.save()
            response_data = serializer.data
            response_data['id'] = file_channel_instance.id
            return Response(response_data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
