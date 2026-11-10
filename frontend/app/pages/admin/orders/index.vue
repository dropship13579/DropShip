<!-- frontend/app/pages/admin/orders/index.vue -->
<template>
    <div class="admin-workstation-page">
        <div class="workstation-container">
            <!-- Page Header & Metrics Summary -->
            <div class="header-section">
                <div>
                    <span class="badge-staff">Fulfillment Station</span>
                    <h1>Order Packaging & Parcel Tracking</h1>
                    <p class="subtitle">Assign carrier tracking codes, manage packaging stages, and monitor customer
                        orders.</p>
                </div>

                <div class="header-actions">
                    <button @click="loadOrders" class="btn-refresh" :disabled="loading">
                        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor"
                            stroke-width="2">
                            <path d="M23 4v6h-6"></path>
                            <path d="M1 20v-6h6"></path>
                            <path d="M3.51 9a9 9 0 0 1 14.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0 0 20.49 15"></path>
                        </svg>
                        <span>{{ loading ? 'Syncing...' : 'Refresh Feed' }}</span>
                    </button>
                </div>
            </div>

            <!-- Quick Metrics Ribbon -->
            <div class="metrics-ribbon">
                <div class="metric-chip" :class="{ active: currentStatus === '' }" @click="setStatusFilter('')">
                    <span class="chip-label">All Orders</span>
                    <span class="chip-count">{{ orders.length }}</span>
                </div>
                <div class="metric-chip pending-chip" :class="{ active: currentStatus === 'pending' }"
                    @click="setStatusFilter('pending')">
                    <span class="chip-label">Placed</span>
                    <span class="chip-count">{{ getCountByStatus('pending') }}</span>
                </div>
                <div class="metric-chip processing-chip" :class="{ active: currentStatus === 'processing' }"
                    @click="setStatusFilter('processing')">
                    <span class="chip-label">Sourcing / Packing</span>
                    <span class="chip-count">{{ getCountByStatus('processing') }}</span>
                </div>
                <div class="metric-chip shipped-chip" :class="{ active: currentStatus === 'shipped' }"
                    @click="setStatusFilter('shipped')">
                    <span class="chip-label">In Transit</span>
                    <span class="chip-count">{{ getCountByStatus('shipped') }}</span>
                </div>
                <div class="metric-chip delivered-chip" :class="{ active: currentStatus === 'delivered' }"
                    @click="setStatusFilter('delivered')">
                    <span class="chip-label">Delivered</span>
                    <span class="chip-count">{{ getCountByStatus('delivered') }}</span>
                </div>
            </div>

            <!-- Filters & Search Toolbar -->
            <div class="toolbar-card">
                <div class="search-box">
                    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <circle cx="11" cy="11" r="8"></circle>
                        <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
                    </svg>
                    <input v-model="searchQuery" type="text"
                        placeholder="Search by Order #, Recipient name, or Tracking Code..." @input="debounceSearch" />
                    <button v-if="searchQuery" @click="searchQuery = ''; loadOrders()"
                        class="btn-clear-search">&times;</button>
                </div>

                <div class="filter-controls">
                    <div class="filter-group">
                        <label>Payment</label>
                        <select v-model="paymentFilter" @change="loadOrders">
                            <option value="">All Payment Statuses</option>
                            <option value="paid">Paid</option>
                            <option value="pending">Pending</option>
                            <option value="unpaid">Unpaid</option>
                            <option value="refunded">Refunded</option>
                        </select>
                    </div>
                </div>
            </div>

            <!-- Feedback Banner -->
            <div v-if="updateFeedback" class="feedback-banner">
                {{ updateFeedback }}
            </div>

            <!-- Loading State -->
            <div v-if="loading" class="loading-wrap">
                <LoadingSpinner text="Connecting to order streams..." />
            </div>

            <!-- Empty State -->
            <div v-else-if="filteredOrders.length === 0" class="empty-orders-card">
                <div class="empty-icon-box"><i class="fa-solid fa-box-open"></i></div>
                <h3>No matching orders found</h3>
                <p>No customer orders matched your search or status filters.</p>
                <button @click="resetFilters" class="btn-reset">Reset Filters</button>
            </div>

            <!-- Orders Workstation Table -->
            <div v-else class="orders-table-card">
                <table class="workstation-table">
                    <thead>
                        <tr>
                            <th>Order ID & Date</th>
                            <th>Customer & Shipping</th>
                            <th>Items Ordered</th>
                            <th>Financials</th>
                            <th>Fulfillment Status</th>
                            <th>Payment</th>
                            <th>Tracking Code</th>
                            <th>Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="ord in filteredOrders" :key="ord.id" class="order-row">
                            <!-- Order ID & Date -->
                            <td class="col-id">
                                <strong class="order-number">{{ ord.order_number }}</strong>
                                <span class="order-date">{{ formatDate(ord.created_at) }}</span>
                            </td>

                            <!-- Customer & Shipping Snapshot -->
                            <td class="col-customer">
                                <strong class="recipient-name">{{ ord.shipping_address_snapshot?.recipient_name ||
                                    'Customer' }}</strong>
                                <span class="dest-city">{{ ord.shipping_address_snapshot?.city }}, {{
                                    ord.shipping_address_snapshot?.country }}</span>
                                <span class="customer-phone">{{ ord.shipping_address_snapshot?.phone }}</span>
                            </td>

                            <!-- Items Mini Thumbnails -->
                            <td class="col-items">
                                <div class="items-preview-strip">
                                    <div v-for="it in ord.items?.slice(0, 3)" :key="it.id" class="item-thumb-box"
                                        :title="`${it.quantity}x ${it.product_name_snapshot}`">
                                        <img v-if="it.product_image_snapshot" :src="it.product_image_snapshot"
                                            :alt="it.product_name_snapshot" />
                                        <span v-else class="thumb-fallback">{{ it.product_name_snapshot?.[0] }}</span>
                                        <span class="thumb-qty">{{ it.quantity }}</span>
                                    </div>
                                    <span v-if="ord.items?.length > 3" class="more-items-badge">+{{ ord.items.length - 3
                                        }}</span>
                                </div>
                                <span class="items-count-text">{{ ord.items?.length }} line item(s)</span>
                            </td>

                            <!-- Financials & Applied Coupon -->
                            <td class="col-financials">
                                <strong class="total-val">${{ Number(ord.total_amount).toFixed(2) }}</strong>
                                <div v-if="ord.coupon_code" class="coupon-chip"
                                    :title="`Saved $${ord.discount_amount}`">
                                    <i class="fa-solid fa-tag"></i> {{ ord.coupon_code }}
                                </div>
                                <span class="pay-method-text">{{ ord.payment_method_display }}</span>
                            </td>

                            <!-- Inline Fulfillment Status Control -->
                            <td class="col-status">
                                <select :value="ord.order_status" @change="handleStatusChange(ord, $event.target.value)"
                                    class="status-select" :class="`status-${ord.order_status}`">
                                    <option value="pending">Order Placed</option>
                                    <option value="confirmed">Confirmed</option>
                                    <option value="processing">Processing & Sourcing</option>
                                    <option value="shipped">Shipped / In Transit</option>
                                    <option value="delivered">Delivered</option>
                                    <option value="cancelled">Cancelled</option>
                                </select>
                            </td>

                            <!-- Payment Status -->
                            <td class="col-payment">
                                <select :value="ord.payment_status"
                                    @change="handlePaymentChange(ord, $event.target.value)" class="payment-select"
                                    :class="`pay-${ord.payment_status}`">
                                    <option value="unpaid">Unpaid</option>
                                    <option value="pending">Pending</option>
                                    <option value="paid">Paid</option>
                                    <option value="refunded">Refunded</option>
                                </select>
                            </td>

                            <!-- KyroKart Tracking Number -->
                            <td class="col-tracking">
                                <div class="tracking-edit-box">
                                    <input type="text" :value="editingTracking[ord.order_number] ?? ord.tracking_number"
                                        @input="onTrackingInput(ord.order_number, $event.target.value)"
                                        placeholder="e.g. USPS-9400..." class="tracking-input" />
                                    <button v-if="hasTrackingChanged(ord)" @click="saveTracking(ord)"
                                        class="btn-save-track" title="Save Tracking Number">
                                        <i class="fa-solid fa-check"></i>
                                    </button>
                                </div>
                            </td>

                            <!-- Actions: Inspect Modal / Packing Slip -->
                            <td class="col-actions">
                                <button @click="openInspectModal(ord)" class="btn-inspect"
                                    title="Inspect Order Details">
                                    Inspect &rarr;
                                </button>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>

            <!-- ORDER INSPECT & PACKING SLIP MODAL -->
            <div v-if="inspectingOrder" class="modal-overlay" @click.self="inspectingOrder = null">
                <div class="inspect-modal-card">
                    <div class="modal-header">
                        <div>
                            <span class="modal-sub">KyroKart Packing Slip</span>
                            <h2>{{ inspectingOrder.order_number }}</h2>
                        </div>
                        <div class="header-modal-actions">
                            <button @click="printModal" class="btn-print">Print Slip</button>
                            <button @click="inspectingOrder = null" class="btn-close-modal">&times;</button>
                        </div>
                    </div>

                    <div class="modal-body" id="printable-slip">
                        <!-- Order Meta Grid -->
                        <div class="meta-grid">
                            <div class="meta-box">
                                <h4>Customer Account</h4>
                                <p><strong>Username:</strong> {{ inspectingOrder.user?.username || 'Customer' }}</p>
                                <p><strong>Ordered on:</strong> {{ formatDate(inspectingOrder.created_at) }}</p>
                                <p><strong>Payment:</strong> {{ inspectingOrder.payment_method_display }} ({{
                                    inspectingOrder.payment_status_display }})</p>
                            </div>

                            <div class="meta-box">
                                <h4>Recipient Delivery Snapshot</h4>
                                <strong>{{ inspectingOrder.shipping_address_snapshot?.recipient_name }}</strong>
                                <p>{{ inspectingOrder.shipping_address_snapshot?.address_line_1 }}</p>
                                <p v-if="inspectingOrder.shipping_address_snapshot?.address_line_2">
                                    {{ inspectingOrder.shipping_address_snapshot?.address_line_2 }}
                                </p>
                                <p>{{ inspectingOrder.shipping_address_snapshot?.city }}, {{
                                    inspectingOrder.shipping_address_snapshot?.state }} {{
                                        inspectingOrder.shipping_address_snapshot?.postal_code }}</p>
                                <p>{{ inspectingOrder.shipping_address_snapshot?.country }}</p>
                                <p class="phone-meta">Phone: {{ inspectingOrder.shipping_address_snapshot?.phone }}</p>
                            </div>
                        </div>

                        <!-- Customer Delivery Notes -->
                        <div v-if="inspectingOrder.customer_notes" class="notes-callout">
                            <strong>Customer Delivery Instructions:</strong>
                            <p>{{ inspectingOrder.customer_notes }}</p>
                        </div>

                        <!-- Items Ordered Table -->
                        <div class="modal-items-table-wrap">
                            <table class="modal-items-table">
                                <thead>
                                    <tr>
                                        <th>Item Description</th>
                                        <th>Unit Price</th>
                                        <th>Qty</th>
                                        <th>Total</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr v-for="it in inspectingOrder.items" :key="it.id">
                                        <td>
                                            <strong>{{ it.product_name_snapshot }}</strong>
                                        </td>
                                        <td>${{ Number(it.unit_price).toFixed(2) }}</td>
                                        <td>&times; {{ it.quantity }}</td>
                                        <td><strong>${{ Number(it.line_total).toFixed(2) }}</strong></td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>

                        <!-- Financial Totals -->
                        <div class="modal-totals-block">
                            <div class="total-line">
                                <span>Subtotal:</span>
                                <span>${{ Number(inspectingOrder.subtotal).toFixed(2) }}</span>
                            </div>
                            <div class="total-line">
                                <span>Shipping:</span>
                                <span class="free-text">Free (KyroKart Direct)</span>
                            </div>
                            <div v-if="inspectingOrder.coupon_code" class="total-line discount-line">
                                <span>Coupon Discount ({{ inspectingOrder.coupon_code }}):</span>
                                <span>-${{ Number(inspectingOrder.discount_amount).toFixed(2) }}</span>
                            </div>
                            <div class="total-line grand-total">
                                <strong>Grand Total:</strong>
                                <strong>${{ Number(inspectingOrder.total_amount).toFixed(2) }}</strong>
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
    middleware: 'admin',
    layout: 'admin'
})

