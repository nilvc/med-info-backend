from django.contrib.auth.models import User
from django.core.files import File 
from django.core.files.storage import FileSystemStorage
from django.db.models.base import Model
from django.http.response import HttpResponse, HttpResponseBadRequest, JsonResponse
from knox.models import AuthToken
from knox.auth import TokenAuthentication
from rest_framework.decorators import api_view
import json



from .models import Invite, Room
from Utilities.models import Report
from accounts.models import Profile

# Create your views here.

def isauth(request):
    try:
        auth_header = request.headers['Authorization']
    except:
        return None

    token = auth_header[auth_header.index(' ')+1:]
    if not token:
        return None
    user = getUser(token)
    if not user:
        return None
    return user

def getUser(token):
    instance = TokenAuthentication()
    user = instance.authenticate_credentials(bytes(token,'utf-8'))[0]
    return user

    
@api_view(["POST"])
def create_room(request):
    body = json.loads(request.body)
    username = isauth(request)
    if username:
        try:
            owner = Profile.objects.get(user__username = username)
            room = Room.objects.create(owner=owner , room_name = body["room_name"])
            room.save()
            room.members.add(owner)
            room.save()
            return HttpResponse("Room creted successfully")
        except :
            return HttpResponseBadRequest("Unable to create room")
    return HttpResponseBadRequest("NOT AUTHORIZED")


#all rooms
@api_view(["GET"])
def get_myrooms(request,email):
    try:
        member = Profile.objects.get(user__email = email)
        rooms = Room.objects.filter(members = member )
        if len(rooms)==0:
            return JsonResponse({"Rooms":[]},status=201)
        else:
            rooms = [{"room":room.short_serialize()} for room in rooms]
            return JsonResponse({"Rooms":rooms},status=201)
    except:
        return HttpResponseBadRequest("Some error occured")
    

#only particular required rooms
@api_view(["GET"])
def get_room(request,room_id):
    try:
        room = Room.objects.get(room_id = room_id)
        return JsonResponse({"Room":room.serialize()},status=200)
    except Room.DoesNotExist:
        return HttpResponseBadRequest("No room with this id")
    except:
        return HttpResponseBadRequest("Some error occured")

## report handling in room

@api_view(["POST"])
def upload_report(request):
    try:
        file = request.FILES['report']
        fs = FileSystemStorage()
        filename = fs.save(file.name,file)
        file = fs.url(filename)
        print("file url",file)
        report = Report.objects.create(
            title = request.POST.get("title"),
            file = file,
            description = request.POST.get("description")
        )
        report.save()
        room_id = request.POST.get("room_id")
        room = Room.objects.get(pk=room_id)
        room.reports.add(report)
        room.save()
        return JsonResponse({"Report":report.serialize()} , status = 201)
    except:
        return HttpResponseBadRequest("Error occured while uploading report")


#adding only one member for now
@api_view(["POST"])
def addmembers_to_room(request):
    body = json.loads(request.body)
    owner = isauth(request)
    if owner:
        try:
            id = body["invite_id"]
            invite = Invite.objects.get(pk=id)
            member = invite.invite_for.user
            room_id = invite.room.room_id
            room = Room.objects.get(pk=room_id)
            member = Profile.objects.get(user = member )
            room.members.add(member)
            room.save()
            invite.delete()
            return HttpResponse("Member added successfully")
        except:
            return HttpResponseBadRequest("Error Occured")
    return HttpResponseBadRequest("NOT AUTHORIZED")


#to see all invites
@api_view(["GET"])
def get_all_invites(request,email):
    try:    
        user = Profile.objects.get(user__email = email)
        all_invites = Invite.objects.filter(invite_for = user)
        if len(all_invites)==0:
            return JsonResponse({"Invites":[]},status=200)
        else:
            invites = [{"Invite" : invite.serialize() for invite in all_invites}]
            return JsonResponse({"Invites":invites},status=200)
    except Profile.DoesNotExist:
        return HttpResponseBadRequest("No profile registered for this email")
    except:
        return HttpResponseBadRequest("Some error occured")

#to send invites to peoples
@api_view(["POST"])
def sendInvite(request):
    try :
        body = json.loads(request.body)
        room_id = body["room_id"]
        email = body["email"]
        user_profile = Profile.objects.get(user__email = email)
        room = Room.objects.get(pk=room_id)
        invite = Invite.objects.create(invite_for = user_profile , room = room)
        invite.save()
        return HttpResponse("Invite sent")
    except Profile.DoesNotExist:
        return HttpResponseBadRequest("No user profile registered for this email")
    except Room.DoesNotExist:
        return HttpResponseBadRequest("Invalid room id")
    except:
        return HttpResponseBadRequest("Data validation error")


#to reject invitation of room
@api_view(["POST"])
def reject_invitation(request,invite_id):
    try:
        invite = Invite.objects.get(pk=invite_id)
        invite.delete()
        return HttpResponse("Invitation rejected")
    except Invite.DoesNotExist:
        return HttpResponseBadRequest("Invalid invite id")
    except:
        return HttpResponseBadRequest("Some error occured")