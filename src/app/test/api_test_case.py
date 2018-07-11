from django.test import TestCase
from mixer.backend.django import mixer
from rest_framework import status
from rest_framework.test import APIClient

USER_PASSWORD = '123456'


class ApiTestCase(TestCase):

    c = APIClient()

    @classmethod
    def setUpClass(cls):
        cls.create_user()
        cls.c.login(username=cls.user.username, password=USER_PASSWORD)
        super().setUpClass()

    def api_get(self, *args, **kwargs):
        return self._api_call('get', status.HTTP_200_OK, *args, **kwargs)

    def api_post(self, *args, **kwargs):
        return self._api_call('post', status.HTTP_201_CREATED, *args, **kwargs)

    def api_put(self, *args, **kwargs):
        return self._api_call('put', status.HTTP_200_OK, *args, **kwargs)

    def api_delete(self, *args, **kwargs):
        return self._api_call('delete', status.HTTP_204_NO_CONTENT, *args, **kwargs)

    def _api_call(self, method, expected, *args, **kwargs):
        kwargs['format'] = kwargs.get('format', 'json')

        method = getattr(self.c, method)
        response = method(*args, **kwargs)

        content = response.json() if len(response.content) else None

        assert response.status_code == expected, content

        return content

    @classmethod
    def create_user(cls):
        """If you want to create user on your way - just override this method in child test class"""
        user = mixer.blend('auth.User')
        user.set_password(USER_PASSWORD)
        user.save()
        cls.user = user
