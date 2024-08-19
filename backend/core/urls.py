from django.urls import path
from . import views


app_name = 'core'

urlpatterns = [
    path('setting/' , views.SettingAPIView.as_view() , name='bot-setting'),
    path('file/', views.FileCreateUpdateView.as_view(), name='file-create-update'),


]