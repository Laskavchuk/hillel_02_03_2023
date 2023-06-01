from django.core.mail import EmailMultiAlternatives

from project.celery import app
import random
from django.core.cache import cache
from django.template import loader
from django.utils.translation import gettext_lazy as _


@app.task
def send_code_task(user_id):
    code = random.randint(10000, 99999)
    cache.set(f'{str(user_id)}_code', code, 60)
    return code


@app.task
def send_registration_email(email_template_name,
                            context,
                            from_email,
                            to_email,
                            html_email_template_name):
    """
           Send a django.core.mail.EmailMultiAlternatives to `to_email`.
           """
    subject = _(f'Registration {context["site_name"]}')
    body = loader.render_to_string(email_template_name, context)

    email_message = EmailMultiAlternatives(subject, body, from_email,
                                           [to_email])
    if html_email_template_name is not None:
        html_email = loader.render_to_string(html_email_template_name, context)
        email_message.attach_alternative(html_email, "text/html")

    email_message.send()
