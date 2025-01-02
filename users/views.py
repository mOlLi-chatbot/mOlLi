from django.contrib.auth import authenticate
from django.db import transaction


from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import ChatUser,ChatHistory,UserTransaction
from .serializers import ChatUserSerializer, LoginSerializer, SignupSerializer,ChatHistorySerializer,UserTransactionSerializer


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
            return Response({"message": "Login successful", "username": user.username}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChatUserViewSet(viewsets.ModelViewSet):
    queryset = ChatUser.objects.all()
    serializer_class = ChatUserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return ChatUser.objects.filter(pk=user.pk)
    
    def get_permissions(self):
        """
        Define custom permissions for actions.
        """
        if self.action == 'destroy':
            return [IsAdminUser()]  # Only admin users can delete
        return super().get_permissions()

    def perform_destroy(self, instance):
        """
        Soft delete by setting `is_deleted` instead of removing the record.
        """
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
        responses={200: ChatUserSerializer()})
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
        operation_description="Update the `is_premium` status of a user. Only admins are allowed.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'is_premium': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='Set premium status')
            }
        ),
        responses={200: ChatUserSerializer()})
    @action(detail=True, methods=['patch'], permission_classes=[IsAdminUser])
    def update_premium_status(self, request, pk=None):
        """
        Handle PATCH request to update user premium status.
        Only admin users are allowed to perform this action.
        """
        try:
            user = ChatUser.objects.get(pk=pk)
            user.is_premium = request.data.get('is_premium', user.is_premium)
            user.save()
            serializer = ChatUserSerializer(user)
            return Response(serializer.data)
        except ChatUser.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        
class ChatHistoryViewSet(viewsets.ModelViewSet):
    """
    ViewSet for ChatHistory with soft delete functionality and restricted access.
    - Admin users can retrieve all chat history.
    - Logged-in users can only retrieve their own chat history.
    - Not logged-in users cannot retrieve chat history.
    """
    serializer_class = ChatHistorySerializer
    permission_classes = [IsAuthenticated]  # Ensure only authenticated users can access the view.

    def get_queryset(self):
        """
        Restrict queryset based on user role:
        - Admin users see all chat history.
        - Non-admin users see only their own chat history.
        """
        if self.request.user.is_staff:  # Admin user
            return ChatHistory.objects.all()
        return ChatHistory.objects.filter(user=self.request.user)  # Logged-in user's chat history only

    def destroy(self, request, *args, **kwargs):
        """
        Override the default delete to perform a soft delete.
        """
        instance = self.get_object()
        instance.delete()
        return Response({"detail": "Chat message soft-deleted."}, status=status.HTTP_404_NOT_FOUND)

class UserTransactionViewSet(viewsets.ViewSet):
    """
    ViewSet for UserTransaction supporting create, retrieve, and list operations.
    """
    permission_classes = [IsAuthenticated]  # Ensure only authenticated users can access these views.

    def list(self, request):
        """
        List transactions:
        - Admins see all transactions.
        - Regular users see only their transactions.
        """
        user = request.user
        if user.is_staff:  # Check if the user is an admin
            transactions = UserTransaction.objects.all()
        else:  # Otherwise, limit to transactions belonging to the current user
            transactions = UserTransaction.objects.filter(user=user)

        serializer = UserTransactionSerializer(transactions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        """
        Retrieve a single UserTransaction by its primary key.
        """
        try:
            transaction = UserTransaction.objects.get(pk=pk)
            if not request.user.is_staff and transaction.user != request.user:
                return Response({"detail": "Not authorized to view this transaction."}, status=status.HTTP_403_FORBIDDEN)

            serializer = UserTransactionSerializer(transaction)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except UserTransaction.DoesNotExist:
            return Response({"detail": "Transaction not found."}, status=status.HTTP_404_NOT_FOUND)

    @transaction.atomic
    def create(self, request):
        """
        Create a new UserTransaction. This operation is atomic.
        """
        serializer = UserTransactionSerializer(data=request.data)
        if serializer.is_valid():
            transaction = serializer.save()
            return Response(
                {"detail": "Transaction created successfully.", "transaction": serializer.data},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)