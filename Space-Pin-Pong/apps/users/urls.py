from django.urls import path

from .views import (FriendAcceptView, FriendRejectView, UserDeactivateView,
                    UserFriendView, UserInfoView, UserUpdateView)

urlpatterns = [
    path('nickname/', UserUpdateView.as_view()), # PUT 요청
    path('picture/', UserUpdateView.as_view()), # PUT 요청
    path('friends/', UserFriendView.as_view()), # GET 요청
    path('deactivate/', UserDeactivateView.as_view()), # DELETE 요청
    path('<str:user_id>/info/', UserInfoView.as_view()), # GET, DELETE 요청
    # path('histories/<str:user_id>/', UserHistoryView.as_view()), # GET 요청
    path('friends/<str:friend_id>/', UserFriendView.as_view()), # POST, DELETE 요청
    path('friends/<str:friend_id>/accept/', FriendAcceptView.as_view()), # POST 요청
    path('friends/<str:friend_id>/reject/', FriendRejectView.as_view()), # DELETE 요청
]
