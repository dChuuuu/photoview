import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

@pytest.fixture
def client():
    client = APIClient()
    return client


@pytest.fixture
def url_posts():
    url = reverse('posts')
    return url


@pytest.fixture
def post(client, url_posts, request):
    data_request = {'title': 'Testing title',
                    'content': 'Testing content',
                    'picture': 'Testing pictures'}
    request = client.post(url_posts, data=data_request, format='json')
    url = reverse('post', args=[request.data['post_id']])
    return {'post_url': url, 'post_id': request.data['post_id'], 'data': request.data}

@pytest.fixture
def comment(client, post, request):
    data_request = {'post_id': post['post_id'],
                    'content': 'Comment content'}
    url = reverse('comment', args=[post['post_id']])
    request = client.post(url, data=data_request, format='json')
    return {'comment_id': request.data['comment_id'], 'data': request.data, 'status': request.status_code, 'url': url}

@pytest.fixture
def comment_delete(client, request, comment):
    data_request = {'comment_id': comment['comment_id']}
    url = reverse('comment-delete', args=[comment['comment_id']])
    return {'url': url}


@pytest.mark.django_db
class TestPosts:

    def test_posts_create(self, client, url_posts):
        data = {'title': 'Testing title',
                'content': 'Testing content',
                'picture': 'Testing pictures'}
        response = client.post(url_posts, data=data, format='json')

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['title'] == data['title']
        assert response.data['content'] == data['content']
        assert response.data['picture'] == data['picture']

    def test_posts_get(self, client, url_posts):
        data_first = {'title': 'Testing title',
                      'content': 'Testing content',
                      'picture': 'Testing pictures'}
        response = client.post(url_posts, data=data_first, format='json')

        data_second = {'title': 'Testing title1',
                       'content': 'Testing content1',
                       'picture': 'Testing pictures1'}
        response = client.post(url_posts, data=data_second, format='json')

        data_third = {'title': 'Testing title2',
                      'content': 'Testing content2',
                      'picture': 'Testing pictures2'}
        response = client.post(url_posts, data=data_third, format='json')

        response = client.get(url_posts, format='json')

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['posts']) == 3


@pytest.mark.django_db
class TestPost:

    def test_post_get(self, client, post, url_posts):
        post_id = post['post_id']
        response = client.get(post['post_url'], data={'post_id': post_id}, format='json')

        assert response.data['post']['post_id'] == post_id
        assert response.status_code == status.HTTP_200_OK
        assert post_id == response.data['post']['post_id']

    def test_post_patch(self, client, post, url_posts):
        response = client.patch(post['post_url'], data={'title': 'Edited title'}, format='json')

        assert response.data['title'] == 'Edited title'

    def test_post_delete(self, client, post, url_posts):
        post_id = post['post_id']
        response = client.delete(post['post_url'], data={'post_id': post_id}, format='json')

        assert response.status_code == status.HTTP_204_NO_CONTENT

@pytest.mark.django_db
class TestComment:
    def test_comments_create(self, comment):
        assert comment['status'] == status.HTTP_200_OK

    def test_comments_get(self, comment, client):
        response = client.get(comment['url'], format='json')

        assert response.status_code == status.HTTP_200_OK
        assert response.data['comments'][0]['comment_id'] == comment['comment_id']

    def test_comments_delete(self, comment_delete, client):
        response = client.delete(comment_delete['url'], format='json')
        assert response.status_code == status.HTTP_204_NO_CONTENT
