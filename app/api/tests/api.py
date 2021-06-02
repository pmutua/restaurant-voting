from rest_framework.test import APITestCase
from django.urls import reverse
from api.models import *
from api.custom_jwt import *
from rest_framework import status


class TestRegisterUserAPI(APITestCase):
    def test_post_request_can_register_new_user(self):

        data = {
            "email": "punakepis@dropjar.com ",
            "first_name": "George",
            "last_name": "Lucas",
            "phone": "+2404554444",
            "identification_no": "5343434242",
            "role": "employee"

        }
        res = self.client.post(reverse("api:register-user"), data=data)
        status = res.json().get('success')
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(status, True)


class TestLoginClientAPI(APITestCase):
    def test_post_request_can_login_user(self):
        user = User.objects.create(
            first_name='John',
            last_name='Hendrix',
            email='lennon@thebeatles.com'
        )

        user.set_password('johnpassword')
        user.save()
        data = {
            "email": "lennon@thebeatles.com",
            "password": "johnpassword"

        }
        res = self.client.post(reverse("api:user-login"), data=data)
        status = res.json().get('success')
        self.assertEqual(status, True)


class TestCreateRestaurantAPI(APITestCase):

    def setUp(self):
        self.user = User.objects.create_superuser('admin', 'admin@admin.com', 'admin123')
        self.payload = jwt_payload_handler(self.user)
        self.token = jwt_encode_handler(self.payload).decode('UTF-8')
        self.api_authentication()

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

    def test_post_request_can_create_new_restaurant(self):
        data = {
            "name": "punakepis@dropjar.com ",
            "contact_no": "+722212132",
            "address": "Nairobi"

        }
        res = self.client.post(reverse("api:create-restaurant"), data=data, format='json')
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_post_request_create_new_restaurant_unauthenticated(self):

        self.client.force_authenticate(user=None)
        data = {
            "name": "punakepis@dropjar.com ",
            "contact_no": "+722212132",
            "address": "Nairobi"

        }
        res = self.client.post(reverse("api:create-restaurant"), data=data, format='json')
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
