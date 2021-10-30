from rest_framework import status, viewsets, mixins 
from rest_framework.response import Response 
from django.views import View 
from django.http import Http404

from .models import Product
from .serializers import ProductSerializer
from drf_yasg.utils import swagger_auto_schema

    

# Create your views here. 

class ProductViewSet(viewsets.GenericViewSet, 
                mixins.ListModelMixin, 
                View): 

    serializer_class = ProductSerializer   # 이 클래스형 view 에서 사용할 시리얼라이저를 선언
    @swagger_auto_schema(tags=['상품 API'])
    def get_queryset(self):
        conditions = {
            'id': self.kwargs.get("product_num", None),
            'name__contains': self.request.GET.get('name', None),
            'created_at__lte': self.request.GET.get('created_at', None),
        }
        conditions = {key: val for key, val in conditions.items() if val is not None}

        products = Product.objects.filter(**conditions)
        if not products.exists():
            raise Http404()

        return products

"""
    def add(self, request): 
        musics = Music.objects.filter(**request.data)
        if musics.exists():
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE)

        music_serializer = MusicSerializer(data=request.data, partial=True)
        if not music_serializer.is_valid():
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE)

        music = music_serializer.save()

        return Response(MusicSerializer(music).data, status=status.HTTP_201_CREATED)
        """