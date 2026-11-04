<!-- frontend/app/pages/account/orders/index.vue -->
<template>
    <div class="orders-page">
        <div class="orders-container">
            <div class="page-header">
                <NuxtLink to="/account" class="back-link">&larr; Back to My Account</NuxtLink>
                <h1>My Orders</h1>
                <p class="subtitle">Track your dropship packages and view past receipts.</p>
            </div>

            <!-- Loading State -->
            <div v-if="loading" class="loading-wrap">
                <LoadingSpinner text="Loading your orders..." />
            </div>

            <!-- Error State -->
            <div v-else-if="error" class="error-banner">
                {{ error }}
            </div>

            <!-- Empty State -->
            <EmptyState v-else-if="orders.length === 0" title="No orders yet"
                description="You haven't placed any orders yet. Discover trending dropship products and place your first order today!">
                <template #action>
                    <NuxtLink to="/shop" class="btn-shop">Explore Products</NuxtLink>
                </template>
            </EmptyState>

            <!-- Order List -->
            <div v-else class="orders-list">
                <div v-for="order in orders" :key="order.id" class="order-card">
                    <div class="order-card-header">
                        <div class="order-meta-group">
                            <div class="order-id">
                                <span class="label">Order</span>
                                <strong>#{{ order.order_number }}</strong>
                            </div>
                            <div class="order-date">
                                <span class="label">Date Placed</span>
                                <span>{{ formatDate(order.created_at) }}</span>
                            </div>
                            <div class="order-total">
                                <span class="label">Total Amount</span>
                                <strong class="price-val">${{ Number(order.total_amount).toFixed(2) }}</strong>
                            </div>
                        </div>

                        <div class="status-group">
                            <span :class="['status-pill', `status-${order.order_status}`]">
                                {{ order.order_status_display }}
                            </span>
                            <span :class="['payment-pill', `payment-${order.payment_status}`]">
                                {{ order.payment_status_display }}
                            </span>
                        </div>
                    </div>

                    <!-- Items Preview -->
                    <div class="order-items-preview">
                        <div v-for="item in order.items" :key="item.id" class="preview-item">
                            <div class="preview-thumb">
                                <img v-if="item.product_image_snapshot" :src="item.product_image_snapshot"
                                    :alt="item.product_name_snapshot" />
                                <div v-else class="thumb-fallback">
                                    {{ item.product_name_snapshot.charAt(0) }}
                                </div>
                            </div>
                            <div class="preview-details">
                                <div class="item-name">{{ item.product_name_snapshot }}</div>
                                <div class="item-sub">
                                    {{ item.quantity }} &times; ${{ Number(item.unit_price).toFixed(2) }}
                                </div>
                            </div>
                            <div class="preview-line-total">
                                ${{ Number(item.line_total).toFixed(2) }}
                            </div>
                        </div>
                    </div>

                    <!-- Order Footer -->
                    <div class="order-card-footer">
                        <div class="shipping-to">
                            <span class="label">Shipping To:</span>
                            <span>
                                {{ order.shipping_address_snapshot?.recipient_name }} &bull;
                                {{ order.shipping_address_snapshot?.city }},
                                {{ order.shipping_address_snapshot?.country }}
                            </span>
                        </div>

                        <div class="footer-actions">
                            <span v-if="order.tracking_number" class="tracking-tag">
                                Tracking: {{ order.tracking_number }}
                            </span>
                            <NuxtLink :to="`/account/orders/${order.order_number}`" class="btn-view-details">
                                View Order Details &rarr;
                            </NuxtLink>
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

const { getOrders } = useOrdersApi()

const orders = ref([])
const loading = ref(true)
const error = ref('')

async function fetchOrders() {
    loading.value = true
    error.value = ''
    try {
        const data = await getOrders()
        orders.value = Array.isArray(data) ? data : (data?.results || [])
    } catch (err) {
        error.value = err.message || 'Failed to load order history.'
    } finally {
        loading.value = false
    }
}


function formatDate(isoStr) {
    if (!isoStr) return ''
    const d = new Date(isoStr)
    return d.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
    })
}

onMounted(() => {
    fetchOrders()
})
</script>

<style scoped>
.orders-page {
    padding: 2.5rem 1.5rem 5rem;
    max-width: 1000px;
    margin: 0 auto;
}

.page-header {
    margin-bottom: 2rem;
}

.back-link {
    display: inline-block;
    color: var(--text-muted);
    font-size: 0.9rem;
    font-weight: 500;
    margin-bottom: 0.5rem;
    transition: color 0.15s;
}

.back-link:hover {
    color: var(--primary);
}

