from rest_framework import status, viewsets, mixins 
from rest_framework.response import Response 
from django.views import View 
from django.http import Http404

from .models import Music 
from .serializers import MusicSerializer

# Create your views here. 

class MusicViewSet(viewsets.GenericViewSet, 
                mixins.ListModelMixin, 
                View): 

    serializer_class = MusicSerializer   # 이 클래스형 view 에서 사용할 시리얼라이저를 선언

    def get_queryset(self):
        conditions = {
            'id': self.kwargs.get("music_num", None),
            'title__contains': self.request.GET.get('title', None),
            'star_rating': self.request.GET.get('star_rating', None),
            'singer__contains': self.request.GET.get('singer', None),
            'category__in': [self.request.GET.get('category_'+str(i+1), None) for i in range(4)],
            'created_at__lte': self.request.GET.get('created_at', None),
        }
        conditions = {key: val for key, val in conditions.items() if val is not None}

        musics = Music.objects.filter(**conditions)
        if not musics.exists():
            raise Http404()

        return musics

    def add(self, request): 
        musics = Music.objects.filter(**request.data)
        if musics.exists():
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE)

        music_serializer = MusicSerializer(data=request.data, partial=True)
        if not music_serializer.is_valid():
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE)

        music = music_serializer.save()

        return Response(MusicSerializer(music).data, status=status.HTTP_201_CREATED)