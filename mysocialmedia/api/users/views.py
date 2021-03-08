from django.shortcuts import render
from rest_framework import viewsets
from .serializers import UserProfileSerializer
from django.http import JsonResponse
from rest_framework.permissions import AllowAny
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login, logout
from django.contrib.auth import get_user_model
from .models import CustomUser
import json
import random
from api.posts.models import UserPost
from django.core import serializers

# Create your views here.

User = get_user_model()

def generate_session_token (length=10):
    return ''.join(random.SystemRandom().choice([chr(i) for i in range(97,123)] + [str(i) for i in range(10)]) for _ in range(length) )

def is_user_authenticated(username, token):
    
    try:
        user = User.objects.get(username =username)

        if user.session_token == token:
            return True
        else:
            return False
    except User.DoesNotExist :
        return False

@csrf_exempt 
def signin(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Ha habido un problema y no se ha podido registrar su logeo'})
    
    user_data = json.loads(request.body)

    username = user_data['username']
    password = user_data['password']
    try:
        
        user = User.objects.get(username= username)
        #To access to password. Need to use get method (above)
        if user.password == password:
            if user.session_token == "0":
                
                usr_dict = User.objects.filter(username = username).values().first()
                #Hide the password
                # print('usr_dict', usr_dict)
                usr_dict.pop('password')

                user_token = generate_session_token()
                user.session_token = user_token
                user.save()
                login(request, user)
                return JsonResponse({'token': user_token, 'user': usr_dict}) #Cannot serialize user object
            else:
                user.session_token = 'else'
                user.save()
                return JsonResponse({'error':'Ya has iniciado sesion en otro sitio'})
        else:
            return JsonResponse ( {'error': 'Asegúrate de escribir correctamente la contraseña!'} )

    except User.DoesNotExist:
        return JsonResponse ({'error': 'Introduce un usuario válido'})

def signout(request, id):

    try:
        logged_user = User.objects.get(pk = id)
        if logged_user.session_token != '0':
            logged_user.session_token = '0'
            logged_user.save()
            logout(request)
            return JsonResponse({'success': 'Has cerrado sesión correctamente. Vuelve pronto!'})

    except User.DoesNotExist:
        return JsonResponse({'error': 'Usuario no válido'})

@csrf_exempt 
def signup(request):
    
    if not request.method == 'POST':
        return JsonResponse({'error': 'Ha habido un problema.... :('})
    
    
    user_data = json.loads(request.body)
    qs = CustomUser.objects.filter(username = user_data['username']).first()

    if qs != None:
        return JsonResponse({'error': 'Ya existe un usuario con este nombre'})
    
    username = user_data['username']
    firstName = user_data['firstName']
    lastName = user_data['lastName']
    email = user_data['email']
    address = user_data['address']
    workAddress = user_data['workAddress']
    study_place = user_data['studyPlace']
    living_place = user_data['livingCity']
    password1 = user_data['password1']
    password2 = user_data['password2']
    
    if password1 != password2:
        return JsonResponse({'error': 'Las contraseñas no coinciden'})
    else:
        if len(password1) <5:
            return JsonResponse({'error': 'La contraseña debe ser mas larga. Por tu seguridad'})
    new_user = CustomUser(
        username=username, first_name= firstName, last_name = lastName, 
        email= email, address =address, work_place = workAddress,study_place = study_place, living_city = living_place
    )
    new_user.save()
    return JsonResponse({'success': 'Usuario creado correctamente. :)'})


def get_friend_user_info(request, username, token, id):
    
    try:
        if (is_user_authenticated(username, token)):
            try:
                friend_user = CustomUser.objects.filter(pk=id).values().first()
                friend_user.pop('password')

                return JsonResponse({'success':'Ahi tienes!', 'friendInfo':friend_user})
            
            except User.DoesNotExist:
                return JsonResponse({'error':'No se encuentra el perfil!'})
        else:
            return JsonResponse({'error': 'No has iniciado sesión!'})
    except User.DoesNotExist:
        return JsonResponse({'error':'Ha habido un problema!'})


class UserViewset(viewsets.ModelViewSet):

    permission_classes_by_action = {'create':[AllowAny]}

    queryset = CustomUser.objects.all().order_by('id')
    serializer_class = UserProfileSerializer

    def get_permissions(self):
        try:
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            return [permission() for permission in self.permission_classes]