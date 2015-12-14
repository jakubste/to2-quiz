from django.core.urlresolvers import reverse
from django.test import TestCase as DjangoTestCase
from quiz.accounts.factories import UserFactory


class TestCase(DjangoTestCase):
    url = ''

    def get_url(self):
        return reverse(self.url)

    def get_response(self, url=None, method='get', data={}):
        if url is None:
            url = self.get_url()

        return getattr(self.client, method)(url, data)

    def login(self, **user_kwargs):
        user = UserFactory.create(**user_kwargs)
        user.set_password('secret')
        user.save()
        self.client.login(username=user.username, password='secret')
        return user
