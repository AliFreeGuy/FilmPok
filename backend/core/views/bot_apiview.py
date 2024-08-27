from rest_framework.authentication import TokenAuthentication
from rest_framework import status, permissions
from django.urls import reverse
from core import serializers, models , tasks
from django.http import  HttpResponseRedirect
from django.contrib.auth.decorators import user_passes_test
from django.utils.decorators import method_decorator
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from core.models import FilesModel, ChannelsModel
import logging
from django.views import View


logger = logging.getLogger('core')



class SettingAPIView(APIView):
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        logger.info('Received GET request for settings.')

        try:
            setting = models.SettingModel.objects.first()
            if setting is None:
                logger.warning('No settings found.')
                return Response({'error': 'Settings not found.'}, status=status.HTTP_404_NOT_FOUND)
            
            setting_data = serializers.SettingSerializer(setting).data
            logger.info('Successfully retrieved settings.')
            return Response(setting_data, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error('An error occurred while retrieving settings: %s', str(e))
            return Response({'error': 'Internal server error.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)






class FileCreateOrUpdateAPIView(APIView):
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        unique_id_hash = request.data.get('unique_id_hash')
        logger.info('Received POST request to create or update file with unique_id_hash: %s', unique_id_hash)

        try:
            file_instance = FilesModel.objects.get(unique_id_hash=unique_id_hash)
            serializer = serializers.FilesModelSerializer(file_instance, data=request.data, partial=True)
            logger.info('Updating existing file instance.')
        except FilesModel.DoesNotExist:
            serializer = serializers.FilesModelSerializer(data=request.data)
            logger.info('Creating new file instance.')

        if serializer.is_valid():
            serializer.save()
            status_code = status.HTTP_200_OK if 'file_instance' in locals() else status.HTTP_201_CREATED
            logger.info('File instance saved successfully.')
            return Response(serializer.data, status=status_code)
        
        logger.error('File instance save failed: %s', serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





class FileChannelAPIView(APIView):
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        channel_id = request.data.get('channel')
        message_id = request.data.get('message_id')

        logger.info('Received POST request to create FileChannel with channel_id: %s and message_id: %s', channel_id, message_id)

        if not channel_id or not message_id:
            logger.warning('Missing required fields: channel_id or message_id.')
            return Response({'error': 'channel and message_id are required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            channel = ChannelsModel.objects.get(id=channel_id)
        except ChannelsModel.DoesNotExist:
            logger.warning('Channel with id %s not found.', channel_id)
            return Response({'error': 'Channel not found.'}, status=status.HTTP_400_BAD_REQUEST)

        if models.FileChannelModel.objects.filter(message_id=message_id, channel=channel).exists():
            logger.warning('FileChannelModel instance with message_id %s already exists.', message_id)
            return Response({'error': 'FileChannelModel instance already exists.'}, status=status.HTTP_400_BAD_REQUEST)

        logger.info('FileChannelModel instance creation parameters are valid.')
        return Response({'status': 'Valid request.'}, status=status.HTTP_200_OK)






class FileChannelAPIView(APIView):
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        chat_id = request.data.get('chat_id')
        message_id = request.data.get('message_id')

        logger.info('Received POST request to create FileChannel with chat_id: %s and message_id: %s', chat_id, message_id)

        if not chat_id or not message_id:
            logger.warning('Missing required fields: chat_id or message_id.')
            return Response({'error': 'chat_id and message_id are required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            channel = ChannelsModel.objects.get(chat_id=chat_id)
        except ChannelsModel.DoesNotExist:
            logger.warning('Channel with chat_id %s not found.', chat_id)
            return Response({'error': 'Channel with the provided chat_id not found.'}, status=status.HTTP_400_BAD_REQUEST)

        if models.FileChannelModel.objects.filter(message_id=message_id, channel=channel).exists():
            logger.warning('FileChannelModel instance with message_id %s already exists.', message_id)
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
            logger.info('FileChannelModel instance created successfully with id %s.', file_channel_instance.id)
            return Response(response_data, status=status.HTTP_200_OK)
        
        logger.error('FileChannelModel instance creation failed: %s', serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class UpdateServerView(APIView):
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        ip = request.data.get('ip')
        traffic_usage = request.data.get('traffic_usage')
        cpu_usage = request.data.get('cpu_usage')
        memory_usage = request.data.get('memory_usage')

        try:
            server = models.ServersModel.objects.get(ip=ip)
        except models.ServersModel.DoesNotExist:
            return Response({"detail": "Server not found."}, status=status.HTTP_404_NOT_FOUND)

        if traffic_usage is not None:
            server.traffic_usage = traffic_usage
        if cpu_usage is not None:
            server.cpu_usage = cpu_usage
        if memory_usage is not None:
            server.memory_usage = memory_usage
        
        server.save()

        updated_data = {
            "ip": server.ip,
            "traffic_usage": server.traffic_usage,
            "cpu_usage": server.cpu_usage,
            "memory_usage": server.memory_usage,
            "is_active": server.is_active,
            "expiry": server.expiry
        }

        return Response({"detail": "Server updated successfully.", "updated_data": updated_data}, status=status.HTTP_200_OK)





def user_is_superuser(user):
    return user.is_superuser

@method_decorator(user_passes_test(user_is_superuser), name='dispatch')
class RestartServerView(View):
    def get(self, request, pk, *args, **kwargs):
        try:
            server = models.ServersModel.objects.filter(pk=pk).first()
            
            if server:
                tasks.server_monitor_runner.delay_on_commit(server.id)
                logger.info("Server with ID %d restarted successfully.", server.id)
            else:
                logger.warning("Server with ID %d not found.", pk)
        except Exception as e:
            logger.error("Error restarting server with ID %d: %s", pk, str(e))
        
        return HttpResponseRedirect(reverse('admin:core_serversmodel_change', args=[pk]))
