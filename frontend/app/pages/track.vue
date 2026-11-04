<!-- frontend/app/pages/track.vue -->
<template>
    <div class="track-page">
        <div class="container">
            <!-- Hero Header -->
            <div class="hero-section">
                <span class="badge-pill">Dropship Live Tracking</span>
                <h1>Track Your Shipment</h1>
                <p class="subtitle">Enter your Order Number and Account Email below for real-time warehouse sourcing &
                    delivery updates.</p>
            </div>

            <!-- Tracking Lookup Form Card -->
            <div class="lookup-card">
                <form @submit.prevent="handleTrack" class="lookup-form">
                    <div class="form-grid">
                        <div class="form-group">
                            <label for="order-num">Order Number</label>
                            <input id="order-num" v-model="orderNumber" type="text" placeholder="e.g. ORD-20261024-XXXX"
                                required class="form-input code-input" />
                        </div>

                        <div class="form-group">
                            <label for="order-email">Customer Email</label>
                            <input id="order-email" v-model="email" type="email" placeholder="e.g. customer@example.com"
                                required class="form-input" />
                        </div>
                    </div>

                    <div v-if="error" class="error-banner">
                        {{ error }}
                    </div>

                    <button type="submit" class="btn-track" :disabled="loading">
                        <span v-if="loading">Locating Shipment...</span>
                        <span v-else>Track Package &rarr;</span>
                    </button>
                </form>
            </div>

            <!-- SHIPMENT RESULTS CARD -->
            <div v-if="shipment" class="result-card">
                <!-- Result Header -->
                <div class="result-header">
                    <div>
                        <span class="order-tag">Order {{ shipment.order_number }}</span>
                        <h2>Shipment Status: {{ shipment.order_status_display }}</h2>
                        <p class="destination-text">
                            Delivering to <strong>{{ shipment.recipient_name }}</strong> &bull; {{ shipment.city }}, {{
                            shipment.country }}
                        </p>
                    </div>

                    <!-- Carrier Tracking Code Callout -->
                    <div class="tracking-code-badge" v-if="shipment.tracking_number">
                        <span class="badge-sub">Carrier Tracking Code</span>
                        <div class="code-copy-row">
                            <strong class="code-val">{{ shipment.tracking_number }}</strong>
                            <button type="button" @click="copyTracking" class="btn-copy">
                                {{ copied ? 'Copied!' : 'Copy' }}
                            </button>
                        </div>
                    </div>
                    <div v-else class="tracking-pending-note">
                        <span>Carrier tracking code will be assigned upon dispatch.</span>
                    </div>
                </div>

                <!-- PROGRESS STEPPER TIMELINE -->
                <div class="stepper-timeline">
                    <div class="stepper-track">
                        <div class="stepper-fill"
                            :style="{ width: `${(shipment.current_step_index / (shipment.status_steps.length - 1)) * 100}%` }">
                        </div>
                    </div>

                    <div class="steps-row">
                        <div v-for="(step, idx) in shipment.status_steps" :key="step.key" class="step-item" :class="{
                            completed: idx < shipment.current_step_index,
                            current: idx === shipment.current_step_index,
                            upcoming: idx > shipment.current_step_index
                        }">
                            <div class="step-indicator">
                                <span v-if="idx < shipment.current_step_index">&#10003;</span>
                                <span v-else-if="idx === shipment.current_step_index">&#9679;</span>
                                <span v-else>{{ idx + 1 }}</span>
                            </div>
                            <div class="step-info">
                                <strong class="step-label">{{ step.label }}</strong>
                                <p class="step-desc">{{ step.desc }}</p>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- PACKAGE ITEMS SNAPSHOT -->
                <div class="package-contents">
                    <h3>Package Contents ({{ shipment.items?.length }} items)</h3>
                    <div class="items-list">
                        <div v-for="(it, idx) in shipment.items" :key="idx" class="package-item">
                            <div class="item-img-wrap">
                                <img v-if="it.product_image" :src="it.product_image" :alt="it.product_name" />
                                <span v-else class="img-fallback">{{ it.product_name[0] }}</span>
                            </div>
                            <div class="item-details">
                                <strong>{{ it.product_name }}</strong>
                                <span class="item-qty">Quantity: {{ it.quantity }}</span>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Support Footer -->
                <div class="support-footer">
                    <span>Need help with your delivery?</span>
                    <NuxtLink to="/shop" class="support-link">Contact Support &rarr;</NuxtLink>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
const route = useRoute()
const { user, isAuthenticated } = useAuthState()
const { trackOrderPublic } = useOrdersApi()

