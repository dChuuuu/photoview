from django.db import models
from django.http import Http404

'''Модели для связи с БД'''

class PostsManager(models.Manager):
    '''Менеджер добавляет функционал по работе с постами
    get_object_or_404 - возвращает объект, либо статус 404'''
    def get_queryset(self):
        return super().get_queryset()

    def get_object_or_404(self, pk):
        try:
            instance = Posts.objects.get(post_id=pk)
        except:
            raise Http404
        return instance

class Posts(models.Model):
    '''Класс описывает модель постов:
    post_id - Идентификатор поста;
    title - Заголовок поста;
    content - Содержимое поста
    picture - Изображение относящееся к посту. Кодировка Base64. По умолчанию None TODO ЗАПИЛИТЬ ДОБАВЛЕНИЕ НЕСКОЛЬКИХ IMG
    likes - Лайки на посте TODO РЕАЛИЗОВАТЬ ОБНОВЛЕНИЕ В РЕАЛЬНОМ ВРЕМЕНИ НА УРОВНЕ БЭКЕНДА
    date_time_created - Дата и время создания поста
    date_time_edited - Дата редактирования поста TODO РЕАЛИЗОВАТЬ ТАЙМЕР СУТКИ НА РЕДАКТИРОВАНИЕ ПОСТА'''

    post_id = models.BigAutoField(primary_key=True, unique=True)
    title = models.CharField(max_length=256, null=True)
    content = models.TextField(max_length=1024, default=None, null=True)
    picture = models.TextField(default=None, null=True)
    likes = models.BigIntegerField(default=0)
    date_time_created = models.DateField(auto_now_add=True)
    date_time_edited = models.DateField(auto_now_add=True)

    objects = PostsManager()


class Comments(models.Model):
    '''Класс описывает модель комментариев:
    comment_id - Идентификатор комментария;
    content - Содержимое комментария;
    post_id - Внешний ключ на Posts
    TODO РЕАЛИЗОВАТЬ ОБНОВЛЕНИЕ В РЕАЛЬНОМ ВРЕМЕНИ НА УРОВНЕ БЭКЕНДА'''
    comment_id = models.BigAutoField(primary_key=True, unique=True)
    content = models.CharField(max_length=256)
    post_id = models.ForeignKey('Posts', on_delete=models.CASCADE)
