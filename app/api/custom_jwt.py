from datetime import datetime
from calendar import timegm
import jwt
from django.conf import settings


def jwt_payload_handler(user):
    """ Custom payload handler
    Token encrypts the dictionary returned by this function,
    and can be decoded by rest_framework_jwt.utils.jwt_decode_handler
    """
    # username field must be included in the payload handler
    return {
        'user_id': str(
            user.pk),
        'username': user.username,
        'email': user.email,
        'full_name': user.first_name + ' ' + user.last_name,
        'is_superuser': user.is_superuser,
        'exp': datetime.utcnow() + settings.JWT_AUTH.get(
            'JWT_EXPIRATION_DELTA'
        ),
        'orig_iat': timegm(
            datetime.utcnow().utctimetuple())}


def jwt_response_payload_handler(token, user=None, request=None):
    """ Custom response payload handler.
    This function controlls the custom payload after
    login ortoken refresh.This data is returned through the web API.
    """
    return {
        'token': token,
        'user': {
            'username': user.username,
            'email': user.email,
            'full_name': user.first_name + ' ' + user.last_name,
        }
    }


def jwt_encode_handler(payload):

    return jwt.encode(payload, 'secret', algorithm='HS256')


def jwt_decode_handler(token):
    return jwt.decode(token, 'secret', algorithms=['HS256'])
