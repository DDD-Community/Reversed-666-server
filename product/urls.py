from django.urls import path 
from django.conf import settings 
from .views import ProductViewSet

urlpatterns = [ 
    path("product/", ProductViewSet.as_view({"get": "list"}), name="musics"),
    path("product/<int:product_num>", ProductViewSet.as_view({"get": "list"}), name="music"),
]