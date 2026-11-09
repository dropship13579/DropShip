<!-- frontend/app/components/CustomerSupportModal.vue -->
<template>
  <Teleport to="body">
    <div v-if="isOpen" class="modal-backdrop" @click.self="close">
      <div class="modal-card" role="dialog" aria-modal="true" aria-labelledby="modal-title">
        <!-- Modal Header -->
        <div class="modal-header">
          <div class="header-info">
            <span class="support-badge">Help & Customer Care</span>
            <h2 id="modal-title">How can we help you?</h2>
          </div>
          <button type="button" class="btn-close" @click="close" aria-label="Close modal">
            &times;
          </button>
        </div>

        <!-- Product Context Badge if opened from product page -->
        <div v-if="productContext" class="product-context-strip">
          <span class="context-tag">Product Context</span>
          <span class="context-name">{{ productContext.name }}</span>
        </div>

        <!-- Navigation Tabs -->
        <div class="modal-tabs">
          <button
            type="button"
            class="tab-btn"
            :class="{ active: activeTab === 'inquiry' }"
            @click="activeTab = 'inquiry'"
          >
            <span class="tab-icon"><i class="fa-solid fa-envelope"></i></span>
            <span>Send Message</span>
          </button>
          <button
            type="button"
            class="tab-btn"
            :class="{ active: activeTab === 'quick' }"
            @click="activeTab = 'quick'"
          >
            <span class="tab-icon"><i class="fa-solid fa-bolt"></i></span>
            <span>Instant Answers</span>
          </button>
          <button
            type="button"
            class="tab-btn"
            :class="{ active: activeTab === 'contact' }"
            @click="activeTab = 'contact'"
          >
            <span class="tab-icon"><i class="fa-solid fa-phone"></i></span>
            <span>Contact Channels</span>
          </button>
        </div>

        <!-- TAB 1: SUBMIT INQUIRY FORM -->
        <div v-if="activeTab === 'inquiry'" class="tab-body">
          <!-- SUCCESS STATE -->
          <div v-if="ticketSuccess" class="success-ticket-box">
            <div class="success-icon-wrap">
              <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
                <polyline points="20 6 9 17 4 12"></polyline>
              </svg>
            </div>
            <h3>Inquiry Submitted Successfully!</h3>
            <p>Our customer support team has received your ticket and is preparing a response.</p>
            
            <div class="ticket-receipt">
              <div class="receipt-row">
                <span class="receipt-label">Ticket Reference:</span>
                <strong class="receipt-code">{{ ticketSuccess.ticket_number }}</strong>
              </div>
              <div class="receipt-row">
                <span class="receipt-label">Response Expected:</span>
                <span class="receipt-val">Within 2 hours to <strong>{{ form.email }}</strong></span>
              </div>
            </div>

            <button type="button" @click="resetAndClose" class="btn-primary-modal">
              Done & Close
            </button>
          </div>

          <!-- SUBMISSION FORM -->
          <form v-else @submit.prevent="handleSubmit" class="inquiry-form">
            <div v-if="submitError" class="error-banner">
              {{ submitError }}
            </div>

            <div class="form-row-2">
              <div class="form-group">
                <label for="supp-name">Your Full Name *</label>
                <input
                  id="supp-name"
                  v-model="form.name"
                  type="text"
                  required
                  placeholder="e.g. Alex Morgan"
                />
              </div>

              <div class="form-group">
                <label for="supp-email">Email Address *</label>
                <input
                  id="supp-email"
                  v-model="form.email"
                  type="email"
                  required
                  placeholder="you@example.com"
                />
              </div>
            </div>

            <div class="form-row-2">
              <div class="form-group">
                <label for="supp-type">Inquiry Topic *</label>
                <select id="supp-type" v-model="form.inquiry_type" required>
                  <option value="product">Product Question & Sizing</option>
                  <option value="order">Order Tracking & Delivery Status</option>
                  <option value="return">30-Day Return & Replacement</option>
                  <option value="general">General Support / Billing</option>
                </select>
              </div>

              <div class="form-group">
                <label for="supp-order">Order Number (Optional)</label>
                <input
                  id="supp-order"
                  v-model="form.order_number"
                  type="text"
                  placeholder="e.g. ORD-20261024-XXXX"
                />
              </div>
            </div>

            <div class="form-group">
              <label for="supp-subject">Subject *</label>
              <input
                id="supp-subject"
                v-model="form.subject"
                type="text"
                required
                placeholder="Brief summary of your question"
              />
            </div>

            <div class="form-group">
              <label for="supp-msg">How can we help? (Details) *</label>
              <textarea
                id="supp-msg"
                v-model="form.message"
                rows="4"
                required
                placeholder="Describe your question or issue in detail..."
              ></textarea>
            </div>

            <div class="modal-footer-actions">
              <button type="button" @click="close" class="btn-secondary-modal">Cancel</button>
              <button type="submit" class="btn-primary-modal" :disabled="submitting">
                <span v-if="submitting">Sending Message...</span>
                <span v-else>Submit Ticket &rarr;</span>
              </button>
            </div>
          </form>
        </div>

        <!-- TAB 2: INSTANT ANSWERS -->
        <div v-else-if="activeTab === 'quick'" class="tab-body quick-answers-tab">
          <div class="search-input-wrap">
            <input
              v-model="quickSearch"
              type="text"
              placeholder="Search instant answers (e.g. tracking, refund, delivery)..."
              class="quick-search-box"
            />
          </div>

          <div class="quick-cards-grid">
            <div
              v-for="item in filteredQuickAnswers"
              :key="item.title"
              class="quick-card"
            >
              <div class="quick-card-head">
                <span class="q-icon"><i :class="item.icon"></i></span>
                <h4>{{ item.title }}</h4>
              </div>
              <p>{{ item.desc }}</p>
              <NuxtLink v-if="item.link" :to="item.link" @click="close" class="quick-link">
                {{ item.linkLabel }} &rarr;
              </NuxtLink>
            </div>
          </div>
        </div>

        <!-- TAB 3: CONTACT CHANNELS -->
        <div v-else class="tab-body contact-tab">
          <div class="channel-cards">
            <div class="channel-card">
              <span class="channel-icon"><i class="fa-solid fa-envelope"></i></span>
              <h4>Email Support</h4>
              <p>For detailed order or billing inquiries.</p>
              <a href="mailto:support@dropshipstore.com" class="channel-action">
                support@dropshipstore.com
              </a>
              <span class="channel-badge">Average reply: &lt; 2 hrs</span>
            </div>

            <div class="channel-card">
              <span class="channel-icon"><i class="fa-solid fa-box-open"></i></span>
              <h4>Live Parcel Tracking</h4>
              <p>Instant real-time warehouse sourcing and carrier checkpoints.</p>
              <NuxtLink to="/track" @click="close" class="channel-action">
                Go to Order Tracker
              </NuxtLink>
              <span class="channel-badge green">Automated & Instant</span>
            </div>

            <div class="channel-card">
              <span class="channel-icon"><i class="fa-solid fa-clock"></i></span>
              <h4>Customer Care Hours</h4>
              <p>Our global fulfillment agents operate around the clock.</p>
              <div class="hours-list">
                <div><strong>Mon – Fri:</strong> 24 Hours Active</div>
                <div><strong>Sat – Sun:</strong> 8:00 AM – 8:00 PM EST</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </Teleport>
