import re

from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, \
    AuthenticationForm as AuthAuthenticationForm, UserChangeForm
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.cache import cache
from django.core.exceptions import ValidationError
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.utils.text import capfirst
from django import forms
from django.utils.translation import gettext_lazy as _
from accounts.tasks import send_registration_email
User = get_user_model()


class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("email", "phone")

    def clean_phone(self):
        phone_number = self.cleaned_data.get('phone')
        if phone_number:
            if not re.fullmatch(
                    r'^\+?\d{1,4}[-.\s]?[(]?\d{1,4}[)]?[-.\s]?\d{1,3}[-.\s]?\d{1,3}[-.\s]?\d{1,3}$',# noqa
                    phone_number
            ):
                raise ValidationError(_('Invalid phone number'))
            phone_number = re.sub(r'[-.\s+()]', '', phone_number)
        return phone_number

    def clean_email(self):
        try:
            User.objects.get(email=self.cleaned_data['email'])
        except User.DoesNotExist:
            return self.cleaned_data['email']
        raise ValidationError(_('Email already exist.'))

    def save(self,
             domain_override=None,
             email_template_name="registration/registration_email.html",
             use_https=False,
             token_generator=default_token_generator,
             from_email=None,
             request=None,
             html_email_template_name=None,
             extra_email_context=None,
             commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.is_active = False
        if commit:
            user.save()
            if hasattr(self, "save_m2m"):
                self.save_m2m()

        user_email = user.email
        if not domain_override:
            current_site = get_current_site(request)
            site_name = current_site.name
            domain = current_site.domain
        else:
            site_name = domain = domain_override
        context = {
            "domain": domain,
            "site_name": site_name,
            "uid": urlsafe_base64_encode(force_bytes(user.pk)),
            "token": token_generator.make_token(user),
            "protocol": "https" if use_https else "http",
            **(extra_email_context or {}),
        }
        send_registration_email.delay(
            email_template_name,
            context,
            from_email,
            user_email,
            html_email_template_name
        )
        return user


class AuthenticationForm(AuthAuthenticationForm):

    def __init__(self, request=None, *args, **kwargs):
        super().__init__(request=request, *args, **kwargs)
        self.fields["username"].label = (
            f'{capfirst(self.username_field.verbose_name)} or Phone number')
        self.error_messages = {
            "invalid_login": _(
                "Please enter a correct %(username)s or phone and password. "
                "Note that both fields may be case-sensitive. "
            ),
            "inactive": _(
                "This account is inactive."
            )}


class PhoneValidationForm(forms.Form):
    code = forms.IntegerField()

    def __init__(self, *args, **kwargs):
        self.user_id = kwargs.pop('user_id')
        super().__init__(*args, **kwargs)

    def clean_code(self):
        code = self.cleaned_data.get('code')
        saved_code = cache.get(f'{self.user_id}_code')
        if not saved_code:
            raise ValidationError(_('Confirmation code has expired. '
                                  'We sent you a new code'))
        if code != saved_code:
            raise ValidationError(_('Invalid code'))

    def save(self):
        user = User.objects.get(id=self.user_id)
        user.is_phone_valid = True
        user.save()


class CustomUserChangeForm(UserChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.pop('password')

    class Meta(UserChangeForm.Meta):
        model = User
        fields = ('first_name', 'last_name', 'email', 'phone')

    def clean_phone(self):
        phone_number = self.cleaned_data.get('phone')
        if phone_number:
            if not re.fullmatch(
                    r'^\+?\d{1,4}[-.\s]?[(]?\d{1,4}[)]?[-.\s]?\d{1,3}[-.\s]?\d{1,3}[-.\s]?\d{1,3}$',# noqa
                    phone_number
            ):
                raise ValidationError(_('Invalid phone number'))
            phone_number = re.sub(r'[-.\s+()]', '', phone_number)
            try:
                User.objects.get(phone=self.cleaned_data['phone'])
            except User.DoesNotExist:
                return phone_number
            raise ValidationError(_('Phone already exist.'))
