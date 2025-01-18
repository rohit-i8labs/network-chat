from celery import shared_task
from datetime import timedelta
from celery.utils.log import get_task_logger
from django.utils.timezone import now  # Import for current time
from .models import Restaurant
import random  # Import for generating random numbers
import string  # Import for string constants

logger = get_task_logger(__name__)

@shared_task
def update_var_id(restaurant_id):
    print("================================================")
    """
    Task to update the var_id, var_id_gen_time, and var_id_expiry_time
    for a Restaurant instance.
    """
    try:
        restaurant = Restaurant.objects.get(id=restaurant_id)

        # Generate new var_id
        def generate_unique_var_id():
            while True:
                var_id = ''.join(random.choices(string.digits, k=6))
                if not Restaurant.objects.filter(var_id=var_id).exists():
                    return var_id

        # Update the Restaurant instance
        restaurant.var_id = generate_unique_var_id()
        restaurant.var_id_gen_time = now()
        qr_hours = dict(Restaurant.QR_GEN_FREQUENCY_CHOICES)[restaurant.qr_gen_frequency]
        restaurant.var_id_expiry_time = restaurant.var_id_gen_time + timedelta(hours=qr_hours)
        restaurant.save()

        logger.info(f"Updated var_id for Restaurant {restaurant.name} to {restaurant.var_id}")
    except Restaurant.DoesNotExist:
        logger.error(f"Restaurant with ID {restaurant_id} does not exist.")