</template>

<script setup>
const props = defineProps({
  isOpen: {
    type: Boolean,
    default: false
  },
  productContext: {
    type: Object,
    default: null
  }
})

const emit = defineEmits(['close'])

const { submitInquiry } = useSupportApi()
const { user } = useAuthState()

const activeTab = ref('inquiry')
const submitting = ref(false)
const submitError = ref('')
const ticketSuccess = ref(null)
const quickSearch = ref('')

const form = reactive({
  name: '',
  email: '',
  subject: '',
  inquiry_type: 'product',
  order_number: '',
  message: ''
})

// Auto-fill form if user is logged in or if product context is passed
watch(
  () => props.isOpen,
  (open) => {
    if (open) {
      submitError.value = ''
      ticketSuccess.value = null
      if (user.value) {
        form.name = `${user.value.first_name || ''} ${user.value.last_name || ''}`.trim() || user.value.username
        form.email = user.value.email || ''
      }
      if (props.productContext) {
        form.subject = `Question regarding ${props.productContext.name}`
        form.inquiry_type = 'product'
      }
    }
  }
)

const quickAnswers = [
  {
    icon: 'fa-solid fa-truck-fast',
    title: 'Track My Order',
    desc: 'Check live status of your order and carrier tracking number anytime without logging in.',
    link: '/track',
    linkLabel: 'Open Order Tracker'
  },
  {
    icon: 'fa-solid fa-arrows-rotate',
    title: '30-Day Money-Back Guarantee',
    desc: 'You can return any undamaged item within 30 days of arrival for a full refund or exchange.',
    link: null
  },
  {
    icon: 'fa-solid fa-tag',
    title: 'Promotional Discounts',
    desc: 'Redeem active coupons like WELCOME10, SAVE20, or FLASH50 directly in the checkout summary.',
    link: '/cart',
    linkLabel: 'View Cart & Checkout'
  },
  {
    icon: 'fa-solid fa-shield-halved',
    title: 'Supplier Quality Standards',
    desc: 'All products undergo rigorous factory pre-shipment inspections and come with a 1-year store warranty.',
    link: null
  }
]

