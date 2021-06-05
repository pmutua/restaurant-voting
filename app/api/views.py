from datetime import datetime
from datetime import date, timedelta

from django.conf import settings
from django.template import loader
from django.utils.html import strip_tags
from django.contrib.auth.hashers import check_password
from django.db.models import Q
from django.db.models import Sum, Max
from django.db import connection
from django.db.models import F, Window
from django.db.models.functions import Rank

from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
# from rest_framework.parsers import (
#     MultiPartParser,
#     FormParser
# )

from .tasks import *
from api.models import *
from api.serializers import *
from .custom_jwt import (
    jwt_payload_handler,
    jwt_encode_handler,
    jwt_decode_handler
)


todays_date = settings.CURRENT_DATE.date()


class RoleListAPIView(generics.ListAPIView):
    serializer_class = RoleSerializer
    queryset = Role.objects.all()


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

                client_html_message = loader.render_to_string(
                    'api/email-user-creds.html')

                client_message_string = strip_tags(client_html_message)

                client_html_content = loader.render_to_string(
                    'api/email-user-creds.html', ctx)

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
                text = 'Check your email for login information'
                res = {
                    "msg": f"Successfully registered.{text}",
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
                roles = [{"id": role.id, "name": role.name}
                         for role in user.roles.all()]
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
                res = {
                    "msg": "Invalid login credentials",
                    "data": None,
                    "success": False}
                return Response(data=res, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            res = {"msg": str(e), "success": False, "data": None}
            return Response(data=res, status=status.HTTP_200_OK)


class UserLogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        try:
            username = jwt_decode_handler(request.auth).get('username')
            user = User.objects.get(username=username)
            payload = jwt_payload_handler(user)
            jwt_encode_handler(payload)
            res = {
                "msg": "User logged out successfully",
                "success": True,
                "data": None}
            return Response(data=res, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class CreateRestaurantAPIView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, format=None):
        req = request.data
        user = {'created_by': jwt_decode_handler(request.auth).get('username')}
        req = dict(request.data)
        req.update(user)
        serializer = CreateRestaurantSerializer(data=req)
        if serializer.is_valid():
            serializer.save()
            res = {
                "msg": "Restaurant Created",
                "success": True,
                "data": serializer.data}
            return Response(data=res, status=status.HTTP_201_CREATED)

        res = {"msg": str(serializer.errors), "success": False, "data": None}
        return Response(data=res, status=status.HTTP_400_BAD_REQUEST)


class UploadMenuAPIView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):

        try:
            req = request.data.dict()
            todays_date = settings.CURRENT_DATE.date()
            menu = Menu.objects.filter(
                Q(restaurant__id=int(req.get('restaurant')))
                and Q(created_at__date=todays_date))
            user = jwt_decode_handler(request.auth).get('username')

            if menu.exists():
                res = {
                    "msg": "Menu already added.",
                    "success": False,
                    "data": None}
                return Response(data=res, status=status.HTTP_200_OK)

            serializer = UploadMenuSerializer(data=req)

            if serializer.is_valid():
                serializer.save(uploaded_by=user)
                res = {
                    "msg": "Menu uploaded",
                    "success": True,
                    "data": serializer.data}
                return Response(data=res, status=status.HTTP_201_CREATED)

            res = {
                "msg": str(
                    serializer.errors),
                "success": False,
                "data": None}
            return Response(data=res, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            res = {"msg": str(e), "success": False, "data": None}
            return Response(data=res, status=status.HTTP_400_BAD_REQUEST)


class CreateEmployeeAPIView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        req = request.data

        user = jwt_decode_handler(request.auth).get('username')
        employee_no = req.get('employee_no')
        employee = Employee.objects.filter(
            Q(employee_no=employee_no)
        )
        text = f"EMPLOYEE NO { employee_no } already exists"
        if employee.exists():
            res = {
                "msg": text,
                "data": None,
                "success": False}
            return Response(data=res, status=status.HTTP_400_BAD_REQUEST)

        role_group, _ = Role.objects.get_or_create(name=req.get('employee'))

        serializer = EmployeeSerializer(data=req)

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
                    is_staff=True,
                    created_by=user

                )

                new_user.roles.add(role_group)

                password = User.objects.make_random_password(length=10)
                new_user.set_password(password)
                new_user.save()

                Employee.objects.create(
                    user=new_user,
                    employee_no=req.get('employee_no'),
                    created_by=user
                )

                login_site = settings.LOGIN_REDIRECT_URL

                ctx = {
                    "username": new_user.username,
                    "password": password,
                    "link": login_site,
                    'user_email': new_user.email
                }

                client_html_message = loader.render_to_string(
                    'api/email-user-creds.html')

                client_message_string = strip_tags(client_html_message)

                client_html_content = loader.render_to_string(
                    'api/email-user-creds.html', ctx)

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
                text = "Login info sent to employee's email"
                res = {
                    "msg": f"Employee successfully created.{text}",
                    "data": serializer.data,
                    "success": True}
                return Response(data=res, status=status.HTTP_201_CREATED)
            except Exception as e:
                res = {"msg": str(e), "data": None, "success": False}
                return Response(data=res, status=status.HTTP_400_BAD_REQUEST)
        res = {"msg": str(serializer.errors), "data": None, "success": False}
        return Response(data=res, status=status.HTTP_400_BAD_REQUEST)


class RestaurantListAPIView(generics.ListAPIView):
    serializer_class = RestaurantListSerializer
    queryset = Restaurant.objects.all()


class CurrentDayMenuList(APIView):

    def get(self, request):
        todays_date = settings.CURRENT_DATE.date()

        qs = Menu.objects.filter(Q(created_at__date=todays_date))
        serializer = MenuListSerializer(qs, many=True)
        res = {"msg": 'success', "data": serializer.data, "success": True}
        return Response(data=res, status=status.HTTP_200_OK)


class VoteAPIView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, menu_id):
        username = jwt_decode_handler(request.auth).get('username')
        todays_date = settings.CURRENT_DATE.date()

        employee = Employee.objects.get(user__username=username)
        menu = Menu.objects.get(id=menu_id)

        if Vote.objects.filter(
                employee__user__username=username,
                voted_at__date=todays_date,
                menu__id=menu_id).exists():
            res = {"msg": 'You already voted!', "data": None, "success": False}
            return Response(data=res, status=status.HTTP_200_OK)
        else:
            new_vote = Vote.objects.create(
                employee=employee,
                menu=menu

            )
            menu.votes += 1
            menu.save()

            qs = Menu.objects.filter(Q(created_at__date=todays_date))
            serializer = ResultMenuListSerializer(qs, many=True)
            res = {
                "msg": 'You voted successfully!',
                "data": serializer.data,
                "success": True}
            return Response(data=res, status=status.HTTP_200_OK)


