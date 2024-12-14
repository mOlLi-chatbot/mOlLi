from django.db import models

from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser


class ChatUser(AbstractUser):
    limit_count = models.IntegerField(default=10)
    is_premium = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    created_time = models.DateTimeField(auto_now_add=True)
    deleted_time = models.DateTimeField(null=True, blank=True)

    groups = models.ManyToManyField(
        'auth.Group', related_name='chatuser_set',
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups' )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='chatuser_set',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions' )

    def __str__(self):
        return self.username

class UserTransaction(models.Model):
    user = models.ForeignKey(ChatUser, on_delete=models.CASCADE)
    amount = models.FloatField()
    created_time = models.DateTimeField()

    def __str__(self):
        return f"Transaction {self.id} by {self.user.username}"