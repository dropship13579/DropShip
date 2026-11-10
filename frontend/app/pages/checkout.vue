<!-- frontend/app/pages/checkout.vue -->
<template>
    <div class="checkout-page">
        <div class="checkout-container">
            <div class="checkout-header">
                <NuxtLink to="/cart" class="btn-back-nav" aria-label="Back to Cart">
                    <span class="back-arrow-wrap">
                        <i class="fa-solid fa-arrow-left"></i>
                    </span>
                    <span>Back to Cart</span>
                </NuxtLink>
                <h1>Secure Checkout</h1>
            </div>

            <!-- Empty cart state -->
            <div v-if="!cartLoading && items.length === 0" class="empty-cart-card">
                <h2>Your cart is empty</h2>
                <p>Add some products to your cart before proceeding to checkout.</p>
                <NuxtLink to="/shop" class="btn-shop">Explore Products</NuxtLink>
            </div>

            <!-- Checkout Layout -->
            <div v-else class="checkout-layout">
                <!-- Left: Form Sections -->
                <div class="checkout-main">
                    <!-- Error Notice -->
                    <div v-if="error" class="error-banner">
                        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor"
                            stroke-width="2">
                            <circle cx="12" cy="12" r="10"></circle>
                            <line x1="12" y1="8" x2="12" y2="12"></line>
                            <line x1="12" y1="16" x2="12.01" y2="16"></line>
                        </svg>
                        <span>{{ error }}</span>
                    </div>

                    <!-- Step 1: Shipping Address -->
                    <section class="checkout-section">
                        <div class="section-header">
                            <div class="step-badge">1</div>
                            <h2>Shipping Address</h2>
                            <button type="button" @click="openNewAddressModal" class="btn-add-address">
                                + Add New Address
                            </button>
                        </div>

                        <div v-if="addressLoading" class="section-loading">
                            <LoadingSpinner text="Loading delivery addresses..." />
                        </div>

                        <!-- No addresses yet -->
                        <div v-else-if="addresses.length === 0" class="no-address-box">
                            <p>You don't have any saved shipping addresses yet.</p>
                            <button type="button" @click="openNewAddressModal" class="btn-primary-sm">
                                + Add Delivery Address
                            </button>
                        </div>

                        <!-- Address Radio Cards -->
                        <div v-else class="address-grid">
                            <label v-for="addr in addresses" :key="addr.id" class="address-card"
                                :class="{ 'selected': selectedAddressId === addr.id }">
                                <input type="radio" name="address" :value="addr.id" v-model="selectedAddressId" />
                                <div class="address-card-content">
                                    <div class="addr-top">
                                        <strong>{{ addr.recipient_name }}</strong>
                                        <span v-if="addr.is_default" class="badge-default">Default</span>
                                    </div>
                                    <div class="addr-text">{{ addr.address_line_1 }}</div>
                                    <div v-if="addr.address_line_2" class="addr-text">{{ addr.address_line_2 }}</div>
                                    <div class="addr-text">{{ addr.city }}, {{ addr.state }} {{ addr.postal_code }}
                                    </div>
                                    <div class="addr-text">{{ addr.country }}</div>
                                    <div class="addr-phone">Phone: {{ addr.phone }}</div>
                                </div>
                            </label>
                        </div>
                    </section>

                    <!-- Step 2: Payment Method -->
                    <section class="checkout-section">
                        <div class="section-header">
                            <div class="step-badge">2</div>
                            <h2>Payment Method</h2>
                        </div>

                        <div class="payment-options">
                            <label class="payment-card" :class="{ 'selected': paymentMethod === 'cod' }">
                                <input type="radio" value="cod" v-model="paymentMethod" />
                                <div class="payment-details">
                                    <div class="payment-title">
                                        <strong>Cash on Delivery (COD)</strong>
                                        <span class="badge-pill">Popular</span>
                                    </div>
                                    <p class="payment-desc">Pay in cash when your KyroKart shipment arrives at your
                                        doorstep.</p>
                                </div>
                            </label>

                            <label class="payment-card" :class="{ 'selected': paymentMethod === 'card' }">
                                <input type="radio" value="card" v-model="paymentMethod" />
                                <div class="payment-details">
                                    <div class="payment-title">
                                        <strong>Credit / Debit Card (Sandbox)</strong>
                                    </div>
                                    <p class="payment-desc">Test simulated instant online card payment in development
                                        mode.</p>
                                </div>
                            </label>

                            <label class="payment-card" :class="{ 'selected': paymentMethod === 'bank' }">
                                <input type="radio" value="bank" v-model="paymentMethod" />
                                <div class="payment-details">
                                    <div class="payment-title">
                                        <strong>Bank Direct Transfer</strong>
                                    </div>
                                    <p class="payment-desc">Transfer directly to our account; order will be verified
                                        after dispatch.</p>
                                </div>
                            </label>
                        </div>
                    </section>

                    <!-- Step 3: Order Notes -->
                    <section class="checkout-section">
                        <div class="section-header">
                            <div class="step-badge">3</div>
                            <h2>Delivery Instructions (Optional)</h2>
                        </div>
                        <textarea v-model="customerNotes" rows="3"
                            placeholder="Special instructions for delivery (e.g. Gate code, leave with receptionist, call before arrival)..."
                            class="notes-textarea"></textarea>
                    </section>
                </div>

                <!-- Right: Order Summary Sidebar -->
                <aside class="checkout-sidebar">
                    <div class="summary-box">
                        <h3>Order Summary</h3>

                        <!-- Items Mini List -->
                        <div class="items-list">
                            <div v-for="item in items" :key="item.id" class="summary-item">
                                <div class="item-img-wrap">
                                    <img v-if="item.product.image" :src="item.product.image" :alt="item.product.name" />
                                    <div v-else class="img-fallback">{{ item.product.name.charAt(0) }}</div>
                                    <span class="item-qty-badge">{{ item.quantity }}</span>
                                </div>
                                <div class="item-info">
                                    <div class="item-name">{{ item.product.name }}</div>
                                    <div class="item-unit-price">${{ Number(item.unit_price).toFixed(2) }} each</div>
                                </div>
                                <div class="item-total-price">
                                    ${{ Number(item.line_total).toFixed(2) }}
                                </div>
                            </div>
                        </div>

                        <!-- Promo Coupon Section -->
                        <div class="coupon-section">
                            <label for="coupon-code-input" class="coupon-label">Promo Code</label>
                            <div v-if="!appliedCoupon" class="coupon-input-group">
                                <input id="coupon-code-input" v-model="couponInput" type="text"
                                    placeholder="e.g. WELCOME10, SAVE20" class="coupon-input"
                                    :disabled="validatingCoupon" @keyup.enter.prevent="handleApplyCoupon" />
                                <button type="button" class="btn-apply-coupon"
                                    :disabled="validatingCoupon || !couponInput.trim()" @click="handleApplyCoupon">
                                    {{ validatingCoupon ? 'Applying...' : 'Apply' }}
                                </button>
                            </div>

                            <!-- Applied Coupon State -->
                            <div v-else class="coupon-applied-box">
                                <div class="coupon-applied-info">
                                    <span class="coupon-badge">&#127991; {{ appliedCoupon.code }}</span>
                                    <span class="coupon-savings">Saved ${{
                                        Number(appliedCoupon.discount_amount).toFixed(2) }}</span>
                                </div>
                                <button type="button" @click="handleRemoveCoupon" class="btn-remove-coupon"
                                    title="Remove coupon">
                                    &times;
                                </button>
                            </div>

                            <p v-if="couponError" class="coupon-error-msg">{{ couponError }}</p>
                            <p v-else-if="couponSuccessMsg" class="coupon-success-msg">{{ couponSuccessMsg }}</p>
                        </div>

                        <!-- Calculations Breakdown -->
                        <div class="summary-breakdown">
                            <div class="calc-row">
                                <span>Subtotal ({{ totalItems }} items)</span>
                                <span>${{ Number(subtotal).toFixed(2) }}</span>
                            </div>
                            <div class="calc-row">
                                <span>Shipping</span>
                                <span class="free-tag">Free</span>
                            </div>
                            <div v-if="discountAmount > 0" class="calc-row discount-row">
                                <span>Discount ({{ appliedCoupon?.code }})</span>
                                <span class="discount-val">-${{ Number(discountAmount).toFixed(2) }}</span>
                            </div>
                            <div class="calc-row divider"></div>
                            <div class="calc-row total-row">
                                <strong>Total</strong>
                                <strong class="total-price">${{ Number(finalTotal).toFixed(2) }}</strong>
                            </div>
                        </div>

                        <button type="button" @click="handlePlaceOrder" class="btn-place-order"
                            :disabled="placingOrder || !selectedAddressId || items.length === 0">
                            <span v-if="placingOrder">Processing Order...</span>
                            <span v-else>Place Order &bull; ${{ Number(finalTotal).toFixed(2) }}</span>
                        </button>

                        <!-- Estimated Delivery Countdown -->
                        <DeliveryEstimator :compact="true" />

                        <div class="guarantee-box">
                            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor"
                                stroke-width="2">
                                <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path>
                            </svg>
                            <span>Buyer Protection & Verified Sourcing Included</span>
                        </div>
                    </div>
                </aside>
            </div>
        </div>

        <!-- Address Modal for Adding New Address -->
        <AddressFormModal :is-open="isAddressModalOpen" @close="isAddressModalOpen = false" @saved="onAddressSaved" />
    </div>
