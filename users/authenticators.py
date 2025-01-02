from rest_framework.authentication import BaseAuthentication
from .models import ChatUser
from django.contrib.auth.models import AnonymousUser
from rest_framework import exceptions
import jwt
from django.conf import settings
from rest_framework.response import Response
import hashlib
import hmac
from urllib.parse import unquote


def validate_init_data(init_data: str, bot_token: str):
    try:
        vals = {k: unquote(v) for k, v in [s.split('=', 1)
            for s in init_data.split('&')]}
        data_check_string = '\n'.join(
            f"{k}={v}" for k, v in sorted(vals.items()) if k != 'hash')

        secret_key = hmac.new("WebAppData".encode(),
            bot_token.encode(), hashlib.sha256).digest()
        
        h = hmac.new(secret_key, data_check_string.encode(), hashlib.sha256)
        return h.hexdigest() == vals['hash']
    except:
        return False



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
