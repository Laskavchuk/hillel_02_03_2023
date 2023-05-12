from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, \
    AuthenticationForm as AuthAuthenticationForm
from django.core.cache import cache
from django.core.exceptions import ValidationError
from django.utils.text import capfirst
from django import forms
User = get_user_model()


class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("email", "phone")

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if len(phone) < 5:
            raise ValidationError('Phone is too short.')
        elif len(phone) > 15:
            raise ValidationError('Phone is too long.')
        elif not isinstance(phone, int):
            raise ValidationError('Phone number must be an integer.')
        try:
            User.objects.get(phone=phone)
        except User.DoesNotExist:
            return phone
        raise ValidationError('Phone already exist.')

    def clean_email(self):
        try:
            User.objects.get(email=self.cleaned_data['email'])
        except User.DoesNotExist:
            return self.cleaned_data['email']
        raise ValidationError('Email already exist.')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class AuthenticationForm(AuthAuthenticationForm):

    def __init__(self, request=None, *args, **kwargs):
        super().__init__(request=request, *args, **kwargs)
        self.fields["username"].label = (
            f'{capfirst(self.username_field.verbose_name)} or Phone number')
        self.error_messages = {
        "invalid_login": (
            "Please enter a correct %(username)s or phone and password. "
            "Note that both fields may be case-sensitive. "
        ),
        "inactive": ("This account is inactive.")}


class PhoneValidationForm(forms.Form):
    code = forms.IntegerField()

    def __init__(self, *args, **kwargs):
        self.user_id = kwargs.pop('user_id')
        super().__init__(*args, **kwargs)

    def clean_code(self):
        code = self.cleaned_data.get('code')
        saved_code = cache.get(f'{self.user_id}_code')
        if not saved_code:
            raise ValidationError('Confirmation code has expired. '
                                  'We sent you a new code')
        if code != saved_code:
            raise ValidationError('Invalid code')

    def save(self):
        user = User.objects.get(id=self.user_id)
        user.is_phone_valid = True
        user.save()