const { getOrders, updateOrder } = useAdminApi()

const orders = ref([])
const loading = ref(true)
const searchQuery = ref('')
const currentStatus = ref('')
const paymentFilter = ref('')
const updateFeedback = ref('')

const inspectingOrder = ref(null)
const editingTracking = reactive({})
let searchTimer = null

async function loadOrders() {
    loading.value = true
    try {
        const params = {}
        if (currentStatus.value) params.status = currentStatus.value
        if (paymentFilter.value) params.payment_status = paymentFilter.value
        if (searchQuery.value.trim()) params.search = searchQuery.value.trim()

        const data = await getOrders(params)
        orders.value = Array.isArray(data) ? data : (data?.results || [])
    } catch (err) {
        console.error('Failed to load admin orders:', err)
    } finally {
        loading.value = false
    }
}

const filteredOrders = computed(() => {
    return orders.value
})

function getCountByStatus(statusKey) {
    return orders.value.filter(o => o.order_status === statusKey).length
}

function setStatusFilter(statusKey) {
    currentStatus.value = statusKey
    loadOrders()
}

function resetFilters() {
    searchQuery.value = ''
    currentStatus.value = ''
    paymentFilter.value = ''
    loadOrders()
}

function debounceSearch() {
    clearTimeout(searchTimer)
    searchTimer = setTimeout(() => {
        loadOrders()
    }, 350)
}

