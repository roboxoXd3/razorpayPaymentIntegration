from .import client
from rest_framework import status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError

class RazorpayClient:
    """
    A client class for interacting with the Razorpay payment gateway.

    This class provides methods to create and manage Razorpay orders for payment processing.
    It uses the Razorpay Python SDK client to communicate with Razorpay's API.

    Usage Example:
    -------------
    # Initialize the client
    razorpay_client = RazorpayClient()
    
    # Create a new order
    order = razorpay_client.create_order(
        amount=299900,    # ₹2,999.00 (amount in paise)
        currency="INR"
    )

    Attributes:
        None - Uses the globally configured Razorpay client
    """

    def create_order(self, amount, currency):
        """
        Creates a new order in Razorpay for payment processing.

        This method creates a new order with the specified amount and currency using
        the Razorpay API. The order can then be used to initiate payment collection
        from the customer.

        Args:
            amount (int): The payment amount in smallest currency unit 
                         (e.g., paise for INR, cents for USD)
            currency (str): The 3-letter currency code (e.g., "INR", "USD")

        Returns:
            dict: The created order details from Razorpay containing:
                - id: The unique order ID
                - entity: Always "order"
                - amount: The order amount
                - currency: The order currency
                - status: The order status
                - other order-related details

        Raises:
            ValidationError: If order creation fails, with details about the error

        Example Response:
            {
                "id": "order_JkVtugqb6axZp8",
                "entity": "order",
                "amount": 299900,
                "currency": "INR",
                "status": "created",
                ...
            }
        """
        data = {
            'amount': amount,
            'currency': currency,
            # 'receipt': receipt,
            # 'notes': notes
        }
        try:
           order_data = client.order.create(data=data)
           return order_data
        except Exception as e:
            print(e)
            raise ValidationError({
                "status_code": status.HTTP_400_BAD_REQUEST,
                "message": "Failed to create order",
                "error": str(e)
            })

    def verify_payment(self, razorpay_payment_id, razorpay_order_id, razorpay_signature):
        """
        Verifies the authenticity of a Razorpay payment using signature verification.

        This method validates that a payment was legitimately processed through Razorpay
        by verifying the cryptographic signature. This is a crucial security step to
        prevent payment tampering.

        Args:
            razorpay_payment_id (str): The unique payment ID from Razorpay
                Example: "pay_29QQoUBi66xm2f"
            razorpay_order_id (str): The order ID for which payment was made
                Example: "order_JkVtugqb6axZp8" 
            razorpay_signature (str): The cryptographic signature from Razorpay
                Example: "9ef4dffbfd84f1318f6739a3ce19f9d85851857ae648f114332d8401e0949a3d"

        Raises:
            ValidationError: If signature verification fails, indicating potential tampering.
                Contains status code, error message and detailed error information.

        Example Usage:
            try:
                client.verify_payment(
                    "pay_29QQoUBi66xm2f",
                    "order_JkVtugqb6axZp8",
                    "9ef4dffbfd84f1318f6739a3ce19f9d85851857ae648f114332d8401e0949a3d"
                )
                # Payment verified successfully
            except ValidationError as e:
                # Handle invalid/tampered payment
                print(e.detail)

        Note:
            - Always verify payments server-side before confirming orders
            - Never skip signature verification as it ensures payment security
            - Store these verification details for audit purposes
        """
        try:
            return client.utility.verify_payment_signature(
                {
                    'razorpay_order_id': razorpay_order_id,
                    'razorpay_payment_id': razorpay_payment_id,
                    'razorpay_signature': razorpay_signature
                }
            )
        except Exception as e:
            print(e)
            raise ValidationError({
                "status_code": status.HTTP_400_BAD_REQUEST,
                "message": "Failed to verify payment",
                "error": str(e)
            })
