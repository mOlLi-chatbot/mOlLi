from django.contrib import admin

from .models import *

admin.site.register(ChatUser)
admin.site.register(ChatHistory)
admin.site.register(UserTransaction)