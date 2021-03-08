from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()

router.register(r'', views.PostsViewset )

urlpatterns = [
    path('perfil/<str:username>/<str:token>/', views.add_new_post_home, name='new_post'),
    path('get-post-list/<str:username>/<str:token>/', views.get_post_list, name='get_post_list'),
    path('friend-user-posts/<str:username>/<str:token>/<int:id>/', views.get_friend_user_posts, name='friend_profile_posts'),
    path('add-new-posts-friend/<str:username>/<str:token>/<int:id>/', views.add_new_post_friend_profile, name='add_post_friend_profile'),
    path('', include(router.urls))
]