from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from .views import ChatUserViewSet,AuthViewSet

router = DefaultRouter()
router.register(r'accounts', ChatUserViewSet, basename='chatuser')
router.register(r'auth', AuthViewSet, basename='auth')

urlpatterns = [
    path('', include(router.urls))
]
