from django.contrib import admin
from .models import ChannelsModel, ServersModel, SettingModel, FilesModel, BotsModel
from django.utils.html import format_html
import jdatetime



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







@admin.register(BotsModel)
class BotsAdmin(admin.ModelAdmin):
    list_display = ('username', 'bot_token', 'api_id', 'is_active', 'creation')
    search_fields = ('username', 'bot_token')
    list_filter = ('is_active', 'creation')
    readonly_fields = ('creation',)
    ordering = ('-creation',)





@admin.register(FilesModel)
class FilesModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'channel_name', 'user_name', 'quality', 'media_type', 'size','duration', 'subtitle_status', 'creation_shamsi')
    list_filter = ('quality', 'media_type', 'subtitle_status', 'creation', 'channel')
    search_fields = ('name', 'unique_id_hash', 'unique_url_path', 'channel__name', 'user__chat_id' , 'user__full_name')
    ordering = ('-creation',)
    readonly_fields = ('creation', 'creation_shamsi')

    fieldsets = (
        (None, {
            'fields': (
                'name', 'ext', 'quality', 'media_type', 'size' ,'duration',
                'message_id', 'unique_id_hash', 'unique_url_path',
                'subtitle_status', 'channel', 'user', 'raw_message', 'creation'
            )
        }),
     
    )

    def channel_name(self, obj):
        return obj.channel.name
    channel_name.short_description = 'Channel'

    def user_name(self, obj):
        return f'{obj.user.full_name} ({obj.user.chat_id})'
    user_name.short_description = 'User'

    def creation_shamsi(self, obj):
        return jdatetime.datetime.fromgregorian(datetime=obj.creation).strftime('%Y/%m/%d %H:%M:%S')
    creation_shamsi.short_description = 'Creation Date'

    def has_add_permission(self, request):
        return True

    def has_change_permission(self, request, obj=None):
        return True

    def has_delete_permission(self, request, obj=None):
        return True

    def has_view_permission(self, request, obj=None):
        return True

