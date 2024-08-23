from django.contrib import admin
from .models import ChannelsModel, ServersModel, SettingModel, FilesModel, BotsModel  ,FileChannelModel
import jdatetime



@admin.register(FileChannelModel)
class FileChannelAdmin(admin.ModelAdmin):
    list_display = ('id', 'message_id', 'channel_name')
    search_fields = ('message_id', 'channel__name')
    list_filter = ('channel',)
    ordering = ('-message_id',)
    readonly_fields = ('channel_name',)

    def channel_name(self, obj):
        return obj.channel.name
    channel_name.short_description = 'Channel Name'

@admin.register(ChannelsModel)
class ChannelsAdmin(admin.ModelAdmin):
    list_display = ('name', 'chat_id', 'is_active', 'creation_shamsi')
    search_fields = ('name', 'chat_id')
    list_filter = ( 'is_active', 'creation')
    readonly_fields = ('creation_shamsi',)
    ordering = ('-creation',)

    def creation_shamsi(self, obj):
        return jdatetime.datetime.fromgregorian(datetime=obj.creation).strftime('%Y/%m/%d %H:%M:%S')
    creation_shamsi.short_description = 'Creation Date'

@admin.register(ServersModel)
class ServersAdmin(admin.ModelAdmin):
    list_display = ('ip', 'username', 'allowed_traffic', 'traffic_usage', 'cpu_usage', 'memory_usage', 'disk_usage', 'creation_shamsi')
    search_fields = ('ip', 'username')
    list_filter = ('creation',)
    readonly_fields = ('creation_shamsi',)
    filter_horizontal = ('bots',)
    ordering = ('-creation',)

    def creation_shamsi(self, obj):
        return jdatetime.datetime.fromgregorian(datetime=obj.creation).strftime('%Y/%m/%d %H:%M:%S')
    creation_shamsi.short_description = 'Creation Date'

@admin.register(SettingModel)
class SettingAdmin(admin.ModelAdmin):
    list_display = ('admin_bot', 'website_url', 'backup_channel')
    search_fields = ('admin_bot__username', 'website_url', 'backup_channel__name')
    ordering = ('admin_bot',)

@admin.register(BotsModel)
class BotsAdmin(admin.ModelAdmin):
    list_display = ('username', 'bot_token', 'api_id', 'is_active', 'creation_shamsi')
    search_fields = ('username', 'bot_token')
    list_filter = ('is_active', 'creation')
    readonly_fields = ('creation_shamsi',)
    ordering = ('-creation',)

    def creation_shamsi(self, obj):
        return jdatetime.datetime.fromgregorian(datetime=obj.creation).strftime('%Y/%m/%d %H:%M:%S')
    creation_shamsi.short_description = 'Creation Date'

@admin.register(FilesModel)
class FilesModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'channel_name', 'user_name', 'quality', 'media_type', 'size', 'duration', 'subtitle_status', 'creation_shamsi')
    list_filter = ('quality', 'media_type', 'subtitle_status', 'creation', 'channel')
    search_fields = ('name', 'unique_id_hash', 'unique_url_path', 'channel__name', 'user__chat_id', 'user__full_name')
    ordering = ('-creation',)
    readonly_fields = ('creation_shamsi',)

    fieldsets = (
        (None, {
            'fields': (
                'name', 'quality', 'media_type', 'size', 'duration',
                'unique_id_hash', 'unique_url_path', 'subtitle_status',
                'channel', 'user', 'creation_shamsi'
            )
        }),
    )

    def channel_name(self, obj):
        return obj.channel.name if obj.channel else '-'
    channel_name.short_description = 'Channel'

    def user_name(self, obj):
        return f'{obj.user.full_name} ({obj.user.chat_id})' if obj.user else '-'
    user_name.short_description = 'User'

    def creation_shamsi(self, obj):
        return jdatetime.datetime.fromgregorian(datetime=obj.creation).strftime('%Y/%m/%d %H:%M:%S')
    creation_shamsi.short_description = 'Creation Date'