function onTrackingInput(orderNumber, val) {
    editingTracking[orderNumber] = val
}

function hasTrackingChanged(ord) {
    const current = editingTracking[ord.order_number]
    return current !== undefined && current !== ord.tracking_number
}

async function saveTracking(ord) {
    const newTracking = editingTracking[ord.order_number]?.trim() || ''
    try {
        const updated = await updateOrder(ord.order_number, { tracking_number: newTracking })
        ord.tracking_number = updated.tracking_number
        delete editingTracking[ord.order_number]
        showFeedback(`Tracking updated for ${ord.order_number}`)
    } catch (err) {
        alert(err.message || 'Failed to update tracking code.')
    }
}

async function handleStatusChange(ord, newStatus) {
    try {
        const updated = await updateOrder(ord.order_number, { order_status: newStatus })
        ord.order_status = updated.order_status
        showFeedback(`Order ${ord.order_number} marked as ${newStatus.toUpperCase()}`)
    } catch (err) {
        alert(err.message || 'Failed to update order status.')
    }
}

async function handlePaymentChange(ord, newPaymentStatus) {
    try {
        const updated = await updateOrder(ord.order_number, { payment_status: newPaymentStatus })
        ord.payment_status = updated.payment_status
        showFeedback(`Payment updated to ${newPaymentStatus.toUpperCase()} for ${ord.order_number}`)
    } catch (err) {
        alert(err.message || 'Failed to update payment status.')
    }
}