</template>

<script setup>
definePageMeta({
    middleware: 'auth'
})

const { items, totalItems, subtotal, loading: cartLoading, refreshCart } = useCartState()
const { getAddresses } = useAccountApi()
const { checkout, validateCoupon } = useOrdersApi()

const addresses = ref([])
const addressLoading = ref(true)
const selectedAddressId = ref(null)
const paymentMethod = ref('cod')
const customerNotes = ref('')

const isAddressModalOpen = ref(false)
const placingOrder = ref(false)
const error = ref('')

// Coupon State
const couponInput = ref('')
const validatingCoupon = ref(false)
const appliedCoupon = ref(null)
const couponError = ref('')
const couponSuccessMsg = ref('')

const discountAmount = computed(() => {
    return appliedCoupon.value ? Number(appliedCoupon.value.discount_amount) : 0
})

const finalTotal = computed(() => {
    return Math.max(0, Number(subtotal.value) - discountAmount.value)
})

async function handleApplyCoupon() {
    const code = couponInput.value.trim().toUpperCase()
    if (!code) return

    validatingCoupon.value = true
    couponError.value = ''
    couponSuccessMsg.value = ''

    try {
        const res = await validateCoupon(code, Number(subtotal.value))
        appliedCoupon.value = res
        couponSuccessMsg.value = res.message || `Coupon ${res.code} applied!`
        couponInput.value = ''
    } catch (err) {
        couponError.value = err.data?.detail || err.message || 'Invalid promotional code.'
        appliedCoupon.value = null
    } finally {
        validatingCoupon.value = false
    }
}

