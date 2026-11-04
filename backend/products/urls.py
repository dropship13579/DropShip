from django.urls import path

from .views import (
    ProductListView,
    ProductDetailView,
    ProductReviewLisCreateView,
    ProductReviewDeleteView,
    WishlistView,
    WishlistToggleView
)



urlpatterns = [
    path('', ProductListView.as_view(), name="product-list"),
    path("wishlist/", WishlistView.as_view(), name="wishlist-list"),
    path("wishlist/toggle/", WishlistToggleView.as_view(), name="wishlist-toggle"),
    path('<slug:slug>/reviews/', ProductReviewLisCreateView.as_view(), name="product-reviews"),
    path('<slug:slug>/reviews/<int:pk>/', ProductReviewDeleteView.as_view(), name="product-review-delete"),
    path('<slug:slug>/', ProductDetailView.as_view(), name="product-detail"),
]