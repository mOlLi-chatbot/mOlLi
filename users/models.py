from django.db import models

from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now


class ChatUser(AbstractUser):
    limit_count = models.IntegerField(default=10)
    is_premium = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    created_time = models.DateTimeField(auto_now_add=True)
    deleted_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.username

class ChatHistoryManager(models.Manager):
    def get_queryset(self):
        # Exclude soft-deleted items by default
        return super().get_queryset().filter(is_deleted=False)


class ChatHistory(models.Model):
    user = models.ForeignKey(ChatUser, on_delete=models.CASCADE)
    text_msg = models.TextField()
    is_deleted = models.BooleanField(default=False)  # Soft delete flag
    deleted_time = models.DateTimeField(null=True, blank=True)  # Track deletion time

    objects = ChatHistoryManager()  # Default manager excluding soft-deleted items
    all_objects = models.Manager()  # Manager to include all items

    def delete(self, *args, **kwargs):
        """Soft delete the object."""
        self.is_deleted = True
        self.deleted_time = now()
        self.save()

    def restore(self):
        """Restore a soft-deleted object."""
        self.is_deleted = False
        self.deleted_time = None
        self.save()

    def __str__(self):
        return f"Chat by {self.user.username}"

class UserTransaction(models.Model):
    user = models.ForeignKey(ChatUser, on_delete=models.CASCADE)
    amount = models.FloatField()
    created_time = models.DateTimeField()

    def __str__(self):
        return f"Transaction {self.id} by {self.user.username}"