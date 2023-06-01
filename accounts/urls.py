from django.contrib.auth.views import LogoutView
from django.urls import path
from django.contrib.auth import views as auth_views

from accounts.views import RegistrationView, LoginView, PhoneValidationView, \
    RegistrationConfirmView

urlpatterns = [
    # path('', include('django.contrib.auth.urls')),
    path("logout/", LogoutView.as_view(), name="logout"),
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('login/', LoginView.as_view(), name='login'),
    path(
        'phone_validation/',
        PhoneValidationView.as_view(),
        name='phone_validation'
    ),

    path(
        "registration/<uidb64>/<token>/",
        RegistrationConfirmView.as_view(),
        name="registration_confirm",
     ),
    path(
        "password_change/", auth_views.PasswordChangeView.as_view(),
        name="password_change"
    ),
    path(
        "password_change/done/",
        auth_views.PasswordChangeDoneView.as_view(),
        name="password_change_done",
    ),
    path("password_reset/", auth_views.PasswordResetView.as_view(),
         name="password_reset"),
    path(
        "password_reset/done/",
        auth_views.PasswordResetDoneView.as_view(),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        auth_views.PasswordResetCompleteView.as_view(),
        name="password_reset_complete",
    ),

]
