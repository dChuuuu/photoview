from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView


from .models import Comments, Posts
from .serializers import CommentsSerializer, PostsSerializer

# Create your views here.ssssss


class PostsAPIView(APIView):

    def get(self, request):
        '''Получает все посты, хранящиеся в БД'''

        paginator = PageNumberPagination()
        data = Posts.objects.all()
        result_page = paginator.paginate_queryset(
            queryset=data, request=request)
        serializer = PostsSerializer(data=result_page, many=True)
        serializer.is_valid()
        return Response({"posts": serializer.data}, status=status.HTTP_200_OK)

    request_schema_dict = openapi.Schema(
        title=("Create post"),
        type=openapi.TYPE_OBJECT,
        properties={

            'title': openapi.Schema(type=openapi.TYPE_STRING,
                                    description=('Заголовок поста'),
                                    example='Post title'),

            'content': openapi.Schema(type=openapi.TYPE_STRING,
                                      description=('Содержимое поста'),
                                      example="Post content"),

            'picture': openapi.Schema(type=openapi.TYPE_STRING,
                                      description=(
                                          'Изображение в Base64 формате'),
                                      example="Some picture"),
        }
    )

    @swagger_auto_schema(request_body=request_schema_dict, responses={200: 'OK'})
    def post(self, request):
        '''Отправляет данные о посте при его создании'''
        data = request.data
        serializer = PostsSerializer(data=data)
        if serializer.is_valid() and 'title' in data:
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostAPIView(APIView):
    request_schema_dict = openapi.Schema(
        title=("Create post"),
        type=openapi.TYPE_OBJECT,
        properties={

            'title': openapi.Schema(type=openapi.TYPE_STRING,
                                    description=('Заголовок поста'),
                                    example='Post title'),

            'content': openapi.Schema(type=openapi.TYPE_STRING,
                                      description=('Содержимое поста'),
                                      example="Post content"),

            'picture': openapi.Schema(type=openapi.TYPE_STRING,
                                      description=(
                                          'Изображение в Base64 формате'),
                                      example="Some picture"),
        }
    )

    @swagger_auto_schema(request_body=request_schema_dict, responses={200: 'OK'})
    def patch(self, request, pk):
        '''Изменение поста'''
        post_id = Posts.objects.get_object_or_404(pk)
        data = request.data
        serializer = PostsSerializer(post_id, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, pk):
        '''Получение одного поста'''
        instance = Posts.objects.get_object_or_404(pk)
        serializer = PostsSerializer(instance)
        return Response({"post": serializer.data}, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        '''Удаление поста'''
        instance = Posts.objects.get_object_or_404(pk)
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CommentsAPIView(APIView):

    def get(self, request, post_id):
        '''Получение списка комментариев для поста'''
        instance = Comments.objects.filter_object_or_404(pk=post_id)
        paginator = PageNumberPagination()
        result_page = paginator.paginate_queryset(
            queryset=instance, request=request)
        serializer = CommentsSerializer(data=result_page, many=True)
        serializer.is_valid()
        return Response({"comments": serializer.data}, status=status.HTTP_200_OK)

    request_schema_dict = openapi.Schema(
        title=("Create post"),
        type=openapi.TYPE_OBJECT,
        properties={

            'post_id': openapi.Schema(type=openapi.TYPE_STRING,
                                      description=('Идентификатор поста'),
                                      example='16'),

            'content': openapi.Schema(type=openapi.TYPE_STRING,
                                      description=('Содержимое комментария'),
                                      example="Это мой комментарий!"),

        }
    )

    @swagger_auto_schema(request_body=request_schema_dict, responses={200: 'OK'})
    def post(self, request, post_id):
        '''Написание комментария к посту'''
        data = request.data
        serializer = CommentsSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentsDeleteAPIView(APIView):
    '''Удаляет комментарий по родному идентификатору comment_id'''

    def delete(self, request, pk):
        instance = Comments.objects.delete_comment_if_found(pk)
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
