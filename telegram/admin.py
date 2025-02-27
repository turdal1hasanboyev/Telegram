from django.contrib import admin

from .models import (
    User,
    Chat,
    Message,
    Reaction,
    Contact,
    Notification,
    Call,
    Bot,
    Media,
)


admin.site.site_header = "Telegram Admin Panel"
admin.site.site_title = "Telegram Admin Panel"
admin.site.index_title = "Welcome to Telegram Admin Panel!"


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'phone_number', 'is_bot', 'is_verified', 'last_seen', 'is_premium',)
    search_fields = ('username', 'email', 'phone_number',)
    list_filter = ('is_bot', 'is_verified', 'is_premium', 'language',)
    ordering = ('-last_seen',)
    readonly_fields = ('last_seen',)
    raw_id_fields = ('blocked_users',)

    fieldsets = (
        ("Basic Information", {
            "fields": ('username', 'password', 'first_name', 'last_name', 'email',),
        }),
        ("Profile", {
            "fields": ('phone_number', 'bio', 'profile_photo', 'language', 'status',),
        }),
        ("Permissions", {
            "fields": ('is_active', 'is_staff', 'is_superuser', 'is_bot', 'is_verified', 'is_premium', 'groups', 'user_permissions',),
        }),
        ("Security", {
            "fields": ('two_factor_auth', 'blocked_users',),
        }),
        ("Important Dates", {
            "fields": ('last_seen', 'date_joined', 'last_login',),
        }),
    )

    add_fieldsets = (
        ("Create Superuser", {
            "classes": ('wide',),
            "fields": ('username', 'email', 'password1', 'password2', 'is_staff', 'is_superuser',),
        }),
    )


@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ('name', 'chat_type', 'created_at', 'is_public',)
    search_fields = ('name', 'description',)
    list_filter = ('chat_type', 'is_public',)
    ordering = ('-created_at',)
    filter_horizontal = ('members', 'admin_users', 'pinned_messages',)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'sender', 'chat', 'timestamp', 'is_pinned', 'is_deleted',)
    search_fields = ('text', 'sender__username', 'chat__name',)
    list_filter = ('is_pinned', 'is_deleted', 'edited_at',)
    ordering = ('-timestamp',)
    raw_id_fields = ('sender', 'chat', 'reply_to', 'forwarded_from',)


@admin.register(Reaction)
class ReactionAdmin(admin.ModelAdmin):
    list_display = ('message', 'user', 'emoji', 'created_at',)
    search_fields = ('emoji', 'user__username', 'message__text',)
    list_filter = ('created_at',)
    ordering = ('-created_at',)
    raw_id_fields = ('message', 'user',)


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('user', 'contact', 'created_at', 'is_favorite', 'is_muted',)
    search_fields = ('user__username', 'contact__username',)
    list_filter = ('is_favorite', 'is_muted',)
    ordering = ('-created_at',)


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'text', 'created_at', 'is_read', 'notification_type',)
    search_fields = ('user__username', 'text',)
    list_filter = ('is_read', 'notification_type',)
    ordering = ('-created_at',)
    raw_id_fields = ('user', 'message',)


@admin.register(Call)
class CallAdmin(admin.ModelAdmin):
    list_display = ('caller', 'receiver', 'call_type', 'started_at', 'ended_at', 'is_missed', 'call_duration',)
    search_fields = ('caller__username', 'receiver__username',)
    list_filter = ('call_type', 'is_missed', 'is_recorded',)
    ordering = ('-started_at',)
    raw_id_fields = ('caller', 'receiver',)


@admin.register(Bot)
class BotAdmin(admin.ModelAdmin):
    list_display = ('owner', 'name', 'username', 'created_at',)
    search_fields = ('name', 'username',)
    list_filter = ('created_at',)
    ordering = ('-created_at',)
    readonly_fields = ('token',)
    raw_id_fields = ('owner',)
    prepopulated_fields = {'username': ('name',)}


@admin.register(Media)
class MediaAdmin(admin.ModelAdmin):
    list_display = ('uploader', 'file', 'media_type', 'uploaded_at', 'views', 'is_private',)
    search_fields = ('uploader__username', 'media_type', 'caption',)
    list_filter = ('media_type', 'is_private',)
    ordering = ('-uploaded_at',)
    raw_id_fields = ('uploader',)
