"""
URL Configuration for Razorpay Payment Integration API

This module defines the URL patterns for the Razorpay payment integration API endpoints.
Each URL pattern maps to a specific API view that handles payment-related functionality.

Available Endpoints:
------------------
1. /api/create-order/ (name: 'create-order')
   - Handled by: CreateOrderApiView
   - Method: POST
   - Purpose: Creates a new Razorpay order for payment processing
   - Request Format:
     {
         "amount": 299900,    # Amount in smallest currency unit (e.g., paise for INR)
         "currency": "INR"    # Currency code
     }
   - Response: Returns order details from Razorpay including order ID and status

Usage Example:
-------------
To create a new order for ₹2999:
1. Send POST request to: http://your-domain.com/api/create-order/
2. With payload:
   {
       "amount": 299900,
       "currency": "INR"
   }
3. Use the returned order ID to initialize Razorpay payment on frontend

Note: Ensure that Razorpay credentials are properly configured in settings.py
"""

from django.urls import path
from .api_razorpay import CreateOrderApiView, TransactionApiView

urlpatterns = [
    path('create-order/', CreateOrderApiView.as_view(), name='create-order_api' ), 
    path('order-complete/', TransactionApiView.as_view(), name='order-complete_api' ),
]
