<!-- frontend/app/pages/cart.vue -->
<template>
    <div class="cart-page">
        <div class="cart-container">
            <h1>Shopping Cart</h1>

            <div v-if="loading && items.length === 0" class="loading-wrap">
                <LoadingSpinner text="Loading cart..." />
            </div>

            <!-- Empty Cart State -->
            <EmptyState v-else-if="items.length === 0" title="Your cart is currently empty"
                description="Looks like you haven't added anything to your cart yet. Explore our catalog to find great deals!">
                <template #action>
                    <NuxtLink to="/shop" class="btn-shop">Start Shopping</NuxtLink>
                </template>
            </EmptyState>

            <!-- Cart Content -->
            <div v-else class="cart-layout">
                <!-- Left: Items List -->
                <div class="cart-items-section">
                    <div class="table-header">
                        <span class="col-product">Product</span>
                        <span class="col-price">Price</span>
                        <span class="col-qty">Quantity</span>
                        <span class="col-total">Total</span>
                        <span class="col-action"></span>
                    </div>

                    <div v-for="item in items" :key="item.id" class="cart-item-row">
                        <!-- Product Info -->
                        <div class="item-product">
                            <NuxtLink :to="`/products/${item.product.slug}`" class="item-thumb">
                                <img v-if="item.product.image" :src="item.product.image" :alt="item.product.name" />
                                <div v-else class="thumb-fallback">{{ item.product.category_name || 'Item' }}</div>
                            </NuxtLink>
                            <div class="item-meta">
                                <NuxtLink :to="`/products/${item.product.slug}`" class="item-name">
                                    {{ item.product.name }}
                                </NuxtLink>
                                <span class="item-category">{{ item.product.category_name }}</span>
                            </div>
                        </div>

                        <!-- Unit Price -->
                        <div class="item-price">
                            ${{ Number(item.unit_price).toFixed(2) }}
                        </div>

                        <!-- Quantity Selector -->
                        <div class="item-qty">
                            <QuantitySelector :model-value="item.quantity" :min="1"
                                :max="item.product.stock_quantity || 1"
                                @update:model-value="(qty) => onUpdateQty(item.id, qty)" />
                        </div>

                        <!-- Line Total -->
                        <div class="item-total">
                            ${{ Number(item.line_total).toFixed(2) }}
                        </div>

                        <!-- Delete Action -->
                        <div class="item-remove">
                            <button @click="onRemoveItem(item.id)" class="btn-remove" title="Remove item">
                                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor"
                                    stroke-width="2">
                                    <polyline points="3 6 5 6 21 6"></polyline>
                                    <path
                                        d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2">
                                    </path>
                                </svg>
                            </button>
                        </div>
                    </div>

                    <div class="cart-actions-row">
                        <NuxtLink to="/shop" class="btn-back-nav" aria-label="Continue Shopping">
                            <span class="back-arrow-wrap">
                                <i class="fa-solid fa-arrow-left"></i>
                            </span>
                            <span>Continue Shopping</span>
                        </NuxtLink>
                    </div>
                </div>

                <!-- Right: Order Summary -->
                <div class="cart-summary-section">
                    <div class="summary-card">
                        <h3>Order Summary</h3>

                        <div class="summary-line">
                            <span>Items Total ({{ totalItems }})</span>
                            <span>${{ Number(subtotal).toFixed(2) }}</span>
                        </div>

                        <div class="summary-line">
                            <span>Standard Shipping</span>
                            <span class="free-text">Free (KyroKart Direct)</span>
                        </div>

                        <div class="summary-divider"></div>

                        <div class="summary-total">
                            <span>Estimated Total</span>
                            <span class="total-amount">${{ Number(subtotal).toFixed(2) }}</span>
                        </div>

                        <NuxtLink to="/checkout" class="btn-checkout">
                            Proceed to Checkout &rarr;
                        </NuxtLink>

                        <!-- Estimated Delivery & Live Urgency -->
                        <DeliveryEstimator :compact="true" />

                        <p class="summary-note">
                            Taxes and final delivery address confirmed during checkout.
                        </p>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
const { items, totalItems, subtotal, loading, updateQuantity, removeItem } = useCartState()

async function onUpdateQty(itemId, newQty) {
    await updateQuantity(itemId, newQty)
}