function handleRemoveCoupon() {
    appliedCoupon.value = null
    couponError.value = ''
    couponSuccessMsg.value = ''
}

// Load customer addresses
async function loadAddresses() {
    addressLoading.value = true
    try {
        const data = await getAddresses()
        const list = Array.isArray(data) ? data : (data?.results || [])
        addresses.value = list

        if (addresses.value.length > 0 && !selectedAddressId.value) {
            const defaultAddr = addresses.value.find(a => a?.is_default)
            selectedAddressId.value = defaultAddr ? defaultAddr.id : addresses.value[0]?.id
        }
    } catch (err) {
        console.error('Failed to load addresses:', err)
    } finally {
        addressLoading.value = false
    }
}

function openNewAddressModal() {
    isAddressModalOpen.value = true
}

async function onAddressSaved() {
    await loadAddresses()
    if (addresses.value.length > 0) {
        selectedAddressId.value = addresses.value[0].id
    }
}

async function handlePlaceOrder() {
    if (!selectedAddressId.value) {
        error.value = 'Please select a delivery address.'
        return
    }

    placingOrder.value = true
    error.value = ''

    try {
        const payload = {
            address_id: selectedAddressId.value,
            payment_method: paymentMethod.value,
            customer_notes: customerNotes.value.trim(),
            coupon_code: appliedCoupon.value ? appliedCoupon.value.code : ''
        }

        const newOrder = await checkout(payload)
        await refreshCart()
        await navigateTo(`/account/orders/${newOrder.order_number}`)
    } catch (err) {
        error.value = err.data?.detail || err.message || 'Failed to complete order. Please review your details and try again.'
    } finally {
        placingOrder.value = false
    }
}

