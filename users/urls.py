from django.urls import path
from .views import (
    RegisterAPI,
    LoginAPI,
    SendFriendRequest,
    AcceptFriendRequest,
    PendingFriendRequests,
    RejectFriendRequest,
    FriendList,
    UserSearch,
)

urlpatterns = [
    path('signup', RegisterAPI.as_view()),
    path('login', LoginAPI.as_view()),
    path('friend-request/send/<int:user_id>/', SendFriendRequest.as_view(), name='send_friend_request'),
    path('friend-request/accept/<int:request_id>/', AcceptFriendRequest.as_view(), name='accept_friend_request'),
    path('friend-request/reject/<int:request_id>/', RejectFriendRequest.as_view(), name='reject_friend_request'),
    path('friend-request/pending/', PendingFriendRequests.as_view(), name='pending_friend_requests'),
    path('friend-list', FriendList.as_view(), name='friend_list'),
    path('search/', UserSearch.as_view(), name='user_search'),
]
