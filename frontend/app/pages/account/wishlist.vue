<!-- frontend/app/pages/account/wishlist.vue -->
<template>
    <div class="wishlist-page">
        <div class="container">
            <div class="page-header">
                <div>
                    <NuxtLink to="/account" class="back-link">&larr; Back to My Account</NuxtLink>
                    <h1>My Wishlist</h1>
                    <p class="subtitle">Keep track of the products you love and want to order later.</p>
                </div>
                <NuxtLink to="/shop" class="btn-continue-shopping">Explore Products</NuxtLink>
            </div>

            <!-- Loading State -->
            <div v-if="loading" class="loading-wrap">
                <LoadingSpinner text="Loading your favorites..." />
            </div>

            <!-- Empty State -->
            <div v-else-if="wishlistItems.length === 0" class="empty-card">
                <div class="empty-icon-circle">
                    <svg width="36" height="36" viewBox="0 0 24 24" fill="none" stroke="#ef4444" stroke-width="2">
                        <path
                            d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z">
                        </path>
                    </svg>
                </div>
                <h2>Your wishlist is empty</h2>
                <p>Save products you like by clicking the heart icon on any product card!</p>
                <NuxtLink to="/shop" class="btn-primary">Browse Shop</NuxtLink>
            </div>

            <!-- Wishlist Grid -->
            <div v-else class="wishlist-grid">
                <div v-for="item in wishlistItems" :key="item.id" class="wishlist-card">
                    <NuxtLink :to="`/products/${item.product.slug}`" class="item-img-link">
                        <div class="img-wrap">
                            <img v-if="item.product.image" :src="item.product.image" :alt="item.product.name" />
                            <div v-else class="img-fallback">{{ item.product.name[0] }}</div>
                        </div>
                    </NuxtLink>

                    <div class="item-content">
                        <span class="category-pill">{{ item.product.category_name }}</span>
                        <h3 class="product-title">
                            <NuxtLink :to="`/products/${item.product.slug}`">{{ item.product.name }}</NuxtLink>
                        </h3>

                        <div class="rating-strip">
                            <span class="stars">&#9733; {{ Number(item.product.rating).toFixed(1) }}</span>
                            <span class="reviews">({{ item.product.review_count }})</span>
                        </div>

                        <div class="price-strip">
                            <span class="current-price">${{ Number(item.product.current_price).toFixed(2) }}</span>
                            <span v-if="item.product.original_price" class="original-price">
                                ${{ Number(item.product.original_price).toFixed(2) }}
                            </span>
                        </div>

                        <div class="stock-status"
                            :class="{ 'in-stock': item.product.is_in_stock, 'out-of-stock': !item.product.is_in_stock }">
                            {{ item.product.is_in_stock ? 'In Stock' : 'Out of Stock' }}
                        </div>

                        <div class="card-actions">
                            <button @click="handleMoveToCart(item.product)" class="btn-cart"
                                :disabled="!item.product.is_in_stock || addingId === item.product.id">
                                {{ addingId === item.product.id ? 'Adding...' : 'Move to Cart' }}
                            </button>
                            <button @click="toggleWishlist(item.product.id)" class="btn-remove"
                                title="Remove from Wishlist">
                                &times;
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
definePageMeta({
    middleware: 'auth'
})

const { wishlistItems, loading, fetchWishlist, toggleWishlist } = useWishlist()
const { addToCart } = useCartState()

const addingId = ref(null)

async function handleMoveToCart(product) {
    addingId.value = product.id
    const res = await addToCart(product.id, 1)
    if (res.success) {
        // Optionally remove from wishlist once moved to cart
        await toggleWishlist(product.id)
    } else {
        alert(res.error || 'Failed to add item to cart.')
    }
    addingId.value = null
}

onMounted(() => {
    fetchWishlist()
})
</script>

<style scoped>
.wishlist-page {
    padding: 3rem 1.5rem 5rem;
    min-height: 80vh;
}

.container {
    max-width: 1200px;
    margin: 0 auto;
}

.page-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-end;
    margin-bottom: 2.5rem;
    border-bottom: 1px solid var(--border-color);
    padding-bottom: 1.5rem;
}

.back-link {
    color: var(--text-muted);
    font-size: 0.85rem;
    font-weight: 500;
    text-decoration: none;
    display: inline-block;
    margin-bottom: 0.5rem;
}

.page-header h1 {
    font-size: 2rem;
    font-weight: 800;
    letter-spacing: -0.02em;
}

