from rest_framework import routers
from django.contrib import admin
from django.urls import path, include
from . import views

# from .views import 

router = routers.DefaultRouter()
router.register(r'', views.ContactViewset)

urlpatterns = [
    path('', include(router.urls)),
    path('get-contactlist/<str:username>/<str:token>/', views.get_contact_list, name ='get_contact_list'),
]