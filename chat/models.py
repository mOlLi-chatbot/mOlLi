from django.db import models
from users.models import *

# Create your models here.

class ChatHistory(models.Model):
    user = models.ForeignKey(ChatUser, on_delete=models.CASCADE)
    session_id = models.CharField(max_length=256)
    user_message = models.TextField()
    ai_response = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'-{self.user.username}: {self.user_message}\n-response: {self.ai_response}'