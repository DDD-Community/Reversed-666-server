from django.core import serializers
from django.db.models import fields
from rest_framework import serializers
from .models import mainBrand, Brand, likedBrand

# Brand 객체에서 필요한 부분만 선택해 직렬화한다.
class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['id', 'name', 'en_name', 'site_url', 'logo_url']


# main_brands 테이블과 brands 테이블을 join하고, 배열 형태로 내보낸다.
class brandJoinSerializer(serializers.ModelSerializer):
    brand_id = BrandSerializer(read_only = True)

    class Meta:
        model = mainBrand
        fields = ["brand_id"]

class mainBrandType(object):
    def __init__(self, list):
        self.list = list

class mainBrandSerializer(serializers.Serializer):
    brandList = serializers.SerializerMethodField()

    def get_brandList(self, obj):
        data = list(map(lambda x : x['brand_id'], obj.list))
        return data
    


class clickCountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ["id", "name", "click_count"]



class popularBrandType(object):
    def __init__(self, size, list):
        self.size = size
        self.sortBy = 'popular'
        self.brandList = list

class popularBrandSerializer(serializers.Serializer):
    size = serializers.IntegerField()
    sortBy = serializers.CharField()
    brandList = BrandSerializer(many = True)