onMounted(async () => {
    await loadAddresses()
})
</script>

<style scoped>
.checkout-page {
    padding: 2.5rem 1.5rem 5rem;
    min-height: 80vh;
}

.checkout-container {
    max-width: 1100px;
    margin: 0 auto;
}

.checkout-header {
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    gap: 0.85rem;
    margin-bottom: 2rem;
}

.checkout-header h1 {
    font-size: 1.85rem;
    font-weight: 800;
}

.empty-cart-card {
    background: var(--bg-surface);
    border: 1px solid var(--border-color);
    border-radius: var(--radius-lg);
    padding: 4rem 2rem;
    text-align: center;
    max-width: 500px;
    margin: 0 auto;
}

.empty-cart-card h2 {
    font-size: 1.5rem;
    margin-bottom: 0.5rem;
}

.empty-cart-card p {
    color: var(--text-muted);
    margin-bottom: 1.5rem;
}

.btn-shop {
    display: inline-block;
    background: var(--primary);
    color: #fff;
    padding: 0.65rem 1.5rem;
    border-radius: var(--radius-md);
    font-weight: 600;
    text-decoration: none;
}

.checkout-layout {
    display: grid;
    grid-template-columns: 1fr 380px;
    gap: 2.5rem;
    align-items: start;
}

.checkout-main {
    display: flex;
    flex-direction: column;
    gap: 2rem;
}

.error-banner {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    background: #fef2f2;
    border: 1px solid #fecaca;
    color: #b91c1c;
    padding: 1rem 1.25rem;
    border-radius: var(--radius-md);
    font-weight: 500;
    font-size: 0.95rem;
}

.checkout-section {
    background: var(--bg-surface);
    border: 1px solid var(--border-color);
    border-radius: var(--radius-lg);
    padding: 1.75rem;
}

.section-header {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    margin-bottom: 1.5rem;
}

.step-badge {
    width: 28px;
    height: 28px;
    border-radius: 50%;
    background: var(--primary);
    color: #fff;
    font-size: 0.85rem;
    font-weight: 700;
    display: flex;
    align-items: center;
    justify-content: center;
}

.section-header h2 {
    font-size: 1.25rem;
    font-weight: 700;
    flex: 1;
}

.btn-add-address {
    background: transparent;
    border: 1px solid var(--primary);
    color: var(--primary);
    font-size: 0.85rem;
    font-weight: 600;
    padding: 0.4rem 0.85rem;
    border-radius: var(--radius-md);
    cursor: pointer;
    transition: all 0.15s;
}

.btn-add-address:hover {
    background: var(--primary);
    color: #fff;
}

.no-address-box {
    text-align: center;
    padding: 2rem;
    background: var(--bg-page);
    border: 1px dashed var(--border-color);
    border-radius: var(--radius-md);
}

.no-address-box p {
    color: var(--text-muted);
    margin-bottom: 1rem;
}

.btn-primary-sm {
    background: var(--primary);
    color: #fff;
    font-size: 0.85rem;
    font-weight: 600;
    padding: 0.5rem 1.25rem;
    border: none;
    border-radius: var(--radius-md);
    cursor: pointer;
}

.address-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 1rem;
}

.address-card {
    display: flex;
    gap: 0.85rem;
    padding: 1.25rem;
    border: 1px solid var(--border-color);
    border-radius: var(--radius-md);
    background: var(--bg-page);
    cursor: pointer;
    transition: all 0.15s;
}

