from django.contrib.auth.decorators import login_required
from django.urls import path

from feedbacks.views import FeedbackView, FeedbackList

urlpatterns = [
    path('create/', login_required(FeedbackView.as_view()), name='feedback_create'),
    path('', FeedbackList.as_view(), name='feedbacks'),
]
