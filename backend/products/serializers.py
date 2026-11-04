from rest_framework import serializers

from .models import Product, ProductReview, WishlistItem, Supplier

from categories.serializers import CategorySerializer



class SupplierSerializer(serializers.ModelSerializer):
    products_count = serializers.IntegerField(source="products.count", read_only=True)
    class Meta:
        model = Supplier
        fields = [
            "id",
            "name",
            "contact_name",
            "email",
            "website_url",
            "average_shipping_days",
            "notes",
            "is_active",
            "products_count",
            "created_at",
        ]
class ProductSourcingSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source="category.name", read_only=True, default="Uncategorized")
    supplier_name = serializers.CharField(source="supplier.name", read_only=True, default="Unassigned")
    net_profit = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    profit_margin_percentage = serializers.FloatField(read_only=True)
    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "slug",
            "category_name",
            "image",
            "current_price",
            "supplier",
            "supplier_name",
            "supplier_cost",
            "supplier_sku",
            "net_profit",
            "profit_margin_percentage",
            "stock_quantity",
            "is_active",
        ]



class ProductListSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source="category.name", read_only=True)
    category_slug = serializers.CharField(source="category.slug", read_only=True)
    is_in_stock = serializers.BooleanField(read_only=True)
    discount_percentage = serializers.IntegerField(read_only=True)

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "slug",
            "category_name",
            "category_slug",
            "image",
            "current_price",
            "original_price",
            "discount_percentage",
            "stock_quantity",
            "is_in_stock",
            "rating",
            "review_count",
            "is_featured",
            "created_at"
        ]


class ProductDetailSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    is_in_stock = serializers.BooleanField(read_only=True)
    discount_percentage = serializers.IntegerField(read_only=True)
    related_products = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "slug",
            "category",
            "description",
            "specifications",
            "image",
            "current_price",
            "original_price",
            "discount_percentage",
            "stock_quantity",
            "is_in_stock",
            "rating",
            "review_count",
            "is_featured",
            "related_products",
            "created_at",
            "updated_at"
        ]

    def get_related_products(self, obj):
        if not obj.category:
            return []
        
        related = Product.objects.filter(category=obj.category, is_active=True).exclude(id=obj.id)[:4]
        return ProductListSerializer(related, many=True).data


class ProductReviewSerializer(serializers.ModelSerializer):
    user_username = serializers.CharField(source="user.username", read_only=True)
    is_own_review = serializers.SerializerMethodField()

    class Meta:
        model = ProductReview
        fields = [
            "id",
            "product",
            "user_username",
            "rating",
            "headline",
            "comment",
            "is_verified_purchase",
            "is_own_review",
            "created_at",
            "updated_at"
        ]
        read_only_fields = [
            "id",
            "product",
            "is_verified_purchase",
            "created_at",
            "updated_at"
        ]
    
    def get_is_own_review(self, obj):
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            return obj.user_id == request.user.id
        return False


class WishlistItemSerializer(serializers.ModelSerializer):
    product = ProductListSerializer(read_only=True)
    class Meta:
        model = WishlistItem
        fields = ["id", "product", "created_at"]
        read_only_fields = fields