function showFeedback(msg) {
    updateFeedback.value = msg
    setTimeout(() => {
        updateFeedback.value = ''
    }, 3500)
}

function openInspectModal(ord) {
    inspectingOrder.value = ord
}

function printModal() {
    window.print()
}

function formatDate(isoStr) {
    if (!isoStr) return ''
    const d = new Date(isoStr)
    return d.toLocaleDateString('en-US', {
        month: 'short',
        day: 'numeric',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    })
}

onMounted(() => {
    loadOrders()
})
</script>

<style scoped>
.admin-workstation-page {
    padding: 2.5rem 1.5rem 5rem;
    background: var(--bg-page);
    min-height: 90vh;
}

.workstation-container {
    max-width: 1400px;
    margin: 0 auto;
}

.header-section {
    display: flex;
    justify-content: space-between;
    align-items: flex-end;
    margin-bottom: 2rem;
}

.badge-staff {
    display: inline-block;
    background: #3b82f6;
    color: #fff;
    font-size: 0.72rem;
    font-weight: 700;
    text-transform: uppercase;
    padding: 0.2rem 0.55rem;
    border-radius: 9999px;
    margin-bottom: 0.5rem;
}

.header-section h1 {
    font-size: 2rem;
    font-weight: 800;
    letter-spacing: -0.02em;
    color: var(--text-main);
}

