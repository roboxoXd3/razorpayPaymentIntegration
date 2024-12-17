from django.db import models

# Create your models here.
class Transaction(models.Model):
    order_id = models.CharField(max_length=255, verbose_name="Order ID")
    payment_id = models.CharField(max_length=255, verbose_name="Payment ID")
    signature = models.CharField(max_length=255, verbose_name="Signature")
    amount = models.IntegerField(verbose_name="Amount")
    datetime = models.DateTimeField(auto_now_add=True)
    # currency = models.CharField(max_length=255, verbose_name="Currency")
    # status = models.CharField(max_length=255, verbose_name="Status")

    def __str__(self):
        return f"{self.order_id} - {self.payment_id} - {self.amount} - {self.datetime}"
