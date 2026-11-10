# backend/dashboard/urls.py
from django.urls import path
from .views import (
    AdminDashboardStatsView,
    AdminOrdersListView,
    AdminOrderDetailUpdateView,
    AdminProductsListView,
    AdminProductQuickUpdateView,
    AdminSupplierListCreateView,
    AdminSupplierDetailView,
    AdminProductSourcingListView,
    AdminProductSourcingUpdateView,
    AdminSupportTicketListView,
    AdminSupportTicketDetailUpdateView,
)

app_name = "dashboard"

urlpatterns = [
    path("stats/", AdminDashboardStatsView.as_view(), name="admin-stats"),
    path("orders/", AdminOrdersListView.as_view(), name="admin-orders-list"),
    path("orders/<str:order_number>/", AdminOrderDetailUpdateView.as_view(), name="admin-order-detail-update"),
    path("products/", AdminProductsListView.as_view(), name="admin-products-list"),
    path("products/<int:pk>/", AdminProductQuickUpdateView.as_view(), name="admin-product-update"),
    path("suppliers/sourcing/", AdminProductSourcingListView.as_view(), name="admin-product-sourcing-list"),
    path("suppliers/sourcing/<int:pk>/", AdminProductSourcingUpdateView.as_view(), name="admin-product-sourcing-update"),
    path("suppliers/", AdminSupplierListCreateView.as_view(), name="admin-suppliers-list"),
    path("suppliers/<int:pk>/", AdminSupplierDetailView.as_view(), name="admin-supplier-detail"),
    path("support/", AdminSupportTicketListView.as_view(), name="admin-support-list"),
    path("support/<int:pk>/", AdminSupportTicketDetailUpdateView.as_view(), name="admin-support-detail-update"),
]
