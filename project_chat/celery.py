from celery import Celery
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project_chat.settings')

app = Celery('project_chat')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print("==============================")
    print(f"Request: {self.request!r}")