.address-card:hover {
    border-color: var(--primary);
}

.address-card.selected {
    border-color: var(--primary);
    background: rgba(99, 102, 241, 0.04);
}

.address-card input[type="radio"] {
    margin-top: 0.25rem;
    accent-color: var(--primary);
}

.address-card-content {
    font-size: 0.9rem;
    line-height: 1.45;
}

.addr-top {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    margin-bottom: 0.35rem;
}

.badge-default {
    background: var(--primary);
    color: #fff;
    font-size: 0.7rem;
    font-weight: 700;
    padding: 0.1rem 0.4rem;
    border-radius: 9999px;
}

.addr-phone {
    margin-top: 0.4rem;
    color: var(--text-muted);
    font-size: 0.85rem;
}

.payment-options {
    display: flex;
    flex-direction: column;
    gap: 1rem;
}

.payment-card {
    display: flex;
    gap: 1rem;
    padding: 1.25rem;
    border: 1px solid var(--border-color);
    border-radius: var(--radius-md);
    background: var(--bg-page);
    cursor: pointer;
    transition: all 0.15s;
}

.payment-card:hover {
    border-color: var(--primary);
}

.payment-card.selected {
    border-color: var(--primary);
    background: rgba(99, 102, 241, 0.04);
}

.payment-card input[type="radio"] {
    margin-top: 0.25rem;
    accent-color: var(--primary);
}

.payment-title {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    margin-bottom: 0.25rem;
}

.badge-pill {
    background: #10b981;
    color: #fff;
    font-size: 0.7rem;
    font-weight: 700;
    padding: 0.1rem 0.45rem;
    border-radius: 9999px;
}

.payment-desc {
    font-size: 0.85rem;
    color: var(--text-muted);
}

.notes-textarea {
    width: 100%;
    padding: 0.85rem;
    font-size: 0.9rem;
    border: 1px solid var(--border-color);
    border-radius: var(--radius-md);
    background: var(--bg-page);
    color: var(--text-main);
    resize: vertical;
}

.notes-textarea:focus {
    outline: none;
    border-color: var(--primary);
}

.checkout-sidebar {
    position: sticky;
    top: 2rem;
}

.summary-box {
    background: var(--bg-surface);
    border: 1px solid var(--border-color);
    border-radius: var(--radius-lg);
    padding: 1.75rem;
}

.summary-box h3 {
    font-size: 1.2rem;
    font-weight: 700;
    margin-bottom: 1.25rem;
}

.items-list {
    display: flex;
    flex-direction: column;
    gap: 0.85rem;
    margin-bottom: 1.25rem;
    max-height: 240px;
    overflow-y: auto;
}

.summary-item {
    display: flex;
    align-items: center;
    gap: 0.85rem;
}

.item-img-wrap {
    position: relative;
    width: 44px;
    height: 44px;
    border-radius: var(--radius-sm);
    overflow: hidden;
    background: #f1f5f9;
    flex-shrink: 0;
}

.item-img-wrap img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.img-fallback {
    width: 100%;
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 700;
    color: var(--text-muted);
}

.item-qty-badge {
    position: absolute;
    top: -4px;
    right: -4px;
    background: var(--text-main);
    color: var(--bg-surface);
    font-size: 0.65rem;
    font-weight: 700;
    width: 16px;
    height: 16px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
}

.item-info {
    flex: 1;
    min-width: 0;
}

