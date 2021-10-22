from django.urls import path,include
from .views import create_room ,delete_room, get_myrooms , get_room , upload_report , sendInvite , get_all_invites , addmembers_to_room ,reject_invitation , get_searched_room , remove_member_from_room


urlpatterns = [
    path("create_room", create_room),
    path("delete_room/<slug:room_id>", delete_room),
    path("get_myrooms/<str:email>", get_myrooms),#all rooms
    path("get_room/<slug:room_id>", get_room), # only one room they asked for
    path("get_searched_room/<slug:room_id>", get_searched_room), # only one room they searched for in search form
    path("upload_report", upload_report),
    path("add_member", addmembers_to_room),
    path("get_allinvites/<str:email>", get_all_invites), 
    path("send_invite", sendInvite),
    path("reject_invite/<slug:invite_id>", reject_invitation),
    path("remove_member", remove_member_from_room),


]
