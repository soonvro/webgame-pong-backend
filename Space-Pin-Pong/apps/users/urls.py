from django.urls import path
from .views import UserInfo

urlpatterns = [
    path('mypage/', UserInfo.as_view()), # GET, DELETE 요청
    # path('mypage/friends/', ) # GET, POST, DELETE 요청
    # path('mypage/histories/', ) # GET 요청
    # path('mypage/nickname/', ) # PUT 요청
    # path('mypage/picture/', ) # PUT 요청
]