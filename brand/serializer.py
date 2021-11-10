from django.core import serializers
from django.db.models import fields
from rest_framework import generics, serializers

from user.serializer import UserIdNameSerializer, UserSerializer
from .models import mainBrand, Brand, likedBrand, addedBrand

# Brand 객체에서 필요한 부분만 선택해 직렬화한다.
class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['id', 'name', 'en_name', 'site_url', 'logo_url']

class addedBrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = addedBrand
        fields = ['id', 'name', 'en_name', 'site_url', 'logo_url', 'user']

class mainBranditemSerializer(serializers.ModelSerializer):
    is_liked = serializers.SerializerMethodField()

    def get_is_liked(self, obj):
        try:
            Is_liked = likedBrand.objects.get(user = self.context.get("userId"), brand = obj.id)
        except likedBrand.DoesNotExist:
            Is_liked = False
        else:
            Is_liked = True
        return Is_liked
    class Meta:
        model = Brand
        fields = ['id', 'name', 'en_name', 'site_url', 'logo_url', 'Img_url', 'is_liked']

class BrandIdNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['id', 'name', 'like_count']

#### main브랜드 관련 serializers ####

# brands 테이블과 leftjoin된 brand_id 필드의 정보만 불러온다.

class MainBrandType:
    def __init__(self, brand, user):
        self.brand = brand
        self.user = user


class brandJoinSerializer(serializers.ModelSerializer):
    brand = mainBranditemSerializer(read_only = True)
    is_liked = serializers.SerializerMethodField()

    def get_is_liked(self, obj):
        return None
    class Meta:
        model = mainBrand
        fields = ["brand", 'is_liked']


#### clickCount 관련 serializers ####

class clickCountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ["id", "name", "click_count"]

class postlikeBrandSerializer(serializers.ModelSerializer):
    brand = BrandSerializer(read_only = True)
    class Meta:
        model = likedBrand
        fields = ['id', 'user', 'brand']
        
    def to_representation(self, instance):
        self.fields['user'] = UserIdNameSerializer(read_only = True)
        self.fields['brand'] = BrandIdNameSerializer(read_only = True)
        return super().to_representation(instance)

class getlikeBrandSerializer(serializers.ModelSerializer):
    brand = BrandSerializer(read_only = True)
    added_brand = addedBrandSerializer(read_only = True)
    Is_added = serializers.SerializerMethodField()

    def get_Is_added (self, obj):
        if (obj.brand and not obj.added_brand):
            return False
        elif (not obj.brand and obj.added_brand):
            return True

    class Meta:
        model = likedBrand
        fields = ['id', 'Is_added', 'brand' , 'added_brand']

class GlobalSearchSerializer(serializers.ModelSerializer):
    Is_added = serializers.SerializerMethodField()

    def get_Is_added (self, obj):
        if isinstance(obj, addedBrand):
            return True
        elif isinstance(obj, Brand):
            return False

    class Meta:
      model = Brand
      exclude = ['created_at', 'updated_at', 'deleted_at', 'Is_deleted', 'click_count', 'like_count']

    def to_native(self, obj):
      if isinstance(obj, addedBrand): 
         serializer = addedBrandSerializer(obj)
      elif isinstance(obj, Brand):
         serializer = BrandSerializer(obj)
      else:
         raise Exception("Neither a Snippet nor User instance!")
      return serializer.data
