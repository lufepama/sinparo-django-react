from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name = 'home'),
    path('contacts/', include('api.contacts.urls')),
    path('users/', include('api.users.urls')),
    path('posts/', include('api.posts.urls')),
]

