from rest_framework import generics , permissions
from django.http.response import HttpResponse, HttpResponseBadRequest ,JsonResponse
from rest_framework.response import Response
from knox.models import AuthToken
from .serializers import UserSerializer,RegisterUserSerializer,LoginUserSerializer
from knox.auth import TokenAuthentication
from rest_framework.decorators import api_view
import json
from django.core.files.storage import FileSystemStorage


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
def update_password(request):
    body = json.loads(request.body)
    password = body["password"] 
    user = User.objects.get(username = body["username"])
    print(password,body["password"],user)
    if user:
        user.set_password(password)
        user.save()
        return HttpResponse("Password updated")
    return HttpResponseBadRequest("Error")


@api_view(["POST"])
def create_profile(request):
        user = isauth(request)
        if not user:
            return HttpResponseBadRequest('Authentication needed')
        user = User.objects.get(username = user)
        file = request.FILES['profile_pic']
        

        fs = FileSystemStorage()
        filename = fs.save(file.name,file)
        pic = fs.url(filename)
        newProfile = Profile.objects.create(
            user = user,
            first_name = request.POST.get('first_name'),
            middle_name = request.POST.get("middle_name"),
            last_name = request.POST.get("last_name"),
            address = request.POST.get("address"),
            contact_number = int(request.POST.get("contact_number")),
            gender = request.POST.get("gender"),
            blood_group = request.POST.get("blood_group"),
            birth_date = request.POST.get("birth_date"),
            weight  = int(request.POST.get("weight")),
            height = int(request.POST.get("height")),
            special_info = request.POST.get("special_info"),
            profile_pic = pic
        )
        newProfile.save()
        return JsonResponse({"profile" : newProfile.serialize()},status = 201)
    
    




@api_view(["GET"])
def get_profile(request,email):
    try:
        profile = Profile.objects.get(user__email = email)
        return JsonResponse({"profile":profile.serialize()},status=200)
    except:
        return HttpResponseBadRequest("Not worked")