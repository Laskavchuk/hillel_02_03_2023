from django.core.mail import send_mail

from main.models import Config
from project.celery import app


@app.task
def send_contact_form(email, text):
    config = Config.load()
    send_mail(
        'Contact form', f'From: {email}\n{text}',
        None, [config.contact_form_email], fail_silently=False
    )
