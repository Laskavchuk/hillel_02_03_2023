from django.urls import reverse_lazy
from django.views.generic import TemplateView, FormView

from main.forms import ContactForm
from main.tasks import send_contact_form


class MainView(TemplateView):
    template_name = 'main/index.html'


class ContactView(FormView):
    form_class = ContactForm
    template_name = 'contacts/index.html'
    success_url = reverse_lazy('main')

    def form_valid(self, form):
        send_contact_form.delay(form.cleaned_data['email'],
                                form.cleaned_data["text"]
                                )
        return super().form_valid(form)