.subtitle {
    color: var(--text-muted);
    font-size: 0.95rem;
}

.btn-refresh {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    background: var(--bg-surface);
    border: 1px solid var(--border-color);
    color: var(--text-main);
    padding: 0.65rem 1.25rem;
    border-radius: var(--radius-md);
    font-size: 0.9rem;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.15s;
}

.btn-refresh:hover:not(:disabled) {
    border-color: var(--primary);
    color: var(--primary);
}

/* Quick Metrics Ribbon */
.metrics-ribbon {
    display: flex;
    gap: 1rem;
    margin-bottom: 1.5rem;
    overflow-x: auto;
    padding-bottom: 0.5rem;
}

.metric-chip {
    display: flex;
    align-items: center;
    gap: 0.65rem;
    padding: 0.6rem 1.15rem;
    background: var(--bg-surface);
    border: 1px solid var(--border-color);
    border-radius: var(--radius-md);
    cursor: pointer;
    font-size: 0.85rem;
    font-weight: 600;
    color: var(--text-muted);
    transition: all 0.15s;
    white-space: nowrap;
}

.metric-chip:hover {
    border-color: var(--primary);
    color: var(--text-main);
}

.metric-chip.active {
    background: #0f172a;
    border-color: #0f172a;
    color: #fff;
}

.chip-count {
    background: rgba(148, 163, 184, 0.2);
    padding: 0.15rem 0.5rem;
    border-radius: 9999px;
    font-size: 0.75rem;
    font-weight: 700;
}

.metric-chip.active .chip-count {
    background: rgba(255, 255, 255, 0.25);
    color: #fff;
}

/* Toolbar Card */
.toolbar-card {
    background: var(--bg-surface);
    border: 1px solid var(--border-color);
    border-radius: var(--radius-lg);
    padding: 1rem 1.5rem;
    display: flex;
    gap: 1.5rem;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 1.5rem;
}

.search-box {
    display: flex;
    align-items: center;
    gap: 0.65rem;
    background: var(--bg-page);
    border: 1px solid var(--border-color);
    border-radius: var(--radius-md);
    padding: 0.55rem 0.95rem;
    flex: 1;
    max-width: 520px;
}

.search-box input {
    border: none;
    background: transparent;
    width: 100%;
    font-size: 0.9rem;
    outline: none;
    color: var(--text-main);
}

.btn-clear-search {
    background: transparent;
    border: none;
    font-size: 1.15rem;
    color: var(--text-muted);
    cursor: pointer;
}

.filter-controls {
    display: flex;
    gap: 1rem;
}

.filter-group {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    font-size: 0.85rem;
    color: var(--text-muted);
}

.filter-group select {
    padding: 0.5rem 0.85rem;
    border: 1px solid var(--border-color);
    border-radius: var(--radius-sm);
    background: var(--bg-page);
    color: var(--text-main);
    font-size: 0.85rem;
}

.feedback-banner {
    background: #ecfdf5;
    border: 1px solid #a7f3d0;
    color: #065f46;
    padding: 0.75rem 1.25rem;
    border-radius: var(--radius-md);
    margin-bottom: 1.5rem;
    font-size: 0.9rem;
    font-weight: 600;
}

/* Empty State */
.empty-orders-card {
    background: var(--bg-surface);
    border: 1px solid var(--border-color);
    border-radius: var(--radius-lg);
    padding: 4rem 2rem;
    text-align: center;
    max-width: 480px;
    margin: 2rem auto;
}

.empty-icon-box {
    font-size: 2.5rem;
    margin-bottom: 0.75rem;
}

