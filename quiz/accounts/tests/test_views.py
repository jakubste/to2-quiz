from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from quiz.utils.unittestcase import TestCase


class RegisterViewTest(TestCase):
    url = 'accounts:register'

    def setUp(self):
        self.data = {
            'username': 'Moniczka86',
            'email': 'test@example.com',
            'password': 'haslo123',
        }

    def test_creates_user(self):
        response = self.get_response(method='post', data=self.data)

        # self.assertEquals(302, response.status_code)
        user = User.objects.get(username=self.data['username'])
        self.assertEquals(response.wsgi_request.user, user)

    def test_does_not_create_user(self):
        data = self.data.copy()
        data['email'] = ""

        response = self.get_response(method='post', data=data)

        self.assertEquals(200, response.status_code)
        self.assertTrue(response.context['form'].errors)
        self.assertFalse(
            User.objects.filter(username=self.data['username']).exists()
        )

    def test_already_exists(self):
        data = self.data.copy()
        self.get_response(method='post', data=data)
        data['email'] = 'test+moniczka@example.com'
        response = self.get_response(method='post', data=data)

        self.assertEquals(200, response.status_code)
        self.assertTrue(response.context['form'].errors)
        self.assertEquals(
            User.objects.get(username=self.data['username']).email,
            self.data['email']
        )

    def test_passes_form(self):
        response = self.get_response()

        self.assertEquals(200, response.status_code)
        self.assertIn('form', response.context)


class LoginTestView(TestCase):
    def setUp(self):
        self.url = reverse('accounts:login')
        self.username = 'henio'
        self.email = 'henio@wp.pl'
        self.password = 'abc123'
        User.objects.filter(username=self.username).delete()
        User.objects.create_user(self.username, self.email, self.password)

    def test_logs_user_by_username(self):
        response = self.client.post(self.url, {'username': self.username, 'password': self.password})
        self.assertEquals(302, response.status_code)


class LogoutView(TestCase):
    def setUp(self):
        self.user = self.login(username='LogoutTestUser')
        self.url = reverse('accounts:logout')

    def test_logout_logouts_user(self):
        self.client.get(self.url)
        response = self.client.get(reverse('polls:quiz_list'))
        self.assertEqual(response.context['user'].is_authenticated(), False)
