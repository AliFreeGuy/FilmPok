from django.urls import path
from . import views


app_name = 'core'

urlpatterns = [
    path('' , views.SettingAPIView.as_view() , name='bot_setting'),


]