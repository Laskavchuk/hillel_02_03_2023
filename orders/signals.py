# from django.db.models.signals import post_save
# from django.dispatch import receiver
#
# from orders.models import Order
#
#
# @receiver(post_save, sender=Order)
# def post_save_order_signal(sender, instance, **kwargs):
#     total_amount = instance.get_total_amount()
#     Order.objects.filter(id=instance.id).update(total_amount=total_amount)
