from django.core import serializers
from django.db.models import fields
from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ("role", "Is_deleted", "deleted_at")

class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'anonymous_id'] 

class UserIdNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'nickname']