<!-- frontend/app/pages/account/orders/[order_number].vue -->
<template>
    <div class="order-detail-page">
        <div class="order-detail-container">
            <!-- Header & Actions -->
            <div class="page-top-bar">
                <NuxtLink to="/account/orders" class="back-link">&larr; Back to Order History</NuxtLink>
                <div class="actions-group">
                    <button @click="printReceipt" class="btn-print" title="Print Invoice / Receipt">
                        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor"
                            stroke-width="2">
                            <polyline points="6 9 6 2 18 2 18 9"></polyline>
                            <path d="M6 18H4a2 2 0 0 1-2-2v-5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-2"></path>
                            <rect x="6" y="14" width="12" height="8"></rect>
                        </svg>
                        <span>Print Receipt</span>
                    </button>
                </div>
            </div>

            <div v-if="loading" class="loading-wrap">
                <LoadingSpinner text="Retrieving order details..." />
            </div>

            <div v-else-if="error" class="error-banner">
                {{ error }}
            </div>

            <div v-else-if="order" class="order-content">
                <!-- Title Row -->
                <div class="order-header-card">
                    <div class="header-main">
                        <h1>Order #{{ order.order_number }}</h1>
                        <p class="placed-date">Placed on {{ formatDate(order.created_at) }}</p>
                    </div>

                    <div class="header-status">
                        <span :class="['status-pill', `status-${order.order_status}`]">
                            {{ order.order_status_display }}
                        </span>
                        <span :class="['payment-pill', `payment-${order.payment_status}`]">
                            {{ order.payment_status_display }}
                        </span>
                    </div>
                </div>

                <!-- Status Progress Stepper -->
                <section v-if="order.order_status !== 'cancelled'" class="stepper-card">
                    <h3>Fulfillment Progress</h3>
                    <div class="stepper-track">
                        <div v-for="(step, idx) in steps" :key="step.key" class="step-node" :class="{
                            'completed': currentStepIndex > idx,
                            'active': currentStepIndex === idx
                        }">
                            <div class="node-icon">
                                <span v-if="currentStepIndex > idx">&#10003;</span>
                                <span v-else>{{ idx + 1 }}</span>
                            </div>
                            <span class="node-label">{{ step.label }}</span>
                        </div>
                    </div>
                </section>

                <div v-else class="cancelled-banner">
                    This order was cancelled.
                </div>

                <!-- Dropship Tracking Box (if available) -->
                <div v-if="order.tracking_number" class="tracking-banner">
                    <div class="tracking-icon">
                        <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor"
                            stroke-width="2">
                            <rect x="1" y="3" width="15" height="13"></rect>
                            <polygon points="16 8 20 8 23 11 23 16 16 16 16 8"></polygon>
                            <circle cx="5.5" cy="18.5" r="2.5"></circle>
                            <circle cx="18.5" cy="18.5" r="2.5"></circle>
                        </svg>
                    </div>
                    <div>
                        <strong>Package Sourced & In Transit</strong>
                        <p>Carrier Tracking Reference: <code>{{ order.tracking_number }}</code></p>
                    </div>
                </div>

                <!-- Main Layout -->
                <div class="order-grid">
                    <!-- Left Column: Items Table -->
                    <div class="grid-main">
                        <div class="card items-card">
                            <h3>Ordered Products ({{ order.items?.length }})</h3>

                            <div class="items-table">
                                <div v-for="item in order.items" :key="item.id" class="table-row">
                                    <div class="product-thumb">
                                        <img v-if="item.product_image_snapshot" :src="item.product_image_snapshot"
                                            :alt="item.product_name_snapshot" />
                                        <div v-else class="thumb-fallback">
                                            {{ item.product_name_snapshot.charAt(0) }}
                                        </div>
                                    </div>

                                    <div class="product-info">
                                        <NuxtLink v-if="item.product_slug" :to="`/products/${item.product_slug}`"
                                            class="product-title link">
                                            {{ item.product_name_snapshot }}
                                        </NuxtLink>
                                        <span v-else class="product-title">{{ item.product_name_snapshot }}</span>
                                        <span class="product-unit">Unit: ${{ Number(item.unit_price).toFixed(2)
                                            }}</span>
                                    </div>

                                    <div class="product-qty">&times; {{ item.quantity }}</div>

                                    <div class="product-line-total">
                                        ${{ Number(item.line_total).toFixed(2) }}
                                    </div>
                                </div>
                            </div>

                            <!-- Customer Notes -->
                            <div v-if="order.customer_notes" class="order-notes-box">
                                <span class="notes-label">Delivery Instructions:</span>
                                <p>{{ order.customer_notes }}</p>
                            </div>
                        </div>
                    </div>

                    <!-- Right Column: Address & Payment Summary -->
                    <div class="grid-side">
                        <!-- Shipping Snapshot -->
                        <div class="card address-card">
                            <h3>Shipping Address</h3>
                            <div class="snapshot-details">
                                <strong>{{ order.shipping_address_snapshot?.recipient_name }}</strong>
                                <p>{{ order.shipping_address_snapshot?.address_line_1 }}</p>
                                <p v-if="order.shipping_address_snapshot?.address_line_2">
                                    {{ order.shipping_address_snapshot?.address_line_2 }}
                                </p>
                                <p>
                                    {{ order.shipping_address_snapshot?.city }},
                                    {{ order.shipping_address_snapshot?.state }}
                                    {{ order.shipping_address_snapshot?.postal_code }}
                                </p>
                                <p>{{ order.shipping_address_snapshot?.country }}</p>
                                <p class="phone-meta">Phone: {{ order.shipping_address_snapshot?.phone }}</p>
                            </div>
                        </div>

                        <!-- Payment Summary -->
                        <div class="card payment-card">
                            <h3>Payment Info</h3>
                            <div class="info-row">
                                <span>Method:</span>
                                <strong>{{ order.payment_method_display }}</strong>
                            </div>
                            <div class="info-row">
                                <span>Payment Status:</span>
                                <strong :class="`pay-status-${order.payment_status}`">
                                    {{ order.payment_status_display }}
                                </strong>
                            </div>
                        </div>

                        <!-- Totals Breakdown -->
                        <div class="card totals-card">
                            <h3>Cost Summary</h3>
                            <div class="calc-line">
                                <span>Subtotal</span>
                                <span>${{ Number(order.subtotal).toFixed(2) }}</span>
                            </div>
                            <div class="calc-line">
                                <span>Shipping (Dropship Direct)</span>
                                <span class="free-badge">Free</span>
                            </div>
                            <div v-if="Number(order.discount_amount) > 0" class="calc-line discount">
                                <span>Discount {{ order.coupon_code ? `(${order.coupon_code})` : '' }}</span>
                                <span>-${{ Number(order.discount_amount).toFixed(2) }}</span>
                            </div>
                            <div class="calc-line total-line">
                                <strong>Total</strong>
                                <strong class="total-val">${{ Number(order.total_amount).toFixed(2) }}</strong>
                            </div>
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

