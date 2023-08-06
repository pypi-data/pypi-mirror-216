from django.urls import path
from .views import AuthTokenView

urlpatterns = [
    path('auth/', AuthTokenView.as_view(), name="auth")
]