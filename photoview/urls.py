"""
URL configuration for photoview project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
import os


from api.views import PostsAPIView, PostAPIView, CommentsAPIView, CommentsDeleteAPIView

'''TODO ДОБАВИТЬ ЛОКАЛЬНЫЕ УРЛЫ ДЛЯ API И ИНТЕГРИРОВАТЬ ЧЕРЕЗ include()'''

schema_view = get_schema_view(
    openapi.Info(
        title="API",
        default_version='v1',
        description="API documentation",
        terms_of_service="<https://www.google.com/policies/terms/>",
        contact=openapi.Contact(email="contact@api.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

# router = SimpleRouter()
# router.register('posts', PostsViewSet)
# router.register('comments', CommentsViewSet)
urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('api/v1/post/<int:pk>/', PostAPIView.as_view(), name='post'),
    # path('api/v1/', include(router.urls))
    path('api/v1/posts/', PostsAPIView.as_view(), name='posts'),
    path('api/v1/comments/<int:post_id>/', CommentsAPIView.as_view(), name='comment'),
    path('api/v1/comments/delete/<int:pk>/', CommentsDeleteAPIView.as_view(), name='comment-delete'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    # path('api/v1/posts/create', PostsViewSet.as_view({'post': 'create'})),
    # path('api/v1/posts/edit/<int:pk>', PostsViewSet.as_view({'put': 'update'})),
    # path('api/v1/posts/delete/<int:pk>', PostsViewSet.as_view({'delete': 'destroy'}))
]
#sometestsssss