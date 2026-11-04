<!-- frontend/app/components/ProductCard.vue -->
<script setup>
const props = defineProps({
    product: {
        type: Object,
        required: true
    }
})

const { isWishlisted, toggleWishlist } = useWishlist()
</script>

<template>
    <div class="product-card">
        <NuxtLink :to="`/products/${product.slug}`" class="image-link">
            <div class="image-wrap">
                <img v-if="product.image" :src="product.image" :alt="product.name" class="product-img" loading="lazy">
                <div v-else class="image-placeholder">
                    <span>{{ product.category_name || 'DropShip' }}</span>
                </div>

                <span v-if="product.discount_percentage > 0" class="card-badge discount">
                    -{{ product.discount_percentage }}%
                </span>

                <span v-else-if="product.is_featured" class="card-badge featured">Featured</span>

                <!-- Floating Wishlist Heart Toggle -->
                <button type="button" class="btn-wishlist-card" :class="{ 'active': isWishlisted(product.id) }"
                    :title="isWishlisted(product.id) ? 'Remove from Wishlist' : 'Add to Wishlist'"
                    @click.prevent.stop="toggleWishlist(product.id)">
                    <svg width="18" height="18" viewBox="0 0 24 24"
                        :fill="isWishlisted(product.id) ? '#ef4444' : 'none'"
                        :stroke="isWishlisted(product.id) ? '#ef4444' : '#64748b'" stroke-width="2"
                        stroke-linecap="round" stroke-linejoin="round">
                        <path
                            d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z">
                        </path>
                    </svg>
                </button>
            </div>
        </NuxtLink>

        <div class="product-info">
            <span class="category-tag">{{ product.category_name }}</span>

            <h3 class="product-title">
                <NuxtLink :to="`/products/${product.slug}`">{{ product.name }}</NuxtLink>
            </h3>

            <div class="rating-row">
                <span class="stars">&#9733; {{ Number(product.rating).toFixed(1) }}</span>
                <span class="reviews">({{ product.review_count }})</span>
            </div>

            <div class="card-footer">
                <PriceDisplay :current-price="product.current_price" :original-price="product.original_price"
                    :discount-percentage="product.discount_percentage" />

                <NuxtLink :to="`/products/${product.slug}`" class="view-btn">View</NuxtLink>
            </div>
        </div>
    </div>
</template>

<style scoped>
.product-card {
    background: var(--bg-surface);
    border: 1px solid var(--border-color);
    border-radius: var(--radius-lg);
    overflow: hidden;
    transition: transform 0.2s, box-shadow 0.2s;
    display: flex;
    flex-direction: column;
    position: relative;
}

.product-card:hover {
    transform: translateY(-3px);
    box-shadow: var(--shadow-md);
}

.image-link {
    display: block;
}

.image-wrap {
    position: relative;
    width: 100%;
    padding-top: 80%;
    background: #f1f5f9;
    overflow: hidden;
}

.product-img {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.image-placeholder {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    color: var(--text-muted);
    font-weight: 600;
    font-size: 0.9rem;
    background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
}

.card-badge {
    position: absolute;
    top: 0.75rem;
    left: 0.75rem;
    font-size: 0.75rem;
    font-weight: 700;
    padding: 0.2rem 0.5rem;
    border-radius: var(--radius-sm);
    z-index: 2;
}

.card-badge.discount {
    background: #ef4444;
    color: #fff;
}

.card-badge.featured {
    background: var(--primary);
    color: #fff;
}

/* Floating Wishlist Button */
.btn-wishlist-card {
    position: absolute;
    top: 0.75rem;
    right: 0.75rem;
    width: 32px;
    height: 32px;
    border-radius: 50%;
    background: rgba(255, 255, 255, 0.9);
    border: none;
    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    z-index: 3;
    transition: all 0.2s ease;
}

.btn-wishlist-card:hover {
    transform: scale(1.1);
    background: #ffffff;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.15);
}

.btn-wishlist-card.active {
    background: #ffffff;
}

.product-info {
    padding: 1.25rem;
    display: flex;
    flex-direction: column;
    flex: 1;
}

.category-tag {
    font-size: 0.75rem;
    font-weight: 600;
    text-transform: uppercase;
    color: var(--text-muted);
    margin-bottom: 0.35rem;
}

.product-title {
    font-size: 0.95rem;
    font-weight: 700;
    line-height: 1.35;
    margin-bottom: 0.5rem;
    flex: 1;
}

.product-title:hover {
    color: var(--primary);
}

.rating-row {
    display: flex;
    align-items: center;
    gap: 0.3rem;
    font-size: 0.8rem;
    margin-bottom: 1rem;
}

.stars {
    color: #f59e0b;
    font-weight: 700;
}

.reviews {
    color: var(--text-muted);
}

.card-footer {
    display: flex;
    align-items: center;
    justify-content: space-between;
    border-top: 1px solid var(--border-color);
    padding-top: 0.85rem;
    margin-top: auto;
}

.view-btn {
    background: var(--bg-page);
    border: 1px solid var(--border-color);
    color: var(--text-main);
    font-size: 0.85rem;
    font-weight: 600;
    padding: 0.35rem 0.85rem;
    border-radius: var(--radius-sm);
    transition: all 0.15s;
}

.view-btn:hover {
    background: var(--primary);
    border-color: var(--primary);
    color: #fff;
}
</style>
