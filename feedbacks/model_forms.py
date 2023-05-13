from django import forms
from django.utils.html import strip_tags

from feedbacks.models import Feedback
from django.utils.translation import gettext_lazy as _


class FeedbackModelForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ('text', 'user', 'rating')

    def __init__(self, user=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user'].widget = forms.HiddenInput()
        self.fields['user'].initial = user
        self.fields[
            'rating'
        ].help_text = _("Rating should be from 1 to 5 points.")

    def clean_text(self):
        text = self.cleaned_data['text']
        cleaned_text = strip_tags(text)
        return cleaned_text
