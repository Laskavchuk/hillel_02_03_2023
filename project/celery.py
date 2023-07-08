import os
# from time import sleep

from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

app = Celery('project')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()


# @app.task(bind=True, default_retry_delay=5)
# def debug_task(self, x, y):
#     try:
#         x['key']
#     except KeyError as err:
#         raise self.retry(exc=err)
#     print(f'Request: {self.request!r}')
#
#
#
# @app.task(bind=True,)
# def debug_task(self):
#     sleep(5)
#     print(f'Request: {self.request!r}')
