from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

class CustomUser(AbstractUser):
    username = models.CharField(max_length=50, unique=True)
    # user = models.ForeignKey(CustomUser, null=True, blank = True, on_delete=models.CASCADE)
    # username = models.CharField(max_length=50, null=True, blank = True)
    profile_image = models.ImageField(upload_to='images/', blank =True, null= True)
    cover_image = models.ImageField(upload_to='images/', blank =True, null= True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length = 100)
    address = models.CharField(max_length = 100, null=True, blank=True)
    work_place = models.CharField(max_length = 100, blank = True, null=True)
    study_place = models.CharField(max_length = 100, blank = True, null=True)
    living_city = models.CharField(max_length = 100, blank = True, null=True)
    account_created_at = models.DateTimeField(auto_now_add=True)
    is_private = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    session_token = models.CharField(max_length=20, default=0)



    def __str__(self):
        return self.first_name