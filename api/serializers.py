from rest_framework import serializers
from .models import Posts, Comments

'''Сериализаторы для моделей. Позволяют де- и сериализовать данные в JSON формат'''


class PostsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Posts
        fields = '__all__'


class CommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = '__all__'
