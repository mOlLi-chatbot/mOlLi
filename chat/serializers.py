from rest_framework import serializers
from .models import *

class ChatHistorySerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = ChatHistory
        fields = ['id', 'user', 'session_id', 'user_message', 'ai_response', 'timestamp']

class SessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Session
        fields = ['id', 'name']

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['category', 'text']
