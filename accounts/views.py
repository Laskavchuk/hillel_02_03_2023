

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.core.cache import cache
from django.http import Http404
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.http import urlsafe_base64_decode
from django.views import generic
from django.views.generic import FormView, RedirectView
from django.contrib.auth.views import LoginView as AuthLoginView
from accounts.model_forms import RegistrationForm, AuthenticationForm, \
    PhoneValidationForm, CustomUserChangeForm
from accounts.tasks import send_code_task
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ImproperlyConfigured, ValidationError

User = get_user_model()


class RegistrationView(FormView):
    template_name = 'registration/signup.html'
    form_class = RegistrationForm
    email_template_name = "registration/registration_email.html"
    extra_email_context = None
    from_email = None
    html_email_template_name = None
    token_generator = default_token_generator
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        messages.success(self.request,
                         _('We will send email with registration link. '
                           'Please follow link and continue your '
                           'registration flow.'))

        opts = {
            "use_https": self.request.is_secure(),
            "token_generator": self.token_generator,
            "from_email": self.from_email,
            "email_template_name": self.email_template_name,
            "request": self.request,
            "html_email_template_name": self.html_email_template_name,
            "extra_email_context": self.extra_email_context,
        }
        form.save(**opts)
        return super().form_valid(form)


class LoginView(AuthLoginView):
    form_class = AuthenticationForm

    def form_valid(self, form):
        """Security check complete. Log the user in."""
        messages.success(self.request, _('Welcome back!'))
        return super().form_valid(form)


class PhoneValidationView(FormView):
    form_class = PhoneValidationForm
    template_name = 'registration/code.html'
    success_url = reverse_lazy('main')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.save()
        messages.success(self.request, _('Phone number confirmed!'))
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user_id'] = self.request.user.id
        return kwargs

    def get(self, request, *args, **kwargs):
        send_code_task.delay(request.user.id)
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        user_id = request.user.id
        saved_code = cache.get(f'{user_id}_code')
        if not saved_code:
            send_code_task.delay(user_id)
        return super().post(request, *args, **kwargs)


class RegistrationConfirmView(RedirectView):
    url = reverse_lazy('login')

    def dispatch(self, *args, **kwargs):
        if "uidb64" not in kwargs or "token" not in kwargs:
            raise ImproperlyConfigured(
                "The URL path must contain 'uidb64' and 'token' parameters."
            )
        self.user = self.get_user(kwargs["uidb64"])
        if self.user is None:
            raise Http404
        if not default_token_generator.check_token(self.user, kwargs["token"]):
            raise Http404
        return super().dispatch(*args, **kwargs)

    def get_user(self, uidb64):
        try:
            # urlsafe_base64_decode() decodes to bytestring
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except (
                TypeError,
                ValueError,
                OverflowError,
                User.DoesNotExist,
                ValidationError,
        ):
            user = None
        return user

    def get(self, request, *args, **kwargs):
        self.user.is_active = True
        self.user.save()
        return super().get(request, *args, **kwargs)


class UserEditView(generic.UpdateView):
    form_class = CustomUserChangeForm
    template_name = 'registration/edit_profile.html'
    success_url = reverse_lazy('main')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, _('Edited successfully!'))
        return response
