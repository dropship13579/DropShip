# backend/dashboard/views.py
from datetime import timedelta
from decimal import Decimal

from django.utils import timezone
from django.db.models import Sum, Count, Q
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User

from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser

from orders.models import Order
from products.models import Product, ProductImage, Category, Supplier
from accounts.models import SupportTicket, NewsletterSubscriber
from orders.serializers import OrderSerializer
from products.serializers import SupplierSerializer, ProductSourcingSerializer
from accounts.serializers import SupportTicketSerializer



class AdminDashboardStatsView(APIView):
    """
    GET /api/admin/stats/
    Comprehensive operational metrics and status charts for the entire website.
    """
    permission_classes = [permissions.IsAdminUser]
    def get(self, request):
        now = timezone.now()
        thirty_days_ago = now - timedelta(days=30)
        # 1. Revenue & Average Order Value
        valid_orders = Order.objects.exclude(order_status="cancelled")
        total_revenue = valid_orders.aggregate(total=Sum("total_amount"))["total"] or Decimal("0.00")
        monthly_revenue = valid_orders.filter(created_at__gte=thirty_days_ago).aggregate(
            total=Sum("total_amount")
        )["total"] or Decimal("0.00")
        total_orders_count = Order.objects.count()
        valid_orders_count = valid_orders.count()
        avg_order_value = (
            round(float(total_revenue) / valid_orders_count, 2)
            if valid_orders_count > 0
            else 0.00
        )
        # 2. 7-Day Revenue Trend
        daily_sales = []
        for i in range(6, -1, -1):
            day_start = (now - timedelta(days=i)).replace(hour=0, minute=0, second=0, microsecond=0)
            day_end = day_start + timedelta(days=1)
            day_total = valid_orders.filter(
                created_at__gte=day_start,
                created_at__lt=day_end
            ).aggregate(total=Sum("total_amount"))["total"] or Decimal("0.00")
            daily_sales.append({
                "date": day_start.strftime("%b %d"),
                "total": float(day_total),
            })
        # 3. Order Status Distribution (for charts)
        status_counts = Order.objects.values("order_status").annotate(count=Count("id"))
        status_map = {item["order_status"]: item["count"] for item in status_counts}
        total_safe_orders = total_orders_count if total_orders_count > 0 else 1
        order_status_distribution = [
            {
                "status": "pending",
                "label": "Pending",
                "count": status_map.get("pending", 0),
                "pct": round((status_map.get("pending", 0) / total_safe_orders) * 100, 1),
                "color": "#f59e0b",
            },
            {
                "status": "confirmed",
                "label": "Confirmed",
                "count": status_map.get("confirmed", 0),
                "pct": round((status_map.get("confirmed", 0) / total_safe_orders) * 100, 1),
                "color": "#0ea5e9",
            },
            {
                "status": "processing",
                "label": "Processing",
                "count": status_map.get("processing", 0),
                "pct": round((status_map.get("processing", 0) / total_safe_orders) * 100, 1),
                "color": "#8b5cf6",
            },
            {
                "status": "shipped",
                "label": "Shipped",
                "count": status_map.get("shipped", 0),
                "pct": round((status_map.get("shipped", 0) / total_safe_orders) * 100, 1),
                "color": "#ec4899",
            },
            {
                "status": "delivered",
                "label": "Delivered",
                "count": status_map.get("delivered", 0),
                "pct": round((status_map.get("delivered", 0) / total_safe_orders) * 100, 1),
                "color": "#10b981",
            },
            {
                "status": "cancelled",
                "label": "Cancelled",
                "count": status_map.get("cancelled", 0),
                "pct": round((status_map.get("cancelled", 0) / total_safe_orders) * 100, 1),
                "color": "#ef4444",
            },
        ]
        # 4. Inventory Health Distribution
        total_products = Product.objects.count()
        total_safe_prods = total_products if total_products > 0 else 1
        in_stock_count = Product.objects.filter(stock_quantity__gt=5, is_active=True).count()
        low_stock_count = Product.objects.filter(stock_quantity__gt=0, stock_quantity__lte=5, is_active=True).count()
        out_of_stock_count = Product.objects.filter(stock_quantity=0, is_active=True).count()
        inventory_health = {
            "total_products": total_products,
            "in_stock": in_stock_count,
            "in_stock_pct": round((in_stock_count / total_safe_prods) * 100, 1),
            "low_stock": low_stock_count,
            "low_stock_pct": round((low_stock_count / total_safe_prods) * 100, 1),
            "out_of_stock": out_of_stock_count,
            "out_of_stock_pct": round((out_of_stock_count / total_safe_prods) * 100, 1),
        }
        # 5. Category Balance Distribution
        categories_breakdown = []
        for cat in Category.objects.annotate(prod_count=Count("products")).all():
            categories_breakdown.append({
                "id": cat.id,
                "name": cat.name,
                "count": cat.prod_count,
                "pct": round((cat.prod_count / total_safe_prods) * 100, 1),
            })
        # 6. Customers & System Information
        total_customers = User.objects.filter(is_staff=False).count()
        try:
            total_open_tickets = SupportTicket.objects.filter(status="open").count()
        except Exception:
            total_open_tickets = 0

        try:
            total_subscribers = NewsletterSubscriber.objects.filter(is_active=True).count()
        except Exception:
            total_subscribers = 0
        return Response({
            "revenue": {
                "total": float(total_revenue),
                "monthly": float(monthly_revenue),
                "aov": avg_order_value,
            },
            "orders": {
                "total": total_orders_count,
                "valid": valid_orders_count,
                "distribution": order_status_distribution,
            },
            "inventory": inventory_health,
            "categories": categories_breakdown,
            "customers": {
                "total": total_customers,
            },
            "support": {
                "open_tickets": total_open_tickets,
                "total_subscribers": total_subscribers,
            },
            "daily_sales": daily_sales,
            "system": {
                "api_status": "Operational",
                "db_engine": "MySQL (InnoDB)",
                "django_version": "5.2",
                "server_time": timezone.now().strftime("%Y-%m-%d %H:%M UTC"),
            },
        })