.btn-reset {
    margin-top: 1rem;
    background: var(--primary);
    color: #fff;
    border: none;
    padding: 0.6rem 1.25rem;
    border-radius: var(--radius-md);
    font-weight: 600;
    cursor: pointer;
}

/* Workstation Table */
.orders-table-card {
    background: var(--bg-surface);
    border: 1px solid var(--border-color);
    border-radius: var(--radius-lg);
    overflow-x: auto;
    box-shadow: var(--shadow-sm);
}

.workstation-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 0.88rem;
    text-align: left;
}

.workstation-table th {
    background: #f8fafc;
    padding: 1rem;
    font-size: 0.75rem;
    font-weight: 700;
    text-transform: uppercase;
    color: var(--text-muted);
    border-bottom: 1px solid var(--border-color);
}

.workstation-table td {
    padding: 1rem;
    border-bottom: 1px solid var(--border-color);
    vertical-align: middle;
}

.order-row:hover {
    background: #f8fafc;
}

.order-number {
    display: block;
    font-weight: 700;
    color: var(--text-main);
    font-family: monospace;
    font-size: 0.92rem;
}

.order-date {
    font-size: 0.75rem;
    color: var(--text-muted);
}

.recipient-name {
    display: block;
    font-weight: 700;
}

.dest-city {
    display: block;
    font-size: 0.8rem;
    color: var(--text-muted);
}

.customer-phone {
    display: block;
    font-size: 0.75rem;
    color: var(--text-muted);
}

/* Items Preview */
.items-preview-strip {
    display: flex;
    align-items: center;
    gap: 0.4rem;
    margin-bottom: 0.25rem;
}

.item-thumb-box {
    position: relative;
    width: 34px;
    height: 34px;
    border-radius: var(--radius-sm);
    background: #e2e8f0;
    overflow: hidden;
    border: 1px solid var(--border-color);
}

.item-thumb-box img {
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
    font-size: 0.8rem;
    color: var(--text-muted);
}

.thumb-qty {
    position: absolute;
    top: -2px;
    right: -2px;
    background: #0f172a;
    color: #fff;
    font-size: 0.6rem;
    font-weight: 800;
    width: 14px;
    height: 14px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
}

.more-items-badge {
    font-size: 0.7rem;
    font-weight: 700;
    color: var(--text-muted);
}

.items-count-text {
    font-size: 0.75rem;
    color: var(--text-muted);
}

/* Financials */
.total-val {
    display: block;
    font-weight: 800;
    color: var(--text-main);
    font-size: 0.95rem;
}

.coupon-chip {
    display: inline-block;
    background: #ecfdf5;
    color: #065f46;
    font-size: 0.7rem;
    font-weight: 700;
    padding: 0.1rem 0.4rem;
    border-radius: 4px;
    margin: 0.2rem 0;
}

.pay-method-text {
    display: block;
    font-size: 0.75rem;
    color: var(--text-muted);
}

/* Status Controls */
.status-select,
.payment-select {
    padding: 0.45rem 0.75rem;
    border-radius: var(--radius-sm);
    font-size: 0.82rem;
    font-weight: 700;
    border: 1px solid transparent;
    cursor: pointer;
    outline: none;
}

.status-pending {
    background: #fef3c7;
    color: #92400e;
}

.status-confirmed {
    background: #e0e7ff;
    color: #3730a3;
}

.status-processing {
    background: #f3e8ff;
    color: #6b21a8;
}

.status-shipped {
    background: #dbeafe;
    color: #1e40af;
}

.status-delivered {
    background: #d1fae5;
    color: #065f46;
}

.status-cancelled {
    background: #fee2e2;
    color: #991b1b;
}

.pay-paid {
    background: #d1fae5;
    color: #065f46;
}

.pay-pending {
    background: #fef3c7;
    color: #92400e;
}

.pay-unpaid {
    background: #fee2e2;
    color: #991b1b;
}

.pay-refunded {
    background: #f1f5f9;
    color: #475569;
}

/* Tracking Box */
.tracking-edit-box {
    display: flex;
    align-items: center;
    gap: 0.35rem;
}

