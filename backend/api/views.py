from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, ValidationError, APIException
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.conf import settings
import logging
import requests
import base64
from datetime import datetime
from product.models import Product, VendorProduct
from payment.models import Payment
from subscription.models import SubscriptionBox, ScheduledItem
from orders.models import Order, OrderItem
from cart.models import Cart, CartItem
from users.models import User
from .serializers import  ProductSerializer, VendorProductSerializer, PaymentSerializer, OrderSerializer,OrderItemSerializer, SubscriptionBoxSerializer, ScheduledItemSerializer, UserSerializer, CartSerializer, CartItemSerializer

from .access_token import generate_access_token
from .utils import timestamp_conversation
from .encode_base64 import generate_password

logger = logging.getLogger(__name__)

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class VendorProductViewSet(viewsets.ModelViewSet):
    queryset = VendorProduct.objects.all()
    serializer_class = VendorProductSerializer

    def perform_create(self, serializer):
        serializer.save()

    def perform_update(self, serializer):
        serializer.save()

class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

class SubscriptionBoxViewSet(viewsets.ModelViewSet):
    queryset = SubscriptionBox.objects.all()
    serializer_class = SubscriptionBoxSerializer
class ScheduledItemViewSet(viewsets.ModelViewSet):
    queryset = ScheduledItem.objects.all()
    serializer_class = ScheduledItemSerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all().order_by('-order_date')
    serializer_class = OrderSerializer
    def get_queryset(self):
        user_id = self.request.query_params.get('user_id')
        qs = self.queryset
        if user_id:
            qs = qs.filter(buyer__user_id=user_id)
        return qs
class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class=OrderItemSerializer
    def get_queryset(self):
        order_id = self.request.query_params.get('order')
        qs = self.queryset
        if order_id:
            qs = qs.filter(order_id=order_id)
        return qs


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['type']
    search_fields = ['name', 'phone_number', 'location', 'shop_name']

