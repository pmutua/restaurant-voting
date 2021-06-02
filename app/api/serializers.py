from rest_framework import serializers
from api.models import *

from django.contrib.auth.models import(
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
