from django.contrib import admin
from .models import ChannelsModel, ServersModel, SettingModel, FilesModel, BotsModel

@admin.register(ChannelsModel)
class ChannelsAdmin(admin.ModelAdmin):
    list_display = ('name', 'chat_id', 'is_active', 'creation')
    search_fields = ('name', 'chat_id')
    list_filter = ('is_active', 'creation')
    readonly_fields = ('creation',)
    ordering = ('-creation',)


@admin.register(ServersModel)
class ServersAdmin(admin.ModelAdmin):
    list_display = ('ip', 'username', 'allowed_traffic', 'traffic_usage', 'cpu_usage', 'memory_usage', 'disk_usage', 'creation')
    search_fields = ('ip', 'username')
    list_filter = ('creation',)
    readonly_fields = ('creation',)
    filter_horizontal = ('bots',)
    ordering = ('-creation',)


@admin.register(SettingModel)
class SettingAdmin(admin.ModelAdmin):
    list_display = ('admin_bot', 'website_url')
    search_fields = ('admin_bot__username', 'website_url')
    ordering = ('admin_bot',)


@admin.register(FilesModel)
class FilesAdmin(admin.ModelAdmin):
    list_display = ('name', 'channel', 'user', 'quality', 'message_id', 'is_dubbed', 'is_subtitled', 'is_hardsub', 'creation')
    search_fields = ('name', 'channel__name', 'user__username', 'unique_id_hash', 'unique_url')
    list_filter = ('quality', 'is_dubbed', 'is_subtitled', 'is_hardsub', 'creation')
    readonly_fields = ('creation',)
    ordering = ('-creation',)


@admin.register(BotsModel)
class BotsAdmin(admin.ModelAdmin):
    list_display = ('username', 'bot_token', 'api_id', 'is_active', 'creation')
    search_fields = ('username', 'bot_token')
    list_filter = ('is_active', 'creation')
    readonly_fields = ('creation',)
    ordering = ('-creation',)