class CartItemViewSet(viewsets.ModelViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        customer_name = self.request.data.get('customer_name') or self.request.query_params.get('customer_name')
        cart = None
        if customer_name:
            try:
                user = User.objects.get(name=customer_name, type='customer')
                cart, _ = Cart.objects.get_or_create(customer=user)
            except User.DoesNotExist:
                raise NotFound(f"Customer with name '{customer_name}' not found or not a customer.")
        context['cart'] = cart
        return context

class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [AllowAny]

    @action(detail=False, methods=['get'], url_path='by-customer')
    def get_cart_by_customer(self, request):
        customer_name = request.query_params.get('customer_name')
        if not customer_name:
            return Response(
                {"error": "customer_name query parameter is required"},
                status=400
            )
        try:
            user = User.objects.get(name=customer_name, type='customer')
        except User.DoesNotExist:
            raise NotFound(f"Customer with name '{customer_name}' not found or not a customer.")
        except User.MultipleObjectsReturned:
            raise ValidationError(
                f"Multiple customers found with name '{customer_name}'. Please use a unique identifier."
            )
        cart, created = Cart.objects.get_or_create(customer=user)
        serializer = self.get_serializer(cart)
        return Response(serializer.data, status=200)

class MPesaAPIException(APIException):
    status_code = 502
    default_detail = "Failed to connect to M-Pesa API."
    default_code = "mpesa_api_error"

class TestView(APIView):
    def get(self, request, format=None):
        access_token = generate_access_token()
        formatted_time = timestamp_conversation()
        decoded_password = generate_password(formatted_time)
        return Response({
            "access_token": access_token,
            "decoded_password": decoded_password
        }, status=status.HTTP_200_OK)

class MakePayment(APIView):
    def post(self, request, *args, **kwargs):
        amount = request.data.get("amount")
        phone_number = request.data.get("phone_number")
        order_id = request.data.get("order_id")

        if not amount or not phone_number or not order_id:
            return Response(
                {"error": "Amount, phone_number, and order_id are required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            order = Order.objects.get(order_id=order_id)
            if float(order.total_price) != float(amount):
                return Response(
                    {"error": "Amount does not match order total_price"},
                    status=status.HTTP_400_BAD_REQUEST
                )
        except ObjectDoesNotExist:
            return Response(
                {"error": f"Order with ID {order_id} not found"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            with transaction.atomic():
                payment_response_data = self.make_mpesa_payment_request(str(amount), str(phone_number))
                
                payment_data = {
                    "order": order.order_id,
                    "amount": amount,
                    "phone_number": phone_number,
                    "status": "pending",
                    "method": "M-Pesa",
                    "merchant_request_id": payment_response_data.get("MerchantRequestID"),
                    "checkout_request_id": payment_response_data.get("CheckoutRequestID"),
                }
                payment_serializer = PaymentSerializer(data=payment_data)
                if payment_serializer.is_valid():
                    payment_serializer.save()
                    logger.info(f"Initial payment record created: {payment_data}")
                else:
                    logger.error(f"Payment serializer errors: {payment_serializer.errors}")
                    return Response(
                        {"error": "Failed to save initial payment", "details": payment_serializer.errors},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                return Response(payment_response_data, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error("Payment request failed: %s", e, exc_info=True)
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def make_mpesa_payment_request(self, amount: str, phone: str) -> dict:
        try:
            access_token = generate_access_token()
            shortcode = '174379'
            passkey = settings.LIPANAMPESA_SHORTCODE
            timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
            password = base64.b64encode(f"{shortcode}{passkey}{timestamp}".encode()).decode()

            headers = {
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json"
            }
            payload = {
                "BusinessShortCode": settings.BUSINESS_SHORT_CODE,
                "Password": password,
                "Timestamp": timestamp,
                "TransactionType": settings.TRANSACTION_TYPE,
                "Amount": amount,
                "PartyA": '254713616003',
                "PartyB": '254713616003',
                "PhoneNumber": '254713616003',
                "CallBackURL": settings.CALL_BACK_URL,
                "AccountReference": settings.ACCOUNT_REFERENCE,
                "TransactionDesc": settings.TRANSACTION_DESCRIPTION
            }

            logger.info("Sending M-Pesa payment request: %s", payload)
            response = requests.post(
                settings.API_RESOURCE_URL,
                json=payload,
                headers=headers,
                timeout=30
            )
            logger.info("M-Pesa API response status: %s", response.status_code)
            logger.info("M-Pesa API response body: %s", response.text)
            response.raise_for_status()
            return response.json()
        except requests.HTTPError as e:
            logger.error("HTTP error: %s, Response: %s", e, response.text)
            raise MPesaAPIException(f"HTTP error: {e}, Response: {response.text}")
        except requests.RequestException as e:
            logger.exception("M-Pesa API connection failed")
            raise MPesaAPIException("Failed to connect to M-Pesa API. Reason: " + str(e))
        except Exception as e:
            logger.exception("Unexpected error during M-Pesa payment request")
            raise MPesaAPIException("Unexpected error: " + str(e))

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime
import logging

from payment.models import Payment
from .serializers import PaymentSerializer

logger = logging.getLogger(__name__)

class STKPushCallbackView(APIView):
    def post(self, request, *args, **kwargs):
        logger.info(f"Raw request body: {request.body}")
        callback_data = request.data
        logger.info(f"Parsed request data: {callback_data}")

        try:
            if "Body" not in callback_data or "stkCallback" not in callback_data["Body"]:
                logger.error(f"Invalid callback data structure: {callback_data}")
                return Response(
                    {"error": "Invalid callback data structure"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            stk_callback = callback_data["Body"]["stkCallback"]
            result_code = stk_callback.get("ResultCode")
            result_desc = stk_callback.get("ResultDesc")
            merchant_request_id = stk_callback.get("MerchantRequestID")
            checkout_request_id = stk_callback.get("CheckoutRequestID")

            payment_data = {
                "merchant_request_id": merchant_request_id,
                "checkout_request_id": checkout_request_id,
                "result_code": result_code,
                "result_desc": result_desc,
            }

            if result_code == 0:
                callback_metadata = stk_callback.get("CallbackMetadata", {}).get("Item", [])
                for item in callback_metadata:
                    name = item.get("Name")
                    value = item.get("Value")
                    if name == "Amount":
                        payment_data["amount"] = value
                    elif name == "MpesaReceiptNumber":
                        payment_data["mpesa_receipt_number"] = value
                    elif name == "PhoneNumber":
                        payment_data["phone_number"] = value
                    elif name == "TransactionDate":
                        payment_data["transaction_date"] = parse_mpesa_date(value)

                payment_data["status"] = "success"
                logger.info(f"Payment successful: {payment_data}")
            else:
                payment_data["status"] = "failed"
                logger.warning(f"Payment failed: {result_desc} (ResultCode: {result_code})")

            try:
                with transaction.atomic():
                    payment = Payment.objects.get(checkout_request_id=checkout_request_id)
                    if payment_data.get("amount") and float(payment_data["amount"]) != float(payment.order.total_price):
                        logger.error(f"Amount mismatch: {payment_data['amount']} vs {payment.order.total_price}")
                        return Response(
                            {"error": "Amount in callback does not match order total_price"},
                            status=status.HTTP_400_BAD_REQUEST
                        )

                    payment_serializer = PaymentSerializer(payment, data=payment_data, partial=True)
                    if payment_serializer.is_valid():
                        payment = payment_serializer.save()
                        logger.info(f"Payment record updated: {payment_data}")

                        if payment_data["status"] == "success":
                            order = payment.order
                            if order.status == "pending":
                                order.status = "paid"
                                order.save()
                                logger.info(f"Order {order.order_id} updated to paid status")
                            else:
                                logger.warning(f"Order {order.order_id} already processed with status: {order.status}")
                    else:
                        logger.error(f"Payment serializer errors: {payment_serializer.errors}")
                        return Response(
                            {"error": "Failed to update payment", "details": payment_serializer.errors},
                            status=status.HTTP_400_BAD_REQUEST
                        )
            except ObjectDoesNotExist:
                logger.error(f"No payment found for CheckoutRequestID: {checkout_request_id}")
                return Response(
                    {"error": f"No payment found for CheckoutRequestID: {checkout_request_id}"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            return Response(
                {"status": "success", "message": "Callback processed successfully"},
                status=status.HTTP_200_OK
            )

        except Exception as e:
            logger.error(f"Unhandled exception during callback processing: {str(e)}", exc_info=True)
            return Response(
                {"error": "Failed to process callback", "details": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
def parse_mpesa_date(date_str):
    try:
        return datetime.strptime(str(date_str), '%Y%m%d%H%M%S')
    except ValueError:
        logger.error(f"Invalid transaction date format: {date_str}")
        return None

def payment_view(request):
    return JsonResponse({'message': 'Payments endpoint'})

class ApiRootView(APIView):
    def get(self, request, *args, **kwargs):
        return Response({
            "message": "API root. Available endpoints: /payment/, /test/, /make-payment/, /stkpush-callback/"
        }, status=status.HTTP_200_OK)