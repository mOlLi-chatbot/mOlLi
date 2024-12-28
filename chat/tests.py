from django.test import TestCase, Client
from .models import *
from users.models import *
from users.serializers import *
from users.utils import *
from faker import Faker
import random
import uuid
from datetime import datetime, timezone

# Create your tests here.
class ChatTest(TestCase):
    def setUp(self):

        # test client
        self.client = Client()

        # set base url pathes
        self.auth_path = '/api/users/auth'
        self.chat_path = '/api/chat/aichat'

        # faker object
        self.faker = Faker()
        
        # set a password for all users
        self.test_password = '12345678'

        # populate database
        for _ in range(5):
            ChatUser.objects.create(username=self.faker.user_name(), password=self.test_password, email=self.faker.email(),
                                        first_name=self.faker.first_name(), last_name=self.faker.last_name())
            Session.objects.create(name=self.faker.text(max_nb_chars=10))
        for user in ChatUser.objects.all():
            for _ in range(5):
                random_session = random.choice(Session.objects.all())
                ChatHistory.objects.create(user=user, session=random_session, user_message=self.faker.text(max_nb_chars=10),
                                            ai_response=self.faker.text(max_nb_chars=10))
        self.client.post(self.chat_path + '/fill_recommendation_table/')

        # test user
        self.user = ChatUser.objects.all()[0]
        self.access_token = generate_access_token(self.user)

        # test admin user
        self.admin_user = ChatUser.objects.create(username=self.faker.user_name(), password=self.test_password, email=self.faker.email(),
                                                    first_name=self.faker.first_name(), last_name=self.faker.last_name(), is_staff=True)
        self.admin_token = generate_access_token(self.admin_user)
        
    

    def test_get_ai_response(self):

        # set needed variables
        url = self.chat_path + '/get_ai_response/'
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Beraer {self.access_token}'
        }

        # unauthorized request
        response = self.client.get(url, data={
            'user_message': 'Hello',
        })
        self.assertEqual(response.status_code, 403)

        # unsatisfied requirements of request
        response = self.client.get(url, headers=headers, query_params={
            'session_id': 'cef1b626-ad0d-439a-acd6-75c07ce77fd8'
        })
        self.assertEqual(response.status_code, 400)
        
        # invalid session_id
        response = self.client.get(url, headers=headers, query_params={
            'user_message': 'Hello',
            'session_id': 'u-u-u-u'
        })
        self.assertEqual(response.status_code, 400)

        # session does not exist
        session_id = uuid.uuid4()
        while session_id in list(map(lambda session: session.id, Session.objects.all())):
            session_id = uuid.uuid4()
        response = self.client.get(url, headers=headers, query_params={
            'user_message': 'Hello',
            'session_id': session_id
        })
        self.assertEqual(response.status_code, 400)

        # creating new session when session_id is None
        n_sessions_before = len(Session.objects.all())
        response = self.client.get(url, headers=headers, query_params={
            'user_message': 'Hello'
        })
        n_sessions_after = len(Session.objects.all())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(n_sessions_after, n_sessions_before + 1)

        # expected response fields
        session = random.choice(Session.objects.all())
        session_id = session.id
        response = self.client.get(url, headers=headers, query_params={
            'user_message': 'Hello',
            'session_id': session_id
        })
        res_json = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(res_json.get('user'))
        self.assertIsNotNone(res_json.get('chat'))
        self.assertIsNotNone(res_json['chat'].get('session_id'))
        self.assertIsNotNone(res_json['chat'].get('ai_response'))
        self.assertIsNotNone(res_json['chat'].get('timestamp'))
    

    def test_get_user_chats(self):
        
        # set needed variables
        url = self.chat_path + '/get_user_chats/'
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Beraer {self.access_token}'
        }

        # unauthorized request
        response = self.client.get(url, query_params={
            'date': '2024-12-28T13:41:29.817077Z'
        })
        self.assertEqual(response.status_code, 403)

        # offset and length params
        length = 3
        response = self.client.get(url, headers=headers, query_params={})
        offset_response = self.client.get(url, headers=headers, query_params={
            'offset': '1',
            'length': str(length)
        })
        res_json = response.json()
        offset_res_json = offset_response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(offset_res_json['chats']), min(len(res_json['chats']), length))

        # expected response fields
        response = self.client.get(url, headers=headers)
        res_json = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(res_json.get('user'))
        self.assertIsNotNone(res_json.get('chats'))

        # date query param
        chats = ChatHistory.objects.filter(user=self.user)
        chats = sorted(chats, key=lambda chat: chat.timestamp)
        date = chats[len(chats) // 2].timestamp
        date_str = datetime.strftime(date, '%Y-%m-%dT%H:%M:%S.%fZ')
        response = self.client.get(url, headers=headers, query_params={
            'date': date_str
        })
        self.assertEqual(response.status_code, 200)
        for chat in res_json['chats']:
            chat_timestamp = datetime.strptime(chat['timestamp'], '%Y-%m-%dT%H:%M:%S.%fZ')
            chat_timestamp = chat_timestamp.replace(tzinfo=timezone.utc, microsecond=0)
            date = date.replace(microsecond=0)
            self.assertLessEqual(chat_timestamp, date)
    

    def test_delete_chat_by_id(self):

        # set needed variables
        url = self.chat_path + '/delete_chat_by_id/'
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Beraer {self.access_token}'
        }
        admin_headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Beraer {self.admin_token}'
        }

        # unauthorized request
        response = self.client.delete(url, query_params={
            'chat_id': '0'
        })
        self.assertEqual(response.status_code, 403)

        
        # non admin user request
        response = self.client.delete(url, headers=headers, query_params={
            'chat_id': '0'
        })
        self.assertEqual(response.status_code, 403)

        # invalid chat id
        response = self.client.delete(url, headers=admin_headers, query_params={
            'chat_id': '-1'
        })
        self.assertEqual(response.status_code, 400)

        # delete chat by id
        random_chat = random.choice(ChatHistory.objects.all())
        random_chat_id = random_chat.id
        n_chats_before = len(ChatHistory.objects.all())
        response = self.client.delete(url, headers=admin_headers, query_params={
            'chat_id': random_chat_id
        })
        n_chats_after = len(ChatHistory.objects.all())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(n_chats_before, n_chats_after + 1)
        self.assertEqual(ChatHistory.objects.filter(id=random_chat_id).exists(), False)

        # recover deleted chat
        ChatHistory.objects.create(user=random_chat.user, session=random_chat.session, user_message=random_chat.user_message,
                                            ai_response=random_chat.ai_response, timestamp=random_chat.timestamp)
        

    def test_delete_user_chats(self):

        # set needed variables
        url = self.chat_path + '/delete_user_chats/'
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Beraer {self.access_token}'
        }
        admin_headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Beraer {self.admin_token}'
        }

        # unauthorized request
        response = self.client.delete(url, query_params={
            'username': self.user.username
        })
        self.assertEqual(response.status_code, 403)

        # non admin user request
        response = self.client.delete(url, headers=headers, query_params={
            'username': self.user.username
        })
        self.assertEqual(response.status_code, 403)

        # user does not exist
        non_username = ''.join([chr(random.randint(ord('a'), ord('z'))) for _ in range(10)])
        while non_username in [user.username for user in ChatUser.objects.all()]:
            non_username = ''.join([chr(random.randint(ord('a'), ord('z'))) for _ in range(10)])
        
        response = self.client.delete(url, headers=admin_headers, qeury_params={
            'username': non_username
        })
        self.assertEqual(response.status_code, 400)

        # delete user chats
        username = self.user.username
        user_chats = ChatHistory.objects.filter(user=self.user)
        response = self.client.delete(url, headers=admin_headers, query_params={
            'username': username
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(ChatHistory.objects.filter(user=self.user).exists(), False)

        # recover chats
        for chat in user_chats:
            ChatHistory.objects.create(user=chat.user, session=chat.session, user_message=chat.user_message,
                                            ai_response=chat.ai_response, timestamp=chat.timestamp)
    

    def test_get_user_sessions(self):

        # set needed variables
        url = self.chat_path + '/get_user_sessions/'
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Beraer {self.access_token}'
        }

        # unauthorized request
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

        # expected response fields
        response = self.client.get(url, headers=headers)
        res_json = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(res_json.get('user'))
        self.assertIsNotNone(res_json.get('sessions'))

        # offset and length params
        length = 1
        response = self.client.get(url, headers=headers, query_params={})
        offset_response = self.client.get(url, headers=headers, query_params={
            'offset': '0',
            'length': '1'
        })
        res_json = response.json()
        offset_res_json = offset_response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(offset_res_json['sessions']), min(len(res_json['sessions']), length))
    
    
    def test_get_session_chats(self):

        # set needed variables
        url = self.chat_path + '/get_session_chats/'
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Beraer {self.access_token}'
        }
        random_session = random.choice(Session.objects.all())
        random_session_id = random_session.id

        # unauthorized request
        response = self.client.get(url, query_params={
            'session_id': random_session_id
        })
        self.assertEqual(response.status_code, 403)

        # required fields of request
        response = self.client.get(url, headers=headers, query_params={})
        self.assertEqual(response.status_code, 400)

        # session does not exist
        non_session_id = uuid.uuid4()
        while non_session_id in list(map(lambda session: session.id, Session.objects.all())):
            non_session_id = uuid.uuid4()
        response = self.client.get(url, headers=headers, query_params={
            'session_id': non_session_id
        })
        self.assertEqual(response.status_code, 400)
        
        # expected response fields
        response = self.client.get(url, headers=headers, query_params={
            'session_id': random_session_id
        })
        res_json = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(res_json.get('user'))
        self.assertIsNotNone(res_json.get('chats'))
        self.assertIsNotNone(res_json.get('session'))
        
        # offset and length params
        length = 3
        response = self.client.get(url, headers=headers, query_params={
            'session_id': random_session_id,
        })
        offset_response = self.client.get(url, headers=headers, query_params={
            'session_id': random_session_id,
            'offset': '0',
            'length': str(length)
        })
        res_json = response.json()
        offset_res_json = offset_response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(offset_res_json['chats']), min(len(res_json['chats']), length))
    

    def test_get_recommendation(self):

        # set needed variables
        url = self.chat_path + '/get_recommendation/'
        
        # expected response fields
        response = self.client.get(url)
        res_json = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(res_json.get('questions'))
        
        # count
        count = 4
        response = self.client.get(url, query_params={
            'count': str(count)
        })
        res_json = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(res_json['questions']), min(len(Question.objects.all()), count))
