from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from ..models import UserTransaction,ChatHistory

ChatUser = get_user_model()


class UserTransactionViewSetTestCase(APITestCase):
    def setUp(self):
        """
        Set up test data for the UserTransaction ViewSet.
        """
        # Create admin user
        self.admin_user = ChatUser.objects.create_superuser(
            username="admin", password="adminpass", email="admin@example.com"
        )
        
        # Create regular user
        self.regular_user = ChatUser.objects.create_user(
            username="user", password="userpass", email="user@example.com"
        )
        
        # Create transactions
        self.transaction1 = UserTransaction.objects.create(
            user=self.admin_user, amount=100.0, created_time="2024-12-16T12:00:00Z"
        )
        self.transaction2 = UserTransaction.objects.create(
            user=self.regular_user, amount=50.0, created_time="2024-12-16T13:00:00Z"
        )
        
        # URLs
        self.list_url = "/api/accounts/usertransactions/"
        self.detail_url = lambda pk: f"{self.list_url}{pk}/"
    
    def test_list_transactions_as_admin(self):
        """
        Test that admin users can list all transactions.
        """
        self.client.login(username="admin", password="adminpass")
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Admin sees all transactions

    def test_list_transactions_as_regular_user(self):
        """
        Test that regular users can only see their own transactions.
        """
        self.client.login(username="user", password="userpass")
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Regular user sees only their transactions
        self.assertEqual(response.data[0]['amount'], 50.0)

    def test_retrieve_transaction_as_admin(self):
        """
        Test that admin users can retrieve any transaction.
        """
        self.client.login(username="admin", password="adminpass")
        response = self.client.get(self.detail_url(self.transaction1.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['amount'], 100.0)

    def test_retrieve_transaction_as_regular_user(self):
        """
        Test that regular users can only retrieve their own transactions.
        """
        self.client.login(username="user", password="userpass")
        
        # User trying to retrieve their own transaction
        response = self.client.get(self.detail_url(self.transaction2.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['amount'], 50.0)

        # User trying to retrieve someone else's transaction
        response = self.client.get(self.detail_url(self.transaction1.id))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve_nonexistent_transaction(self):
        """
        Test retrieving a transaction that does not exist.
        """
        self.client.login(username="admin", password="adminpass")
        response = self.client.get(self.detail_url(999))  # Non-existent ID
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_transaction_as_admin(self):
        """
        Test that an admin user can create a transaction.
        """
        self.client.login(username="admin", password="adminpass")
        data = {"user": self.admin_user.id, "amount": 200.0, "created_time": "2024-12-16T14:00:00Z"}
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['transaction']['amount'], 200.0)

    def test_create_transaction_as_regular_user(self):
        """
        Test that a regular user can create a transaction.
        """
        self.client.login(username="user", password="userpass")
        data = {"user": self.regular_user.id, "amount": 75.0, "created_time": "2024-12-16T15:00:00Z"}
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['transaction']['amount'], 75.0)

    def test_create_transaction_with_invalid_data(self):
        """
        Test creating a transaction with invalid data.
        """
        self.client.login(username="admin", password="adminpass7")
        data = {"user": self.admin_user.id, "amount": -100.0, "created_time": "2024-12-16T14:00:00Z"}  # Invalid amount
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class ChatHistoryViewSetTestCase(APITestCase):
    def setUp(self):
        """
        Set up test data for the ChatHistory ViewSet.
        """
        # Create a user
        self.user = ChatUser.objects.create_user(username="testuser", password="testpass")

        # Create a second user
        self.other_user = ChatUser.objects.create_user(username="otheruser", password="otherpass")

        # Create chat histories for both users
        self.chat1 = ChatHistory.objects.create(user=self.user, text_msg="First message")
        self.chat2 = ChatHistory.objects.create(user=self.other_user, text_msg="Second message")

        # URLs
        self.list_url = "/api/accounts/chathistory/"
        self.detail_url = lambda pk: f"{self.list_url}{pk}/"

        # Login the user
        self.client.login(username="testuser", password="testpass")

    def test_list_chat_history(self):
        """
        Test that the chat history is listed correctly.
        """
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Should only see their own chat history
        self.assertEqual(response.data[0]["text_msg"], "First message")

    def test_retrieve_chat_history(self):
        """
        Test that a user can retrieve their own chat history.
        """
        response = self.client.get(self.detail_url(self.chat1.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["text_msg"], "First message")

    def test_retrieve_other_user_chat_history(self):
        """
        Test that a user cannot retrieve another user's chat history.
        """
        response = self.client.get(self.detail_url(self.chat2.id))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)  # Assuming no cross-user access

    def test_create_chat_history(self):
        """
        Test that a user can create a new chat message.
        """
        data = {"user": self.user.id, "text_msg": "New message"}
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["text_msg"], "New message")

    def test_soft_delete_chat_history(self):
        """
        Test that a user can soft-delete their own chat message.
        """
        response = self.client.delete(self.detail_url(self.chat1.id))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        
        # Verify that the chat is soft-deleted
        self.chat1.refresh_from_db()
        self.assertTrue(self.chat1.is_deleted)

    def test_soft_delete_other_user_chat_history(self):
        """
        Test that a user cannot soft-delete another user's chat message.
        """
        response = self.client.delete(self.detail_url(self.chat2.id))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)  # Assuming no cross-user delete


