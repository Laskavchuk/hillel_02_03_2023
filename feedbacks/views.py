from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import FormView, ListView
from feedbacks.model_forms import FeedbackModelForm
from feedbacks.models import Feedback
#from project.celery import debug_task
from project.model_choices import FeedbackCacheKeys


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
        messages.success(self.request, ('Feedback added!'))
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('feedbacks')

    @method_decorator(login_required())
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class FeedbackList(ListView):
    template_name = 'feedbacks/index.html'
    model = Feedback

    def get_queryset(self):
        queryset = cache.get(FeedbackCacheKeys.FEEDBACKS)
        if not queryset:
            print('TO CACHE')
            queryset = Feedback.objects.all()
            cache.set(FeedbackCacheKeys.FEEDBACKS, queryset)

        ordering = self.get_ordering()
        if ordering:
            if isinstance(ordering, str):
                ordering = (ordering,)
            queryset = queryset.order_by(*ordering)

        return queryset


    #def get(self, request, *args, **kwargs):
    #    debug_task.delay()
    #    return super().get(request, *args, **kwargs)

    #def get(self, request, *args, **kwargs):
    #    debug_task.apply_async((2, 2), retry=True, retry_policy={
    #        'max_retries': 3
    #    })
    #    return super().get(request, *args, **kwargs)

