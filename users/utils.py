import jwt
import datetime
from django.conf import settings

ACCESS_TOKEN_EXPIRE_TIME = datetime.timedelta(days = 0, hours=5, minutes=0)
REFRESH_TOKEN_EXPIRE_TIME = datetime.timedelta(days = 2, hours=0, minutes=0)


def generate_access_token(user):
    access_token_payload = {
        'user_id' : user.id,
        'sub' : user.id,
        'exp' : datetime.datetime.utcnow() + ACCESS_TOKEN_EXPIRE_TIME,
        'iat' : datetime.datetime.utcnow(),
    }
    access_token = jwt.encode(access_token_payload, settings.SECRET_KEY, algorithm='HS256')
    return access_token


def generate_refresh_token(user):
    refresh_token_payload = {
        'user_id': user.id,
        'sub': user.id,
        'exp': datetime.datetime.utcnow() + REFRESH_TOKEN_EXPIRE_TIME,
        'iat': datetime.datetime.utcnow()
    }
    refresh_token = jwt.encode(refresh_token_payload, settings.SECRET_KEY, algorithm='HS256')
    return refresh_token