from rest_framework import serializers
from django.contrib.auth.models import User
from users.models import ChatUser
from django.contrib.auth import authenticate
from .models import ChatHistory,UserTransaction

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        """
        Validate username and password.
        """
        username = data.get('username')
        password = data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if user is None:
                raise serializers.ValidationError("Invalid credentials. Please try again.")
            if user.is_deleted:
                raise serializers.ValidationError("This account has been deactivated.")
        else:
            raise serializers.ValidationError("Both username and password are required.")

        data['user'] = user
        return data
class SignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatUser
        fields = ['id', 'username', 'email', 'password', 'limit_count', 'is_premium']
        extra_kwargs = {
            'password': {'write_only': True},  # Password is write-only to enhance security
            'limit_count': {'read_only': True},  # Set by default, not needed during signup
            'is_premium': {'read_only': True},  # Premium status can't be set during signup
        }

    def create(self, validated_data):
        # Create a new ChatUser and hash the password
        user = ChatUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user


class ChatUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatUser
        fields = [
            'id', 'username', 'email', 'password', 'limit_count', 'is_premium', 
            'is_deleted', 'created_time', 'deleted_time'
        ]
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = ChatUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            limit_count=validated_data.get('limit_count', 10),
            is_premium=validated_data.get('is_premium', False),
            is_deleted=validated_data.get('is_deleted', False)
        )
        return user

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            if attr == 'password':
                instance.set_password(value)
            else:
                setattr(instance, attr, value)
        instance.save()
        return instance
    

class ChatHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatHistory
        fields = ['id', 'user', 'text_msg', 'is_deleted', 'deleted_time']
        read_only_fields = ['is_deleted', 'deleted_time']


class UserTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserTransaction
        fields = ['id', 'user', 'amount', 'created_time']