from django.urls import path 
from django.conf import settings 
from .views import brandView, brandAddView, brandMainView,brandPopularView,brandSearchView, markedBrandCountView, markedBrandSearchView, markedBrandView

urlpatterns = [ 
    path("brand/<int:brandId>", brandView.as_view(), name = "getBrand"),
    path("brand", brandAddView.as_view(), name = "postBrand"),
    path("brands/popular", brandPopularView.as_view(), name = "GetpopularBrands"),
    path("brands/main/", brandMainView.as_view(), name = "GetmainBrands"),
    path("brands/search", brandSearchView.as_view({'get': 'list'}), name = "GetmainBrands"),
    path("brands/liked", markedBrandView.as_view(), name = "GetmainBrands"),
    path("brands/liked/<search>", markedBrandSearchView.as_view(), name = "GetmainBrands"),
    path("brand/like", markedBrandCountView.as_view(), name = "PostmainBrands"),
]