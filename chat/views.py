from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import *
from .serializers import *
from bot.openai_api import *
from users.serializers import *
from django.utils.dateparse import parse_datetime
from django.utils import timezone


# Create your views here.

class AIChatViewSet(viewsets.ViewSet):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        load_dotenv()
        self.base_url = "https://api.avalai.ir/v1"
        self.model = "gpt-4o-mini"
        self.api_key = get_api_key()
        self.session_id = "q2Rt6h4G8gh$TH1er3E"  # Replace with a dynamic session ID
        self.llm = initialize_chat_openai(self.model, self.base_url, self.api_key)
        self.parser = StrOutputParser()


    @action(detail=False, methods=['get'], url_path='get_ai_response', permission_classes=[IsAuthenticated])
    def get_ai_response(self, request):

        user = request.user
        user_message = request.data.get('user_message')

        response = get_ai_response_with_history(self.session_id, user_message, self.llm, self.parser)
        idx = response.find("AI:")
        if idx >= 0:
            response = response[idx + 3:].strip()

        chathistory = ChatHistory.objects.create(user=user, \
                                                    user_message=user_message, \
                                                    session_id=self.session_id, \
                                                    ai_response=response) 
        
        serialized_user = ChatUserSerializer(user).data
        serialized_chat = ChatHistorySerializer(chathistory).data
        return Response({"user": serialized_user, "chat": serialized_chat})
    
    @action(detail=False, methods=['get'], url_path='get_user_chats', permission_classes=[IsAuthenticated])
    def get_user_chats(self, request):

        user = request.user
        date = request.data.get('date')
        if date is None:
            date = str(timezone.now())
        date = parse_datetime(date)
        
        chats = ChatHistory.objects.filter(user=user, timestamp__lt=date)

        chats_serialized = ChatHistorySerializer(chats, many=True).data
        serialized_user = ChatUserSerializer(user).data
        return Response({"user": serialized_user, "chats": chats_serialized})
        
        
