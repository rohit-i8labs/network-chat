from celery import shared_task
from datetime import timedelta
from django.utils.timezone import now
from .models import ChatRoom,ChatSession
import uuid

@shared_task
def regenerate_variable_ids():
    """Task to regenerate variable IDs and update expiry times for chat rooms."""
    rooms = ChatRoom.objects.all()
    for room in rooms:
        room.variable_id = uuid.uuid4()
        # Set expiry to 1 day from now (adjust as needed)
        room.variable_id_expiry = now() + timedelta(days=1)
        room.save()