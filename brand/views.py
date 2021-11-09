from django.core import serializers
from django.http.response import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.shortcuts import render
from rest_framework import filters, viewsets
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from django.utils.decorators import method_decorator
from .serializer import BrandSerializer, brandJoinSerializer, mainBranditemSerializer, postlikeBrandSerializer, getlikeBrandSerializer
from .models import likedBrand, mainBrand, Brand
from user.models import User

response_schema_dict = {
    "200": openapi.Response(
        description="브랜드를 좋아요하는 데 성공했을 시",
        examples={
            "application/json": {
                "status": "Success",
            }
        }
    ),
    "404": openapi.Response(
        description="이미 좋아요한 항목을 다시 좋아요 했을 시",
        examples={
            "application/json": {
                "status": "Fail",
                "message": "(1062, \"Duplicate entry '10-2' for key 'liked_brands.unique user brand'\")"
            }
        }
    ),
    
}




class brandView(APIView):
    '''
    brandId에 해당하는 브랜드 정보를 불러오고, 브랜드 클릭 횟수를 증가시킨다.
    '''
    @swagger_auto_schema(tags=['브랜드 API'], responses = {200:BrandSerializer})
    def get(self, request, brandId):

        try:
            queryset = Brand.objects.get(id = brandId)
        except Exception as ex:
            return JsonResponse({"status": 404, "message" : str(ex)}, status = 404, safe = False)
        else:
            queryset.click_count += 1
            queryset.save()
            serializer = BrandSerializer(queryset)
            return JsonResponse(serializer.data, status = 200, safe = False)

class brandAddView(APIView):
    @swagger_auto_schema(tags=['브랜드 API'])
    def post(self, request):
        return Response("브랜드의 정보를 받아와 추가합니다", status = 200)

class brandPopularView(APIView):
    '''
    브랜드를 인기순으로 받아온다.
    '''
    @swagger_auto_schema(tags=['브랜드 API'], responses = {200: BrandSerializer(many = True)})
    def get(self, request):
        size = 10
        query = Brand.objects.all().order_by('-click_count')[:size]
        serializer = BrandSerializer(query, many = True)

        return JsonResponse(serializer.data, status = 200, safe = False)
        
class brandMainView(APIView):
    '''
    메인화면에 띄울 브랜드 리스트를 가져온다.
    '''
    @swagger_auto_schema(tags=['브랜드 API'], 
    manual_parameters=[openapi.Parameter('userId', openapi.IN_QUERY, description = "유저 아이디", type = openapi.TYPE_INTEGER)],
    responses = {200:mainBranditemSerializer(many = True)})
    def get(self, request):
        query = mainBrand.objects.filter(Is_deleted = False)
        query = query.select_related("brand")
        serializer = brandJoinSerializer(query, many = True, context={'userId': request.GET.get('userId')})
        data = list(map(lambda x : x['brand'], serializer.data))
        return JsonResponse(data, status = 200, safe = False)


@method_decorator(name="list", decorator=swagger_auto_schema(tags=["브랜드 API"]))
class brandSearchView(viewsets.ModelViewSet):
    '''
    검색 키워드를 받아 해당하는 브랜드 리스트를 돌려준다.
    '''
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['^name', '^en_name']

class markedBrandView(APIView):
    @swagger_auto_schema(tags=['좋아요한 브랜드 API'],
    responses = {200:getlikeBrandSerializer}
    )
    def get(self, request):
        userId = request.GET.get('userId')
        query = likedBrand.objects.filter(user = userId, Is_deleted = False)
        query = query.select_related("brand")
        serializer = getlikeBrandSerializer(query, many = True)
        return JsonResponse(serializer.data, safe = False)

class markedBrandSearchView(APIView):
    @swagger_auto_schema(tags=['좋아요한 브랜드 API'])
    def get(self, request):
        return Response("북마크한 브랜드 중에서 검색한 결과를 보여줍니다.", status = 200)


class markedBrandCountView(APIView):
    @swagger_auto_schema(tags=['좋아요한 브랜드 API'], 
    request_body = openapi.Schema(type = openapi.TYPE_OBJECT,
    properties = {
        'user': openapi.Schema(type = openapi.TYPE_INTEGER, description = 'userId'),
        'brand': openapi.Schema(type = openapi.TYPE_INTEGER, description = 'brandId')    
    }),
    responses = response_schema_dict)
    def post(self, request):
        '''
        브랜드 Id와 유저 Id를 받아와 좋아요 목록에 추가합니다.
        '''
        serializer = postlikeBrandSerializer(data = request.data)
        queryset = Brand.objects.get(id = request.data['brand'])
        queryset.like_count +=1
        queryset.save()
        if serializer.is_valid():
            try:
                serializer.save()
            except Exception as ex:
                return JsonResponse({"status": "Fail", "message" : str(ex)}, status = 404, safe = False)
            else:
                return JsonResponse({"status": "Success"}, status = 200)
        return JsonResponse({"status": "Fail", "message" : "올바르지 않은 요청입니다."}, status = 404, safe = False)
