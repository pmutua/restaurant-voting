from rest_framework.test import APITestCase
from django.urls import reverse
from api.models import *



# class TestRegisterUserAPI(APITestCase):
#     def test_post_request_can_register_new_user(self):

#         data = {
#             "email": "punakepis@dropjar.com ",
#             "first_name": "George",
#             "last_name": "Lucas",
#             "phone": "+2404554444",
#             "identification_no": "5343434242",
#             "role": "employee"

#         }
#         res = self.client.post(reverse("api:register-user"), data=data)
#         status = res.json().get('success')
#         self.assertEqual(User.objects.count(), 1)
#         self.assertEqual(status, True)

class TestLoginClientAPI(APITestCase):
    def test_post_request_can_register_new_user(self):
        user = User.objects.create(
            first_name= 'John',
            last_name= 'Hendrix',
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