class ResultsAPIView(APIView):

    def get(self, request):

        today = date.today()

        start = today - timedelta(days=today.weekday())

        current_menu_qs = Menu.objects.filter(
            Q(created_at__date=todays_date)).order_by('-votes')

        if len(current_menu_qs) == 0:
            res = {
                "msg": 'Results not found! no menus found for today.',
                "data": None,
                "success": False}
            return Response(data=res, status=status.HTTP_200_OK)

        # Populate menu list from monday to today.
        consecutive_list = Menu.objects.filter(
            created_at__gte=start
        ).extra(select={
                'day': connection.ops.date_trunc_sql(
                    'day',
                    'created_at')}
                ).values('day', 'id').annotate(max_vote=Max('votes'))

        # populate consecutive Days
        date_strs = [str(date.get('day')) for date in consecutive_list]

        dates = [datetime.strptime(d, "%Y-%m-%d %H:%M:%S") for d in date_strs]

        date_ints = set([d.toordinal() for d in dates])

        if len(date_ints) == 1:
            # If all unique
            new_queryset = Menu.objects.filter(
                created_at__date=todays_date).annotate(
                rank=Window(
                    expression=Rank(),
                    order_by=F('votes').desc(),
                )
            )

            result = [{"rank": item.rank,
                       "restaurant": item.restaurant.name,
                       "votes": item.votes} for item in new_queryset]

            res = {"msg": 'success', "data": result, "success": True}
            return Response(data=res, status=status.HTTP_200_OK)

        elif max(date_ints) - min(date_ints) == 3:
            # If consecutive winner found 3 times
            list_ = [item for item in consecutive_list if str(item.get(
                'day'))[:10] == str(todays_date)]
            current_max = list_[0]
            current_max_pk = current_max.get('id')
            new_current_list = [
                item.id for item in current_menu_qs
                if item.id != current_max_pk]

            new_queryset = Menu.objects.filter(id__in=new_current_list
                                               ).annotate(
                rank=Window(
                    expression=Rank(),
                    order_by=F('votes').desc(),
                )
            )

            result = [
                {
                    "rank": item.rank,
                    "votes": item.votes,
                    "restaurant": item.restaurant.name
                }
                for item in new_queryset
            ]

            res = {"msg": 'success', "data": result, "success": True}
            return Response(data=res, status=status.HTTP_200_OK)

        else:
            new_queryset = Menu.objects.filter(
                created_at__date=todays_date
            ).annotate(
                rank=Window(
                    expression=Rank(),
                    order_by=F('votes').desc(),
                )
            )

            result = [{"rank": item.rank,
                       "votes": item.votes,
                       "restaurant": item.restaurant.name,
                       "file": item.file.url} for item in new_queryset]

            res = {"msg": 'success', "data": result, "success": True}
            return Response(data=res, status=status.HTTP_200_OK)
