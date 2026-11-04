# backend/cart/urls.py
from django.urls import path
from .views import (
    CartDetailView,
    AddToCartView,
    UpdateCartItemView,
    RemoveCartItemView,
    ClearCartView,
)

urlpatterns = [
    path("", CartDetailView.as_view(), name="cart-detail"),
    path("items/", AddToCartView.as_view(), name="cart-add-item"),
    path("items/<int:pk>/", UpdateCartItemView.as_view(), name="cart-update-item"),
    path("items/<int:pk>/remove/", RemoveCartItemView.as_view(), name="cart-remove-item"),
    path("clear/", ClearCartView.as_view(), name="cart-clear"),
]
