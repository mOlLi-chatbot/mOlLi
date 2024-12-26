from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from .models import *
from .serializers import *
from bot.openai_api import *
from users.serializers import *
from django.utils.dateparse import parse_datetime
from django.utils import timezone
import random


# Create your views here.

class AIChatViewSet(viewsets.ViewSet):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        load_dotenv()
        self.base_url = "https://api.avalai.ir/v1"
        self.model = "gpt-4o-mini"
        self.api_key = get_api_key()
        self.session_id = "q2Rt6h4G8gh$Her3w"  # Replace with a dynamic session ID
        self.llm = initialize_chat_openai(self.model, self.base_url, self.api_key)
        self.parser = StrOutputParser()


    @action(detail=False, methods=['get'], url_path='get_ai_response', permission_classes=[IsAuthenticated])
    def get_ai_response(self, request):

        user = request.user
        user_message = request.data.get('user_message')
        session_id = request.data.get('session_id')

        response = get_ai_response_with_history(session_id, user_message, self.llm, self.parser)
        idx = response.find("AI:")
        if idx >= 0:
            response = response[idx + 3:].strip()

        try:
            session = Session.objects.get(id=session_id)
        except:
            get_name_prompt = f'Make a title for this text, just write the title without any additional content: {user_message}'
            session_name = get_ai_response_with_history(None, get_name_prompt, self.llm, self.parser)
            session_name = session_name.strip('"')
            session = Session.objects.create(name=session_name)

        chathistory = ChatHistory.objects.create(user=user, \
                                                    user_message=user_message, \
                                                    session=session, \
                                                    ai_response=response) 
        
        serialized_user = ChatUserSerializer(user).data
        serialized_chat = ChatHistorySerializer(chathistory).data
        return Response({"user": serialized_user, "chat": serialized_chat})
    
    
    @action(detail=False, methods=['get'], url_path='get_user_chats', permission_classes=[IsAuthenticated])
    def get_user_chats(self, request):
 
        user = request.user

        date = request.query_params.get('date')
        offset = int(request.query_params.get('offset', 0))
        length = int(request.query_params.get('length', 10))

        if date is None:
            date = str(timezone.now())
        date = parse_datetime(date)
        
        chats = ChatHistory.objects.filter(user=user, timestamp__lt=date)[offset:offset + length]

        chats_serialized = ChatHistorySerializer(chats, many=True).data
        serialized_user = ChatUserSerializer(user).data

        return Response({"user": serialized_user, "chats": chats_serialized})
    
        
    @action(detail=False, methods=['delete'], url_path='delete_chat_by_id', permission_classes=[IsAdminUser])
    def delete_chat_by_id(self, request):

        chat_id = request.data.get('chat_id')
        
        try:
            chat = ChatHistory.objects.get(id=chat_id)
        except:
            return Response({"message": f"chat with id: {chat_id} does not exist"}, status=status.HTTP_400_BAD_REQUEST)
        
        chat.delete()
        
        return Response({"message": f"chat with id: {chat_id} deleted successfully"})


    @action(detail=False, methods=['delete'], url_path='delete_user_chats', permission_classes=[IsAdminUser])
    def delete_user_chats(self, request):

        username = request.data.get('username')

        try:
            user = ChatUser.objects.get(username=username)
        except:
            return Response({"message": f"user with username: {username} does not exist"})
        
        chats = ChatHistory.objects.filter(user=user)
        chats.delete()

        return Response({"message": f"user: {username} chats deleted successfully"})

    @action(detail=False, methods=['get'], url_path='get_user_sessions', permission_classes=[IsAuthenticated])
    def get_user_sessions(self, request):
        
        user = request.user
        user_serialized = ChatUserSerializer(user).data

        offset = int(request.query_params.get('offset', 0))
        length = int(request.query_params.get('length', 10))
        
        chats = ChatHistory.objects.filter(user=user)

        sessions = list(set([chat.session for chat in chats]))
        sessions = sessions[offset:offset + length]
        sessions_serialized = SessionSerializer(sessions, many=True).data

        return Response({"user": user_serialized, "sessions": sessions_serialized})


    @action(detail=False, methods=['get'], url_path='get_session_chats', permission_classes=[IsAuthenticated])
    def get_session_chats(self, request):

        user = request.user
        offset = int(request.query_params.get('offset', 0))
        length = int(request.query_params.get('length', 10))
        session_id = request.data.get('session_id')
        if session_id is None:
            return Response({"message": "the field \'session_id\' is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            session = Session.objects.get(id=session_id)
        except:
            return Response({"message": f"session with given id: {session_id} does not exist"}, status=status.HTTP_400_BAD_REQUEST)

        session_chats = ChatHistory.objects.filter(user=user, session=session)
        session_chats = session_chats[offset: offset + length]
        chats_serialized = ChatHistorySerializer(session_chats, many=True).data
        user_serialized = ChatUserSerializer(user).data

        return Response({"user": user_serialized, "chats": chats_serialized})

    @action(detail=False, methods=['get'], url_path='get_recommendation', permission_classes=[AllowAny])
    def get_recommendation(self, request):

        category = request.data.get('category')
        count = request.data.get('count')

        questions = Question.objects.all()
        if category is not None:
            questions = Question.objects.filter(category=category)
        
        if count is not None:
            try:
                count = int(count)
            except:
                return Response({"message": "the \'count\' field should be a integer"}, status=status.HTTP_400_BAD_REQUEST)
            questions = questions.order_by('?')[:count]
        
        questions_serialized = QuestionSerializer(questions, many=True).data
        
        return Response({"questions": questions_serialized})