const route = useRoute()
const { getOrder } = useOrdersApi()

const order = ref(null)
const loading = ref(true)
const error = ref('')

const steps = [
    { key: 'pending', label: 'Order Placed' },
    { key: 'confirmed', label: 'Confirmed' },
    { key: 'processing', label: 'Processing' },
    { key: 'shipped', label: 'Shipped' },
    { key: 'delivered', label: 'Delivered' }
]

const currentStepIndex = computed(() => {
    if (!order.value) return 0
    const idx = steps.findIndex(s => s.key === order.value.order_status)
    return idx >= 0 ? idx : 0
})

async function fetchOrder() {
    loading.value = true
    error.value = ''
    try {
        const data = await getOrder(route.params.order_number)
        order.value = data
    } catch (err) {
        error.value = err.message || 'Unable to retrieve order details.'
    } finally {
        loading.value = false
    }
}

function formatDate(isoStr) {
    if (!isoStr) return ''
    const d = new Date(isoStr)
    return d.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    })
}

function printReceipt() {
    if (import.meta.client) {
        window.print()
    }
}

onMounted(() => {
    fetchOrder()
})
</script>

<style scoped>
.order-detail-page {
    padding: 2.5rem 1.5rem 5rem;
    max-width: 1100px;
    margin: 0 auto;
}

