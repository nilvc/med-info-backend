from django.urls import path,include
from knox import views as knox_views
from .views import RegisterApi,LoginApi,update_password,get_profile,create_profile,validate_token,update_profilepic

urlpatterns = [
    path("api/auth", include("knox.urls") ),
    path("api/auth/register", RegisterApi.as_view() ),
    path("api/auth/login", LoginApi.as_view() ),
    path("api/auth/logout", knox_views.LogoutView.as_view(),name="knox_logout" ),
    path("api/auth/update_password", update_password),
    path("api/auth/update_profile_pic", update_profilepic),
    path("api/auth/create_profile", create_profile),
    path("api/auth/get_profile/<str:email>", get_profile),
    path("api/auth/validate_token",validate_token ),
]
    
