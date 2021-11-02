from django.core import serializers
from django.db.models import fields
from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("anonymous_id")
    
    def create(self, anonymous):
        user = User.objects.create_user(anonymous)
        return user