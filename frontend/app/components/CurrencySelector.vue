<!-- frontend/app/components/CurrencySelector.vue -->
<template>
  <div class="currency-selector" ref="rootRef">
    <button
      type="button"
      class="currency-btn"
      @click="isOpen = !isOpen"
      :aria-expanded="isOpen"
      title="Change Currency"
    >
      <span class="curr-flag">{{ currentCurrency.flag }}</span>
      <span class="curr-code">{{ currentCurrency.code }}</span>
      <span class="curr-symbol">({{ currentCurrency.symbol }})</span>
      <svg class="chevron" :class="{ rotated: isOpen }" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
        <polyline points="6 9 12 15 18 9"></polyline>
      </svg>
    </button>

    <div v-if="isOpen" class="currency-dropdown">
      <div class="dropdown-header">Select Store Currency</div>
      <button
        v-for="curr in Object.values(currencies)"
        :key="curr.code"
        type="button"
        class="currency-option"
        :class="{ active: curr.code === selectedCurrency }"
        @click="select(curr.code)"
      >
        <span class="opt-flag">{{ curr.flag }}</span>
        <div class="opt-text">
          <span class="opt-name">{{ curr.name }}</span>
          <span class="opt-sub">{{ curr.code }} &bull; {{ curr.symbol }}</span>
        </div>
        <span v-if="curr.code === selectedCurrency" class="check-mark">&#10003;</span>
      </button>
    </div>
  </div>
</template>

<script setup>
const { currencies, selectedCurrency, currentCurrency, setCurrency } = useCurrency()

const isOpen = ref(false)
const rootRef = ref(null)

function select(code) {
  setCurrency(code)
  isOpen.value = false
}

// Click outside to close
if (import.meta.client) {
  onMounted(() => {
    window.addEventListener('click', onWindowClick)
  })
  onUnmounted(() => {
    window.removeEventListener('click', onWindowClick)
  })
}

function onWindowClick(e) {
  if (rootRef.value && !rootRef.value.contains(e.target)) {
    isOpen.value = false
  }
}
</script>

<style scoped>
.currency-selector {
  position: relative;
  display: inline-block;
}

.currency-btn {
  display: inline-flex;
  align-items: center;
  gap: 0.35rem;
  padding: 0.4rem 0.65rem;
  border-radius: var(--radius-sm);
  background: var(--bg-surface);
  border: 1px solid var(--border-color);
  font-size: 0.82rem;
  font-weight: 700;
  color: var(--text-main);
  cursor: pointer;
  transition: all 0.15s;
}

.currency-btn:hover {
  border-color: var(--primary);
  color: var(--primary);
}

.curr-flag {
  font-size: 1rem;
}

.curr-code {
  letter-spacing: 0.02em;
}

.curr-symbol {
  color: var(--text-muted);
  font-weight: 500;
  font-size: 0.78rem;
}

.chevron {
  transition: transform 0.2s ease;
  color: var(--text-muted);
}

.chevron.rotated {
  transform: rotate(180deg);
}

/* Dropdown */
.currency-dropdown {
  position: absolute;
  top: calc(100% + 6px);
  right: 0;
  background: var(--bg-surface);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-md);
  box-shadow: var(--shadow-lg);
  padding: 0.4rem;
  min-width: 210px;
  z-index: 1000;
  animation: fadeInDown 0.15s ease-out;
}

@keyframes fadeInDown {
  from {
    opacity: 0;
    transform: translateY(-6px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.dropdown-header {
  font-size: 0.72rem;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: var(--text-muted);
  padding: 0.4rem 0.65rem;
  border-bottom: 1px solid var(--border-color);
  margin-bottom: 0.25rem;
}

.currency-option {
  width: 100%;
  display: flex;
  align-items: center;
  gap: 0.65rem;
  padding: 0.5rem 0.65rem;
  border-radius: var(--radius-sm);
  background: transparent;
  border: none;
  cursor: pointer;
  text-align: left;
  transition: background 0.15s;
}

.currency-option:hover {
  background: #f1f5f9;
}

.currency-option.active {
  background: var(--primary-light);
  color: var(--primary);
}

.opt-flag {
  font-size: 1.15rem;
}

.opt-text {
  display: flex;
  flex-direction: column;
  flex: 1;
}

.opt-name {
  font-size: 0.82rem;
  font-weight: 700;
  color: var(--text-main);
  line-height: 1.2;
}

.opt-sub {
  font-size: 0.72rem;
  color: var(--text-muted);
}

.check-mark {
  color: var(--primary);
  font-weight: 800;
  font-size: 0.85rem;
}
</style>
