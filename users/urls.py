from django.urls import path
from .views import UserView, UserViewSpecif
from rest_framework_simplejwt.views import TokenObtainPairView

urlpatterns = [
    path('users/', UserView.as_view()),
    path('users/login/', TokenObtainPairView.as_view()),
    path('users/<int:user_id>/', UserViewSpecif.as_view())
]
