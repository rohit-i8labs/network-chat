from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ChatRoomViewSet, MessageViewSet, ChatSessionViewSet, UserViewSet,TodaysSpecialViewSet, CouponViewSet

# Initialize the router
router = DefaultRouter()
router.register(r'chatrooms', ChatRoomViewSet, basename='chatroom')
router.register(r'chatrooms/(?P<chat_room_id>\d+)/messages', MessageViewSet, basename='message')
router.register(r'chat_sessions', ChatSessionViewSet, basename='chat_session')
router.register(r'user', UserViewSet, basename='userdet')
router.register(r'todays-special', TodaysSpecialViewSet, basename='todays-special')
router.register(r'coupon', CouponViewSet, basename='coupon')

# URLs for the app
urlpatterns = [
    path('', include(router.urls)),  # Include the router-generated URLs
]
