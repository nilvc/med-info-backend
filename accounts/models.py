from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User , on_delete= models.CASCADE , primary_key=True , editable=False)
    first_name = models.CharField(max_length=255)
    middle_name = models.CharField(max_length=255,null=True,blank=True,default="Not provided")
    last_name = models.CharField(max_length=255)
    address = models.TextField(null=True,blank=True,default="Not provided")
    contact_number = models.PositiveBigIntegerField(null=True,blank=True,default=0000)
    gender = models.CharField(max_length=20,null=True,blank=True,default="Not provided")
    blood_group = models.CharField(max_length=20,null=True,blank=True,default="Not provided")
    birth_date = models.DateField(null=True,blank=True,default=None)
    weight = models.PositiveIntegerField(null=True , blank=True,default=0000)
    height = models.PositiveIntegerField(null=True , blank=True,default=0000)
    profile_pic = models.FileField(default="profile_pics/default.png",upload_to="profile_pics/")
    special_info = models.TextField(null=True , blank=True,default="No message")

    def __str__(self) -> str:
        return self.first_name+" "+self.last_name

    def serialize(self):
        first_name = self.first_name
        last_name = self.last_name
        pic = self.profile_pic
        return {
            'first_name':first_name,
            'middle_name':self.middle_name,
            'last_name':last_name,
            'pic':str(pic),
            'address':self.address,
            'contact_number':self.contact_number,
            'gender':self.gender,
            'blood_group':self.blood_group,
            'birth_date':self.birth_date,
            'weight':self.weight,
            'height':self.height,
            'special_info':self.special_info
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


