from .models import *
from rest_framework import serializers

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        music = Product.objects.all()
        model = Product
        fields = '__all__'