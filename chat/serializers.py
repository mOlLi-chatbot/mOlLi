from rest_framework import serializers
from .models import ChatHistory

class ChatHistorySerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = ChatHistory
        fields = ['id', 'user', 'session_id', 'user_message', 'ai_response', 'timestamp']
