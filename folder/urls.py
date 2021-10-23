from django.urls import path 
from django.conf import settings 
from .views import foldersView,folderView

urlpatterns = [ 
    path("folder/<int:folderId>", folderView.as_view(), name = "getBrand"),
    path("folder", foldersView.as_view(), name = "postBrand"),
]