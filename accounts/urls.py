from django.contrib.auth.views import LogoutView
from django.urls import path, include

from accounts.views import RegistrationView

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
