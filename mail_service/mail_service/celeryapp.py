import os

from django.conf import settings

from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mail_service.settings')

app = Celery('mail_service')

app.config_from_object('django.conf:settings')

app.autodiscover_tasks(settings.INSTALLED_APPS)
app.conf.task_track_started = True
app.conf.task_ignore_result = False


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print('Request: {}'.format(self.request))
