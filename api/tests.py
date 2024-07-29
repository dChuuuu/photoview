from django.conf import settings
from django.db import IntegrityError
from django.test import TestCase
from .models import Posts, Comments, PostsCommentsManager

import pytest
'''ЮНИТ-ТЕСТЫ ДЛЯ МОДЕЛЕЙ ПОСТОВ И КОММЕНТАРИЕВ'''

def create_post():
    '''Создаёт пост'''
    post = Posts.objects.create(title='TestTitle', content='TestContent', picture='TestPicture')
    return post


def create_post_invalid():
    '''Создаёт пост с некорректным id'''
    post = Posts.objects.create(post_id='asdsad')
    return post

def get_post(post=None):
    '''Получение поста из БД'''
    post = Posts.objects.get(post_id=post.post_id)
    return post


def create_comment(post=None):
    '''Создание комментария со ссылкой на пост(объект)'''
    comment = Comments.objects.create(post_id=post, comment_id=111111, content='TestComment')
    return comment


def create_comment_invalid(post=None):
    '''Создание комментария с некорректным id'''
    comment = Comments.objects.create(post_id=post, comment_id='111111', content='TestComment')


def get_comment(comment=None):
    '''Получение комментария из БД'''
    comment = Comments.objects.get(comment_id=comment.comment_id)
    return comment

@pytest.mark.django_db
class TestPostsModel:
    '''Тестирование функционала модели постов'''
    def test_post_add(self):
        '''Создаёт пост с базовыми параметрами и проверяет их наличие, соответствие'''
        post = create_post()

        assert post.title == 'TestTitle'
        assert post.content == 'TestContent'
        assert post.picture == 'TestPicture'

    def test_post_add_invalid_data(self):
        '''Создаёт пост с некорректным id, проверяет на возникновение исключения'''
        try:
            post = create_post_invalid()
            assert False
        except:
            assert True


    def test_post_edit(self):
        '''Редактирование поста, проверка на соответствие данных исходным и их наличие'''
        post = create_post()
        updated_post = get_post(post)
        updated_post.title = 'TestEditedTitle'
        updated_post.content = 'TestEditedContent'
        updated_post.picture = 'TestEditedPicture'

        assert updated_post.title == 'TestEditedTitle'
        assert updated_post.content == 'TestEditedContent'
        assert updated_post.picture == 'TestEditedPicture'

    def test_post_nocomments_delete(self):
        '''Удаление поста, не содержащего комментарии, проверка'''
        post = create_post()
        post_delete = get_post(post)
        post_delete.delete()

        try:
            get_post(post)
            assert False
        except:
            assert True

    def test_post_wcomments_delete(self):
        '''Удаление поста с комментариями, проверка на связь моделей'''
        post = create_post()
        comment = create_comment(post)
        post_delete = get_post(post)
        post_delete.delete()

        try:
            get_comment(comment)
            assert False
        except:
            assert True


@pytest.mark.django_db
class TestCommentsModel:
    '''Тестирование функционала модели комментариев'''
    def test_add_comment_wpostid(self):
        '''Добавление комментария с имеющимся id поста'''
        post = create_post()
        comment = create_comment(post)
        assert comment.post_id == post
        assert comment.content == 'TestComment'

    def add_comment_invalid_data(self):
        '''Добавление комментария с некорректным id'''
        try:
            comment = create_comment_invalid()
            assert False
        except:
            assert True

    def test_add_comment_nopostid(self):
        '''Добавление комментария без id поста, проверка на исключение'''
        try:
            comment = create_comment()
            assert False
        except:
            assert True

    def test_comment_edit(self):
        '''Редактирование поста, проверка на соответствие данным'''
        post = create_post()
        comment = create_comment(post)
        updated_comment = get_comment(comment)
        updated_comment.content = 'UpdatedCommentContent'

        assert updated_comment.content == 'UpdatedCommentContent'

    def test_comment_delete(self):
        '''Удаление комментария, проверка'''
        post = create_post()
        comment = create_comment(post)
        comment = get_comment(comment)
        comment.delete()

        try:
            get_comment(comment)
            assert False
        except:
            assert True

