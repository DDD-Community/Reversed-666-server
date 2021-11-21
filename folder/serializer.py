from django.core import serializers
from django.db.models import fields
from rest_framework import serializers
from brand.serializer import BrandSerializer
from .models import Folder
from product.models import Product
from product.serializers import productImageSerializer

class FolderSerializer(serializers.ModelSerializer):
    thumbnailurls = serializers.SerializerMethodField()
    products_num = serializers.SerializerMethodField()

    def get_thumbnailurls(self, obj):
        query = Product.objects.filter(folder = obj.id)[:3]
        serializer = productImageSerializer(query, many = True)
        return serializer.data
    
    def get_products_num(self, obj):
        return Product.objects.filter(folder = obj.id).count()

    class Meta:
        model = Folder
        exclude = ['user','deleted_at', 'Is_deleted', 'created_at', 'updated_at']

class postFolderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Folder
        fields = ['id', 'name', 'description']

class postFolderInfoSerializer(serializers.ModelSerializer):
    thumbnailurl = serializers.SerializerMethodField()

    def get_thumbnailurl(self, obj):
        query = Product.objects.filter(folder = obj.id)[:3]
        serializer = productImageSerializer(query, many = True)
        return serializer.data

    class Meta:
        model = Folder
        fields = ['id', 'name', 'thumbnailurl']