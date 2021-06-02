from api.models import *
from api.serializers import *

from rest_framework.views import APIView

from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny

from rest_framework.parsers import (
    MultiPartParser,
    FormParser
)


from django.db.models import Q

from django.conf import settings

from .tasks import *

from django.template import loader
from django.utils.html import strip_tags
from django.contrib.auth.hashers import check_password

from .custom_jwt import (
    jwt_payload_handler,
    jwt_encode_handler,
    jwt_decode_handler
)


class RegisterUserAPIView(APIView):
    def post(self, request, format=None):
        req = request.data
        user_group, _ = Group.objects.get_or_create(name=req.get('role'))
        role_group, _ = Role.objects.get_or_create(name=req.get('role'))

        serializer = UserSerializer(data=req)

        if serializer.is_valid():
            try:
                new_user = User.objects.create(
                    username=req.get('email'),
                    email=req.get('email'),
                    first_name=req.get('first_name').capitalize(),
                    last_name=req.get('last_name').capitalize(),
                    is_active=True,
                    phone=req.get('phone'),
                    identification_no=req.get('identification_no'),
                    is_staff=True

                )

                new_user.roles.add(role_group)
                new_user.groups.add(user_group)

                password = User.objects.make_random_password(length=10)
                new_user.set_password(password)
                new_user.save()

                login_site = settings.LOGIN_REDIRECT_URL

                ctx = {
                    "username": new_user.username,
                    "password": password,
                    "link": login_site,
                    'user_email': new_user.email
                }

                client_html_message = loader.render_to_string('api/email-user-creds.html')

                client_message_string = strip_tags(client_html_message)

                client_html_content = loader.render_to_string('api/email-user-creds.html', ctx)

                client_message = {
                    "html": client_html_content,
                    "text": client_message_string
                }

                serializer = UserSerializer(new_user)

                send_mail_to_admin = send_credentials(
                    'Welcome onboard',
                    client_message,
                    new_user.email
                )

                ser = UserDetailSerializer(new_user)

                res = {
                    "msg": "You have successfully registered. Check your email for login information",
                    "data": ser.data,
                    "success": True}
                return Response(data=res, status=status.HTTP_201_CREATED)
            except Exception as e:
                res = {"msg": str(e), "data": None, "success": False}
                return Response(data=res, status=status.HTTP_400_BAD_REQUEST)
        res = {"msg": str(serializer.errors), "data": None, "success": False}
        return Response(data=res, status=status.HTTP_400_BAD_REQUEST)


class UserLoginAPIView(APIView):
    queryset = User.objects.all()
    serializer_class = UserLoginSerializer

    def post(self, request, format=None):
        try:
            user = User.objects.get(email=request.data["email"])

            if check_password(request.data["password"], user.password):
                payload = jwt_payload_handler(user)

                token = jwt_encode_handler(payload)

                user.save()
                roles = [{"id": role.id, "name": role.name} for role in user.roles.all()]
                fullname = user.first_name + " " + user.last_name
                res = {
                    "msg": "Login success",
                    "success": True,
                    "data": {
                        "name": fullname,
                        "username": user.username,
                        "id": user.id,
                        "token": token,
                        "roles": roles}}
                return Response(data=res, status=status.HTTP_200_OK)

            else:
                res = {"msg": "Invalid login credentials", "data": None, "success": False}
                return Response(data=res, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            res = {"msg": str(e), "success": False, "data": None}
            return Response(data=res, status=status.HTTP_200_OK)
