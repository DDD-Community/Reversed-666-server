from .models import *
from rest_framework import serializers

class MusicSerializer(serializers.ModelSerializer):
    class Meta:
        music = Music.objects.all()
        model = Music
        fields = '__all__' 