async function onRemoveItem(itemId) {
    if (confirm('Remove this item from your cart?')) {
        await removeItem(itemId)
    }
}
</script>

<style scoped>
.cart-page {
    padding: 3rem 1.5rem 5rem;
}

.cart-container {
    max-width: 1200px;
    margin: 0 auto;
}

h1 {
    font-size: 2rem;
    font-weight: 800;
    letter-spacing: -0.02em;
    margin-bottom: 2rem;
}

.loading-wrap {
    padding: 3rem;
}

.btn-shop {
    background: var(--primary);
    color: #fff;
    font-weight: 600;
    padding: 0.75rem 1.5rem;
    border-radius: var(--radius-md);
    display: inline-block;
}

.cart-layout {
    display: grid;
    grid-template-columns: 1fr 360px;
    gap: 3rem;
    align-items: start;
}

.table-header {
    display: grid;
    grid-template-columns: 3fr 1fr 1fr 1fr 40px;
    padding-bottom: 0.75rem;
    border-bottom: 1px solid var(--border-color);
    font-size: 0.85rem;
    font-weight: 700;
    color: var(--text-muted);
    text-transform: uppercase;
    letter-spacing: 0.05em;
}

.cart-item-row {
    display: grid;
    grid-template-columns: 3fr 1fr 1fr 1fr 40px;
    align-items: center;
    padding: 1.5rem 0;
    border-bottom: 1px solid var(--border-color);
}

.item-product {
    display: flex;
    align-items: center;
    gap: 1rem;
}

.item-thumb {
    width: 70px;
    height: 70px;
    border-radius: var(--radius-md);
    overflow: hidden;
    background: #f1f5f9;
    border: 1px solid var(--border-color);
    flex-shrink: 0;
}

.item-thumb img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.thumb-fallback {
    width: 100%;
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    color: var(--text-muted);
    font-size: 0.8rem;
    font-weight: 700;
}

.item-meta {
    display: flex;
    flex-direction: column;
    gap: 0.25rem;
}

.item-name {
    font-size: 0.95rem;
    font-weight: 700;
    color: var(--text-main);
    line-height: 1.3;
}

.item-name:hover {
    color: var(--primary);
}

.item-category {
    font-size: 0.75rem;
    color: var(--text-muted);
    text-transform: uppercase;
}

.item-price,
.item-total {
    font-weight: 700;
    font-size: 1rem;
}

.btn-remove {
    color: var(--text-muted);
    padding: 0.35rem;
    transition: color 0.15s;
}

.btn-remove:hover {
    color: #dc2626;
}

.cart-actions-row {
    padding-top: 1.5rem;
}

.btn-continue {
    font-size: 0.9rem;
    font-weight: 600;
    color: var(--primary);
}

.summary-card {
    background: var(--bg-surface);
    border: 1px solid var(--border-color);
    border-radius: var(--radius-lg);
    padding: 2rem;
    box-shadow: var(--shadow-sm);
}

.summary-card h3 {
    font-size: 1.25rem;
    font-weight: 800;
    margin-bottom: 1.5rem;
}

.summary-line {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 1rem;
    font-size: 0.95rem;
    color: var(--text-muted);
}

.free-text {
    color: #16a34a;
    font-weight: 600;
    font-size: 0.85rem;
}

.summary-divider {
    height: 1px;
    background: var(--border-color);
    margin: 1.25rem 0;
}

.summary-total {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 1.5rem;
    font-size: 1.1rem;
    font-weight: 800;
}

.total-amount {
    font-size: 1.4rem;
    color: var(--primary);
}

.btn-checkout {
    display: block;
    text-align: center;
    background: var(--primary);
    color: #fff;
    font-weight: 700;
    font-size: 1rem;
    padding: 0.9rem;
    border-radius: var(--radius-md);
    transition: background 0.15s;
}

.btn-checkout:hover {
    background: var(--primary-hover);
}

.summary-note {
    margin-top: 1rem;
    font-size: 0.75rem;
    color: var(--text-muted);
    text-align: center;
    line-height: 1.4;
}

@media (max-width: 900px) {
    .cart-layout {
        grid-template-columns: 1fr;
    }
}

@media (max-width: 640px) {
    .table-header {
        display: none;
    }

    .cart-item-row {
        grid-template-columns: 1fr auto;
        gap: 1rem;
    }

    .item-product {
        grid-column: 1 / -1;
    }
}
</style>
