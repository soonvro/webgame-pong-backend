from django.urls import path
from .views import *

urlpatterns = [
    path('login/', LoginView.as_view()), # GET, POST
    path('logout/', LogoutView.as_view()), # POST
    path('signup/', SignupView.as_view()), # POST
    path('auth/refresh/', CustomTokenRefreshView.as_view()), # POST
]