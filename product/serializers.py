from .models import *
from rest_framework import serializers
from brand.serializer import BrandSerializer

class productImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['image_url']

class ProductSerializer(serializers.ModelSerializer):
    brand = BrandSerializer(read_only = True)
    class Meta:
        music = Product.objects.all()
        model = Product
        exclude = ['deleted_at', 'Is_deleted', 'created_at', 'updated_at', 'user', 'folder']

class postProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ['user', 'folder', 'brand', 'added_brand', 'name', 'price', 'image_url', 'site_url']