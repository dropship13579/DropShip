# In backend/products/models.py
from decimal import Decimal
from django.db import models
from django.utils.text import slugify
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import Avg, Count
from django.contrib.auth.models import User
from categories.models import Category


class Supplier(models.Model):
    name = models.CharField(max_length=150, unique=True, help_text="e.g. CJ Dropshipping, AliExpress, Spocket")
    contact_name = models.CharField(max_length=150, blank=True, default="")
    email = models.EmailField(blank=True, default="")
    website_url = models.URLField(blank=True, default="", help_text="Supplier catalog or portal URL")
    average_shipping_days = models.PositiveSmallIntegerField(default=7, help_text="Estimated shipping days to customers")
    notes = models.TextField(blank=True, default="")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category, related_name="products", on_delete=models.SET_NULL, null=True, blank=True)
    supplier = models.ForeignKey(Supplier, related_name="products", on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=280, unique=True, blank=True)
    description = models.TextField(blank=True, default="")
    specifications = models.JSONField(default=dict, blank=True)
    image = models.ImageField(upload_to="products/", blank=True, null=True)
    current_price = models.DecimalField(max_digits=10, decimal_places=2)
    original_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    # Wholesale Dropship Sourcing fields
    supplier_cost = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal("0.00"),
        help_text="Wholesale cost charged by supplier per unit"
    )
    supplier_sku = models.CharField(
        max_length=100,
        blank=True,
        default="",
        help_text="Supplier item SKU or catalog identifier"
    )

    stock_quantity = models.PositiveIntegerField(default=0)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    review_count = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["slug"]),
            models.Index(fields=["is_active", "is_featured"]),
            models.Index(fields=["current_price"]),
        ]

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            while Product.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    @property
    def is_in_stock(self):
        return self.stock_quantity > 0

    @property
    def discount_percentage(self):
        if self.original_price and self.original_price > self.current_price:
            discount = ((self.original_price - self.current_price) / self.original_price) * 100
            return round(discount)
        return 0

    @property
    def net_profit(self):
        """Dollar profit per unit sold: Current Price - Supplier Cost"""
        if self.current_price and self.supplier_cost:
            return max(Decimal("0.00"), self.current_price - self.supplier_cost)
        return self.current_price or Decimal("0.00")

    @property
    def profit_margin_percentage(self):
        """Profit margin percentage: ((Retail - Cost) / Retail) * 100"""
        if self.current_price and self.current_price > 0 and self.supplier_cost:
            margin = ((self.current_price - self.supplier_cost) / self.current_price) * 100
            return round(max(0.0, float(margin)), 1)
        return 100.0 if self.current_price and self.current_price > 0 else 0.0

    def __str__(self):
        return self.name
    

class ProductReview(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="product_reviews")
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], help_text="Rating between 1 and 5 stars")
    headline = models.CharField(max_length=150, blank=True, default="")
    comment = models.TextField()
    is_verified_purchase = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        unique_together = ("product", "user")
    
    def __str__(self):
        return f"{self.rating}★ by {self.user.username} for {self.product.name}"

def update_product_rating(product):
    stats = product.reviews.aggregate(avg=Avg("rating"), count=Count("id"))   
    product.rating = round(Decimal(str(stats["avg"] or 0)), 2)
    product.review_count = stats["count"] or 0
    product.save(update_fields=["rating", "review_count"])


# In backend/products/models.py

class WishlistItem(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="wishlist_items"
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="wishlisted_by"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        unique_together = ("user", "product")
        indexes = [
            models.Index(fields=["user", "product"]),
        ]

    def __str__(self):
        return f"{self.user.username} ❤️ {self.product.name}"