const filteredQuickAnswers = computed(() => {
  if (!quickSearch.value.trim()) return quickAnswers
  const q = quickSearch.value.toLowerCase()
  return quickAnswers.filter(
    (item) => item.title.toLowerCase().includes(q) || item.desc.toLowerCase().includes(q)
  )
})

async function handleSubmit() {
  submitError.value = ''
  submitting.value = true

  try {
    const payload = {
      name: form.name.trim(),
      email: form.email.trim(),
      subject: form.subject.trim(),
      inquiry_type: form.inquiry_type,
      order_number: form.order_number.trim(),
      message: form.message.trim(),
      product_name: props.productContext?.name || ''
    }

    const res = await submitInquiry(payload)
    ticketSuccess.value = res.ticket || { ticket_number: 'TICK-' + Date.now() }
  } catch (err) {
    if (err.data && typeof err.data === 'object') {
      const msgs = Object.values(err.data).flat()
      submitError.value = msgs.join(' ')
    } else {
      submitError.value = err.message || 'Failed to submit inquiry. Please try again.'
    }
  } finally {
    submitting.value = false
  }
}

function resetAndClose() {
  ticketSuccess.value = null
  close()
}

function close() {
  emit('close')
}
</script>

<style scoped>
.modal-backdrop {
  position: fixed;
  inset: 0;
  background: rgba(15, 23, 42, 0.65);
  backdrop-filter: blur(5px);
  z-index: 9999;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 1.25rem;
  animation: fadeIn 0.15s ease-out;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

.modal-card {
  background: var(--bg-surface);
  border-radius: var(--radius-lg);
  border: 1px solid var(--border-color);
  max-width: 640px;
  width: 100%;
  max-height: 90vh;
  display: flex;
  flex-direction: column;
  box-shadow: 0 20px 40px -10px rgba(0, 0, 0, 0.25);
  overflow: hidden;
  animation: slideUp 0.2s cubic-bezier(0.16, 1, 0.3, 1);
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(16px) scale(0.98);
  }
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

.modal-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  padding: 1.5rem 1.75rem 1rem;
  border-bottom: 1px solid var(--border-color);
}

.support-badge {
  display: inline-block;
  background: var(--primary-light);
  color: var(--primary);
  font-size: 0.75rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  padding: 0.25rem 0.65rem;
  border-radius: 9999px;
  margin-bottom: 0.35rem;
}

.modal-header h2 {
  font-size: 1.35rem;
  font-weight: 800;
  color: var(--text-main);
}

.btn-close {
  background: none;
  border: none;
  font-size: 1.85rem;
  line-height: 1;
  color: var(--text-muted);
  cursor: pointer;
  padding: 0.25rem 0.5rem;
  border-radius: var(--radius-sm);
  transition: color 0.15s;
}

.btn-close:hover {
  color: var(--text-main);
}

.product-context-strip {
  display: flex;
  align-items: center;
  gap: 0.65rem;
  background: #f1f5f9;
  padding: 0.6rem 1.75rem;
  font-size: 0.85rem;
  border-bottom: 1px solid var(--border-color);
}

.context-tag {
  background: #e2e8f0;
  color: #475569;
  font-weight: 700;
  font-size: 0.72rem;
  padding: 0.15rem 0.5rem;
  border-radius: 4px;
  text-transform: uppercase;
}