class ChatUserViewSetTestCase(APITestCase):
    def setUp(self):
        """
        Set up test data for ChatUserViewSet.
        """
        # Create an admin user
        self.admin_user = ChatUser.objects.create_superuser(
            username="admin", password="adminpass", email="admin@example.com"
        )

        # Create a regular user
        self.regular_user = ChatUser.objects.create_user(
            username="user", password="userpass", email="user@example.com"
        )

        # Define URLs
        self.list_url = "/api/accounts/accounts/"
        self.detail_url = lambda pk: f"{self.list_url}{pk}/"
        self.premium_status_url = lambda pk: f"{self.list_url}{pk}/update_premium_status/"

    def test_list_users_as_admin(self):
        """
        Test that an admin can list all users.
        """
        self.client.login(username="admin", password="adminpass")
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Admin sees all users

    def test_list_users_as_regular_user(self):
        """
        Test that a regular user cannot access the list of users.
        """
        self.client.login(username="user", password="userpass1")
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve_user_as_admin(self):
        """
        Test that an admin can retrieve any user.
        """
        self.client.login(username="admin", password="adminpass")
        response = self.client.get(self.detail_url(self.regular_user.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["username"], "user")

    def test_retrieve_user_as_regular_user(self):
        """
        Test that a regular user can retrieve their own details.
        """
        self.client.login(username="user", password="userpass")
        response = self.client.get(self.detail_url(self.regular_user.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["username"], "user")

    def test_retrieve_other_user_as_regular_user(self):
        """
        Test that a regular user cannot retrieve another user's details.
        """
        self.client.login(username="user", password="userpass2")
        response = self.client.get(self.detail_url(self.admin_user.id))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_user_as_admin(self):
        """
        Test that an admin can create a new user.
        """
        self.client.login(username="admin", password="adminpass")
        data = {"username": "newuser", "password": "newpass", "email": "newuser@example.com"}
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["username"], "newuser")

 
    def test_update_premium_status_as_regular_user(self):
        """
        Test that a regular user cannot update the premium status of any user.
        """
        self.client.login(username="user", password="userpass")
        data = {"is_premium": True}
        response = self.client.patch(self.premium_status_url(self.regular_user.id), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    
    def test_soft_delete_user_as_regular_user(self):
        """
        Test that a regular user cannot delete a user.
        """
        self.client.login(username="user", password="userpass")
        response = self.client.delete(self.detail_url(self.regular_user.id))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
