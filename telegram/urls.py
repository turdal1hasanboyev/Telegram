from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import (
    UserViewSet,
    ChatViewSet,
    MessageViewSet,
    ReactionViewSet,
    ContactViewSet, 
    NotificationViewSet,
    CallViewSet,
    BotViewSet,
    MediaViewSet,
)


router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'chats', ChatViewSet)
router.register(r'messages', MessageViewSet)
router.register(r'reactions', ReactionViewSet)
router.register(r'contacts', ContactViewSet)
router.register(r'notifications', NotificationViewSet)
router.register(r'calls', CallViewSet)
router.register(r'bots', BotViewSet)
router.register(r'media', MediaViewSet)


urlpatterns = [
    path('', include(router.urls)),
]
