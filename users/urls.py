from django.urls import path
from . import views
from .views import AuthorizationAPIView,RegistrationAPIView
urlpatterns = [
    path('registration/', RegistrationAPIView.as_view()),
    path('authorization/', AuthorizationAPIView.as_view()),
]