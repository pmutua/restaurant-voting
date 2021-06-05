
from datetime import timedelta
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile

from api.models import (
    Role,
    User,
    Employee,
    Restaurant,
    Menu,
    Vote

)

from api.custom_jwt import *

from rest_framework import status
from rest_framework.test import APITestCase

import mock




class TestRolesAPI(APITestCase):

    def setUp(self):
        self.role = Role.objects.create(name='admin')

    def test_get_request_get_all_roles(self):

        res = self.client.get(reverse("api:roles"))
        self.assertEqual(Role.objects.count(), 1)
        self.assertEqual(res.status_code, status.HTTP_200_OK)


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
        res = self.client.post(reverse("api:login"), data=data)
        status = res.json().get('success')
        self.assertEqual(status, True)


class TestUserLogOutAPI(APITestCase):

    def setUp(self):
        self.user = User.objects.create_superuser('admin', 'admin@admin.com', 'admin123')
        self.payload = jwt_payload_handler(self.user)
        self.token = jwt_encode_handler(self.payload).decode('UTF-8')
        self.api_authentication()

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

    def test_post_request_user_can_logout(self):

        res = self.client.get(reverse("api:logout"))

        self.assertEqual(res.status_code, status.HTTP_205_RESET_CONTENT)

    def test_post_request_can_logout_unauthenticated(self):

        self.client.force_authenticate(user=None)

        res = self.client.post(reverse("api:logout"))
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


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


class TestCreateUploadMenuAPI(APITestCase):

    def setUp(self):
        self.user = User.objects.create_superuser('admin', 'admin@admin.com', 'admin123')
        self.payload = jwt_payload_handler(self.user)
        self.token = jwt_encode_handler(self.payload).decode('UTF-8')
        self.api_authentication()

        self.restaurant = Restaurant.objects.create(name='Burger King', contact_no='+722212132', address='Nairobi')

        self.file = SimpleUploadedFile("file.txt", b"abc", content_type="text/plain")
        self.payload = {"file": self.file, 'restaurant': self.restaurant.id}

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

    def test_post_request_can_upload_menu(self):

        res = self.client.post(reverse("api:upload-menu"), data=self.payload, format="multipart")

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_post_request_upload_menu_unauthenticated(self):

        self.client.force_authenticate(user=None)

        res = self.client.post(reverse("api:upload-menu"), data=self.payload, format="multipart")
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class TestCreateEmployeeAPI(APITestCase):

    def setUp(self):
        self.user = User.objects.create_superuser('admin', 'admin@admin.com', 'admin123')
        self.payload = jwt_payload_handler(self.user)
        self.token = jwt_encode_handler(self.payload).decode('UTF-8')
        self.api_authentication()

        self.payload = {
            "email": "punakepis@dropjar.com ",
            "first_name": "George",
            "last_name": "Lucas",
            "phone": "+2404554444",
            "identification_no": "5343434242",
            "employee_no": "XV-098335"

        }

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

    def test_post_request_can_create_new_employee(self):

        res = self.client.post(reverse("api:create-employee"), data=self.payload, format="json")
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_post_request_create_new_employee_unauthenticated(self):

        self.client.force_authenticate(user=None)

        res = self.client.post(reverse("api:create-employee"), data=self.payload, format="json")
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class TestGetRestaurantsAPI(APITestCase):

    def setUp(self):
        self.restaurant = Restaurant.objects.create(name='Burger King', contact_no='+722212132', address='Nairobi')

    def test_get_request_all_restaurants(self):

        res = self.client.get(reverse("api:restaurants"))
        self.assertEqual(Restaurant.objects.count(), 1)
        self.assertEqual(res.status_code, status.HTTP_200_OK)


class TestGetCurrentDayMenuListAPI(APITestCase):

    def setUp(self):
        self.user = User.objects.create_superuser('admin', 'admin@admin.com', 'admin123')

        self.restaurant = Restaurant.objects.create(name='Burger King', contact_no='+722212132', address='Nairobi')

        self.file = SimpleUploadedFile("file.txt", b"abc", content_type="text/plain")

        self.menu = Menu.objects.create(restaurant=self.restaurant, file=self.file, uploaded_by=self.user.username)

    def test_get_request_all_current_day_menu_list(self):
        res = self.client.get(reverse("api:menu-list"))
        self.assertEqual(Menu.objects.count(), 1)
        self.assertEqual(res.status_code, status.HTTP_200_OK)


