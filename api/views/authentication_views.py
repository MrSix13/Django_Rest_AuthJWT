from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view
from rest_framework import status
from django.http import JsonResponse


from ..repositories.authentication_repository import AuthenticationRepository



# Registo de Usuarios
@api_view(["POST"])
class Register(APIView):
    @staticmethod
    def post(request):  # Cambio de nombre del método a "post"
        try:
            if request.method == "POST":
                username = request.data.get("username")
                password = request.data.get("password")

                if not username or not password:
                    return JsonResponse(
                        {"Message": "Username and password are required"}, status=400
                    )
                try:
                    user = AuthenticationRepository.register_user(username=username, password=password)
                    if user is not None:
                        return JsonResponse(
                            {"Message": "Registration Successfuly", "username": user.username}, status=200
                        )
                    else:
                        return JsonResponse(
                            {"Message": "Username already exists"}, status=500
                        )
                except AuthenticationRepository.DoesNotExist:
                    return JsonResponse(
                        {"Message": "Username already exists"}, status=500
                    )
            else:
                return JsonResponse({"Message": "Method not allowed"}, status=405)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#Login de Usuarios
@api_view(["POST"])
class Login(APIView):
    def post(self, request):
        try:
            email = request.data.get('email')
            password = request.data.get('password')

            #Validamos que los campos no esten vacios
            if not email or not password:
                return JsonResponse({'Error':'Email or Password are requeired'}, status=status.HTTP_400_BAD_REQUEST)

            #LLamada al metodo del repositorio de autenticacion
            user = AuthenticationRepository.authenticate_user(email = email, password = password)

            if user is not None:
                if user.is_active:
                    refresh = RefreshToken.for_user(user)
                    acces_token = str(refresh.access_token)
                    email = str(email)

                    return JsonResponse({
                        'access': acces_token,
                        'refresh': str(refresh),
                        'email':user.email,
                        "mail":email,
                        'name':user.name,
                        "prueba":"prueba 1"
                    })
                else:
                    return JsonResponse({'error': 'User is inactive'}, status= status.HTTP_401_UNAUTHORIZED)

            else:
                return JsonResponse({'error':'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        
        except Exception as e:
         return JsonResponse({'error':str(e)}, stauts=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

#Reset user password
@api_view(["POST"])
def reset_password_request(request):
    try:

        email = request.data.get('email')
        if not email:
            return JsonResponse({'error':'Email is requeired'}, status=status.HTTP_404_NOT_FOUND)


        success, message = AuthenticationRepository.reset_password_request(email)
        if success:
            return JsonResponse({'success': message}, status=status.HTTP_200_OK)
        else:
            return JsonResponse({'error': message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    except Exception as e:
        return JsonResponse({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    


#Reset password confirm
@api_view(['POST'])
def reset_password_confirm(request):
    try:
        uid = request.data.get('uid')
        token = request.data.get('token')
        new_password = request.data.get('new_password')

        if not uid or not token or not new_password:
            return JsonResponse({'error':'UID, token, and new password are required'}, status=status.HTTP_400_BAD_REQUEST)

        success, message = AuthenticationRepository.reset_password_confirm(uid,token, new_password)

        if success:
            return JsonResponse({'Success': message}, status=status.HTTP_200_OK)
        else:
            return JsonResponse({'error': message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)