from rest_framework.authentication import BaseAuthentication
from .models import ChatUser
from django.contrib.auth.models import AnonymousUser
from rest_framework import exceptions
import jwt
from django.conf import settings
from rest_framework.response import Response


class JWTAuthenticator(BaseAuthentication):
    def authenticate(self, request):
        authorized_header = request.headers.get('Authorization')
        if authorized_header is None:
            return None
        try:
            access_token = authorized_header.split(' ')[1]
            payload = jwt.decode(access_token, settings.SECRET_KEY, algorithms=['HS256'])
            
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed("Access token expired")
        except IndexError:
            raise  exceptions.AuthenticationFailed('Token prefix missing')
        except jwt.DecodeError:
            raise exceptions.AuthenticationFailed("Invalid Token")
        user = ChatUser.objects.filter(id=payload['user_id']).first()
        if user is None:
            raise exceptions.AuthenticationFailed("user not found")
        return user, access_token
