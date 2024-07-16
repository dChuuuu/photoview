from django.http import Http404
from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import PostsSerializer, CommentsSerializer
from .models import Posts, Comments
# Create your views here.


class PostsAPIView(APIView):
    def get(self, request):
        data = Posts.objects.all()
        serializer = PostsSerializer(data=data, many=True)
        serializer.is_valid()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data
        serializer = PostsSerializer(data=data)
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class PostAPIView(APIView):
    def get(self, request, pk):
        try:
            instance = Posts.objects.get(post_id=pk)
        except:
            raise Http404
        serializer = PostsSerializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)





class CommentsViewSet(viewsets.ModelViewSet):
     serializer_class = CommentsSerializer
     queryset = Comments.objects.all()

