from django.core import serializers
from django.db.models import fields
from rest_framework import serializers
from .models import mainBrand, Brand, likedBrand

class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['id', 'name', 'en_name', 'site_url', 'logo_url']

class mainBrandsSerializer(serializers.ModelSerializer):
    brand_id = BrandSerializer(read_only = True)
    class Meta:
        model = mainBrand
        fields = ["brand_id"]

    @classmethod
    def setup_preloading(cls, queryset):
        return queryset.select_related("brand_id")



"""
class mainBrandsSerializer(serializers.Serializer):
    mainBrands = serializers.SerializerMethodField()

    class Meta:
        model = mainBrand
        fields = '__all__'

    def get_mainBrands(self, instance):
        brands_queryset = Brand.objects.filter(id = 2)
        serializer = BrandSerializer(instance = brands_queryset, many = True, read_only = True)
        return serializer.data
"""