from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.shortcuts import render
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema

class foldersView(APIView):
    @swagger_auto_schema(tags=['폴더 API'])
    def get(self, request):
        return Response("사용자의 모든 폴더를 가져옵니다")

    @swagger_auto_schema(tags=['폴더 API'])
    def post(self, request):
        return Response("폴더 정보를 받아와 폴더를 생성합니다.")

class folderView(APIView):
    @swagger_auto_schema(tags=['폴더 API'])
    def get(self, request, folderId):
        return Response(f"폴더아이디 {folderId}에 해당하는 폴더의 정보를 가져옵니다.")
