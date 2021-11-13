from django.urls import path 
from django.conf import settings 
from .views import AnonymousUserView, MakeAnonymousUserView

urlpatterns = [ 
    path("user/anonymous", MakeAnonymousUserView.as_view(), name="make user"),
    path("user", AnonymousUserView.as_view(), name="get user"),
]
