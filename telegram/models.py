from django.db import models

from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """
    Custom User model that inherits from Django's AbstractUser model.
    """
    phone_number = models.CharField(max_length=15, unique=True, null=True, blank=True, db_index=True)
    bio = models.TextField(blank=True, null=True)
    profile_photo = models.ImageField(upload_to='profiles/', blank=True, null=True)
    is_bot = models.BooleanField(default=False)
    last_seen = models.DateTimeField(auto_now=True)
    is_verified = models.BooleanField(default=False)
    language = models.CharField(max_length=10, default='en')
    two_factor_auth = models.BooleanField(default=False)
    status = models.CharField(max_length=255, blank=True, null=True, unique=True, db_index=True)
    is_premium = models.BooleanField(default=False)
    blocked_users = models.ManyToManyField('self', symmetrical=False, related_name='blocked_by', blank=True)

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        if self.first_name and self.last_name:
            return f"{self.get_full_name()}"
        if self.email:
            return f"{self.email}"
        return f"{self.username}"


class Chat(models.Model):
    """
    Model for chat.
    """
    CHAT_TYPES = (
        ('private', ('Private')),
        ('group', ('Group')),
        ('channel', ('Channel')),
        ('supergroup', ('Supergroup')),
    )
    name = models.CharField(max_length=255, blank=True, null=True, db_index=True)
    chat_type = models.CharField(max_length=20, choices=CHAT_TYPES)
    members = models.ManyToManyField(User, related_name='chats', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_public = models.BooleanField(default=False)
    invite_link = models.CharField(max_length=255, blank=True, null=True, db_index=True)
    description = models.TextField(blank=True, null=True)
    admin_users = models.ManyToManyField(User, related_name='admin_in_chats', blank=True)
    pinned_messages = models.ManyToManyField('Message', blank=True, related_name='pinned_in')

    class Meta:
        verbose_name = 'Chat'
        verbose_name_plural = 'Chats'

    def __str__(self):
        return f"{self.name}"


class Message(models.Model):
    """
    Model for message.
    """
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='messages')
    text = models.TextField(blank=True, null=True)
    media = models.FileField(upload_to='messages/', blank=True, null=True)
    reply_to = models.ForeignKey('self', on_delete=models.SET_NULL, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(null=True, blank=True)
    is_pinned = models.BooleanField(default=False)
    forwarded_from = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='forwarded_messages')
    is_deleted = models.BooleanField(default=False)
    reactions = models.ManyToManyField(User, through='Reaction', related_name='reacted_messages')

    class Meta:
        ordering = ['-timestamp']
        verbose_name = 'Message'
        verbose_name_plural = 'Messages'

    def __str__(self):
        return f"{self.sender.username}"


class Reaction(models.Model):
    """
    Model for reaction.
    """
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    emoji = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('message', 'user')
        verbose_name = 'Reaction'
        verbose_name_plural = 'Reactions'

    def __str__(self):
        if self.user.first_name and self.user.last_name:
            return f"{self.user.get_full_name()}"
        return f"{self.user.username}"
    

class Contact(models.Model):
    """
    Model for contact.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='contacts')
    contact = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_favorite = models.BooleanField(default=False)
    is_muted = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user', 'contact')
        verbose_name = 'Contact'
        verbose_name_plural = 'Contacts'

    def __str__(self):
        return f"{self.user}"


class Notification(models.Model):
    """
    Model for notification.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.ForeignKey(Message, on_delete=models.CASCADE, null=True, blank=True)
    text = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    notification_type = models.CharField(max_length=50, default='message')
    seen_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = 'Notification'
        verbose_name_plural = 'Notifications'

    def __str__(self):
        return f"{self.user}"


class Call(models.Model):
    """
    Model for call.
    """
    CALL_TYPES = (
        ('voice', ('Voice')),
        ('video', ('Video')),
    )
    caller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='calls_made')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='calls_received')
    call_type = models.CharField(max_length=10, choices=CALL_TYPES)
    started_at = models.DateTimeField(auto_now_add=True)
    ended_at = models.DateTimeField(null=True, blank=True)
    is_missed = models.BooleanField(default=False)
    call_duration = models.IntegerField(default=0)
    is_recorded = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Call'
        verbose_name_plural = 'Calls'

    def __str__(self):
        return f"{self.caller.username}"


class Bot(models.Model):
    """
    Model for bot.
    """
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, db_index=True)
    username = models.CharField(max_length=50, unique=True, db_index=True)
    token = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    commands = models.JSONField(default=dict)

    class Meta:
        verbose_name = 'Bot'
        verbose_name_plural = 'Bots'

    def __str__(self):
        return f"{self.username}"


class Media(models.Model):
    """
    Model for media.
    """

    MEDIA_TYPES = (
        ('image', ('Image')),
        ('video', ('Video')),
        ('audio', ('Audio')),
        ('document', ('Document')),
    )
    uploader = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to='media/')
    media_type = models.CharField(max_length=10, choices=MEDIA_TYPES)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    caption = models.TextField(blank=True, null=True)
    views = models.PositiveIntegerField(default=0)
    is_private = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Media'
        verbose_name_plural = 'Media'

    def __str__(self):
        return f"{self.uploader.username}"