const orderNumber = ref('')
const email = ref('')
const loading = ref(false)
const error = ref('')
const shipment = ref(null)
const copied = ref(false)

// Prefill from query params or auth state
onMounted(() => {
    if (route.query.order) {
        orderNumber.value = String(route.query.order).trim()
    }
    if (route.query.email) {
        email.value = String(route.query.email).trim()
    } else if (isAuthenticated.value && user.value?.email) {
        email.value = user.value.email
    }

    // Auto-search if both params exist
    if (orderNumber.value && email.value) {
        handleTrack()
    }
})

async function handleTrack() {
    const ord = orderNumber.value.trim().toUpperCase()
    const em = email.value.trim().toLowerCase()

    if (!ord || !em) {
        error.value = 'Please provide both your Order Number and Email address.'
        return
    }

    loading.value = true
    error.value = ''
    shipment.value = null

    try {
        const data = await trackOrderPublic(ord, em)
        shipment.value = data
    } catch (err) {
        error.value = err.data?.detail || err.message || 'No shipment found with those credentials. Please check for typos.'
    } finally {
        loading.value = false
    }
}

function copyTracking() {
    if (!shipment.value?.tracking_number) return
    navigator.clipboard.writeText(shipment.value.tracking_number)
    copied.value = true
    setTimeout(() => { copied.value = false }, 2500)
}
</script>

<style scoped>
.track-page {
    padding: 3.5rem 1.5rem 6rem;
    min-height: 85vh;
    background: var(--bg-page);
}

.container {
    max-width: 900px;
    margin: 0 auto;
}

.hero-section {
    text-align: center;
    margin-bottom: 2.5rem;
}

.badge-pill {
    display: inline-block;
    background: #dbeafe;
    color: #1e40af;
    font-size: 0.75rem;
    font-weight: 700;
    text-transform: uppercase;
    padding: 0.25rem 0.75rem;
    border-radius: 9999px;
    margin-bottom: 0.75rem;
}

.hero-section h1 {
    font-size: 2.25rem;
    font-weight: 800;
    letter-spacing: -0.02em;
    margin-bottom: 0.5rem;
}

.subtitle {
    color: var(--text-muted);
    font-size: 1rem;
    max-width: 600px;
    margin: 0 auto;
}

/* Lookup Form Card */
.lookup-card {
    background: var(--bg-surface);
    border: 1px solid var(--border-color);
    border-radius: var(--radius-lg);
    padding: 2rem;
    box-shadow: var(--shadow-sm);
    margin-bottom: 2.5rem;
}

.form-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 1.5rem;
    margin-bottom: 1.5rem;
}

.form-group label {
    display: block;
    font-size: 0.85rem;
    font-weight: 600;
    color: var(--text-main);
    margin-bottom: 0.4rem;
}

.form-input {
    width: 100%;
    padding: 0.75rem 0.95rem;
    border: 1px solid var(--border-color);
    border-radius: var(--radius-md);
    font-size: 0.95rem;
    background: var(--bg-page);
    color: var(--text-main);
    outline: none;
}

.form-input:focus {
    border-color: var(--primary);
    box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.15);
}

.code-input {
    text-transform: uppercase;
    font-family: monospace;
    font-weight: 700;
}

.error-banner {
    background: #fef2f2;
    border: 1px solid #fecaca;
    color: #b91c1c;
    padding: 0.85rem 1.25rem;
    border-radius: var(--radius-md);
    margin-bottom: 1.25rem;
    font-size: 0.9rem;
    font-weight: 500;
}

.btn-track {
    width: 100%;
    background: var(--primary);
    color: #fff;
    border: none;
    padding: 0.9rem;
    border-radius: var(--radius-md);
    font-size: 1rem;
    font-weight: 700;
    cursor: pointer;
    transition: background 0.15s;
}

