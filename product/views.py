from django.http.response import JsonResponse
from rest_framework import status, viewsets, mixins 
from rest_framework.views import APIView
from rest_framework.response import Response 
from django.views import View 
from django.http import Http404
from drf_yasg import openapi
from .models import Product
from .serializers import ProductSerializer, postProductSerializer
from drf_yasg.utils import swagger_auto_schema
from brand.views import response_schema_dict
from .useOpengraph import productOpengraph
from user.models import User
from folder.models import Folder

class ProductPostView(APIView):
    @swagger_auto_schema(tags=['상품 API'],
    request_body = openapi.Schema(type = openapi.TYPE_OBJECT,
        properties = {
        'folder': openapi.Schema(type = openapi.TYPE_INTEGER, description = '폴더 id'),
        'site_url': openapi.Schema(type = openapi.TYPE_INTEGER, description = '상품 링크')    
    }),
    responses = response_schema_dict
    )
    def post(self, request):
        '''
        상품을 좋아요 리스트에 추가한다.
        '''
        anonymousId = request.META['HTTP_AUTHORIZATION']
        product = productOpengraph(request.data['site_url'])
        user = User.objects.get(anonymous_id = anonymousId)
        folder = Folder.objects.get(id = request.data['folder'], user = user)
        query = Product.objects.create(
            user = user, folder = folder,
            name = product.title , price = product.price_amount, image_url = product.image, site_url = product.url
            )
        return JsonResponse({"status": "Success"}, status = 200)


        '''
        serializer = postProductSerializer(data = request.data)
        if serializer.is_valid():
            try:
                serializer.save()
            except Exception as ex:
                return JsonResponse({"status": "Fail", "message" : str(ex)}, status = 404, safe = False)
            else:
                return JsonResponse({"status": "Success"}, status = 200)
        return JsonResponse({"status": "Fail", "message" : "올바르지 않은 요청입니다."}, status = 404, safe = False)
        '''
    
class ProductGetView(APIView):
    @swagger_auto_schema(tags=['상품 API'], responses = {200:ProductSerializer})
    def get(self, request, folderId):
        '''
        폴더 아이디에 맞는 상품들의 리스트를 불러온다.
        '''
        queryset = Product.objects.filter(id = folderId, Is_deleted = False)
        queryset = queryset.select_related("brand")
        serializer = ProductSerializer(queryset, many = True)
        return JsonResponse(serializer.data, safe = False)
