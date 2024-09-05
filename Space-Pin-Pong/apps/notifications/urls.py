from django.urls import path
from .views import NotificationUpdateView

urlpatterns = [
    path('update/', NotificationUpdateView.as_view()), # PUT 요청
]