from django.db import models

'''Модели для связи с БД'''


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
    title = models.CharField(max_length=256)
    content = models.TextField(max_length=1024, default=None)
    picture = models.TextField(default=None)
    likes = models.BigIntegerField(default=0)
    date_time_created = models.DateField(auto_now_add=True)
    date_time_edited = models.DateField(auto_now_add=True)


class Comments(models.Model):
    '''Класс описывает модель комментариев:
    comment_id - Идентификатор комментария;
    content - Содержимое комментария;
    post_id - Внешний ключ на Posts
    TODO РЕАЛИЗОВАТЬ ОБНОВЛЕНИЕ В РЕАЛЬНОМ ВРЕМЕНИ НА УРОВНЕ БЭКЕНДА'''
    comment_id = models.BigAutoField(primary_key=True, unique=True)
    content = models.CharField(max_length=256)
    post_id = models.ForeignKey('Posts', on_delete=models.CASCADE)
