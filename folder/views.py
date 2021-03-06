from django.core import serializers
from django.http.response import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.shortcuts import render
from rest_framework import status
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from .models import Folder
from .serializer import postFolderSerializer, FolderSerializer, postFolderInfoSerializer
from user.models import User

response_schema_dict = {
    "200": openapi.Response(
        description="DB 저장에 성공했을 시",
        examples={
            "application/json": {
                "id": 12,
                "name": "나의 코트",
                "thumbnailurl": []
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

class foldersView(APIView):
    @swagger_auto_schema(tags=['폴더 API'],
    manual_parameters=[openapi.Parameter('Authorization', openapi.IN_HEADER, description="유저 익명 아이디 ex) 51131230-d4b6-48f9-8807-b83f27f4b825", type=openapi.TYPE_STRING)],
    responses = {200:FolderSerializer(many = True)}
    )
    def get(self, request):
        '''
        유저에 해당하는 폴더 리스트를 받아온다.
        '''
        anonymousId = request.META['HTTP_AUTHORIZATION']
        user = User.objects.get(anonymous_id = anonymousId)
        queryset= Folder.objects.filter(user = user, Is_deleted = False)
        serializer = FolderSerializer(queryset, many = True)
        return JsonResponse(serializer.data, status = 200, safe = False)
    
    @swagger_auto_schema(tags=['폴더 API'], 
    request_body = openapi.Schema(type = openapi.TYPE_OBJECT,
    properties = {
        'name': openapi.Schema(type = openapi.TYPE_INTEGER, description = '폴더 이름'),
        'description': openapi.Schema(type = openapi.TYPE_INTEGER, description = '폴더 설명')    
    }),
    manual_parameters=[openapi.Parameter('Authorization', openapi.IN_HEADER, description="유저 익명 아이디 ex) 51131230-d4b6-48f9-8807-b83f27f4b825", type=openapi.TYPE_STRING)],
    responses = response_schema_dict
    )
    def post(self, request):
        '''
        새로운 폴더를 만든다.
        '''
        user = User.objects.get(anonymous_id = request.META['HTTP_AUTHORIZATION'])
        serializer = postFolderSerializer(data = request.data)
        if serializer.is_valid():
            try:
                serializer.save(user = user)
                folder = Folder.objects.get(id = serializer.data['id'])
                serializer = postFolderInfoSerializer(folder)
            except Exception as ex:
                return JsonResponse({"status": "Fail", "message" : str(ex)}, status = 404, safe = False)
            else:
                return JsonResponse(serializer.data, status = 200)
        return JsonResponse({"status": "Fail", "message" : "올바르지 않은 요청입니다."}, status = 404, safe = False)
    
class folderView(APIView):
    @swagger_auto_schema(tags=['폴더 API'],
    responses = {200:FolderSerializer}
    )
    def get(self, request, folderId):
        '''
        폴더 아이디에 맞는 단일 폴더 정보를 가져온다.
        '''
        queryset  = Folder.objects.get(id = folderId)
        serializer = FolderSerializer(queryset)
        return JsonResponse(serializer.data, status = 200, safe = False)