.context-name {
  font-weight: 600;
  color: var(--text-main);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

/* Tabs */
.modal-tabs {
  display: flex;
  border-bottom: 1px solid var(--border-color);
  background: var(--bg-page);
}

.tab-btn {
  flex: 1;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 0.45rem;
  padding: 0.75rem 0.5rem;
  font-size: 0.85rem;
  font-weight: 600;
  color: var(--text-muted);
  background: transparent;
  border: none;
  border-bottom: 2px solid transparent;
  cursor: pointer;
  transition: all 0.15s;
}

.tab-btn:hover {
  color: var(--text-main);
}

.tab-btn.active {
  color: var(--primary);
  border-bottom-color: var(--primary);
  background: var(--bg-surface);
}

.tab-icon {
  font-size: 0.95rem;
}

/* Tab Body */
.tab-body {
  padding: 1.5rem 1.75rem;
  overflow-y: auto;
  flex: 1;
}

/* Form Styles */
.inquiry-form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.form-row-2 {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.35rem;
}

.form-group label {
  font-size: 0.8rem;
  font-weight: 700;
  color: var(--text-main);
}

.form-group input,
.form-group select,
.form-group textarea {
  border: 1px solid var(--border-color);
  border-radius: var(--radius-sm);
  padding: 0.65rem 0.8rem;
  font-size: 0.88rem;
  outline: none;
  background: var(--bg-surface);
  transition: border-color 0.15s;
}

.form-group input:focus,
.form-group select:focus,
.form-group textarea:focus {
  border-color: var(--primary);
}

.error-banner {
  background: #fef2f2;
  border: 1px solid #fecaca;
  color: #dc2626;
  padding: 0.65rem 0.85rem;
  border-radius: var(--radius-sm);
  font-size: 0.85rem;
}

.modal-footer-actions {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 0.75rem;
  margin-top: 0.5rem;
}

.btn-secondary-modal {
  padding: 0.65rem 1.25rem;
  background: transparent;
  border: 1px solid var(--border-color);
  color: var(--text-muted);
  font-weight: 600;
  font-size: 0.88rem;
  border-radius: var(--radius-sm);
  cursor: pointer;
}

.btn-secondary-modal:hover {
  background: #f8fafc;
  color: var(--text-main);
}

.btn-primary-modal {
  padding: 0.65rem 1.5rem;
  background: var(--primary);
  border: none;
  color: #fff;
  font-weight: 700;
  font-size: 0.88rem;
  border-radius: var(--radius-sm);
  cursor: pointer;
  transition: background 0.15s;
}

.btn-primary-modal:hover:not(:disabled) {
  background: var(--primary-hover);
}

.btn-primary-modal:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

/* Success Ticket Box */
.success-ticket-box {
  text-align: center;
  padding: 1.5rem 1rem;
}

.success-icon-wrap {
  width: 56px;
  height: 56px;
  border-radius: 50%;
  background: #dcfce7;
  color: #16a34a;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 1rem;
}

.success-ticket-box h3 {
  font-size: 1.25rem;
  font-weight: 800;
  color: var(--text-main);
  margin-bottom: 0.4rem;
}

.success-ticket-box p {
  color: var(--text-muted);
  font-size: 0.9rem;
  margin-bottom: 1.5rem;
}

.ticket-receipt {
  background: #f8fafc;
  border: 1px solid var(--border-color);
  border-radius: var(--radius-md);
  padding: 1rem 1.25rem;
  margin-bottom: 1.5rem;
  text-align: left;
  display: flex;
  flex-direction: column;
  gap: 0.65rem;
}

.receipt-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 0.88rem;
}

.receipt-label {
  color: var(--text-muted);
}

.receipt-code {
  font-family: monospace;
  font-size: 0.95rem;
  color: var(--primary);
  background: var(--primary-light);
  padding: 0.15rem 0.45rem;
  border-radius: 4px;
}

/* Quick Answers */
.quick-search-box {
  width: 100%;
  padding: 0.7rem 0.9rem;
  border: 1px solid var(--border-color);
  border-radius: var(--radius-md);
  font-size: 0.88rem;
  margin-bottom: 1.25rem;
  outline: none;
}

.quick-search-box:focus {
  border-color: var(--primary);
}

.quick-cards-grid {
  display: flex;
  flex-direction: column;
  gap: 0.85rem;
}

.quick-card {
  background: #f8fafc;
  border: 1px solid var(--border-color);
  border-radius: var(--radius-md);
  padding: 1rem 1.15rem;
}

.quick-card-head {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 0.35rem;
}

.quick-card-head h4 {
  font-size: 0.95rem;
  font-weight: 700;
}

.quick-card p {
  font-size: 0.85rem;
  color: #475569;
  line-height: 1.5;
  margin-bottom: 0.5rem;
}

.quick-link {
  font-size: 0.85rem;
  font-weight: 700;
  color: var(--primary);
}

/* Contact Channels */
.channel-cards {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.channel-card {
  border: 1px solid var(--border-color);
  border-radius: var(--radius-md);
  padding: 1.25rem;
  background: var(--bg-surface);
}

.channel-icon {
  font-size: 1.5rem;
  margin-bottom: 0.5rem;
  display: inline-block;
}

.channel-card h4 {
  font-size: 1rem;
  font-weight: 700;
  margin-bottom: 0.25rem;
}

.channel-card p {
  font-size: 0.85rem;
  color: var(--text-muted);
  margin-bottom: 0.65rem;
}

.channel-action {
  display: inline-block;
  font-weight: 700;
  color: var(--primary);
  font-size: 0.92rem;
  margin-bottom: 0.5rem;
}

.channel-badge {
  display: inline-block;
  font-size: 0.75rem;
  font-weight: 700;
  background: #eff6ff;
  color: var(--primary);
  padding: 0.2rem 0.5rem;
  border-radius: 9999px;
}

.channel-badge.green {
  background: #dcfce7;
  color: #166534;
}

.hours-list {
  font-size: 0.85rem;
  color: var(--text-main);
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

@media (max-width: 600px) {
  .form-row-2 {
    grid-template-columns: 1fr;
  }
}
</style>
