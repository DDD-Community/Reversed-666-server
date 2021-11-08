from django.core import serializers
from django.db.models import fields
from rest_framework import serializers

from user.serializer import UserIdNameSerializer, UserSerializer
from .models import mainBrand, Brand, likedBrand

# Brand 객체에서 필요한 부분만 선택해 직렬화한다.
class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['id', 'name', 'en_name', 'site_url', 'logo_url', 'click_count', 'like_count']

class mainBranditemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['id', 'name', 'en_name', 'site_url', 'logo_url', 'Img_url']

class BrandIdNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['id', 'name', 'like_count']

#### main브랜드 관련 serializers ####

# brands 테이블과 leftjoin된 brand_id 필드의 정보만 불러온다.
class brandJoinSerializer(serializers.ModelSerializer):
    brand = mainBranditemSerializer(read_only = True)
    Is_liked = serializers.SerializerMethodField()

    def get_Is_liked (self, obj, data):
        likedBrand.objects.get(userId = data, )
        return 

    class Meta:
        model = mainBrand
        fields = ["brand"]

#### clickCount 관련 serializers ####

class clickCountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ["id", "name", "click_count"]

class likeBrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = likedBrand
        fields = ['user', 'brand']
        
    def to_representation(self, instance):
        self.fields['user'] = UserIdNameSerializer(read_only = True)
        self.fields['brand'] = BrandIdNameSerializer(read_only = True)
        return super().to_representation(instance)
