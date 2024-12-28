from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from django.contrib.auth import authenticate
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import ChatUser
from .serializers import *
from .utils import *
import bot.settings as settings
from urllib.parse import unquote
from .authenticators import validate_init_data
import json


class AuthViewSet(viewsets.ViewSet):
    """
    A ViewSet for user authentication (signup and login).
    """
    @swagger_auto_schema(
        request_body=SignupSerializer,
        operation_summary="Sign up a new user",
        responses={
            201: "User created successfully",
            400: "Validation error"
        }
    )
    @action(detail=False, methods=['post'], url_path='signup')
    def signup(self, request):
        """
        Handle user signup.
        """
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        request_body=LoginSerializer,
        operation_summary="User login",
        responses={
            200: "Login successful",
            400: "Validation error"
        }
    )
    @action(detail=False, methods=['post'], url_path='login')
    def login(self, request):
        """
        Handle user login.
        """
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            access_token = generate_access_token(user)
            refresh_token = generate_refresh_token(user)
            return Response({"access_token": access_token, "refresh_token": refresh_token}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['post'], url_path='refresh_token')
    def refresh_token(self, request):

        refresh_token = request.data.get('refresh_token')
        if refresh_token is None:
            return Response({"message": "refresh token not found!"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            payload = jwt.decode(refresh_token, settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return Response({"message": "refresh token expired!"}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.DecodeError:
            return Response({"message": "invalid token!"}, status=status.HTTP_400_BAD_REQUEST)
        user = ChatUser.objects.filter(id=payload['user_id']).first()
        if user is None:
            return Response({"message": "user not found!"}, status=status.HTTP_400_BAD_REQUEST)
        access_token = generate_access_token(user)
        
        return Response({"access_token" : access_token, "refresh_token": refresh_token})
    
    @action(detail=False, methods=['get'], url_path='get_user')
    def get_user(self, request):
        user = request.user
        serialized_user = ChatUserSerializer(user)
        return Response({"user": serialized_user.data})
    
    @action(detail=False, methods=['get'], url_path='get_full_user')
    def get_full_user(self, request):
        user = request.user
        serialized_user = ChatUserFullSerializer(user)
        return Response({"user": serialized_user.data})
    
    @action(detail=False, methods=['post'], url_path='mini_app_signup')
    def mini_app_signup(self, request):
        
        app_token = request.data.get('app_token')
        if app_token is None:
            return Response({"message": "the 'app_token' field is required"}, status=status.HTTP_400_BAD_REQUEST)

        if not validate_init_data(app_token, settings.TELEGRAM_BOT_SECRET_TOKEN):
            return Response({"message": "app token validation failed"}, status=status.HTTP_400_BAD_REQUEST)

        app_token = unquote(app_token)
        user_info = app_token.split('&')[0]
        user_info = user_info.split('=')[1]
        json_user = json.loads(user_info)
        username = json_user['username']
        first_name = json_user['first_name']
        last_name = json_user['last_name']

        if ChatUser.objects.filter(username=username).exists():
            return Response({"message": f"user with username: {username} already exists"}, status=status.HTTP_400_BAD_REQUEST)

        created_user = ChatUser.objects.create(username=username, first_name=first_name, last_name=last_name,
                                                app_token=app_token)
        password = ChatUser.objects.make_random_password(length=16)
        created_user.set_password(password)
        
        created_user_serialized = ChatUserSerializer(created_user).data
        return Response({"user": created_user_serialized})
        
        
    @action(detail=False, methods=['post'], url_path='mini_app_update_user', permission_classes=[IsAuthenticated])
    def mini_app_update_user(self, request):

        app_token = request.data.get('app_token')
        if app_token is None:
            return Response({"message": "the 'app_token' field is required"}, status=status.HTTP_400_BAD_REQUEST)

        if not validate_init_data(app_token, settings.TELEGRAM_BOT_SECRET_TOKEN):
            return Response({"message": "app token validation failed"}, status=status.HTTP_400_BAD_REQUEST)
        
        app_token = unquote(app_token)
        user_info = app_token.split('&')[0]
        user_info = user_info.split('=')[1]
        json_user = json.loads(user_info)
        username = json_user['username']
        first_name = json_user['first_name']
        last_name = json_user['last_name']

        if not ChatUser.objects.filter(username=username).exists():
            return Response({"message": f"user with username: {username} does not exists"}, status=status.HTTP_400_BAD_REQUEST)

        user = ChatUser.objects.get(username=username)
        user.first_name = first_name
        user.last_name = last_name
        user.app_token = app_token

        user_serialized = ChatUserSerializer(user).data
        return Response({"user": user_serialized})
    
    @action(detail=False, methods=['post'], url_path='mini_app_login')
    def mini_app_login(self, request):

        app_token = request.data.get('app_token')
        if app_token is None:
            return Response({"message": "the 'app_token' field is required"}, status=status.HTTP_400_BAD_REQUEST)

        if not validate_init_data(app_token, settings.TELEGRAM_BOT_SECRET_TOKEN):
            return Response({"message": "app token validation failed"}, status=status.HTTP_400_BAD_REQUEST)
        
        app_token = unquote(app_token)
        user_info = app_token.split('&')[0]
        user_info = user_info.split('=')[1]
        json_user = json.loads(user_info)
        username = json_user['username']

        if not ChatUser.objects.filter(username=username).exists():
            return Response({"message": f"user with given username: {username} does not exists"}, status=status.HTTP_400_BAD_REQUEST)

        user = ChatUser.objects.get(username=username)
        access_token = generate_access_token(user)
        refreh_token = generate_refresh_token(user)

        return Response({"access_token": access_token, "refreh_token": refreh_token})


class ChatUserViewSet(viewsets.ModelViewSet):
    queryset = ChatUser.objects.all()
    serializer_class = ChatUserSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        # Example: Only admins can delete users
        if self.action == 'destroy':
            return [IsAdminUser()]
        return super().get_permissions()

    def perform_destroy(self, instance):
        # Example: Soft delete by setting `is_deleted` instead of removing the record
        instance.is_deleted = True
        instance.save()

    @swagger_auto_schema(
        operation_summary="List all users",
        operation_description="Fetch a list of all users.",
        responses={200: ChatUserSerializer(many=True)}
    )
    def list(self, request):
        """
        Handle GET request to list all users.
        """
        users = ChatUser.objects.all()
        serializer = ChatUserSerializer(users, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_summary="Retrieve a user",
        operation_description="Fetch details of a user by ID.",
        responses={200: ChatUserSerializer()}
    )
    def retrieve(self, request, pk=None):
        """
        Handle GET request to retrieve a specific user by ID.
        """
        try:
            user = ChatUser.objects.get(pk=pk)
            serializer = ChatUserSerializer(user)
            return Response(serializer.data)
        except ChatUser.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(
        operation_summary="Create a user",
        operation_description="Create a new user with `username`, `email`, and `password`.",
        request_body=ChatUserSerializer,
        responses={201: ChatUserSerializer()}
    )
    def create(self, request):
        """
        Handle POST request to create a new user.
        """
        serializer = ChatUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        method='patch',
        operation_summary="Update user premium status",
        operation_description="Update the `is_premium` status of a user.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'is_premium': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='Set premium status')
            }
        ),
        responses={200: ChatUserSerializer()}
    )
    @action(detail=True, methods=['patch'])
    def update_premium_status(self, request, pk=None):
        """
        Handle PATCH request to update user premium status.
        """
        try:
            user = ChatUser.objects.get(pk=pk)
            user.is_premium = request.data.get('is_premium', user.is_premium)
            user.save()
            serializer = ChatUserSerializer(user)
            return Response(serializer.data)
        except ChatUser.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