.page-header h1 {
    font-size: 2rem;
    font-weight: 800;
    letter-spacing: -0.02em;
    color: var(--text-main);
}

.subtitle {
    color: var(--text-muted);
    font-size: 0.95rem;
    margin-top: 0.25rem;
}

.loading-wrap {
    padding: 4rem 0;
}

.error-banner {
    background: #fef2f2;
    border: 1px solid #fecaca;
    color: #dc2626;
    padding: 1rem 1.25rem;
    border-radius: var(--radius-md);
}

.btn-shop {
    background: var(--primary);
    color: #fff;
    font-weight: 600;
    padding: 0.75rem 1.75rem;
    border-radius: var(--radius-md);
    display: inline-block;
    margin-top: 1rem;
}

.orders-list {
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
}

.order-card {
    background: var(--bg-surface);
    border: 1px solid var(--border-color);
    border-radius: var(--radius-lg);
    box-shadow: var(--shadow-sm);
    overflow: hidden;
    transition: box-shadow 0.15s;
}

.order-card:hover {
    box-shadow: var(--shadow-md);
}

.order-card-header {
    background: #f8fafc;
    border-bottom: 1px solid var(--border-color);
    padding: 1.25rem 1.5rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 1rem;
}

.order-meta-group {
    display: flex;
    gap: 2rem;
    flex-wrap: wrap;
}

.order-id,
.order-date,
.order-total {
    display: flex;
    flex-direction: column;
    font-size: 0.9rem;
}

.label {
    font-size: 0.75rem;
    color: var(--text-muted);
    text-transform: uppercase;
    font-weight: 600;
    letter-spacing: 0.03em;
    margin-bottom: 0.15rem;
}

.price-val {
    color: var(--primary);
    font-size: 1.05rem;
}

.status-group {
    display: flex;
    gap: 0.5rem;
}

.status-pill {
    font-size: 0.75rem;
    font-weight: 700;
    padding: 0.3rem 0.7rem;
    border-radius: 999px;
    text-transform: capitalize;
}

.status-pending {
    background: #fef3c7;
    color: #92400e;
}

.status-confirmed {
    background: #e0f2fe;
    color: #0369a1;
}

.status-processing {
    background: #ede9fe;
    color: #6b21a8;
}

.status-shipped {
    background: #fce7f3;
    color: #9d174d;
}

.status-delivered {
    background: #dcfce7;
    color: #166534;
}

.status-cancelled {
    background: #fee2e2;
    color: #991b1b;
}

.payment-pill {
    font-size: 0.75rem;
    font-weight: 600;
    padding: 0.3rem 0.65rem;
    border-radius: 999px;
    background: #f1f5f9;
    color: var(--text-muted);
}

.payment-paid {
    background: #dcfce7;
    color: #166534;
}

.payment-pending {
    background: #fef9c3;
    color: #854d0e;
}

.order-items-preview {
    padding: 1.25rem 1.5rem;
    display: flex;
    flex-direction: column;
    gap: 0.85rem;
}

.preview-item {
    display: flex;
    align-items: center;
    gap: 1rem;
}

.preview-thumb {
    width: 48px;
    height: 48px;
    border-radius: var(--radius-sm);
    background: #f1f5f9;
    overflow: hidden;
    flex-shrink: 0;
}

.preview-thumb img {
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
    font-weight: 700;
    color: var(--text-muted);
}

.preview-details {
    flex: 1;
    min-width: 0;
}

.item-name {
    font-size: 0.9rem;
    font-weight: 600;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

.item-sub {
    font-size: 0.8rem;
    color: var(--text-muted);
}

.preview-line-total {
    font-weight: 700;
    font-size: 0.95rem;
}

.order-card-footer {
    border-top: 1px solid var(--border-color);
    padding: 1rem 1.5rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 1rem;
    font-size: 0.85rem;
}

.shipping-to {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    color: var(--text-muted);
}

.footer-actions {
    display: flex;
    align-items: center;
    gap: 1rem;
}

.tracking-tag {
    background: #f1f5f9;
    padding: 0.3rem 0.6rem;
    border-radius: var(--radius-sm);
    font-family: monospace;
    font-size: 0.8rem;
}

.btn-view-details {
    font-weight: 600;
    color: var(--primary);
    transition: color 0.15s;
}

.btn-view-details:hover {
    color: var(--primary-hover);
    text-decoration: underline;
}

@media (max-width: 640px) {
    .order-card-header {
        flex-direction: column;
        align-items: flex-start;
    }

    .order-card-footer {
        flex-direction: column;
        align-items: flex-start;
    }
}
</style>
