from decimal import Decimal

from django.db.models import F, Q, Count
from django.shortcuts import get_object_or_404

from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response

from orders.models import OrderItem

from .models import Product, ProductReview, update_product_rating, WishlistItem
from .serializers import ProductListSerializer, ProductDetailSerializer, ProductReviewSerializer, WishlistItemSerializer



class ProductListView(generics.ListAPIView):
    serializer_class = ProductListSerializer
    permission_classes = [permissions.AllowAny]
    def get_queryset(self):
        queryset = Product.objects.filter(is_active=True).select_related("category")
        # 1. Search Query (name or description)
        query = self.request.query_params.get("search") or self.request.query_params.get("q")
        if query:
            queryset = queryset.filter(Q(name__icontains=query) | Q(description__icontains=query))
        
        # 2. Category Filter
        category_slug = self.request.query_params.get("category")
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)
        # 3. Featured Flag
        featured = self.request.query_params.get("featured")
        if featured is not None:
            is_featured_bool = featured.lower() in ("true", "1")
            queryset = queryset.filter(is_featured=is_featured_bool)
        # 4. Price Range Filters (min_price & max_price)
        min_price = self.request.query_params.get("min_price")
        if min_price:
            try:
                queryset = queryset.filter(current_price__gte=Decimal(min_price))
            except Exception:
                pass
        max_price = self.request.query_params.get("max_price")
        if max_price:
            try:
                queryset = queryset.filter(current_price__lte=Decimal(max_price))
            except Exception:
                pass
        # 5. Minimum Star Rating Filter (e.g. 4.0, 3.0)
        min_rating = self.request.query_params.get("min_rating")
        if min_rating:
            try:
                queryset = queryset.filter(rating__gte=Decimal(min_rating))
            except Exception:
                pass
        # 6. In-Stock Only Filter
        in_stock = self.request.query_params.get("in_stock")
        if in_stock is not None and in_stock.lower() in ("true", "1"):
            queryset = queryset.filter(stock_quantity__gt=0)
        # 7. On-Sale / Deals Filter (original_price > current_price)
        on_sale = self.request.query_params.get("on_sale")
        if on_sale is not None and on_sale.lower() in ("true", "1"):
            queryset = queryset.filter(
                original_price__isnull=False,
                original_price__gt=F("current_price")
            )
        # 8. Sort Ordering
        sort = self.request.query_params.get("sort")
        if sort == "price_asc":
            queryset = queryset.order_by("current_price")
        elif sort == "price_desc":
            queryset = queryset.order_by("-current_price")
        elif sort == "rating_desc":
            queryset = queryset.order_by("-rating", "-review_count")
        elif sort == "popular":
            queryset = queryset.order_by("-review_count", "-rating")
        elif sort == "newest":
            queryset = queryset.order_by("-created_at")
        else:
            queryset = queryset.order_by("-created_at")
        return queryset

    

class ProductDetailView(generics.RetrieveAPIView):
    queryset = Product.objects.filter(is_active=True).select_related("category").prefetch_related("images")
    serializer_class = ProductDetailSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = "slug"


class  ProductReviewLisCreateView(APIView):

    def get_permissions(self):
        if self.request.method == "POST":
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    
    def get(self, request, slug):
        product = get_object_or_404(Product, slug=slug)
        reviews = product.reviews.select_related("user").all()
        total = reviews.count()
        star_counts = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
        for item in reviews.values("rating").annotate(count=Count("id")):
            star_counts[item["rating"]] = item["count"]

        star_percentages = {}
        for star, count in star_counts.items():
            pct = round((count / total) * 100, 1) if total > 0 else 0
            star_percentages[str(star)] = pct

        user_reviewd = False
        if request.user.is_authenticated:
            user_reviewd = reviews.filter(user=request.user).exists()

        serializer = ProductReviewSerializer(reviews, many=True, context={"request": request})

        return Response({
            "average_rating": float(product.rating),
            "review_count": product.review_count,
            "star_counts": star_counts,
            "star_percentages": star_percentages,
            "user_has_reviewed": user_reviewd,
            "reviews": serializer.data,
        })

    def post(self, request, slug):
        product = get_object_or_404(Product, slug=slug)
        rating = request.data.get("rating")
        headline = request.data.get("headline", "").strip()
        comment = request.data.get("comment", "").strip()

        if not rating or not (1 <= int(rating) <= 5):
            return Response(
                {
                    "detail": "Please provide a valid rating between 1 and 5 stars."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        if not comment:
            return Response(
                {
                    "detail": "Review comment cannot be empty."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        is_verified = OrderItem.objects.filter(
            order__user=request.user,
            product=product,
            order__order_status__in=["confirmed", "processing", "shipped", "delivered"]
        ).exists()

        review, _ = ProductReview.objects.update_or_create(
            product=product,
            user=request.user,
            defaults={
                "rating": int(rating),
                "headline": headline,
                "comment": comment,
                "is_verified_purchase": is_verified
            }
        )

        update_product_rating(product)

        serializer = ProductReviewSerializer(review, context={"request": request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ProductReviewDeleteView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, slug, pk):
        product = get_object_or_404(Product, slug=slug)
        review = get_object_or_404(ProductReview, pk=pk, product=product, user=request.user)
        review.delete()
        update_product_rating(product)
        return Response(
            {
                "detail": "Review removed successfully."
            },
            status=status.HTTP_204_NO_CONTENT
        )


class WishlistView(APIView):
    """
    GET /api/products/wishlist/
    Returns all wishlisted products for the authenticated user,
    plus a direct list of product IDs for instant client-side lookups.
    """
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        items = WishlistItem.objects.filter(user=request.user).select_related("product__category")
        product_ids = list(items.values_list("product_id", flat=True))
        serializer = WishlistItemSerializer(items, many=True, context={"request": request})
        return Response({
            "count": items.count(),
            "ids": product_ids,
            "items": serializer.data
        })
class WishlistToggleView(APIView):
    """
    POST /api/products/wishlist/toggle/
    Payload: { "product_id": 4 }
    Toggles the product in or out of the user's wishlist in a single request.
    """
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request):
        product_id = request.data.get("product_id")
        if not product_id:
            return Response(
                {"detail": "product_id is required."},
                status=status.HTTP_400_BAD_REQUEST
            )
        product = get_object_or_404(Product, id=product_id, is_active=True)
        item = WishlistItem.objects.filter(user=request.user, product=product).first()
        if item:
            item.delete()
            return Response({
                "wishlisted": False,
                "product_id": product.id,
                "message": f"'{product.name}' removed from your wishlist."
            })
        else:
            WishlistItem.objects.create(user=request.user, product=product)
            return Response({
                "wishlisted": True,
                "product_id": product.id,
                "message": f"'{product.name}' saved to your wishlist!"
            }, status=status.HTTP_201_CREATED)
