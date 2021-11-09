from django.core import serializers
from django.db.models import fields
from rest_framework import serializers
from brand.serializer import BrandSerializer
from .models import Folder

class postFolderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Folder
        fields = ['user', 'name', 'description']