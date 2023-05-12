from project.celery import app
import random
from django.core.cache import cache


@app.task
def send_code_task(user_id):
    code = random.randint(10000, 99999)
    cache.set(f'{str(user_id)}_code', code, 60)
    return code
