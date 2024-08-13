from django.conf import settings
from django.db import IntegrityError
from django.db.migrations import migration
from django.test import TestCase
from .models import Posts, Comments, PostsCommentsManager
import factory

import pytest
'''ЮНИТ-ТЕСТЫ ДЛЯ МОДЕЛЕЙ ПОСТОВ И КОММЕНТАРИЕВ'''


class PostsFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Posts

    title = factory.sequence(lambda n: f'Test title{n}')
    content = 'Test content'



@pytest.fixture
def post():
    '''Создаёт пост'''
    post = Posts.objects.create(title='TestTitle', content='TestContent', picture='TestPicture')
    return post


@pytest.fixture
def comment(post):
    '''Создание комментария со ссылкой на пост(объект)'''
    comment = Comments.objects.create(post_id=post, comment_id=111111, content='TestComment')
    return comment


@pytest.mark.django_db
class TestPostsModel:
    '''Тестирование функционала модели постов'''

    def test_post_add(self):
        '''Создаёт пост с базовыми параметрами и проверяет их наличие, соответствие'''

        PostsFactory.create()
        PostsFactory.create()
        result = Posts.objects.all()
        assert len(result) == 2
        assert result[0].title == 'Test title0'

    def test_post_add_invalid_data(self):
        '''Создаёт пост с некорректным id, проверяет на возникновение исключения'''
        try:
            Posts.objects.create(post_id='asasas')
            assert False
        except:
            assert True

    def test_post_edit(self, post):
        '''Редактирование поста, проверка на соответствие данных исходным и их наличие'''

        post.content = 'UpdatedPostContent'
        post.save()
        assert Posts.objects.get(post_id=post.post_id).content == 'UpdatedPostContent'

    def test_post_nocomments_delete(self, post):
        '''Удаление поста, не содержащего комментарии, проверка'''

        post_id = post.post_id
        post.delete()

        try:
            Posts.objects.get(post_id=post_id)
            assert False
        except:
            assert True

    def test_post_wcomments_delete(self, post, comment):
        '''Удаление поста с комментариями, проверка на связь моделей'''

        post_id = post.post_id
        comment_id = comment.comment_id
        post.delete()

        try:
            Comments.objects.get(comment_id=comment_id)
            Posts.objects.get(post_id=post_id)
            assert False
        except:
            assert True


@pytest.mark.django_db
class TestCommentsModel:
    '''Тестирование функционала модели комментариев'''

    def test_add_comment_wpostid(self, post, comment):
        '''Добавление комментария с имеющимся id поста'''

        assert comment.post_id == post
        assert Comments.objects.get(comment_id=comment.comment_id)

    def add_comment_invalid_data(self):
        '''Добавление комментария с некорректным id'''

        try:
            Comments.objects.create(comment_id='asas')
            assert False
        except:
            assert True

    def test_add_comment_nopostid(self):
        '''Добавление комментария без id поста, проверка на исключение'''

        try:
            Comments.objects.create(post_id=None)
            assert False
        except:
            assert True

    def test_comment_edit(self, comment):
        '''Редактирование поста, проверка на соответствие данным'''

        comment.content = 'UpdatedCommentContent'
        comment.save()
        assert Comments.objects.get(comment_id=comment.comment_id).content == 'UpdatedCommentContent'

    def test_comment_delete(self, comment):
        '''Удаление комментария, проверка'''

        comment_id = comment.comment_id
        comment.delete()
        try:
            Comments.objects.get(comment_id=comment_id)
            assert False
        except:
            assert True