class TestVoteMenuAPI(APITestCase):

    def setUp(self):
        self.user = User.objects.create_superuser('admin', 'admin@admin.com', 'admin123')
        self.employee = Employee.objects.create(user=self.user, employee_no="BN-0966333")
        self.payload = jwt_payload_handler(self.user)
        self.token = jwt_encode_handler(self.payload).decode('UTF-8')
        self.api_authentication()

        self.restaurant = Restaurant.objects.create(name='Burger King', contact_no='+722212132', address='Nairobi')

        self.file = SimpleUploadedFile("file.txt", b"abc", content_type="text/plain")

        self.menu = Menu.objects.create(restaurant=self.restaurant, file=self.file, uploaded_by=self.user.username)

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

    def test_get_request_employee_can_vote(self):

        res = self.client.get(reverse("api:new-vote", kwargs={'menu_id': self.menu.id}))

        self.assertEqual(Vote.objects.count(), 1)
        self.assertEqual(res.status_code, status.HTTP_200_OK)


class TestGetResultsAPI(APITestCase):

    def setUp(self):
        self.user = User.objects.create_superuser('admin', 'admin@admin.com', 'admin123')

        self.file = SimpleUploadedFile("file.txt", b"abc", content_type="text/plain")

        self.data = [
            {
                "votes": 10,
                "name": 'Burger King'
            },
            {
                "votes": 4,
                "name": 'Caribean Food Dishes'
            },
            {
                "votes": 8,
                "name": 'Janet Dishes'
            }

        ]

        self.restaurant_list = [
            Restaurant.objects.create(
                name=item.get('name'),
                contact_no='+722212132',
                address='Nairobi') for item in self.data]

        yesterday = datetime.now() - timedelta(days=1)

        yy = yesterday - timedelta(days=1)

        yyy = yy - timedelta(days=1)

        with mock.patch('django.utils.timezone.now') as mock_now:
            mock_now.return_value = yesterday

            self.menu_list = [
                Menu.objects.create(
                    restaurant=restaurant,
                    uploaded_by=self.user.username,
                    votes=data.get('votes')) for restaurant,
                data in zip(
                    self.restaurant_list,
                    self.data)]

        with mock.patch('django.utils.timezone.now') as mock_now:
            mock_now.return_value = yy
            self.data = [
                {
                    "votes": 12,
                    "name": 'Burger King'
                },
                {
                    "votes": 3,
                    "name": 'Caribean Food Dishes'
                },
                {
                    "votes": 9,
                    "name": 'Janet Dishes'
                }

            ]

            self.menu_list = [
                Menu.objects.create(
                    restaurant=restaurant,
                    uploaded_by=self.user.username,
                    votes=data.get('votes')) for restaurant,
                data in zip(
                    self.restaurant_list,
                    self.data)]

        with mock.patch('django.utils.timezone.now') as mock_now:
            mock_now.return_value = yyy
            self.data = [
                {
                    "votes": 10,
                    "name": 'Burger King'
                },
                {
                    "votes": 7,
                    "name": 'Caribean Food Dishes'
                },
                {
                    "votes": 6,
                    "name": 'Janet Dishes'
                }

            ]

            self.menu_list = [
                Menu.objects.create(
                    restaurant=restaurant,
                    uploaded_by=self.user.username,
                    votes=data.get('votes')) for restaurant,
                data in zip(
                    self.restaurant_list,
                    self.data)]

        # current day items

        self.data = [
            {
                "votes": 10,
                "name": 'Burger King'
            },
            {
                "votes": 7,
                "name": 'Caribean Food Dishes'
            },
            {
                "votes": 6,
                "name": 'Janet Dishes'
            }

        ]

        self.menu_list = [
            Menu.objects.create(
                restaurant=restaurant,
                uploaded_by=self.user.username,
                votes=data.get('votes')) for restaurant,
            data in zip(
                self.restaurant_list,
                self.data)]

    def test_get_request_results_if_restaurant_found_won_3_consecutive_days(self):

        res = self.client.get(reverse("api:results"))

        expected_response_data = {
            'msg': 'success',
            'data': [
                {'rank': 2, 'votes': 6, 'restaurant': 'Janet Dishes'},
                {'rank': 1, 'votes': 7, 'restaurant': 'Caribean Food Dishes'}
            ],
            'success': True}

        self.assertEqual(res.json(), expected_response_data)
