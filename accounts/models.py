from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User , on_delete= models.CASCADE , primary_key=True , editable=False)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    profile_pic = models.FileField(default="profile_pics/default.png",upload_to="profile_pics/")
    

    def __str__(self) -> str:
        return self.first_name+" "+self.last_name

    def serialize(self):
        first_name = self.first_name
        last_name = self.last_name
        pic = self.profile_pic
        username = self.user.username
        email = self.user.email
        return {
            'user_name' : username,
            'email' : email,
            'first_name':first_name,
            'last_name':last_name,
            'pic':str(pic),
        }
    
    def short_serialize(self):
        first_name = self.first_name
        last_name = self.last_name
        pic = self.profile_pic
        return {
            'first_name':first_name,
            'last_name':last_name,
            'pic':str(pic),
        }


