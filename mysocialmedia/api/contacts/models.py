from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.

class ContactList(models.Model):
    
    user = models.ForeignKey(User, null=True, blank = True, on_delete=models.CASCADE)
    id_contact = models.CharField(max_length=100, null=True, blank = True)

    def __str__(self):
        return self.user.first_name