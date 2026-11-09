<!-- frontend/app/components/PromoTopBar.vue -->
<template>
  <aside class="promo-top-bar" aria-label="Announcement">
    <div class="promo-container">
      <!-- Promo message with animated icon -->
      <div class="promo-content">
        <span class="promo-icon"><i :class="currentMessage.icon"></i></span>
        <span class="promo-text">
          <strong>{{ currentMessage.bold }}</strong> {{ currentMessage.text }}
          <span v-if="currentMessage.code" class="promo-code" @click="copyCode(currentMessage.code)" :title="'Click to copy ' + currentMessage.code">
            {{ currentMessage.code }}
            <span class="copy-badge">{{ copied ? 'Copied!' : 'Copy' }}</span>
          </span>
        </span>
      </div>

      <!-- Quick Trust Highlights on Desktop -->
      <div class="promo-trust-pills">
        <span class="trust-pill">
          <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
            <polyline points="20 6 9 17 4 12"></polyline>
          </svg>
          Direct Factory Sourcing
        </span>
        <span class="trust-divider">•</span>
        <span class="trust-pill">
          <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
            <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path>
          </svg>
          Buyer Protection
        </span>
        <span class="trust-divider">•</span>
        <span class="trust-pill">
          <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
            <circle cx="12" cy="12" r="10"></circle>
            <polyline points="12 6 12 12 14 14"></polyline>
          </svg>
          24/7 Support Desk
        </span>
      </div>
    </div>
  </aside>
</template>

<script setup>
const copied = ref(false)
const currentIndex = ref(0)

const messages = [
  {
    icon: 'fa-solid fa-bolt',
    bold: 'WELCOME OFFER:',
    text: 'Get 10% off your entire first order with code',
    code: 'WELCOME10'
  },
  {
    icon: 'fa-solid fa-truck-fast',
    bold: 'FREE SHIPPING:',
    text: 'Complimentary tracked direct delivery on orders over $50',
    code: null
  },
  {
    icon: 'fa-solid fa-shield-halved',
    bold: 'RISK-FREE SHOPPING:',
    text: 'Enjoy our 30-day money back guarantee on all curated items',
    code: null
  }
]

const currentMessage = computed(() => messages[currentIndex.value])

let interval = null
onMounted(() => {
  interval = setInterval(() => {
    currentIndex.value = (currentIndex.value + 1) % messages.length
  }, 4500)
})

onUnmounted(() => {
  if (interval) clearInterval(interval)
})

function copyCode(code) {
  if (navigator?.clipboard) {
    navigator.clipboard.writeText(code)
    copied.value = true
    setTimeout(() => {
      copied.value = false
    }, 2000)
  }
}
</script>

<style scoped>
.promo-top-bar {
  background: linear-gradient(90deg, #0b0f19 0%, #1e293b 50%, #0b0f19 100%);
  color: #f8fafc;
  font-size: 0.8rem;
  padding: 0.45rem 1rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.08);
  position: relative;
  z-index: 60;
}

.promo-container {
  max-width: 1240px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
}

.promo-content {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin: 0 auto;
  text-align: center;
  animation: fadeInText 0.3s ease-out;
}

@keyframes fadeInText {
  from { opacity: 0; transform: translateY(-2px); }
  to { opacity: 1; transform: translateY(0); }
}

.promo-icon {
  font-size: 0.95rem;
  display: inline-block;
}

.promo-text {
  letter-spacing: 0.01em;
  color: #e2e8f0;
}

.promo-text strong {
  color: #ffffff;
  font-weight: 700;
  letter-spacing: 0.02em;
}

.promo-code {
  display: inline-flex;
  align-items: center;
  gap: 0.35rem;
  background: rgba(37, 99, 235, 0.35);
  border: 1px dashed rgba(96, 165, 250, 0.6);
  color: #93c5fd;
  font-family: monospace;
  font-weight: 700;
  font-size: 0.8rem;
  padding: 0.15rem 0.55rem;
  border-radius: 4px;
  margin-left: 0.4rem;
  cursor: pointer;
  transition: all 0.15s ease;
}

.promo-code:hover {
  background: rgba(37, 99, 235, 0.6);
  color: #ffffff;
}

.copy-badge {
  font-size: 0.65rem;
  text-transform: uppercase;
  background: #2563eb;
  color: #fff;
  padding: 0.1rem 0.3rem;
  border-radius: 3px;
  font-family: inherit;
}

.promo-trust-pills {
  display: flex;
  align-items: center;
  gap: 0.65rem;
  font-size: 0.74rem;
  color: #94a3b8;
}

.trust-pill {
  display: flex;
  align-items: center;
  gap: 0.3rem;
}

.trust-pill svg {
  color: #38bdf8;
}

.trust-divider {
  color: #475569;
}

@media (max-width: 900px) {
  .promo-trust-pills {
    display: none;
  }
}

@media (max-width: 600px) {
  .promo-top-bar {
    font-size: 0.74rem;
    padding: 0.4rem 0.75rem;
  }
  .promo-code {
    display: block;
    margin: 0.25rem auto 0;
    width: fit-content;
  }
}
</style>

