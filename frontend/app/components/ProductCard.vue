<!-- frontend/app/components/ProductCard.vue -->
<script setup>
const props = defineProps({
  product: {
    type: Object,
    required: true
  }
})

const { isWishlisted, toggleWishlist } = useWishlist()
const { addToCart } = useCartState()

const isAdding = ref(false)
const justAdded = ref(false)

async function handleQuickAdd() {
  if (isAdding.value || !props.product?.id) return
  isAdding.value = true
  try {
    const res = await addToCart(props.product.id, 1)
    if (res?.success) {
      justAdded.value = true
      setTimeout(() => {
        justAdded.value = false
      }, 1800)
    }
  } finally {
    isAdding.value = false
  }
}
</script>

<template>
  <div class="product-card group">
    <!-- Card Media Wrapper -->
    <NuxtLink :to="`/products/${product.slug}`" class="image-link" :aria-label="product.name">
      <div class="image-wrap">
        <img
          v-if="product.image"
          :src="product.image"
          :alt="product.name"
          class="product-img"
          loading="lazy"
        />
        <div v-else class="image-placeholder">
          <span class="placeholder-icon"><i class="fa-solid fa-box"></i></span>
          <span class="placeholder-text">{{ product.category_name || 'KyroKart Item' }}</span>
        </div>

        <!-- Badges -->
        <div class="badge-stack">
          <span v-if="product.discount_percentage > 0" class="card-badge discount-badge">
            <span class="badge-fire"><i class="fa-solid fa-fire"></i></span>
            <span>-{{ product.discount_percentage }}% OFF</span>
          </span>
          <span v-else-if="product.is_featured" class="card-badge featured-badge">
            <span><i class="fa-solid fa-wand-magic-sparkles"></i> TOP PICK</span>
          </span>
        </div>

        <!-- Floating Wishlist Heart Toggle -->
        <button
          type="button"
          class="btn-wishlist-card"
          :class="{ active: isWishlisted(product.id) }"
          :title="isWishlisted(product.id) ? 'Remove from Wishlist' : 'Save to Wishlist'"
          @click.prevent.stop="toggleWishlist(product.id)"
          aria-label="Save to Wishlist"
        >
          <svg
            width="18"
            height="18"
            viewBox="0 0 24 24"
            :fill="isWishlisted(product.id) ? '#ef4444' : 'none'"
            :stroke="isWishlisted(product.id) ? '#ef4444' : '#64748b'"
            stroke-width="2.2"
            stroke-linecap="round"
            stroke-linejoin="round"
          >
            <path
              d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"
            ></path>
          </svg>
        </button>

        <!-- Quick Add Floating Bar on Hover (Desktop) -->
        <div class="quick-add-overlay">
          <button
            type="button"
            class="btn-quick-add"
            :class="{ added: justAdded }"
            :disabled="isAdding || !product.is_in_stock"
            @click.prevent.stop="handleQuickAdd"
          >
            <span v-if="justAdded"><i class="fa-solid fa-check"></i> Added to Cart!</span>
            <span v-else-if="isAdding">Adding...</span>
            <span v-else-if="!product.is_in_stock">Out of Stock</span>
            <span v-else class="quick-add-label">
              <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
                <line x1="12" y1="5" x2="12" y2="19"></line>
                <line x1="5" y1="12" x2="19" y2="12"></line>
              </svg>
              Quick Add
            </span>
          </button>
        </div>
      </div>
    </NuxtLink>

    <!-- Card Body Information -->
    <div class="product-info">
      <div class="meta-row">
        <span class="category-tag">{{ product.category_name }}</span>
        <div class="rating-row" v-if="Number(product.rating) > 0">
          <span class="star-icon"><i class="fa-solid fa-star"></i></span>
          <span class="rating-score">{{ Number(product.rating).toFixed(1) }}</span>
          <span class="review-count">({{ product.review_count }})</span>
        </div>
      </div>

      <h3 class="product-title">
        <NuxtLink :to="`/products/${product.slug}`" :title="product.name">
          {{ product.name }}
        </NuxtLink>
      </h3>

      <div class="card-footer">
        <PriceDisplay
          :current-price="product.current_price"
          :original-price="product.original_price"
          :discount-percentage="product.discount_percentage"
        />

        <NuxtLink :to="`/products/${product.slug}`" class="view-details-btn" aria-label="View Product Details">
          <span>Details</span>
          <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
            <polyline points="9 18 15 12 9 6"></polyline>
          </svg>
        </NuxtLink>
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
  transition: transform var(--transition-base), box-shadow var(--transition-base), border-color var(--transition-base);
  display: flex;
  flex-direction: column;
  position: relative;
  box-shadow: var(--shadow-xs);
}

