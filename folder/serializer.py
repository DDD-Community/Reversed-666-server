from django.core import serializers
from django.db.models import fields
from rest_framework import serializers
from brand.serializer import BrandSerializer
from .models import Folder
from product.models import Product
from product.serializers import productImageSerializer

class FolderSerializer(serializers.ModelSerializer):
    represent_image = serializers.SerializerMethodField()

    def get_represent_image(self, obj):
        query = Product.objects.filter(folder = obj.id)[:3]
        serializer = productImageSerializer(query, many = True)
        return serializer.data

    class Meta:
        model = Folder
        exclude = ['user','deleted_at', 'Is_deleted']

class postFolderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Folder
        fields = ['user', 'name', 'description']