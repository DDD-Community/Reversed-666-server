from django.core import serializers
from django.db.models import fields
from rest_framework import serializers
from .models import mainBrand, Brand, likedBrand

# Brand 객체에서 필요한 부분만 선택해 직렬화한다.
class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['id', 'name', 'en_name', 'site_url', 'logo_url']


#### main브랜드 관련 serializers ####

# mainBrand 응답을 커스텀하기 위한 class
class mainBrandType(object):
    def __init__(self, list):
        self.list = list

# brands 테이블과 leftjoin된 brand_id 필드의 정보만 불러온다.
class brandJoinSerializer(serializers.ModelSerializer):
    brand_id = BrandSerializer(read_only = True)

    class Meta:
        model = mainBrand
        fields = ["brand_id"]

# join된 정보에는 모두 brand_id column이 맨 앞에 붙어 있기에 제거해준다.
class mainBrandSerializer(serializers.Serializer):
    brandList = serializers.SerializerMethodField()

    def get_brandList(self, obj):
        data = list(map(lambda x : x['brand_id'], obj.list))
        return data

class swaggermainBrand(serializers.Serializer):
    brandList = BrandSerializer(many = True)
    

#### popular 브랜드 관련 serializers ####

# popularBrand 응답을 커스텀하기 위한 class
class popularBrandType(object):
    def __init__(self, size, list):
        self.size = size
        self.sortBy = 'popular'
        self.brandList = list

# popularBrand를 객체로 받아 serialize 해준다.
class popularBrandSerializer(serializers.Serializer):
    size = serializers.IntegerField()
    sortBy = serializers.CharField()
    brandList = BrandSerializer(many = True)



#### clickCount 관련 serializers ####

class clickCountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ["id", "name", "click_count"]

