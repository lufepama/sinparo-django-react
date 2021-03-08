from django.db import models
from django.contrib.postgres.fields import JSONField
from django.contrib.auth import get_user_model


# Create your models here.

User = get_user_model()

class UserPost(models.Model):

    user = models.ForeignKey(User, null=True, blank = True, on_delete=models.CASCADE)
    post_content = models.CharField(max_length = 120)
    upload_date = models.DateTimeField(auto_now_add=True)
    who_did_post = models.IntegerField(blank=True, null=True)
    likes_number = models.PositiveSmallIntegerField( default = 0,blank= True, null=True)
    dislikes_number = models.PositiveSmallIntegerField( default = 0, blank=True, null=True)
    user_who_posted = models.JSONField(null=True, blank = True)


    def __str__(self):
        return self.post_content
    
    # @property
    # def get_person_who_posted(self):
    
    #     profile_user_list = User.objects.filter(pk = self.who_did_post)
    #     return profile_user_list.first()

    # @property
    # def increase_likes_number(self):
    #     self.likes_number +=1
    #     self.save()
    
    # @property
    # def increase_dislikes_number(self):
    #     self.dislikes_number +=1
    #     self.save()