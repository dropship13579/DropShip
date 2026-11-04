from rest_framework import serializers

from .models import Category





class CategorySerializer(serializers.ModelSerializer):
    product_count = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = [
            "id",
            "name",
            "slug",
            "description",
            "image",
            "is_active",
            "product_count",
            "created_at"
        ]

    def get_product_count(self, obj):
        return obj.products.filter(is_active=True).count()