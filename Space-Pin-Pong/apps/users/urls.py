from django.urls import path
from .views import *

urlpatterns = [
    # {42-id}/ GET Authorization: Bearer "access_token"
    path('<str:user_id>/', UserInfoView.as_view()), # GET, DELETE 요청

    # {42-id}/ DELETE Authorization: Bearer "access_token"
    path('deactivate/', UserDeactivateView.as_view()), # DELETE 요청

    # histories/{42-id} GET Authorization: Bearer "access_token"
    path('histories/<str:user_id>', UserHistoryView.as_view()), # GET 요청

    # nicknames/{42-id} PUT Authorization: Bearer "access_token"
    path('nicknames/', UserNicknameUpdateView.as_view()), # PUT 요청

    # pictures/{42-id} PUT Authorization: Bearer "access_token"
    path('pictures/', UserPictureUpdateView.as_view()), # PUT 요청

    # friends/ GET Authorization: Bearer "access_token"
    path('friends/', UserFriendsListView.as_view()), # GET 요청

    # friends/{42-friend-id} POST Authorization: Bearer "access_token"
    path('friends/<str:friend_id>/', UserFriendAddView.as_view()), # POST 요청

    # friends/{42-friend-id} DELETE Authorization: Bearer "access_token"
    path('friends/<str:friend_id>/', UserFriendDeleteView.as_view()), # DELETE 요청
]