.subtitle {
    color: var(--text-muted);
    font-size: 0.95rem;
}

.btn-continue-shopping {
    background: var(--bg-surface);
    border: 1px solid var(--border-color);
    color: var(--text-main);
    padding: 0.65rem 1.25rem;
    border-radius: var(--radius-md);
    font-weight: 600;
    font-size: 0.9rem;
    text-decoration: none;
    transition: all 0.15s;
}

.btn-continue-shopping:hover {
    border-color: var(--primary);
    color: var(--primary);
}

.empty-card {
    text-align: center;
    padding: 4.5rem 2rem;
    background: var(--bg-surface);
    border: 1px solid var(--border-color);
    border-radius: var(--radius-lg);
    max-width: 520px;
    margin: 2rem auto;
}

.empty-icon-circle {
    width: 72px;
    height: 72px;
    border-radius: 50%;
    background: #fef2f2;
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 0 auto 1.5rem;
}

.empty-card h2 {
    font-size: 1.5rem;
    font-weight: 700;
    margin-bottom: 0.5rem;
}

.empty-card p {
    color: var(--text-muted);
    margin-bottom: 1.5rem;
}

.btn-primary {
    display: inline-block;
    background: var(--primary);
    color: #fff;
    padding: 0.75rem 1.75rem;
    border-radius: var(--radius-md);
    font-weight: 600;
    text-decoration: none;
}

.wishlist-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
    gap: 1.5rem;
}

.wishlist-card {
    background: var(--bg-surface);
    border: 1px solid var(--border-color);
    border-radius: var(--radius-lg);
    overflow: hidden;
    display: flex;
    flex-direction: column;
    transition: transform 0.15s, box-shadow 0.15s;
}

.wishlist-card:hover {
    transform: translateY(-3px);
    box-shadow: var(--shadow-md);
}

.img-wrap {
    width: 100%;
    padding-top: 75%;
    position: relative;
    background: #f1f5f9;
}

.img-wrap img {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.img-fallback {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 2rem;
    font-weight: 700;
    color: var(--text-muted);
}

.item-content {
    padding: 1.25rem;
    display: flex;
    flex-direction: column;
    flex: 1;
}

.category-pill {
    font-size: 0.7rem;
    font-weight: 700;
    text-transform: uppercase;
    color: var(--text-muted);
    margin-bottom: 0.25rem;
}

.product-title {
    font-size: 0.95rem;
    font-weight: 700;
    line-height: 1.35;
    margin-bottom: 0.5rem;
}

.product-title a {
    color: var(--text-main);
    text-decoration: none;
}

.rating-strip {
    display: flex;
    align-items: center;
    gap: 0.35rem;
    font-size: 0.8rem;
    margin-bottom: 0.65rem;
}

.stars {
    color: #f59e0b;
    font-weight: 700;
}

.reviews {
    color: var(--text-muted);
}

.price-strip {
    display: flex;
    align-items: baseline;
    gap: 0.5rem;
    margin-bottom: 0.5rem;
}

.current-price {
    font-size: 1.15rem;
    font-weight: 800;
    color: var(--primary);
}

.original-price {
    font-size: 0.85rem;
    color: var(--text-muted);
    text-decoration: line-through;
}

.stock-status {
    font-size: 0.75rem;
    font-weight: 600;
    margin-bottom: 1rem;
}

.stock-status.in-stock {
    color: #10b981;
}

.stock-status.out-of-stock {
    color: #ef4444;
}

.card-actions {
    display: flex;
    gap: 0.5rem;
    margin-top: auto;
}

.btn-cart {
    flex: 1;
    background: var(--primary);
    color: #fff;
    border: none;
    padding: 0.65rem 0.85rem;
    border-radius: var(--radius-sm);
    font-size: 0.85rem;
    font-weight: 600;
    cursor: pointer;
    transition: background 0.15s;
}

.btn-cart:hover:not(:disabled) {
    background: var(--primary-hover, #4f46e5);
}

.btn-cart:disabled {
    opacity: 0.5;
    cursor: not-allowed;
}

.btn-remove {
    background: var(--bg-page);
    border: 1px solid var(--border-color);
    color: var(--text-muted);
    font-size: 1.25rem;
    line-height: 1;
    width: 36px;
    border-radius: var(--radius-sm);
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: all 0.15s;
}

.btn-remove:hover {
    background: #fef2f2;
    border-color: #fecaca;
    color: #ef4444;
}
</style>
