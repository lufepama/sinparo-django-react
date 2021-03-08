from django.shortcuts import render
from rest_framework import viewsets
from .models import ContactList
from .serializers import ContactListSerializer
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from .models import ContactList

User = get_user_model()

# Create your views here.

def get_contact_list(request, username, token):

    try:
        user = User.objects.get(username = username)
        if user.session_token == token:
            qs = ContactList.objects.filter(user = user)
            my_contact_list =[]
            for i in qs:
                contact_user = User.objects.filter(pk = i.id_contact).values().first()
                contact_user.pop('password')
                my_contact_list.append(contact_user)
            #To send JsonResponse, need to get values() of filtered query. That will transform to object form
            return JsonResponse({'success': 'Ahi tienes!','lista':my_contact_list})

        else:
            return JsonResponse({'error':'Ha habido un problema'})

    except User.DoesNotExist:
        return JsonResponse({'error':'Ha habido un problema. Identificate!'})
    


class ContactViewset(viewsets.ModelViewSet):

    queryset = ContactList.objects.all().order_by('id')
    serializer_class = ContactListSerializer
    