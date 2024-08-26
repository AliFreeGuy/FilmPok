from django.urls import path
from . import views


app_name = 'core'

urlpatterns = [
    path('setting/' , views.SettingAPIView.as_view() , name='bot-setting'),
    path('files/', views.FileCreateOrUpdateAPIView.as_view(), name='file-create-update'),
    path('save-file-channel/', views.FileChannelAPIView.as_view(), name='save-file-channel'),

    path('server-monitoring/' , views.UpdateServerView.as_view() , name='server-monitoring')
            ]