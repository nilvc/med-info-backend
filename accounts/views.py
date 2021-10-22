from rest_framework import generics , permissions
from django.http.response import HttpResponse, HttpResponseBadRequest, HttpResponseBase ,JsonResponse
from rest_framework.response import Response
from knox.models import AuthToken

from medbackend.settings import BASE_DIR
from .serializers import UserSerializer,RegisterUserSerializer,LoginUserSerializer
from knox.auth import TokenAuthentication
from rest_framework.decorators import api_view
import json
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.hashers import make_password


from django.contrib.auth.models import User
from .models import Profile



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


class RegisterApi(generics.GenericAPIView):
    serializer_class = RegisterUserSerializer
   

    def post(self,request,*args,**kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "token":AuthToken.objects.create(user)[1],
            "user":UserSerializer(user,context=self.get_serializer_context()).data
        }) 


#login user
class LoginApi(generics.GenericAPIView):
    serializer_class = LoginUserSerializer

    def post(self,request,*args,**kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        return Response({
            "token":AuthToken.objects.create(user)[1],
            "user":UserSerializer(user,context=self.get_serializer_context()).data,
        }) 


@api_view(["POST"])
def create_profile(request):
    try:
        first_name = request.POST.get('first_name')
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        password = make_password(request.POST.get("password"))
        username = email.split("@")[0]
        file = request.FILES['profile_pic']
        fs = FileSystemStorage()
        filename = fs.save(file.name,file)
        pic = fs.url(filename)
        user = User.objects.create(username = username , email = email , password = password)
        user.save()
        profile = Profile.objects.create(user = user , first_name = first_name , last_name = last_name , profile_pic = pic)
        profile.save()
        return HttpResponse("Profile created successfully")
    except:
        return HttpResponseBadRequest("Some error occured")
    

@api_view(["GET"])
def get_profile(request,email):
    try:
        profile = Profile.objects.get(user__email = email)
        return JsonResponse({"profile":profile.serialize()},status=200)
    except:
        return HttpResponseBadRequest("Not worked")


@api_view(["GET"])
def validate_token(request):
    try:
        user =isauth(request)
        if user:
            return HttpResponse("Autenticated")
        else:
            return HttpResponseBadRequest("Not Autenticated")
    except:
        return HttpResponseBadRequest("Not Autenticated")


@api_view(["POST"])
def update_password(request):
    try:
        username = isauth(request)
        if username:
            user = User.objects.get(username=username)
            body = json.loads(request.body)
            new_password = body["new_password"] 
            success = user.check_password(new_password)
            if success: 
                user.set_password(new_password)
                user.save()
                return HttpResponse("Password updated successfully")
            else:
                return HttpResponseBadRequest("Password validation error")
        else:
            return HttpResponse("Not authorized")
    except:
        return HttpResponseBadRequest("Error occured")


@api_view(["POST"])
def update_profilepic(request):
    try:
        username = isauth(request)
        if username:
            fs=FileSystemStorage()
            user = Profile.objects.get(user__username = username)
            prev_profile_path = user.profile_pic
            new_profile_pic = request.FILES['new_profile_pic']
            path = str(BASE_DIR) +str(prev_profile_path)
            path = path.replace("/","\\")
            fs.delete(path)
            filename = fs.save(new_profile_pic.name,new_profile_pic)
            pic_url = fs.url(filename)
            user.profile_pic = pic_url
            user.save()
            return JsonResponse({"pic":pic_url})
        else:
            return HttpResponseBadRequest("Not authorized")
    except Profile.DoesNotExist:
        return HttpResponseBadRequest("No profile for given username")

    