.page-top-bar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1.5rem;
}

.back-link {
    color: var(--text-muted);
    font-size: 0.9rem;
    font-weight: 500;
}

.back-link:hover {
    color: var(--primary);
}

.btn-print {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    background: #fff;
    border: 1px solid var(--border-color);
    padding: 0.5rem 1rem;
    border-radius: var(--radius-md);
    font-size: 0.85rem;
    font-weight: 600;
    color: var(--text-main);
    transition: all 0.15s;
}

.btn-print:hover {
    background: #f8fafc;
    border-color: #cbd5e1;
}

.loading-wrap {
    padding: 5rem 0;
}

.error-banner {
    background: #fef2f2;
    border: 1px solid #fecaca;
    color: #dc2626;
    padding: 1rem 1.25rem;
    border-radius: var(--radius-md);
}

.order-header-card {
    background: var(--bg-surface);
    border: 1px solid var(--border-color);
    border-radius: var(--radius-lg);
    padding: 1.75rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 1rem;
    margin-bottom: 1.5rem;
}

.header-main h1 {
    font-size: 1.75rem;
    font-weight: 800;
    letter-spacing: -0.02em;
    color: var(--text-main);
}

.placed-date {
    color: var(--text-muted);
    font-size: 0.9rem;
    margin-top: 0.25rem;
}

.header-status {
    display: flex;
    gap: 0.5rem;
}

.status-pill {
    font-size: 0.8rem;
    font-weight: 700;
    padding: 0.4rem 0.85rem;
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
    font-size: 0.8rem;
    font-weight: 600;
    padding: 0.4rem 0.85rem;
    border-radius: 999px;
    background: #f1f5f9;
}

.payment-paid {
    background: #dcfce7;
    color: #166534;
}

.payment-pending {
    background: #fef9c3;
    color: #854d0e;
}

/* Progress Stepper */
.stepper-card {
    background: var(--bg-surface);
    border: 1px solid var(--border-color);
    border-radius: var(--radius-lg);
    padding: 1.75rem;
    margin-bottom: 1.5rem;
}

.stepper-card h3 {
    font-size: 1.05rem;
    font-weight: 700;
    margin-bottom: 1.5rem;
}

.stepper-track {
    display: flex;
    justify-content: space-between;
    position: relative;
    max-width: 800px;
    margin: 0 auto;
}

.stepper-track::before {
    content: '';
    position: absolute;
    top: 16px;
    left: 20px;
    right: 20px;
    height: 3px;
    background: var(--border-color);
    z-index: 1;
}

.step-node {
    position: relative;
    z-index: 2;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 0.5rem;
}

.node-icon {
    width: 34px;
    height: 34px;
    border-radius: 50%;
    background: #f1f5f9;
    border: 3px solid #fff;
    box-shadow: 0 0 0 1px var(--border-color);
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 700;
    font-size: 0.85rem;
    color: var(--text-muted);
}

.node-label {
    font-size: 0.75rem;
    font-weight: 600;
    color: var(--text-muted);
    text-align: center;
}

.step-node.completed .node-icon {
    background: #16a34a;
    color: #fff;
    box-shadow: 0 0 0 1px #16a34a;
}

.step-node.active .node-icon {
    background: var(--primary);
    color: #fff;
    box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.25);
}

.step-node.active .node-label {
    color: var(--primary);
    font-weight: 700;
}

.cancelled-banner {
    background: #fee2e2;
    border: 1px solid #fecaca;
    color: #991b1b;
    padding: 1.25rem;
    border-radius: var(--radius-lg);
    font-weight: 600;
    margin-bottom: 1.5rem;
}

