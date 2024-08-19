from django.urls import path
from .views import *

urlpatterns = [
    # {42-id}/ GET Authorization: Bearer "access_token"
    path('<str:user_id>/', UserInfoView.as_view()), # GET, DELETE 요청

    # {42-id}/ DELETE Authorization: Bearer "access_token"
    path('<str:user_id>/', UserDeleteView.as_view()), # DELETE 요청

    # histories/{42-id} GET Authorization: Bearer "access_token"
    path('histories/<str:user_id>/', UserHistoryView.as_view()), # GET 요청

    # nicknames/{42-id} PUT Authorization: Bearer "access_token"
    path('nicknames/<str:user_id>/', UserNicknameUpdateView.as_view()), # PUT 요청

    # pictures/{42-id} PUT Authorization: Bearer "access_token"
    path('pictures/<str:user_id>/', UserPictureUpdateView.as_view()), # PUT 요청

    # {42-id}/friends/ GET Authorization: Bearer "access_token"
    path('<str:user_id>/friends/', UserFriendsListView.as_view()), # GET 요청

    # {42-id}/friends/ POST Authorization: Bearer "access_token" {"friend_id": "user"}
    path('<str:user_id>/friends/', UserFriendAddView.as_view()), # POST 요청

    # {42-id}/friends/{42-friend-id} DELETE Authorization: Bearer "access_token"
    path('<str:user_id>/friends/<str:friend_id>/', UserFriendDeleteView.as_view()), # DELETE 요청
]