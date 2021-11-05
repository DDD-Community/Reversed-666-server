from django.http.response import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.shortcuts import render
from rest_framework import status
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from .serializer import BrandSerializer, brandJoinSerializer, clickCountSerializer, mainBrandSerializer, popularBrandSerializer, popularBrandType, mainBrandType
from .models import mainBrand, Brand
import json

class brandView(APIView):
    @swagger_auto_schema(tags=['브랜드 API'])
    def get(self, request, brandId):
        return Response(f"id가 {brandId}인 브랜드를 return합니다.", status = 200)

class brandAddView(APIView):
    @swagger_auto_schema(tags=['브랜드 API'])
    def post(self, request):
        return Response("브랜드의 정보를 받아와 추가합니다", status = 200)

class brandPopularView(APIView):
    '''
    브랜드를 인기순으로 받아온다.
    '''
    @swagger_auto_schema(tags=['브랜드 API'], 
    manual_parameters=[openapi.Parameter('size', openapi.IN_QUERY, description="받아오고자 하는 브랜드의 개수", type = openapi.TYPE_STRING)],
    responses = {200: popularBrandSerializer})
    def get(self, request):
        size = int(request.GET.get('size'))
        query = Brand.objects.all().order_by('-click_count')[:size]
        serializer = BrandSerializer(query, many = True)
        brandsInfo = popularBrandType(size, serializer.data)
        serializer = popularBrandSerializer(brandsInfo)
        
        return JsonResponse(serializer.data, status = 200, safe = False)
        
class brandMainView(APIView):
    '''
    메인화면에 띄울 브랜드 리스트를 가져온다.
    '''
    @swagger_auto_schema(tags=['브랜드 API'], responses = {200:mainBrandSerializer})
    def get(self, request):
        query = mainBrand.objects.filter(Is_deleted = False)
        query = query.select_related("brand_id")
        serializer = brandJoinSerializer(query, many = True)
        mainBrandInfo = mainBrandType(serializer.data)
        serializer = mainBrandSerializer(mainBrandInfo)
        return JsonResponse(serializer.data, status = 200, safe = False)

class brandSearchView(APIView):
    @swagger_auto_schema(tags=['브랜드 API'])
    def get(self, request):
        return Response("브랜드 검색 결과를 보여줍니다.", status = 200)

class markedBrandView(APIView):
    @swagger_auto_schema(tags=['담은 브랜드 API'])
    def get(self, request):
        return Response("북마크한 브랜드를 모아서 보여줍니다.", status = 200)

class markedBrandSearchView(APIView):
    @swagger_auto_schema(tags=['담은 브랜드 API'])
    def get(self, request):
        return Response("북마크한 브랜드 중에서 검색한 결과를 보여줍니다.", status = 200)


class markedBrandCountView(APIView):
    @swagger_auto_schema(tags=['담은 브랜드 API'])
    def post(self, request):
        return Response("브랜드를 북마크한 횟수를 카운팅합니다.", status = 200)

class BrandCountView(APIView):
    @swagger_auto_schema(tags=['브랜드 API'], responses = {200: clickCountSerializer})

    def post(self, request, brandId):
        try:
            queryset = Brand.objects.get(id = brandId)
        except Exception as ex:
            return JsonResponse({"status": 404, "message" : str(ex)}, status = 404, safe = False)
        else:
            queryset.click_count += 1
            queryset.save()
            serializer = clickCountSerializer(queryset)
            return JsonResponse(serializer.data, status = 200, safe = False)
