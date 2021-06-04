from rest_framework import serializers
from api.models import *

from django.contrib.auth.models import (
    Group
)


class RoleSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Role
        fields = ['id', 'name']


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['name']


class UserSerializer(serializers.ModelSerializer):

    id = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = [
            'id',
            'first_name',
            'last_name',
            'email',
            'phone',
            "identification_no"
        ]


class UserDetailSerializer(serializers.ModelSerializer):

    id = serializers.CharField(read_only=True)
    roles = RoleSerializer(many=True)
    groups = GroupSerializer(many=True)

    class Meta:
        model = User
        fields = [
            'id',
            'first_name',
            'last_name',
            'email',
            'phone',
            "identification_no",
            "roles",
            "groups"

        ]


class UserLoginSerializer(serializers.Serializer):
    token = serializers.CharField(allow_blank=True, read_only=True)
    password = serializers.CharField()
    username = serializers.CharField()

    class Meta:
        fields = [
            'username',
            'password',
        ]
        extra_kwargs = {"password":
                        {"write_only": True}
                        }
        read_only_fields = ('id',)


class CreateRestaurantSerializer(serializers.ModelSerializer):

    class Meta:
        fields = [
            'name',
            'contact_no',
            'address',
            # 'created_by'

        ]
        model = Restaurant


class UploadMenuSerializer(serializers.ModelSerializer):

    def create(self, validated_data):

        menu = Menu(
            file=validated_data['file'],
            restaurant=validated_data['restaurant'],
            uploaded_by=validated_data['uploaded_by']
        )
        menu.save()
        return menu

    class Meta:
        fields = [
            'restaurant',
            'file',
            'uploaded_by'

        ]
        model = Menu


class EmployeeSerializer(serializers.ModelSerializer):

    id = serializers.CharField(read_only=True)
    employee_no = serializers.CharField()

    class Meta:
        model = User
        fields = [
            'id',
            'employee_no',
            'first_name',
            'last_name',
            'email',
            'phone',
            "identification_no",
            "employee_no"

        ]


class RestaurantListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = '__all__'


class MenuListSerializer(serializers.ModelSerializer):

    restaurant = serializers.CharField(read_only=True)

    class Meta:
        model = Menu
        fields = '__all__'


class ResultMenuListSerializer(serializers.ModelSerializer):

    restaurant = serializers.CharField(read_only=True)

    class Meta:
        model = Menu
        fields = [
            'id',
            'file',
            'restaurant',
            'votes',
            'created_at'
        ]
