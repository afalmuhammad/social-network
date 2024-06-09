from django.urls import path, include
from .views import (
    SignupView,
    LoginView,
    UserListView,
    UserSearchView,
    SendFriendRequestView,
    ManageFriendRequestView,
    FriendsListView,
    PendingFriendRequestsView,
)

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('list-users/', UserListView.as_view(), name='list-user'),
    path('search/', UserSearchView.as_view(), name='user-search'),
    path('friend-request/', SendFriendRequestView.as_view(), name='send-friend-request'),
    path('friend-request/<int:request_id>/<str:action>/', ManageFriendRequestView.as_view(), name='manage-friend-request'),
    path('friends/', FriendsListView.as_view(), name='friends-list'),
    path('pending-requests/', PendingFriendRequestsView.as_view(), name='pending-friend-requests'),
]