.tracking-banner {
    display: flex;
    align-items: center;
    gap: 1rem;
    background: #f0fdf4;
    border: 1px solid #bbf7d0;
    border-radius: var(--radius-lg);
    padding: 1.25rem 1.5rem;
    margin-bottom: 1.5rem;
    color: #166534;
}

.tracking-banner code {
    background: #dcfce7;
    padding: 0.2rem 0.5rem;
    border-radius: 4px;
    font-size: 0.9rem;
}

/* Grid Layout */
.order-grid {
    display: grid;
    grid-template-columns: 1fr 360px;
    gap: 1.5rem;
}

.card {
    background: var(--bg-surface);
    border: 1px solid var(--border-color);
    border-radius: var(--radius-lg);
    padding: 1.5rem;
    margin-bottom: 1.5rem;
}

.card h3 {
    font-size: 1.05rem;
    font-weight: 700;
    margin-bottom: 1.25rem;
}

.table-row {
    display: flex;
    align-items: center;
    gap: 1rem;
    padding: 1rem 0;
    border-bottom: 1px solid var(--border-color);
}

.table-row:last-child {
    border-bottom: none;
}

.product-thumb {
    width: 56px;
    height: 56px;
    background: #f1f5f9;
    border-radius: var(--radius-sm);
    overflow: hidden;
    flex-shrink: 0;
}

.product-thumb img {
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

.product-info {
    flex: 1;
    min-width: 0;
}

.product-title {
    font-size: 0.95rem;
    font-weight: 600;
    display: block;
    color: var(--text-main);
}

.product-title.link:hover {
    color: var(--primary);
}

.product-unit {
    font-size: 0.8rem;
    color: var(--text-muted);
}

.product-qty {
    font-size: 0.9rem;
    color: var(--text-muted);
    font-weight: 600;
}

.product-line-total {
    font-size: 1rem;
    font-weight: 700;
}

.order-notes-box {
    margin-top: 1.5rem;
    background: #f8fafc;
    border-left: 3px solid var(--primary);
    padding: 0.85rem 1rem;
    border-radius: 0 var(--radius-sm) var(--radius-sm) 0;
}

.notes-label {
    font-size: 0.75rem;
    font-weight: 700;
    text-transform: uppercase;
    color: var(--text-muted);
    display: block;
    margin-bottom: 0.25rem;
}

.snapshot-details p {
    font-size: 0.9rem;
    color: var(--text-muted);
    line-height: 1.4;
}

.snapshot-details strong {
    font-size: 0.95rem;
    color: var(--text-main);
    display: block;
    margin-bottom: 0.25rem;
}

.phone-meta {
    margin-top: 0.5rem;
    font-weight: 500;
}

.info-row {
    display: flex;
    justify-content: space-between;
    font-size: 0.9rem;
    margin-bottom: 0.5rem;
}

.calc-line {
    display: flex;
    justify-content: space-between;
    font-size: 0.9rem;
    color: var(--text-muted);
    margin-bottom: 0.5rem;
}

.free-badge {
    color: #16a34a;
    font-weight: 600;
}

.total-line {
    border-top: 1px solid var(--border-color);
    padding-top: 0.75rem;
    margin-top: 0.75rem;
    font-size: 1.15rem;
    color: var(--text-main);
}

.total-val {
    color: var(--primary);
    font-size: 1.3rem;
    font-weight: 800;
}

@media (max-width: 860px) {
    .order-grid {
        grid-template-columns: 1fr;
    }
}

/* Print Invoice Styles */
@media print {

    .page-top-bar,
    .btn-print,
    .back-link,
    :deep(.app-header),
    :deep(.app-footer) {
        display: none !important;
    }

    .order-detail-page {
        padding: 0 !important;
        max-width: 100% !important;
    }

    .card,
    .order-header-card,
    .stepper-card {
        box-shadow: none !important;
        border: 1px solid #000 !important;
    }
}
</style>
