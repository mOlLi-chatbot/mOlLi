from django.db import models
from users.models import *
import uuid

# Create your models here.

class Question(models.Model):
    category = models.CharField(max_length=32)
    text = models.CharField(max_length=256)

class Session(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=256)

class ChatHistory(models.Model):
    user = models.ForeignKey(ChatUser, on_delete=models.CASCADE)
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    user_message = models.TextField()
    ai_response = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'-{self.user.username}: {self.user_message}\n-response: {self.ai_response}'