from random import randint

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import FormView
from django.contrib.auth.views import LoginView as AuthLoginView
from accounts.model_forms import RegistrationForm, AuthenticationForm, \
    PhoneValidationForm
from accounts.tasks import send_code_task


class RegistrationView(FormView):
    template_name = 'registration/signup.html'
    form_class = RegistrationForm
    success_url = reverse_lazy('phone_validation')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        messages.success(self.request, 'Registration success!')
        return super().form_valid(form)


class LoginView(AuthLoginView):
    form_class = AuthenticationForm

    def form_valid(self, form):
        """Security check complete. Log the user in."""
        messages.success(self.request, 'Welcome back!')
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
        messages.success(self.request, 'Phone number confirmed!')
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
