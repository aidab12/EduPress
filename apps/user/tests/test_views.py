from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase

User = get_user_model()

class UsersAPIViewsTests(APITestCase):

    def test_singup_api_view_is_working(self):
        url = reverse('user:singup_api_view')
        body = {'email': 'abdatest@maildrop.cc', 'password': 'secret12345'}
        response = self.client.post(url, body, format='json')
        self.assertEqual(response.status_code, 201)
        user = User.objects.filter(email=body['email']).first()
        self.assertIsNotNone(user)
        self.assertTrue(user.check_password(body['password']))

    def test_signup_api_view_no_double_email(self):
        user = User.objects.create_user(email="abdatest@maildrop.cc", password="secret12345")
        url = reverse("user:singup_api_view")
        body = {'email': 'abdatest@maildrop.cc', 'password': 'secret12345'}
        response = self.client.post(url, body, format='json')
        self.assertEqual(response.status_code, 400)
