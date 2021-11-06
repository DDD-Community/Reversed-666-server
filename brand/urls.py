from django.urls import path 
from django.conf import settings 
from .views import brandView, brandAddView, brandMainView,brandPopularView,brandSearchView, BrandCountView, markedBrandCountView, markedBrandSearchView, markedBrandView

urlpatterns = [ 
    path("brand/<int:brandId>", brandView.as_view(), name = "getBrand"),
    path("brand", brandAddView.as_view(), name = "postBrand"),
    path("brands/popular", brandPopularView.as_view(), name = "GetpopularBrands"),
    path("brands/main", brandMainView.as_view(), name = "GetmainBrands"),
    path("brands/search", brandSearchView.as_view({'get': 'list'}), name = "GetmainBrands"),
    path("brands/marked", markedBrandView.as_view(), name = "GetmainBrands"),
    path("brands/marked/<search>", markedBrandSearchView.as_view(), name = "GetmainBrands"),
    path("brand/mark", markedBrandCountView.as_view(), name = "GetmainBrands"),
    path("brand/count/<int:brandId>", BrandCountView.as_view(), name = "GetmainBrands"),
]