class AdminOrdersListView(APIView):
    """
    GET /api/admin/orders/?status=pending&search=ORD-123
    Lists all orders with optional search and status filtering.
    """
    permission_classes = [permissions.IsAdminUser]

    def get(self, request):
        queryset = Order.objects.prefetch_related("items__product").order_by("-created_at")

        # Filter by status
        status_filter = request.query_params.get("status")
        if status_filter:
            queryset = queryset.filter(order_status=status_filter)

        # Filter by payment status
        payment_filter = request.query_params.get("payment_status")
        if payment_filter:
            queryset = queryset.filter(payment_status=payment_filter)

        # Search query (order number, customer username, recipient name)
        search = request.query_params.get("search")
        if search:
            queryset = queryset.filter(
                Q(order_number__icontains=search) |
                Q(user__username__icontains=search) |
                Q(user__email__icontains=search) |
                Q(shipping_address_snapshot__recipient_name__icontains=search)
            )

        serializer = OrderSerializer(queryset, many=True)
        return Response(serializer.data)


class AdminOrderDetailUpdateView(APIView):
    """
    GET /api/admin/orders/<order_number>/
    PATCH /api/admin/orders/<order_number>/
    Retrieve and update order fulfillment, payment status, and tracking number.
    """
    permission_classes = [permissions.IsAdminUser]

    def get(self, request, order_number):
        order = get_object_or_404(
            Order.objects.prefetch_related("items__product"),
            order_number=order_number
        )
        return Response(OrderSerializer(order).data)

    def patch(self, request, order_number):
        order = get_object_or_404(Order, order_number=order_number)

        allowed_fields = ["order_status", "payment_status", "tracking_number"]
        updated = False

        for field in allowed_fields:
            if field in request.data:
                setattr(order, field, request.data[field])
                updated = True

        if updated:
            order.save()

        fresh_order = Order.objects.prefetch_related("items__product").get(pk=order.pk)
        return Response(OrderSerializer(fresh_order).data)


