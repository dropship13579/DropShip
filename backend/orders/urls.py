# backend/orders/urls.py
from django.urls import path
from .views import (
    CheckoutView,
    OrderListView,
    OrderDetailView,
    CouponValidateView,
    PublicOrderTrackView,
)

app_name = "orders"

urlpatterns = [
    path("checkout/", CheckoutView.as_view(), name="checkout"),
    path("coupons/validate/", CouponValidateView.as_view(), name="coupon-validate"),
    path("track/", PublicOrderTrackView.as_view(), name="order-track-public"),
    path("", OrderListView.as_view(), name="order-list"),
    path("<str:order_number>/", OrderDetailView.as_view(), name="order-detail"),
]
