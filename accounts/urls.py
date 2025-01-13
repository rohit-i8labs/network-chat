from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import PlatformOwnerViewSet

router = DefaultRouter()
router.register(r'getusers', PlatformOwnerViewSet, basename='get-users')

urlpatterns = [
    path('', include(router.urls)),  # Include the router-generated URLs
]