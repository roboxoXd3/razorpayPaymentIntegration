import razorpay
from django.conf import settings

# add the reson in documentation

client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
