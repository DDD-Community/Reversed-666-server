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
from .serializer import postFolderSerializer
from brand.views import response_schema_dict

class foldersView(APIView):
    @swagger_auto_schema(tags=['폴더 API'])
    def get(self, request):
        return Response("사용자의 모든 폴더를 가져옵니다")

    @swagger_auto_schema(tags=['폴더 API'], 
    request_body = openapi.Schema(type = openapi.TYPE_OBJECT,
    properties = {
        'user': openapi.Schema(type = openapi.TYPE_INTEGER, description = '사용자 id'),
        'name': openapi.Schema(type = openapi.TYPE_INTEGER, description = '폴더 이름'),
        'description': openapi.Schema(type = openapi.TYPE_INTEGER, description = '폴더 설명')    
    }),
    responses = response_schema_dict
    )
    def post(self, request):
        '''
        새로운 폴더를 만듭니다.
        '''
        serializer = postFolderSerializer(data = request.data)
        if serializer.is_valid():
            try:
                serializer.save()
            except Exception as ex:
                return JsonResponse({"status": "Fail", "message" : str(ex)}, status = 404, safe = False)
            else:
                return JsonResponse({"status": "Success"}, status = 200)
        return JsonResponse({"status": "Fail", "message" : "올바르지 않은 요청입니다."}, status = 404, safe = False)

class folderView(APIView):
    @swagger_auto_schema(tags=['폴더 API'])
    def get(self, request, folderId):
        return Response(f"폴더아이디 {folderId}에 해당하는 폴더의 정보를 가져옵니다.")
