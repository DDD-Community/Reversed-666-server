from django.urls import path 
from django.conf import settings 
from .views import ProductViewSet

urlpatterns = [ 
    #path("v1/product", ProductViewSet.as_view({"get": "list", "post": "add"}), name="musics"),
    path("v1/product/", ProductViewSet.as_view({"get": "list"}), name="musics"),
    path("v1/<int:product_num>", ProductViewSet.as_view({"get": "list"}), name="music"),
]