class AdminProductsListView(APIView):
    """
    GET /api/admin/products/ - Full product inventory list with gallery images for staff.
    POST /api/admin/products/ - Create new product with several uploaded images.
    """
    permission_classes = [permissions.IsAdminUser]
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def get(self, request):
        products = Product.objects.select_related("category").prefetch_related("images").order_by("-created_at")
        data = []
        for p in products:
            gallery_urls = [request.build_absolute_uri(img.image.url) for img in p.images.all() if img.image]
            data.append({
                "id": p.id,
                "name": p.name,
                "slug": p.slug,
                "category_id": p.category_id,
                "category_name": p.category.name if p.category else "Uncategorized",
                "image": request.build_absolute_uri(p.image.url) if p.image else (gallery_urls[0] if gallery_urls else None),
                "images": gallery_urls,
                "current_price": float(p.current_price),
                "original_price": float(p.original_price) if p.original_price else None,
                "supplier_cost": float(p.supplier_cost) if p.supplier_cost else 0.0,
                "supplier_sku": p.supplier_sku,
                "stock_quantity": p.stock_quantity,
                "description": p.description,
                "is_active": p.is_active,
                "is_featured": p.is_featured,
            })
        return Response(data)

    def post(self, request):
        name = request.data.get("name")
        if not name:
            return Response({"error": "Product name is required."}, status=status.HTTP_400_BAD_REQUEST)

        current_price = request.data.get("current_price")
        if current_price is None:
            return Response({"error": "Current price is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            current_price_dec = Decimal(str(current_price))
        except Exception:
            return Response({"error": "Invalid current price format."}, status=status.HTTP_400_BAD_REQUEST)

        original_price = request.data.get("original_price")
        original_price_dec = None
        if original_price:
            try:
                original_price_dec = Decimal(str(original_price))
            except Exception:
                pass

        supplier_cost = request.data.get("supplier_cost")
        supplier_cost_dec = Decimal("0.00")
        if supplier_cost:
            try:
                supplier_cost_dec = Decimal(str(supplier_cost))
            except Exception:
                pass

        stock_quantity = int(request.data.get("stock_quantity", 0))
        description = request.data.get("description", "")
        supplier_sku = request.data.get("supplier_sku", "")
        
        is_active = request.data.get("is_active", True)
        if isinstance(is_active, str):
            is_active = is_active.lower() in ("true", "1", "yes")

        is_featured = request.data.get("is_featured", False)
        if isinstance(is_featured, str):
            is_featured = is_featured.lower() in ("true", "1", "yes")

        category_id = request.data.get("category") or request.data.get("category_id")
        category = None
        if category_id:
            try:
                category = Category.objects.filter(pk=category_id).first()
            except Exception:
                pass

        # Check for images: single cover image and/or list of images
        single_image = request.FILES.get("image")
        uploaded_images = request.FILES.getlist("images")

        product = Product(
            name=name,
            current_price=current_price_dec,
            original_price=original_price_dec,
            supplier_cost=supplier_cost_dec,
            supplier_sku=supplier_sku,
            stock_quantity=stock_quantity,
            description=description,
            category=category,
            is_active=is_active,
            is_featured=is_featured,
        )

        if single_image:
            product.image = single_image
        elif uploaded_images:
            product.image = uploaded_images[0]

        product.save()

        # Save all uploaded images to ProductImage gallery
        order_idx = 0
        if single_image:
            ProductImage.objects.create(
                product=product,
                image=single_image,
                alt_text=f"{product.name} primary",
                order=order_idx
            )
            order_idx += 1

        for img_file in uploaded_images:
            if single_image and img_file.name == single_image.name:
                continue
            ProductImage.objects.create(
                product=product,
                image=img_file,
                alt_text=f"{product.name} photo {order_idx + 1}",
                order=order_idx
            )
            order_idx += 1

        # Return fresh data
        fresh = Product.objects.select_related("category", "supplier").prefetch_related("images").get(pk=product.pk)
        gallery_urls = [request.build_absolute_uri(img.image.url) for img in fresh.images.all() if img.image]

        return Response({
            "id": fresh.id,
            "name": fresh.name,
            "slug": fresh.slug,
            "category_id": fresh.category_id,
            "category_name": fresh.category.name if fresh.category else "Uncategorized",
            "image": request.build_absolute_uri(fresh.image.url) if fresh.image else (gallery_urls[0] if gallery_urls else None),
            "images": gallery_urls,
            "current_price": float(fresh.current_price),
            "original_price": float(fresh.original_price) if fresh.original_price else None,
            "supplier_cost": float(fresh.supplier_cost),
            "stock_quantity": fresh.stock_quantity,
            "is_active": fresh.is_active,
            "is_featured": fresh.is_featured,
        }, status=status.HTTP_201_CREATED)


class AdminProductQuickUpdateView(APIView):
    """
    PATCH /api/admin/products/<int:pk>/ - Quick update stock, price, or visibility.
    DELETE /api/admin/products/<int:pk>/ - Delete a product.
    """
    permission_classes = [permissions.IsAdminUser]

    def patch(self, request, pk):
        product = get_object_or_404(Product, pk=pk)

        if "stock_quantity" in request.data:
            product.stock_quantity = max(0, int(request.data["stock_quantity"]))
        if "current_price" in request.data:
            product.current_price = Decimal(str(request.data["current_price"]))
        if "is_active" in request.data:
            product.is_active = bool(request.data["is_active"])
        if "is_featured" in request.data:
            product.is_featured = bool(request.data["is_featured"])

        product.save()

        return Response({
            "id": product.id,
            "name": product.name,
            "stock_quantity": product.stock_quantity,
            "current_price": float(product.current_price),
            "is_active": product.is_active,
            "is_featured": product.is_featured,
        })

    def delete(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        product_name = product.name
        product.delete()
        return Response({"message": f"Product '{product_name}' deleted successfully."}, status=status.HTTP_200_OK)


class AdminSupplierListCreateView(APIView):
    """
    GET /api/admin/suppliers/
    POST /api/admin/suppliers/
    List all dropship suppliers or register a new supplier.
    """
    permission_classes = [permissions.IsAdminUser]
    def get(self, request):
        suppliers = Supplier.objects.annotate(prod_count=Count("products")).order_by("name")
        data = []
        for s in suppliers:
            data.append({
                "id": s.id,
                "name": s.name,
                "contact_name": s.contact_name,
                "email": s.email,
                "website_url": s.website_url,
                "average_shipping_days": s.average_shipping_days,
                "notes": s.notes,
                "is_active": s.is_active,
                "products_count": s.prod_count,
                "created_at": s.created_at,
            })
        return Response(data)
    def post(self, request):
        serializer = SupplierSerializer(data=request.data)
        if serializer.is_valid():
            supplier = serializer.save()
            return Response(SupplierSerializer(supplier).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class AdminSupplierDetailView(APIView):
    """
    GET /api/admin/suppliers/<int:pk>/
    PATCH /api/admin/suppliers/<int:pk>/
    DELETE /api/admin/suppliers/<int:pk>/
    """
    permission_classes = [permissions.IsAdminUser]
    def get(self, request, pk):
        supplier = get_object_or_404(Supplier, pk=pk)
        return Response(SupplierSerializer(supplier).data)
    def patch(self, request, pk):
        supplier = get_object_or_404(Supplier, pk=pk)
        serializer = SupplierSerializer(supplier, data=request.data, partial=True)
        if serializer.is_valid():
            updated = serializer.save()
            return Response(SupplierSerializer(updated).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def delete(self, request, pk):
        supplier = get_object_or_404(Supplier, pk=pk)
        supplier.delete()
        return Response({"detail": "Supplier removed successfully."}, status=status.HTTP_204_NO_CONTENT)
class AdminProductSourcingListView(APIView):
    """
    GET /api/admin/suppliers/sourcing/
    Returns products sourcing roster with profit margins, net profits, and portfolio analytics.
    """
    permission_classes = [permissions.IsAdminUser]
    def get(self, request):
        queryset = Product.objects.select_related("category", "supplier").order_by("-created_at")
        supplier_filter = request.query_params.get("supplier")
        if supplier_filter:
            queryset = queryset.filter(supplier_id=supplier_filter)
        search = request.query_params.get("search")
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(supplier_sku__icontains=search) |
                Q(supplier__name__icontains=search)
            )
        products_data = ProductSourcingSerializer(queryset, many=True, context={"request": request}).data
        # Calculate portfolio aggregates
        all_prods = Product.objects.filter(is_active=True)
        total_prods = all_prods.count()
        margins = [p.profit_margin_percentage for p in all_prods if p.profit_margin_percentage is not None]
        avg_margin = round(sum(margins) / len(margins), 1) if margins else 0.0
        total_potential_profit = sum(
            float(p.net_profit) * p.stock_quantity for p in all_prods
        )
        suppliers = Supplier.objects.annotate(p_count=Count("products")).all()
        distribution = [
            {"id": s.id, "name": s.name, "count": s.p_count} for s in suppliers
        ]
        return Response({
            "products": products_data,
            "analytics": {
                "total_products": total_prods,
                "average_margin": avg_margin,
                "total_potential_profit": round(total_potential_profit, 2),
                "supplier_distribution": distribution,
            }
        })
class AdminProductSourcingUpdateView(APIView):
    """
    PATCH /api/admin/suppliers/sourcing/<int:pk>/
    Inline quick-edit of supplier, wholesale cost, and SKU.
    """
    permission_classes = [permissions.IsAdminUser]
    def patch(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        if "supplier_id" in request.data:
            s_id = request.data["supplier_id"]
            product.supplier_id = s_id if s_id else None
        if "supplier_cost" in request.data:
            try:
                product.supplier_cost = max(Decimal("0.00"), Decimal(str(request.data["supplier_cost"])))
            except Exception:
                pass
        if "supplier_sku" in request.data:
            product.supplier_sku = str(request.data["supplier_sku"]).strip()
        if "current_price" in request.data:
            try:
                product.current_price = Decimal(str(request.data["current_price"]))
            except Exception:
                pass
        product.save()
        fresh = Product.objects.select_related("category", "supplier").get(pk=product.pk)
        return Response(ProductSourcingSerializer(fresh, context={"request": request}).data)


class AdminSupportTicketListView(APIView):
    """
    GET /api/admin/support/?status=open&inquiry_type=product&search=ORD-123
    Lists customer support tickets and inquiries for staff with operational metrics.
    """
    permission_classes = [permissions.IsAdminUser]

    def get(self, request):
        queryset = SupportTicket.objects.select_related("user").order_by("-created_at")

        status_filter = request.query_params.get("status")
        if status_filter:
            queryset = queryset.filter(status=status_filter)

        inquiry_type = request.query_params.get("inquiry_type")
        if inquiry_type:
            queryset = queryset.filter(inquiry_type=inquiry_type)

        search_query = request.query_params.get("search", "").strip()
        if search_query:
            queryset = queryset.filter(
                Q(ticket_number__icontains=search_query)
                | Q(name__icontains=search_query)
                | Q(email__icontains=search_query)
                | Q(subject__icontains=search_query)
                | Q(order_number__icontains=search_query)
                | Q(product_name__icontains=search_query)
            )

        # Meta counters for quick tabs
        all_count = SupportTicket.objects.count()
        open_count = SupportTicket.objects.filter(status="open").count()
        in_progress_count = SupportTicket.objects.filter(status="in_progress").count()
        resolved_count = SupportTicket.objects.filter(status="resolved").count()

        serializer = SupportTicketSerializer(queryset, many=True)
        return Response({
            "tickets": serializer.data,
            "counts": {
                "all": all_count,
                "open": open_count,
                "in_progress": in_progress_count,
                "resolved": resolved_count,
            }
        })


class AdminSupportTicketDetailUpdateView(APIView):
    """
    GET /api/admin/support/<int:pk>/
    PATCH /api/admin/support/<int:pk>/
    Inspect customer ticket details or update status (open, in_progress, resolved).
    """
    permission_classes = [permissions.IsAdminUser]

    def get(self, request, pk):
        ticket = get_object_or_404(SupportTicket, pk=pk)
        return Response(SupportTicketSerializer(ticket).data)

    def patch(self, request, pk):
        ticket = get_object_or_404(SupportTicket, pk=pk)
        new_status = request.data.get("status")
        if new_status and new_status in dict(SupportTicket.STATUS_CHOICES):
            ticket.status = new_status
            ticket.save()
            return Response({
                "message": f"Ticket #{ticket.ticket_number} status updated to {new_status}.",
                "ticket": SupportTicketSerializer(ticket).data
            })
        return Response({"error": "Invalid status choice."}, status=status.HTTP_400_BAD_REQUEST)