.tracking-input {
    padding: 0.45rem 0.65rem;
    font-size: 0.82rem;
    border: 1px solid var(--border-color);
    border-radius: var(--radius-sm);
    background: var(--bg-page);
    color: var(--text-main);
    width: 140px;
}

.tracking-input:focus {
    outline: none;
    border-color: var(--primary);
}

.btn-save-track {
    background: #10b981;
    color: #fff;
    border: none;
    border-radius: var(--radius-sm);
    width: 28px;
    height: 28px;
    font-weight: 800;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
}

.btn-inspect {
    background: var(--bg-page);
    border: 1px solid var(--border-color);
    color: var(--text-main);
    padding: 0.45rem 0.85rem;
    border-radius: var(--radius-sm);
    font-size: 0.8rem;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.15s;
}

.btn-inspect:hover {
    background: var(--primary);
    border-color: var(--primary);
    color: #fff;
}

/* Modal Overlay */
.modal-overlay {
    position: fixed;
    inset: 0;
    background: rgba(15, 23, 42, 0.6);
    backdrop-filter: blur(4px);
    z-index: 100;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 1.5rem;
}

.inspect-modal-card {
    background: var(--bg-surface);
    border: 1px solid var(--border-color);
    border-radius: var(--radius-xl);
    width: 100%;
    max-width: 800px;
    max-height: 90vh;
    overflow-y: auto;
    box-shadow: var(--shadow-xl);
}

.modal-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1.5rem 2rem;
    border-bottom: 1px solid var(--border-color);
}

.modal-sub {
    font-size: 0.75rem;
    font-weight: 700;
    text-transform: uppercase;
    color: var(--text-muted);
}

.header-modal-actions {
    display: flex;
    align-items: center;
    gap: 0.75rem;
}

.btn-print {
    background: #0f172a;
    color: #fff;
    border: none;
    padding: 0.5rem 1rem;
    border-radius: var(--radius-sm);
    font-size: 0.85rem;
    font-weight: 600;
    cursor: pointer;
}

.btn-close-modal {
    background: transparent;
    border: none;
    font-size: 1.75rem;
    line-height: 1;
    color: var(--text-muted);
    cursor: pointer;
}

.modal-body {
    padding: 2rem;
}

.meta-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 1.5rem;
    margin-bottom: 1.5rem;
}

.meta-box {
    background: var(--bg-page);
    padding: 1.25rem;
    border-radius: var(--radius-md);
    font-size: 0.88rem;
    line-height: 1.45;
}

.meta-box h4 {
    font-size: 0.85rem;
    text-transform: uppercase;
    color: var(--text-muted);
    margin-bottom: 0.75rem;
}

.notes-callout {
    background: #fefce8;
    border: 1px solid #fef08a;
    padding: 1rem;
    border-radius: var(--radius-md);
    margin-bottom: 1.5rem;
    font-size: 0.88rem;
    color: #713f12;
}

.modal-items-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 0.88rem;
    margin-bottom: 1.5rem;
}

.modal-items-table th {
    border-bottom: 1px solid var(--border-color);
    padding: 0.65rem 0.5rem;
    font-size: 0.75rem;
    text-transform: uppercase;
    color: var(--text-muted);
    text-align: left;
}

.modal-items-table td {
    padding: 0.85rem 0.5rem;
    border-bottom: 1px solid var(--border-color);
}

.modal-totals-block {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
    max-width: 320px;
    margin-left: auto;
    font-size: 0.9rem;
}

.total-line {
    display: flex;
    justify-content: space-between;
}

.free-text {
    color: #10b981;
    font-weight: 700;
}

.discount-line {
    color: #059669;
    font-weight: 600;
}

.grand-total {
    font-size: 1.15rem;
    border-top: 1px solid var(--border-color);
    padding-top: 0.5rem;
    margin-top: 0.25rem;
    color: var(--primary);
}

@media print {
    body * {
        visibility: hidden;
    }

    #printable-slip,
    #printable-slip * {
        visibility: visible;
    }

    #printable-slip {
        position: absolute;
        left: 0;
        top: 0;
        width: 100%;
    }
}
</style>
