from django.urls import path
from .views import OAuthView

urlpatterns = [
    path('oauth/', OAuthView.as_view()),
]