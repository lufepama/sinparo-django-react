from rest_framework import routers
from django.urls import path, include
from . import views

router = routers.DefaultRouter()
router.register(r'', views.UserViewset)

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    # path('contactlist/<int:id>/', views.contact_list, name='contact_list'),
    path('signin/', views.signin, name='signin'),
    path('signout/<int:id>/', views.signout, name='signout'),
    path('friend-user-info/<str:username>/<str:token>/<int:id>/', views.get_friend_user_info, name='friend_profile'),
    path('', include(router.urls)),
]
