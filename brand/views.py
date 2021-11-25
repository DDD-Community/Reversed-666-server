from django.core import serializers
from django.http.response import JsonResponse
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, generics, permissions
from django.shortcuts import render
from rest_framework import filters, viewsets
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from django.utils.decorators import method_decorator
from .serializer import BrandSerializer, brandJoinSerializer, BranditemSerializer, postlikeBrandSerializer, getlikeBrandSerializer, addedBrandSerializer, GlobalSearchSerializer, SgetlikeBrandSerializer
from .models import addedBrand, likedBrand, mainBrand, Brand
from user.models import User
from itertools import chain
from .logoCrawler import logoCroller

response_schema_dict = {
    "200": openapi.Response(
        description="DB 저장에 성공했을 시",
        examples={
            "application/json": {
                "status": "Success",
            }
        }
    ),
    "404": openapi.Response(
        description="DB 저장에 실패했을 시",
        examples={
            "application/json": {
                "status": "Fail",
                "message": "error message (상황에 따라 다름)"
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
    @swagger_auto_schema(tags=['브랜드 API'], 
    request_body = openapi.Schema(type = openapi.TYPE_OBJECT,
    properties = {
        'name': openapi.Schema(type = openapi.TYPE_STRING, description = '브랜드 이름'),
        'en_name': openapi.Schema(type = openapi.TYPE_STRING, description = '브랜드 영어 이름'),
        'site_url': openapi.Schema(type = openapi.TYPE_STRING, description = '브랜드 주소')          
    }),
    manual_parameters=[openapi.Parameter('Authorization', openapi.IN_HEADER, description="유저 익명 아이디 ex) 51131230-d4b6-48f9-8807-b83f27f4b825", type=openapi.TYPE_STRING)]
    , responses = response_schema_dict )
    def post(self, request):
        '''
        브랜드를 추가하는 API
        '''
        anonymousId = request.META['HTTP_AUTHORIZATION']
        serializer = addedBrandSerializer(data = request.data)
        user = User.objects.get(anonymous_id = anonymousId)
        if serializer.is_valid():
            try:
                serializer.save(user = user)
                user = User.objects.get(anonymous_id=anonymousId)
                print(user.id)
                added_brand = addedBrand.objects.get(id = serializer.data['id'])
                query = likedBrand.objects.create(user = user, added_brand = added_brand)
            except Exception as ex:
                return JsonResponse({"status": "Fail", "message" : str(ex)}, status = 404, safe = False)
            else:
                return JsonResponse({"status": "Success"}, status = 200)
        return JsonResponse({"status": "Fail", "message" : "올바르지 않은 요청입니다."}, status = 404, safe = False)

class brandPopularView(APIView):
    '''
    브랜드를 인기순으로 받아온다.
    '''
    @swagger_auto_schema(tags=['브랜드 API'], 
    manual_parameters=[openapi.Parameter('Authorization', openapi.IN_HEADER, description="유저 익명 아이디 ex) 51131230-d4b6-48f9-8807-b83f27f4b825", type=openapi.TYPE_STRING)],
    responses = {200: BrandSerializer(many = True)})
    def get(self, request):
        size = 10
        query = Brand.objects.all().order_by('-click_count')[:size]
        serializer = BranditemSerializer(query, many = True, context={'anonymousId': request.META['HTTP_AUTHORIZATION']})

        return JsonResponse(serializer.data, status = 200, safe = False)
        
class brandMainView(APIView):
    '''
    메인화면에 띄울 브랜드 리스트를 가져온다.
    '''
    @swagger_auto_schema(tags=['브랜드 API'], 
    manual_parameters=[openapi.Parameter('Authorization', openapi.IN_HEADER, description="유저 익명 아이디 ex) 51131230-d4b6-48f9-8807-b83f27f4b825", type=openapi.TYPE_STRING)],
    responses = {200:BranditemSerializer(many = True)})
    def get(self, request):
        query = mainBrand.objects.filter(Is_deleted = False)
        query = query.select_related("brand")
        serializer = brandJoinSerializer(query, many = True, context={'anonymousId': request.META['HTTP_AUTHORIZATION']})
        data = list(map(lambda x : x['brand'], serializer.data))
        return JsonResponse(data, status = 200, safe = False)


@method_decorator(name="list", decorator=swagger_auto_schema(tags=["브랜드 API"],
manual_parameters=[openapi.Parameter('Authorization', openapi.IN_HEADER, description="유저 익명 아이디 ex) 51131230-d4b6-48f9-8807-b83f27f4b825", type=openapi.TYPE_STRING)],
))
class brandSearchView(viewsets.ModelViewSet):
    '''
    검색 키워드를 받아 해당하는 브랜드 리스트를 돌려준다.
    '''
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['^name', '^en_name']

    def list(self, request):
        query = Brand.objects.all()
        query = self.filter_queryset(query)
        serializer = BranditemSerializer(query, many = True, context={'anonymousId': request.META['HTTP_AUTHORIZATION']})
        return JsonResponse(serializer.data, safe = False, status = 200)
        

class markedBrandView(APIView):
    @swagger_auto_schema(tags=['좋아요한 브랜드 API'],
    manual_parameters=[openapi.Parameter('Authorization', openapi.IN_HEADER, description="유저 익명 아이디 ex) 51131230-d4b6-48f9-8807-b83f27f4b825", type=openapi.TYPE_STRING)],
    responses = {200:SgetlikeBrandSerializer}
    )
    def get(self, request):
        '''
        유저가 좋아요한 브랜드 리스트를 보여준다.
        '''
        user = User.objects.get(anonymous_id = request.META['HTTP_AUTHORIZATION'])
        query = likedBrand.objects.filter(user = user, Is_deleted = False)
        query = query.select_related("brand", "added_brand")
        serializer = getlikeBrandSerializer(query, many = True)

        for i in range(len(serializer.data)):
            if(not serializer.data[i]['Is_added']):
                del(serializer.data[i]['added_brand'])
            else:
                serializer.data[i]['brand'] = serializer.data[i]['added_brand']
                del(serializer.data[i]['added_brand'])

        return JsonResponse(serializer.data, safe = False)

#@method_decorator(name = "get_object", decorator=swagger_auto_schema(tags=["좋아요한 브랜드 API"]))
class markedBrandSearchView(generics.ListAPIView):
    '''
    유저가 좋아요한 브랜드 중 검색 키워드를 받아 해당하는 브랜드 리스트를 돌려준다.
    '''
    serializer_class = GlobalSearchSerializer
    @swagger_auto_schema(tags=['좋아요한 브랜드 API'])
    def get_queryset(self):
        #미작업내용 : brands결과 유저별로 다르게 보여주는 것. liked brand를 join해서 가져오는 게 나을 듯 하다.
        query = self.request.query_params.get('search', None)
        user = self.request.query_params.get('userId', None)
        addedbrand = addedBrand.objects.filter(Q(name__icontains=query) | Q(en_name__icontains=query))
        addedbrand = addedbrand.filter(user = user)
        brand = Brand.objects.filter(Q(name__icontains=query) | Q(en_name__icontains=query))
        all_results = list(chain(addedbrand, brand)) 
        all_results.sort(key=lambda x: x.created_at)
        return all_results


class markedBrandCountView(APIView):
    @swagger_auto_schema(tags=['좋아요한 브랜드 API'], 
    request_body = openapi.Schema(type = openapi.TYPE_OBJECT,
    properties = {
        'brand': openapi.Schema(type = openapi.TYPE_INTEGER, description = 'brandId')    
    }),
    manual_parameters=[openapi.Parameter('Authorization', openapi.IN_HEADER, description="유저 익명 아이디 ex) 51131230-d4b6-48f9-8807-b83f27f4b825", type=openapi.TYPE_STRING)],
    responses = response_schema_dict)
    def post(self, request):
        '''
        브랜드 Id를 받아와 좋아요 목록에 추가한다.
        '''
        serializer = postlikeBrandSerializer(data = request.data)
        user = User.objects.get(anonymous_id = request.META['HTTP_AUTHORIZATION'])
        queryset = Brand.objects.get(id = request.data['brand'])
        queryset.like_count +=1
        queryset.save()
        if serializer.is_valid():
            try:
                serializer.save(user = user)
            except Exception as ex:
                return JsonResponse({"status": "Fail", "message" : str(ex)}, status = 404, safe = False)
            else:
                return JsonResponse({"status": "Success"}, status = 200)
        return JsonResponse({"status": "Fail", "message" : "올바르지 않은 요청입니다."}, status = 404, safe = False)