.product-card:hover {
  transform: translateY(-4px);
  box-shadow: var(--shadow-hover);
  border-color: #cbd5e1;
}

.image-link {
  display: block;
}

.image-wrap {
  position: relative;
  width: 100%;
  padding-top: 85%;
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
  transition: transform 0.4s var(--ease-out);
}

.product-card:hover .product-img {
  transform: scale(1.05);
}

.image-placeholder {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 0.35rem;
  color: var(--text-muted);
  background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
}

.placeholder-icon {
  font-size: 2rem;
}

.placeholder-text {
  font-size: 0.82rem;
  font-weight: 600;
}

/* Badges */
.badge-stack {
  position: absolute;
  top: 0.75rem;
  left: 0.75rem;
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
  z-index: 5;
}

.card-badge {
  display: inline-flex;
  align-items: center;
  gap: 0.25rem;
  font-size: 0.72rem;
  font-weight: 800;
  padding: 0.25rem 0.55rem;
  border-radius: var(--radius-xs);
  letter-spacing: 0.02em;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
}

.discount-badge {
  background: #ef4444;
  color: #ffffff;
}

.featured-badge {
  background: #0f172a;
  color: #38bdf8;
  border: 1px solid rgba(56, 189, 248, 0.3);
}

/* Wishlist Button */
.btn-wishlist-card {
  position: absolute;
  top: 0.75rem;
  right: 0.75rem;
  width: 34px;
  height: 34px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(4px);
  border: 1px solid rgba(226, 232, 240, 0.8);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 5;
  transition: all var(--transition-fast);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
}

.btn-wishlist-card:hover {
  transform: scale(1.1);
  background: #ffffff;
  box-shadow: 0 4px 12px rgba(239, 68, 68, 0.18);
}

.btn-wishlist-card.active {
  background: #fef2f2;
  border-color: #fecaca;
}

/* Quick Add Overlay */
.quick-add-overlay {
  position: absolute;
  bottom: 0.75rem;
  left: 0.75rem;
  right: 0.75rem;
  z-index: 6;
  opacity: 0;
  transform: translateY(8px);
  transition: all var(--transition-base);
}

.product-card:hover .quick-add-overlay {
  opacity: 1;
  transform: translateY(0);
}

.btn-quick-add {
  width: 100%;
  background: rgba(11, 15, 25, 0.92);
  backdrop-filter: blur(8px);
  color: #ffffff;
  font-weight: 700;
  font-size: 0.84rem;
  padding: 0.65rem 1rem;
  border-radius: var(--radius-sm);
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 14px rgba(0, 0, 0, 0.2);
  transition: all var(--transition-fast);
}

.btn-quick-add:hover:not(:disabled) {
  background: var(--primary);
  color: #ffffff;
}

.btn-quick-add.added {
  background: #10b981;
  color: #ffffff;
}

.quick-add-label {
  display: inline-flex;
  align-items: center;
  gap: 0.35rem;
}

/* Card Body */
.product-info {
  padding: 1rem 1.15rem 1.15rem;
  display: flex;
  flex-direction: column;
  flex: 1;
}

.meta-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 0.45rem;
}

.category-tag {
  font-size: 0.74rem;
  font-weight: 700;
  color: var(--primary);
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.rating-row {
  display: inline-flex;
  align-items: center;
  gap: 0.2rem;
  font-size: 0.78rem;
  background: #fefce8;
  padding: 0.1rem 0.35rem;
  border-radius: var(--radius-xs);
  border: 1px solid #fef08a;
}

.star-icon {
  color: #eab308;
  font-size: 0.85rem;
}

.rating-score {
  font-weight: 700;
  color: #854d0e;
}

.review-count {
  color: #a16207;
  font-size: 0.72rem;
}

.product-title {
  font-family: 'Plus Jakarta Sans', sans-serif;
  font-size: 0.98rem;
  font-weight: 700;
  line-height: 1.35;
  margin-bottom: 0.85rem;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  height: 2.7em;
}

.product-title a {
  color: var(--text-main);
  transition: color var(--transition-fast);
}

.product-title a:hover {
  color: var(--primary);
}

.card-footer {
  margin-top: auto;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding-top: 0.65rem;
  border-top: 1px solid var(--border-subtle);
}

.view-details-btn {
  display: inline-flex;
  align-items: center;
  gap: 0.2rem;
  font-size: 0.82rem;
  font-weight: 700;
  color: var(--text-muted);
  padding: 0.35rem 0.65rem;
  border-radius: var(--radius-xs);
  background: var(--bg-subtle);
  transition: all var(--transition-fast);
}

.view-details-btn:hover {
  color: var(--primary);
  background: var(--primary-light);
}

@media (max-width: 768px) {
  .quick-add-overlay {
    display: none;
  }
}
</style>
