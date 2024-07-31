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

    # def test_posts_patch(self, client, url_posts):
    #     data = {'title': 'Testing title',
    #             'content': 'Testing content',
    #             'picture': 'Testing pictures'}
    #     response = client.post(url_posts, data=data, format='json')
    #     response = client.get(url_posts, data=response.post_id, format='json')

    # def test_post_get(self, client, url_posts):
    #     data_request = {'title': 'Testing title',
    #             'content': 'Testing content',
    #             'picture': 'Testing pictures'}
    #     request = client.post(url_posts, data=data_request, format='json')
    #     data_response = {'post_id': request.data['post_id']}
    #     response = client.get(url_posts, data=data_response, format='json')
    #
    #     assert response.status_code == status.HTTP_200_OK
