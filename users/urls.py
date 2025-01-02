from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from .views import ChatUserViewSet,AuthViewSet,ChatHistoryViewSet,UserTransactionViewSet

router = DefaultRouter()
router.register(r'accounts', ChatUserViewSet, basename='chatuser')
router.register(r'auth', AuthViewSet, basename='auth')
router.register(r'chathistory', ChatHistoryViewSet, basename='chathistory')
router.register(r'usertransactions', UserTransactionViewSet, basename='usertransaction')

urlpatterns = [
    path('', include(router.urls)),

    # path('signup/', views.signup, name='signup'),
    # path('login/', views.login, name='login'),
]
