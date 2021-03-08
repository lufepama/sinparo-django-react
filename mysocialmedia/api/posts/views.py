from django.shortcuts import render
from rest_framework import viewsets
from .models import UserPost
from .serializers import UserPostSerializer
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_exempt
import json
from .models import UserPost
from django.http import JsonResponse
from django.core import serializers

# Create your views here.
User = get_user_model()

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
def add_new_post_home(request, username, token):
    print('entre')
    if not request.method == 'POST':
        return JsonResponse ({'error': 'No se ha podido enviar la publicación.'})
    
    if is_user_authenticated(username, token):
        data = json.loads(request.body)

        post_message = data['post_content']
        
        try:
            current_user = User.objects.get(username = username)
            if post_message != '':
                new_post = UserPost(
                    user=current_user, post_content = post_message, 
                    who_did_post = current_user.id,
                    user_who_posted = {'username': current_user.username, 'profile_img':current_user.profile_image.url}
                )
                new_post.save()
                return JsonResponse({'success': 'Post publicado'})
            else:
                return JsonResponse({'error': 'No puedes publicar algo vacío!'})
        except User.DoesNotExist:
            return Json({'error':'Ha habido un error.'})

def get_post_list(request, username, token):
    
    try:
        current_user = User.objects.get(username=username)

        if is_user_authenticated(username, token):
            post_user_list = UserPost.objects.filter(user=current_user).order_by('-id')
            
            serializer_qs = serializers.serialize('json', post_user_list, fields=('user_who_posted, post_content'))

            return JsonResponse({'success':'Ahi tienes!', 'postlist':serializer_qs})
        else:
            return JsonResponse({'error':'No has iniciado sesión!'})

    except User.DoesNotExist:
        return JsonResponse({'error': 'Ha habido un error'})

def get_friend_user_posts(request, username, token, id):
    
    try:
        
        if (is_user_authenticated(username, token)):
            
            try:
                friend_user = User.objects.get(pk=id)
                post_user_list = UserPost.objects.filter(user=friend_user).order_by('-id')
                
                serializer_qs = serializers.serialize('json', post_user_list, fields=('user_who_posted, post_content'))
            
                return JsonResponse({'success':'Ahi tienes!', 'postlist':serializer_qs})

            except:
                return JsonResponse({'error':'El usuario no existe!'})

    except:
        return JsonResponse({'error':'Ha habido un problema'})


#TODO: Add comments to post view
#TODO: Add likes and dislikes view 

class PostsViewset(viewsets.ModelViewSet):

    queryset = UserPost.objects.all().order_by('id')
    serializer_class = UserPostSerializer