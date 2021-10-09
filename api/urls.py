from django.urls import path 
from django.conf import settings 
from .views import MusicViewSet

urlpatterns = [ 
    path("v1/music", MusicViewSet.as_view({"get": "list", "post": "add"}), name="musics"),
    path("v1/music/<int:music_num>", MusicViewSet.as_view({"get": "list"}), name="music"),
]