.btn-track:hover:not(:disabled) {
    background: var(--primary-hover, #4f46e5);
}

.btn-track:disabled {
    opacity: 0.6;
    cursor: not-allowed;
}

/* Result Card */
.result-card {
    background: var(--bg-surface);
    border: 1px solid var(--border-color);
    border-radius: var(--radius-lg);
    padding: 2.5rem;
    box-shadow: var(--shadow-md);
    animation: fadeIn 0.25s ease-out;
}

@keyframes fadeIn {
    from {
        opacity: 0;
        transform: translateY(8px);
    }

    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.result-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    padding-bottom: 2rem;
    border-bottom: 1px solid var(--border-color);
    margin-bottom: 2.5rem;
    gap: 1.5rem;
}

.order-tag {
    display: inline-block;
    font-family: monospace;
    font-size: 0.8rem;
    font-weight: 700;
    background: #f1f5f9;
    color: var(--text-muted);
    padding: 0.2rem 0.55rem;
    border-radius: 4px;
    margin-bottom: 0.5rem;
}

.result-header h2 {
    font-size: 1.5rem;
    font-weight: 800;
    margin-bottom: 0.35rem;
}

.destination-text {
    font-size: 0.9rem;
    color: var(--text-muted);
}

.tracking-code-badge {
    background: #ecfdf5;
    border: 1px solid #a7f3d0;
    padding: 0.75rem 1rem;
    border-radius: var(--radius-md);
    text-align: right;
}

.badge-sub {
    display: block;
    font-size: 0.72rem;
    font-weight: 700;
    text-transform: uppercase;
    color: #065f46;
    margin-bottom: 0.25rem;
}

.code-copy-row {
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.code-val {
    font-family: monospace;
    font-size: 0.95rem;
    font-weight: 800;
    color: #065f46;
}

.btn-copy {
    background: #10b981;
    color: #fff;
    border: none;
    font-size: 0.75rem;
    font-weight: 700;
    padding: 0.25rem 0.6rem;
    border-radius: 4px;
    cursor: pointer;
}

.tracking-pending-note {
    font-size: 0.82rem;
    color: var(--text-muted);
    font-style: italic;
    max-width: 240px;
    text-align: right;
}

/* Stepper Timeline */
.stepper-timeline {
    position: relative;
    margin: 3rem 0;
}

.stepper-track {
    position: absolute;
    top: 18px;
    left: 36px;
    right: 36px;
    height: 4px;
    background: #e2e8f0;
    z-index: 1;
}

.stepper-fill {
    height: 100%;
    background: #10b981;
    transition: width 0.4s ease;
}

.steps-row {
    position: relative;
    display: flex;
    justify-content: space-between;
    z-index: 2;
}

.step-item {
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
    width: 140px;
}

.step-indicator {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 800;
    font-size: 0.9rem;
    background: #f1f5f9;
    color: #64748b;
    border: 3px solid #fff;
    box-shadow: 0 0 0 2px #e2e8f0;
    margin-bottom: 0.75rem;
    transition: all 0.2s;
}

.step-item.completed .step-indicator {
    background: #10b981;
    color: #fff;
    box-shadow: 0 0 0 2px #10b981;
}

.step-item.current .step-indicator {
    background: var(--primary);
    color: #fff;
    box-shadow: 0 0 0 4px rgba(99, 102, 241, 0.2);
    transform: scale(1.1);
}

.step-label {
    display: block;
    font-size: 0.88rem;
    color: var(--text-main);
    margin-bottom: 0.2rem;
}

.step-desc {
    font-size: 0.72rem;
    color: var(--text-muted);
    line-height: 1.3;
}

/* Package Contents */
.package-contents {
    padding-top: 2rem;
    border-top: 1px solid var(--border-color);
    margin-bottom: 2rem;
}

.package-contents h3 {
    font-size: 1.05rem;
    font-weight: 700;
    margin-bottom: 1rem;
}

.items-list {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 1rem;
}

.package-item {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    padding: 0.75rem;
    background: var(--bg-page);
    border: 1px solid var(--border-color);
    border-radius: var(--radius-md);
}

.item-img-wrap {
    width: 48px;
    height: 48px;
    border-radius: var(--radius-sm);
    background: #e2e8f0;
    overflow: hidden;
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

.item-details strong {
    display: block;
    font-size: 0.85rem;
    line-height: 1.3;
}

.item-qty {
    font-size: 0.75rem;
    color: var(--text-muted);
}

/* Support Footer */
.support-footer {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding-top: 1.5rem;
    border-top: 1px solid var(--border-color);
    font-size: 0.85rem;
    color: var(--text-muted);
}

.support-link {
    color: var(--primary);
    font-weight: 600;
    text-decoration: none;
}

@media (max-width: 768px) {
    .form-grid {
        grid-template-columns: 1fr;
    }

    .result-header {
        flex-direction: column;
    }

    .tracking-code-badge {
        text-align: left;
        width: 100%;
    }

    .steps-row {
        flex-direction: column;
        gap: 1.5rem;
        align-items: flex-start;
    }

    .stepper-track {
        display: none;
    }

    .step-item {
        flex-direction: row;
        gap: 1rem;
        text-align: left;
        width: 100%;
    }

    .items-list {
        grid-template-columns: 1fr;
    }
}
</style>
