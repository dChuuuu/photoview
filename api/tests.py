from django.conf import settings
from django.test import TestCase
from .models import Comments, PostsCommentsManager
import pytest
# Create your tests here.

def test_comment_without_post():

    instance = Comments()
    instance.objects.create(post_id=1, content='content')
