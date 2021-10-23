from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.shortcuts import render
from rest_framework import status

class brandView(APIView):
    def get(self, request, brandId):
        return Response(f"id가 {brandId}인 브랜드를 return합니다.", status = 200)

class brandAddView(APIView):
    def post(self, request):
        return Response("브랜드의 정보를 받아와 추가합니다", status = 200)

class brandPopularView(APIView):
    def get(self, request):
        return Response("브랜드를 인기있는 순으로 받아와 출력합니다.", status = 200)
        
class brandMainView(APIView):
    def get(self, request):
        return Response("메인화면에 보여줄 브랜드를 가져옵니다.", status = 200)

class brandSearchView(APIView):
    def get(self, request):
        return Response("브랜드 검색 결과를 보여줍니다.", status = 200)

class markedBrandView(APIView):
    def get(self, request):
        return Response("북마크한 브랜드를 모아서 보여줍니다.", status = 200)

class markedBrandSearchView(APIView):
    def get(self, request):
        return Response("북마크한 브랜드 중에서 검색한 결과를 보여줍니다.", status = 200)

class markedBrandSearchView(APIView):
    def get(self, request):
        return Response("북마크한 브랜드 중에서 검색한 결과를 보여줍니다.", status = 200)

class markedBrandCountView(APIView):
    def post(self, request):
        return Response("브랜드를 북마크한 횟수를 카운팅합니다.", status = 200)

class BrandCountView(APIView):
    def post(self, request):
        return Response("브랜드를 클릭한 횟수를 카운팅합니다.", status = 200)
