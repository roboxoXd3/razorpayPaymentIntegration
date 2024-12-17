from rest_framework import serializers
from razorpaybackend.models import Transaction

class CreateOrderSerializer(serializers.Serializer):
    amount = serializers.IntegerField()
    currency = serializers.CharField()
    # receipt = serializers.CharField()
    # notes = serializers.JSONField()

class TransactionModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['order_id', 'payment_id', 'signature', 'amount']
