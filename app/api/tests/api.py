from rest_framework.test import APITestCase
from django.urls import reverse
from api.models import *
from api.custom_jwt import *
from rest_framework import status
from django.core.files.uploadedfile import SimpleUploadedFile


from django.utils.http import urlencode


def reverse_querystring(view, urlconf=None, args=None, kwargs=None, current_app=None, query_kwargs=None):
    '''Custom reverse to handle query strings.
    Usage:
        reverse('app.views.my_view', kwargs={'pk': 123}, query_kwargs={'search': 'Bob'})
    '''
    base_url = reverse(view, urlconf=urlconf, args=args, kwargs=kwargs, current_app=current_app)
    if query_kwargs:
        return '{}?{}'.format(base_url, urlencode(query_kwargs))
    return base_url


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