.item-name {
    font-size: 0.85rem;
    font-weight: 600;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

.item-unit-price {
    font-size: 0.75rem;
    color: var(--text-muted);
}

.item-total-price {
    font-size: 0.85rem;
    font-weight: 700;
}

/* Coupon Styles */
.coupon-section {
    padding: 1rem 0;
    border-top: 1px solid var(--border-color);
    border-bottom: 1px solid var(--border-color);
    margin-bottom: 1.25rem;
}

.coupon-label {
    display: block;
    font-size: 0.82rem;
    font-weight: 600;
    color: var(--text-muted);
    margin-bottom: 0.4rem;
}

.coupon-input-group {
    display: flex;
    gap: 0.5rem;
}

.coupon-input {
    flex: 1;
    padding: 0.55rem 0.75rem;
    font-size: 0.85rem;
    border: 1px solid var(--border-color);
    border-radius: var(--radius-sm);
    text-transform: uppercase;
    font-weight: 700;
    background: var(--bg-page);
    color: var(--text-main);
    letter-spacing: 0.05em;
}

.coupon-input:focus {
    outline: none;
    border-color: var(--primary);
    box-shadow: 0 0 0 2px rgba(99, 102, 241, 0.15);
}

.btn-apply-coupon {
    padding: 0.55rem 1rem;
    font-size: 0.85rem;
    font-weight: 600;
    background: var(--primary);
    color: #fff;
    border: none;
    border-radius: var(--radius-sm);
    cursor: pointer;
    transition: background 0.15s;
}

.btn-apply-coupon:hover:not(:disabled) {
    background: var(--primary-hover, #4f46e5);
}

.btn-apply-coupon:disabled {
    opacity: 0.6;
    cursor: not-allowed;
}

.coupon-applied-box {
    display: flex;
    align-items: center;
    justify-content: space-between;
    background: #ecfdf5;
    border: 1px solid #a7f3d0;
    padding: 0.55rem 0.85rem;
    border-radius: var(--radius-sm);
}

.coupon-applied-info {
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.coupon-badge {
    font-size: 0.85rem;
    font-weight: 700;
    color: #065f46;
}

.coupon-savings {
    font-size: 0.78rem;
    font-weight: 600;
    color: #059669;
}

.btn-remove-coupon {
    background: transparent;
    border: none;
    font-size: 1.25rem;
    line-height: 1;
    color: #047857;
    cursor: pointer;
    padding: 0.1rem 0.35rem;
    border-radius: var(--radius-sm);
}

.btn-remove-coupon:hover {
    background: #d1fae5;
    color: #064e3b;
}

.coupon-error-msg {
    margin-top: 0.4rem;
    font-size: 0.78rem;
    color: #dc2626;
    font-weight: 500;
}

.coupon-success-msg {
    margin-top: 0.4rem;
    font-size: 0.78rem;
    color: #059669;
    font-weight: 500;
}

/* Calculations Breakdown */
.summary-breakdown {
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
    margin-bottom: 1.5rem;
}

.calc-row {
    display: flex;
    justify-content: space-between;
    font-size: 0.9rem;
    color: var(--text-muted);
}

.free-tag {
    color: #10b981;
    font-weight: 700;
}

.calc-row.discount-row {
    color: #059669;
    font-weight: 600;
}

.discount-val {
    color: #059669;
    font-weight: 700;
}

.calc-row.divider {
    height: 1px;
    background: var(--border-color);
    margin: 0.25rem 0;
}

.calc-row.total-row {
    color: var(--text-main);
    font-size: 1.15rem;
}

.total-price {
    color: var(--primary);
    font-weight: 800;
}

.btn-place-order {
    width: 100%;
    background: var(--primary);
    color: #fff;
    padding: 0.9rem;
    font-size: 1rem;
    font-weight: 700;
    border: none;
    border-radius: var(--radius-md);
    cursor: pointer;
    transition: background 0.15s;
    margin-bottom: 1.25rem;
}

.btn-place-order:hover:not(:disabled) {
    background: var(--primary-hover, #4f46e5);
}

.btn-place-order:disabled {
    opacity: 0.6;
    cursor: not-allowed;
}

.guarantee-box {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    font-size: 0.78rem;
    color: var(--text-muted);
    justify-content: center;
}

.guarantee-box svg {
    color: #10b981;
    flex-shrink: 0;
}

@media (max-width: 900px) {
    .checkout-layout {
        grid-template-columns: 1fr;
    }

    .address-grid {
        grid-template-columns: 1fr;
    }

    .checkout-sidebar {
        position: static;
    }
}
</style>
