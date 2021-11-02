from django.urls import path 
from django.conf import settings 
from .views import ProductGetView, ProductPostView

urlpatterns = [ 
    path("product/", ProductPostView.as_view(), name="postproducts"),
    path("product/<int:folderId>", ProductGetView.as_view(), name="getproducts"),
]