from django.contrib.auth.models import User
from django.db import models
from django.db.models.base import Model
from accounts.models import Profile
from Utilities.models import Report
import uuid

# Create your models here.
class Room(models.Model):
    owner = models.ForeignKey(Profile, on_delete = models.CASCADE , related_name="owner")
    patient = models.ForeignKey(Profile, on_delete = models.CASCADE , null=True , related_name= "patient")
    room_id =  models.UUIDField(primary_key = True,default = uuid.uuid4,editable = False)
    room_name = models.CharField(max_length = 255 , null= True , default= "Default room name")
    members = models.ManyToManyField(Profile , related_name = "members")
    reports = models.ManyToManyField(Report,blank=True)


    def __str__(self) -> str:
        return self.room_name

    def serialize(self):
        owner = {
            "first_name":self.owner.first_name,
            "last_name":self.owner.last_name,
            "email":self.owner.user.email
        }
        if self.patient:
            patient = {
                "first_name":self.patient.first_name,
                "last_name":self.patient.last_name,
                "email":self.patient.user.email
            }
        else:
            patient = {"first_name":"Not assigned",
                "last_name":"Not assigned",
                "email":"Not assigned"}

        room_id = self.room_id
        room_name = self.room_name


        members = [{ 'profile':member.short_serialize()} 
                    for member in self.members.all()] 
        
        reports = [{ 'report':report.serialize()} 
                    for report in self.reports.all()] 

        return {
            "owner" : owner,
            "patient" : patient,
            "room_id" : room_id,
            "room_name" : room_name,
            "members" : members,
            "reports" : reports
        }


    def short_serialize(self):
        owner = {
            "name":self.owner.first_name +" "+self.owner.last_name
        }
        if self.patient:
            patient = {
                "name":self.patient.first_name +" "+self.patient.last_name
            }
        else:
            patient = {"name":"Not assigned"}

        room_id = self.room_id
        room_name = self.room_name

        return {
            "owner" : owner,
            "patient" : patient,
            "room_id" : room_id,
            "room_name" : room_name
        }


class Invite(models.Model):
    invite_id = models.UUIDField(primary_key = True,default = uuid.uuid4,editable = False)
    invite_for = models.OneToOneField(Profile , on_delete=models.CASCADE)
    room = models.OneToOneField(Room , on_delete=models.CASCADE)

    def serialize(self):
        return{
            "invite_id" : self.invite_id,
            "room" : self.room.short_serialize()
        }