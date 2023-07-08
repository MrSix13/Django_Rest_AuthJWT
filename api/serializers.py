from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from myapp.models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ("id", "name", "email", "password", "username")
        extra_kwargs = {"password": {'write_only': True}}

    def create(self, validated_data):
        # Extraemos y eliminamos el campo 'password' de los datos validados
        password = validated_data.pop('password')
        # Creamos un nuevo usuario utilizando los datos validados
        user = CustomUser.objects.create_user(**validated_data)
        # Establecemos la contraseña para el usuario
        user.set_password(password)
        # Guardamos el usuario en la base de datos
        user.save()
        return user
    

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def get_token(self, user):
        # Obtenemos el token utilizando la implementación base
        token = super().get_token(user)

        # Agregamos campos personalizados al token
        token['email'] = user.email
        token['name'] = user.name
        token['isStaff'] = user.is_staff

        return token