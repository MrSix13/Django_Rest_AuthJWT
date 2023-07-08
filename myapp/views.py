from api.serializers import CustomTokenObtainPairSerializer, CustomUserSerializer
from django.shortcuts import render
from rest_framework.generics import CreateAPIView
from rest_framework_simplejwt.views import TokenObtainPairView


from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Personalizar los campos adicionales en el token si es necesario
        # Por ejemplo:
        token['username'] = user.username
        token['email'] = user.email
        return token
    
    def validate(self, attrs):
        data = super().validate(attrs)
        serializer = CustomUserSerializer(self.user)
        data['username'] = serializer.data.get('username')
        data['email'] = serializer.data.get('email')
        return data


# Create your views here.
class RegisterView(CreateAPIView):
    serializer_class = CustomUserSerializer


class LoginView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer