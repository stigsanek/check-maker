import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'check_maker.settings')

app = Celery('check_maker')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
