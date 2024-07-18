from django.http import Http404
from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import PostsSerializer, CommentsSerializer
from .models import Posts, Comments
# Create your views here.


class PostsAPIView(APIView):
    '''Полный набор CRUD-операций над постами'''

    def get(self, request):
        paginator = PageNumberPagination()
        data = Posts.objects.all()
        result_page = paginator.paginate_queryset(queryset=data, request=request)
        serializer = PostsSerializer(data=result_page, many=True)
        serializer.is_valid()
        return Response({"posts": serializer.data}, status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data
        serializer = PostsSerializer(data=data)
        if serializer.is_valid() and 'title' in data:
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        post_id = Posts.objects.get_object_or_404(pk)
        data = request.data
        serializer = PostsSerializer(post_id, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        '''TODO ВЕРНУТЬ ИНСТАНС В ОТВЕТЕ'''
        instance = Posts.objects.get_object_or_404(pk)
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class PostAPIView(APIView):
    def get(self, request, pk):
        try:
            instance = Posts.objects.get_object_or_404(post_id=pk)
        except:
            raise Http404
        serializer = PostsSerializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CommentsViewSet(viewsets.ModelViewSet):
     serializer_class = CommentsSerializer
     queryset = Comments.objects.all()

