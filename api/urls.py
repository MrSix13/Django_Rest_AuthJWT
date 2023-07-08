from django.urls import path
from myapp.views import RegisterView, LoginView
from .views.authentication_views import reset_password_confirm, reset_password_request

urlpatterns = [
    path("register/",RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name='login'),
    path("reset-password/request/", reset_password_request, name='reset_password_request'),
    path("reset-password/confirm/", reset_password_confirm, name='reset_password_confirm'),
    
]