from django.urls import reverse
from django.views.generic import FormView, ListView
from feedbacks.model_forms import FeedbackModelForm
from feedbacks.models import Feedback


class FeedbackView(FormView):
    form_class = FeedbackModelForm
    template_name = 'feedbacks/create.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        context['feedbacks'] = Feedback.objects.all()
        return context

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('feedbacks')


class FeedbackList(ListView):
    template_name = 'feedbacks/index.html'
    model = Feedback

