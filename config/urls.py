from django.contrib import admin
from django.urls import path, re_path, include
from django.conf import settings
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view( 
    openapi.Info( 
        title="Bring Swagger Api", 
        default_version="v1", 
        description="bring App을 위한 API 문서", 
        terms_of_service="https://www.google.com/policies/terms/", 
        contact=openapi.Contact(name="hyeyeon", email="dlgpdus0416@gmail.com"), 
    ), 
    public=True, 
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include(("product.urls", "product"))),
    path("", include(("brand.urls", "brand"))),
    path("", include(("folder.urls", "folder"))),
    path("", include(("user.urls", "user"))),
]


# 이건 디버그일때만 swagger 문서가 보이도록 해주는 설정이라는 듯. urlpath도 이 안에 설정 가능해서, debug일때만 작동시킬 api도 설정할 수 있음.
urlpatterns += [
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name="schema-json"),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),    ]

