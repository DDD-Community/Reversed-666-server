from django.core import serializers
from django.db.models import fields
from rest_framework import serializers
from .models import mainBrand, Brand, likedBrand

class mainBrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = mainBrand
        fields = "__all__"

