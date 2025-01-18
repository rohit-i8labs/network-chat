from django_celery_beat.models import PeriodicTask, IntervalSchedule
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Restaurant
from .tasks import update_var_id
import json

@receiver(post_save, sender=Restaurant)
def schedule_var_id_update(sender, instance, created, **kwargs):
    """
    Schedule a Celery Beat periodic task for updating var_id when a Restaurant is created.
    """
    if created:
        # For testing: Use a fixed 10-second interval
        interval, created = IntervalSchedule.objects.get_or_create(
            every=10,  # 10 seconds for testing
            period=IntervalSchedule.SECONDS,
        )

        # Create a periodic task for this Restaurant
        PeriodicTask.objects.create(
            interval=interval,
            name=f"Update var_id for {instance.name} (ID {instance.id})",
            task='chat.tasks.update_var_id',  # Task to run
            args=json.dumps([instance.id]),  # Pass the Restaurant instance ID
        )


# # signals.py
# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from django_celery_beat.models import PeriodicTask, IntervalSchedule
# from .models import Restaurant
# from .tasks import update_var_id
# import json

# @receiver(post_save, sender=Restaurant)
# def schedule_var_id_update(sender, instance, created, **kwargs):
#     """
#     Schedule a Celery Beat periodic task for updating var_id when a Restaurant is created.
#     """
#     if created:
#         # Create or get the interval schedule based on qr_gen_frequency
#         qr_hours = dict(Restaurant.QR_GEN_FREQUENCY_CHOICES)[instance.qr_gen_frequency]
#         interval, created = IntervalSchedule.objects.get_or_create(
#             every=qr_hours,
#             period=IntervalSchedule.HOURS,
#         )

#         # Create a periodic task for this Restaurant
#         PeriodicTask.objects.create(
#             interval=interval,
#             name=f"Update var_id for {instance.name} (ID {instance.id})",
#             task='chat.tasks.update_var_id',
#             args=json.dumps([instance.id]),
#         )
