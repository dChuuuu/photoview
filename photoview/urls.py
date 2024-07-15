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
from api.views import PostsViewSet, CommentsViewSet

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/posts', PostsViewSet.as_view({'get': 'list'})),
    path('api/v1/posts/create', PostsViewSet.as_view({'post': 'create'})),
    path('api/v1/posts/edit/<int:pk>', PostsViewSet.as_view({'put': 'retrieve'})),
    path('api/v1/posts/delete/<int:pk>', PostsViewSet.as_view({'delete': 'destroy'}))
]
