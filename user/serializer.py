from django.core import serializers
from django.db.models import fields
from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "anonymous_id", "apple_id", "kakao_id", "email", "password", "nickname", "profile_image", "created_at", "updated_at"]

class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'anonymous_id'] 

        