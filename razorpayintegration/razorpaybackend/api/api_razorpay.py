from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .razorpay_serializers import CreateOrderSerializer, TransactionModelSerializer
# relative import
from .razorpay.main import RazorpayClient

razorpay_client = RazorpayClient()


class CreateOrderApiView(APIView):
    """
    API View to create a Razorpay order for payment processing.
    
    This view handles the creation of payment orders through Razorpay's payment gateway.
    
    Real-world Example:
    ------------------
    Consider an e-commerce website selling shoes:
    1. A customer adds a pair of shoes worth ₹2999 to their cart
    2. When they click "Buy Now", the frontend makes a POST request to this API with:
       {
           "amount": 299900,    # Amount in paise (₹2999 * 100)
           "currency": "INR"
       }
    3. The API creates a Razorpay order and returns the order details
    4. The frontend uses this order data to show the Razorpay payment modal
    
    Request Format:
    -------------
    POST /api/create-order/
    {
        "amount": 299900,       # Amount in smallest currency unit (paise for INR)
        "currency": "INR"       # Currency code (e.g., INR, USD)
    }
    
    Response Format:
    --------------
    Success (200 OK):
    {
        "id": "order_JkVtugqb6axZp8",
        "entity": "order",
        "amount": 299900,
        "currency": "INR",
        "status": "created",
        ...
    }
    
    Error (400 Bad Request):
    {
        "amount": ["This field is required"],
        "currency": ["Invalid currency specified"]
    }
    """
    
    def post(self, request):
        # Validate the incoming request data using the serializer
        create_order_serializer = CreateOrderSerializer(data=request.data)
        if create_order_serializer.is_valid():
            # Initialize Razorpay client and create the order
            order_response = razorpay_client.create_order(
                amount=create_order_serializer.validated_data.get('amount'),
                currency=create_order_serializer.validated_data.get('currency'),
                # receipt=serializer.validated_data['receipt'],
                # notes=serializer.validated_data['notes']
            )
            return Response({"status_code": status.HTTP_200_OK, "message": "Order created successfully", "data": order_response})
        return Response({"status_code": status.HTTP_400_BAD_REQUEST, "message": "Failed to create order", "error": create_order_serializer.errors})

class TransactionApiView(APIView):
    """
    API View for handling Razorpay transaction records.

    This view allows creating new transaction records in the database after successful
    Razorpay payments. It validates and stores important payment details like order ID,
    payment ID, signature and amount for future reference and reconciliation.

    Endpoint:
    --------
    POST /api/transaction/

    Request Format:
    -------------
    {
        "order_id": "order_JkVtugqb6axZp8",     # Razorpay Order ID
        "payment_id": "pay_29QQoUBi66xm2f",      # Razorpay Payment ID
        "signature": "9ef4dffbfd84f1318f...",    # Razorpay Payment Signature
        "amount": 299900                         # Amount in smallest currency unit
    }

    Response Format:
    --------------
    Success (200 OK):
    {
        "status_code": 200,
        "message": "Transaction created successfully",
        "data": {
            "order_id": "order_JkVtugqb6axZp8",
            "payment_id": "pay_29QQoUBi66xm2f",
            "signature": "9ef4dffbfd84f1318f...",
            "amount": 299900
        }
    }

    Error (400 Bad Request):
    {
        "status_code": 400,
        "message": "Failed to create transaction",
        "error": {
            "order_id": ["This field is required"],
            "payment_id": ["Invalid payment ID format"]
        }
    }

    Note:
    ----
    - All successful Razorpay payments should be recorded using this endpoint
    - The transaction details are stored in the Transaction model
    - Datetime is automatically added when the transaction is created
    """

    def post(self, request):
        transaction_serializer = TransactionModelSerializer(data=request.data)
        if transaction_serializer.is_valid():
            razorpay_client.verify_payment(
            razorpay_payment_id=transaction_serializer.validated_data.get('payment_id'),
            razorpay_order_id=transaction_serializer.validated_data.get('order_id'),
            razorpay_signature=transaction_serializer.validated_data.get('signature')
            )
            transaction_serializer.save()
            return Response({"status_code": status.HTTP_200_OK, "message": "Transaction created successfully", "data": transaction_serializer.data})
        return Response({"status_code": status.HTTP_400_BAD_REQUEST, "message": "Failed to create transaction", "error": transaction_serializer.errors})
