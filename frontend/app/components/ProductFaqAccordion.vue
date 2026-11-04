<!-- frontend/app/components/ProductFaqAccordion.vue -->
<template>
  <section class="faq-section">
    <div class="faq-container">
      <div class="faq-header">
        <span class="faq-badge">Got Questions?</span>
        <h2>Frequently Asked Questions</h2>
        <p class="faq-subtext">Everything you need to know about delivery, buyer protection, returns, and product quality.</p>
      </div>

      <!-- Category Filter Pills -->
      <div class="faq-category-pills">
        <button
          v-for="cat in categories"
          :key="cat.id"
          type="button"
          class="cat-pill"
          :class="{ active: selectedCategory === cat.id }"
          @click="selectedCategory = cat.id"
        >
          <span class="cat-icon">{{ cat.icon }}</span>
          <span>{{ cat.label }}</span>
        </button>
      </div>

      <!-- Accordion List -->
      <div class="accordion-list">
        <div
          v-for="(item, index) in filteredFaqs"
          :key="index"
          class="accordion-item"
          :class="{ 'is-open': openIndex === index }"
        >
          <button
            type="button"
            class="accordion-trigger"
            :aria-expanded="openIndex === index"
            @click="toggleItem(index)"
          >
            <div class="trigger-left">
              <span class="faq-q-icon">?</span>
              <span class="faq-question">{{ item.question }}</span>
            </div>
            <span class="toggle-icon" :class="{ rotated: openIndex === index }">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
                <polyline points="6 9 12 15 18 9"></polyline>
              </svg>
            </span>
          </button>

          <div v-show="openIndex === index" class="accordion-content">
            <div class="content-inner">
              <p>{{ item.answer }}</p>
              <div v-if="item.highlight" class="content-callout">
                <span class="callout-icon">💡</span>
                <span>{{ item.highlight }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Still have questions? Help Banner -->
      <div class="faq-help-box">
        <div class="help-box-left">
          <div class="help-avatar-group">
            <span class="avatar-pill a1">👩‍💼</span>
            <span class="avatar-pill a2">👨‍💻</span>
            <span class="avatar-pill a3">🎧</span>
          </div>
          <div>
            <h3>Still have questions about this product?</h3>
            <p>Our dedicated support team is available 24/7 with an average response time of under 2 hours.</p>
          </div>
        </div>
        <button type="button" @click="$emit('open-support')" class="btn-ask-support">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path>
          </svg>
          <span>Ask Customer Support</span>
        </button>
      </div>
    </div>
  </section>
</template>

<script setup>
defineEmits(['open-support'])

const selectedCategory = ref('all')
const openIndex = ref(0) // Default first FAQ open

const categories = [
  { id: 'all', label: 'All Questions', icon: '✨' },
  { id: 'shipping', label: 'Shipping & Delivery', icon: '🚚' },
  { id: 'returns', label: 'Returns & Refunds', icon: '🔄' },
  { id: 'payment', label: 'Payment & Security', icon: '🔒' },
  { id: 'quality', label: 'Quality & Warranty', icon: '🛡️' }
]

const faqs = [
  {
    category: 'shipping',
    question: 'How long does shipping take to my address?',
    answer: 'Standard tracked shipping usually arrives within 4 to 9 business days depending on your destination. Orders are processed and dispatched within 24–48 hours from our verified direct fulfillment hubs.',
    highlight: 'You will receive an automated email with your tracking code the moment your package is handed to the local carrier.'
  },
  {
    category: 'shipping',
    question: 'How do I track my order once it has shipped?',
    answer: 'You can track your package directly on our website at any time using our dedicated Track Order page. Simply input your Order Number (e.g. ORD-20261024-XXXX) and your email address to view real-time carrier checkpoints and live status updates.',
    highlight: 'No account needed—guests can look up live shipments instantly.'
  },
  {
    category: 'returns',
    question: 'What is your 30-Day Money-Back Guarantee policy?',
    answer: 'We want you to shop with complete peace of mind. If you are not 100% satisfied with your item or if it arrives damaged, you may return it within 30 days of delivery for a full refund or a free replacement.',
    highlight: 'Returns are hassle-free with prompt refund processing directly to your original payment method.'
  },
  {
    category: 'returns',
    question: 'What should I do if my package arrives damaged or defective?',
    answer: 'Contact our customer support team immediately through the "Ask Customer Support" button with a brief photo of the damage. We will dispatch a brand-new replacement at zero cost or issue an instant refund.',
    highlight: 'Damaged item claims are verified and resolved within 24 hours.'
  },
  {
    category: 'payment',
    question: 'Is my payment information safe and encrypted?',
    answer: 'Yes, absolutely. We use industry-standard 256-bit SSL encryption to protect your transaction. Your payment details are processed through PCI-compliant gateways and are never stored on our servers.',
    highlight: 'We support Credit/Debit Cards, Cash on Delivery (COD), and direct bank transfers.'
  },
  {
    category: 'payment',
    question: 'Can I apply promotional coupon codes during checkout?',
    answer: 'Yes! You can redeem promotional discounts (such as WELCOME10, SAVE20, or FLASH50) on the checkout page before completing payment. The discount will calculate and reflect dynamically on your subtotal.',
    highlight: 'Enter your coupon code in Step 2 of the checkout page to activate your discount.'
  },
  {
    category: 'quality',
    question: 'How do you ensure product authenticity and supplier quality?',
    answer: 'Every supplier on our platform undergoes strict vetting including factory audits, material quality evaluations, and delivery speed benchmarks before their items are listed in our catalog.',
    highlight: 'All products are covered by our 1-year store warranty against manufacturer defects.'
  },
  {
    category: 'quality',
    question: 'Can I cancel or modify my delivery address after placing an order?',
    answer: 'Orders can be amended or cancelled within 2 hours of placement before warehouse sourcing begins. Reach out to our customer support team immediately with your Order Number and our agents will adjust your delivery details.',
    highlight: 'Fast response guaranteed via our Customer Support ticket desk.'
  }
]

const filteredFaqs = computed(() => {
  if (selectedCategory.value === 'all') return faqs
  return faqs.filter(f => f.category === selectedCategory.value)
})

function toggleItem(idx) {
  openIndex.value = openIndex.value === idx ? -1 : idx
}
</script>

<style scoped>
.faq-section {
  margin-top: 4rem;
  padding-top: 3.5rem;
  border-top: 1px solid var(--border-color);
}

.faq-container {
  max-width: 900px;
  margin: 0 auto;
}

.faq-header {
  text-align: center;
  margin-bottom: 2rem;
}

.faq-badge {
  display: inline-block;
  background: var(--primary-light);
  color: var(--primary);
  font-size: 0.8rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  padding: 0.35rem 0.85rem;
  border-radius: 9999px;
  margin-bottom: 0.75rem;
}

.faq-header h2 {
  font-size: 2rem;
  font-weight: 800;
  letter-spacing: -0.02em;
  color: var(--text-main);
  margin-bottom: 0.5rem;
}

.faq-subtext {
  color: var(--text-muted);
  font-size: 0.95rem;
}

/* Category Filter Pills */
.faq-category-pills {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  flex-wrap: wrap;
  margin-bottom: 2rem;
}

.cat-pill {
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  padding: 0.5rem 1rem;
  border-radius: 9999px;
  font-size: 0.85rem;
  font-weight: 600;
  background: var(--bg-surface);
  border: 1px solid var(--border-color);
  color: var(--text-muted);
  transition: all 0.2s ease;
}

.cat-pill:hover {
  border-color: var(--primary);
  color: var(--primary);
}

.cat-pill.active {
  background: var(--primary);
  border-color: var(--primary);
  color: #fff;
  box-shadow: 0 4px 12px rgba(37, 99, 235, 0.25);
}

.cat-icon {
  font-size: 0.95rem;
}

/* Accordion Item */
.accordion-list {
  display: flex;
  flex-direction: column;
  gap: 0.85rem;
}

.accordion-item {
  background: var(--bg-surface);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-md);
  overflow: hidden;
  transition: border-color 0.2s, box-shadow 0.2s;
}

