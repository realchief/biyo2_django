from datetime import datetime
from order.models import OrderItem
from django.db.models.signals import post_save,pre_save

def save_change_void(sender, instance, **kwargs):

    if instance.void_status == 1:
        instance.voided_at = datetime.now()

pre_save.connect(save_change_void, sender=OrderItem)
