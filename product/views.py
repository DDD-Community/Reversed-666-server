from rest_framework import status, viewsets, mixins 
from rest_framework.views import APIView
from rest_framework.response import Response 
from django.views import View 
from django.http import Http404
from .models import Product
from .serializers import ProductSerializer
from drf_yasg.utils import swagger_auto_schema

class ProductPostView(APIView):
    @swagger_auto_schema(tags=['상품 API'])
    def post(self, request):
        return Response("상품을 좋아요한 리스트에 추가합니다.")

    
class ProductGetView(APIView):
    @swagger_auto_schema(tags=['상품 API'])
    def get(self, request, folderId):
        return Response(f"폴더아이디 {folderId}에 포함되는 상품의 정보를 가져옵니다")
