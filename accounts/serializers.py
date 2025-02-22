from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'date_joined', 'user_type']
