from django.shortcuts import render
from rest_framework import viewsets
from .serializers import PostsSerializer, CommentsSerializer
from .models import Posts, Comments
# Create your views here.


class PostsViewSet(viewsets.ModelViewSet):
    serializer = PostsSerializer
    queryset = Posts.objects.all()


class CommentsViewSet(viewsets.ModelViewSet):
    serializer = CommentsSerializer
    queryset = Comments.objects.all()