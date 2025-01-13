from rest_framework import viewsets, permissions, filters
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from .serializers import UserDetailSerializer

User = get_user_model()

class PlatformOwnerViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]  # Requires Bearer token authentication
    filter_backends = [filters.SearchFilter]
    search_fields = ['user_type']

    def list(self, request):
        # Check if the authenticated user is a platform_owner
        if request.user.user_type != 'platform_owner':
            return Response({"error": "Access denied. Only platform owners are allowed."}, status=403)

        # If user is a platform_owner, retrieve all users
        users = User.objects.all()
        serializer = UserDetailSerializer(users, many=True)
        return Response(serializer.data)