.accordion-item:hover {
  border-color: #cbd5e1;
}

.accordion-item.is-open {
  border-color: var(--primary);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.04);
}

.accordion-trigger {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1.15rem 1.4rem;
  text-align: left;
  background: transparent;
  gap: 1rem;
}

.trigger-left {
  display: flex;
  align-items: center;
  gap: 0.85rem;
}

.faq-q-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 26px;
  height: 26px;
  border-radius: 50%;
  background: var(--primary-light);
  color: var(--primary);
  font-weight: 800;
  font-size: 0.8rem;
  flex-shrink: 0;
}

.faq-question {
  font-size: 1.05rem;
  font-weight: 700;
  color: var(--text-main);
  line-height: 1.35;
}

.toggle-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: var(--bg-page);
  color: var(--text-muted);
  flex-shrink: 0;
  transition: transform 0.25s ease, background 0.2s, color 0.2s;
}

.toggle-icon.rotated {
  transform: rotate(180deg);
  background: var(--primary-light);
  color: var(--primary);
}

.accordion-content {
  padding: 0 1.4rem 1.35rem 3.45rem;
  animation: fadeIn 0.2s ease-out;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(-4px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.content-inner p {
  color: #475569;
  font-size: 0.95rem;
  line-height: 1.65;
  margin-bottom: 0.85rem;
}

.content-callout {
  display: flex;
  align-items: flex-start;
  gap: 0.6rem;
  background: #f0fdf4;
  border-left: 3px solid #22c55e;
  padding: 0.65rem 0.85rem;
  border-radius: 0 var(--radius-sm) var(--radius-sm) 0;
  font-size: 0.85rem;
  font-weight: 600;
  color: #166534;
}

.callout-icon {
  font-size: 1rem;
}

/* Help Box Banner */
.faq-help-box {
  margin-top: 2.5rem;
  background: linear-gradient(135deg, #eff6ff 0%, #f8fafc 100%);
  border: 1px solid #bfdbfe;
  border-radius: var(--radius-lg);
  padding: 1.75rem 2rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1.5rem;
  flex-wrap: wrap;
}

.help-box-left {
  display: flex;
  align-items: center;
  gap: 1.25rem;
  max-width: 580px;
}

.help-avatar-group {
  display: flex;
  position: relative;
  flex-shrink: 0;
}

.avatar-pill {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: #fff;
  border: 2px solid #eff6ff;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.08);
  font-size: 1.2rem;
  margin-left: -10px;
}

.avatar-pill:first-child {
  margin-left: 0;
}

.help-box-left h3 {
  font-size: 1.1rem;
  font-weight: 800;
  color: var(--text-main);
  margin-bottom: 0.25rem;
}

.help-box-left p {
  font-size: 0.85rem;
  color: var(--text-muted);
  line-height: 1.45;
}

.btn-ask-support {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  background: var(--primary);
  color: #fff;
  font-size: 0.95rem;
  font-weight: 700;
  padding: 0.85rem 1.6rem;
  border-radius: var(--radius-md);
  box-shadow: 0 4px 12px rgba(37, 99, 235, 0.25);
  transition: background 0.15s, transform 0.15s;
}

.btn-ask-support:hover {
  background: var(--primary-hover);
  transform: translateY(-2px);
}

@media (max-width: 768px) {
  .accordion-content {
    padding-left: 1.4rem;
  }
  .help-box-left {
    flex-direction: column;
    align-items: flex-start;
  }
  .btn-ask-support {
    width: 100%;
    justify-content: center;
  }
}
</style>
