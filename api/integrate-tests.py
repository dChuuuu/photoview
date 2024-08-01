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


# @pytest.fixture
# def url_post(request):
#     url = reverse('post', args=[request.param])
#     return url


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
    def test_post_get(self, client, url_posts):
        data_request = {'title': 'Testing title',
                        'content': 'Testing content',
                        'picture': 'Testing pictures'}
        request = client.post(url_posts, data=data_request, format='json')
        data_response = {'post_id': request.data['post_id']}
        url_post = reverse('post', args=str(request.data['post_id']))
        response = client.get(url_post, data=data_response, format='json')

        assert response.status_code == status.HTTP_200_OK
        assert request.data['post_id'] == response.data['post']['post_id']

    def test_post_patch(self, client, url_posts):
        data = {'title': 'Testing title',
                'content': 'Testing content',
                'picture': 'Testing pictures'}
        response = client.post(url_posts, data=data, format='json')
        url_post = reverse('post', args=str(response.data['post_id']))
        data_response = {'post_id': response.data['post_id']}
        response = client.get(url_post, data=data_response, format='json')
        response.data['title'] = 'Edited title'
        response = client.patch(url_post, data=response.data, format='json')

        assert response.data['title'] == 'Edited title'

    def test_post_delete(self, client, url_posts):
        data = {'title': 'Testing title',
                'content': 'Testing content',
                'picture': 'Testing pictures'}
        response = client.post(url_posts, data=data, format='json')
        url_post = reverse('post', args=str(response.data['post_id']))
        response = client.delete(url_post, data=response.data['post_id'], format='json')

        assert response.status_code == status.HTTP_204_NO_CONTENT
