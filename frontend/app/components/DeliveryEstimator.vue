<!-- frontend/app/components/DeliveryEstimator.vue -->
<template>
  <div class="delivery-estimator" :class="{ 'is-compact': compact }">
    <!-- Header with Live Urgency Countdown -->
    <div class="estimator-header">
      <div class="countdown-row">
        <span class="live-dot-wrap">
          <span class="live-dot"></span>
        </span>
        <span class="countdown-label">Order within</span>
        <div class="timer-display">
          <span class="time-part"><strong class="num">{{ hours }}</strong>h</span>
          <span class="colon">:</span>
          <span class="time-part"><strong class="num">{{ minutes }}</strong>m</span>
          <span class="colon">:</span>
          <span class="time-part"><strong class="num">{{ seconds }}</strong>s</span>
        </div>
        <span class="countdown-suffix">for same-day dispatch</span>
      </div>

      <!-- Destination Selector -->
      <div class="destination-picker">
        <span class="dest-label">Deliver to:</span>
        <button type="button" @click="showCountrySelect = !showCountrySelect" class="btn-dest-change">
          <span class="country-badge"><i class="fa-solid fa-earth-americas"></i> {{ selectedCountry.code }}</span>
          <span class="country-name">{{ selectedCountry.name }}</span>
          <svg width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
            <polyline points="6 9 12 15 18 9"></polyline>
          </svg>
        </button>

        <!-- Country Dropdown -->
        <div v-if="showCountrySelect" class="country-dropdown">
          <button
            v-for="c in countries"
            :key="c.code"
            type="button"
            class="country-opt"
            :class="{ active: c.code === selectedCountry.code }"
            @click="selectCountry(c)"
          >
            <span class="country-pill">{{ c.code }}</span>
            <span>{{ c.name }}</span>
            <span class="transit-tag">{{ c.transit }}</span>
          </button>
        </div>
      </div>
    </div>

    <!-- Estimated Arrival Highlight Box -->
    <div class="arrival-box">
      <div class="arrival-top">
        <div class="truck-icon-wrap">
          <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <rect x="1" y="3" width="15" height="13"></rect>
            <polygon points="16 8 20 8 23 11 23 16 16 16 16 8"></polygon>
            <circle cx="5.5" cy="18.5" r="2.5"></circle>
            <circle cx="18.5" cy="18.5" r="2.5"></circle>
          </svg>
        </div>
        <div class="arrival-info">
          <div class="arrival-title">
            Estimated Delivery Date:
          </div>
          <div class="arrival-dates">
            {{ activeDeliveryRange }}
          </div>
        </div>
      </div>

      <!-- Visual Fulfillment Progress Bar -->
      <div class="mini-stepper">
        <div class="stepper-line">
          <div class="line-fill"></div>
        </div>
        <div class="stepper-points">
          <div class="step-point done">
            <span class="pt-dot"></span>
            <span class="pt-label">Order Placed</span>
          </div>
          <div class="step-point current">
            <span class="pt-dot"></span>
            <span class="pt-label">Dispatched (24h)</span>
          </div>
          <div class="step-point future">
            <span class="pt-dot"></span>
            <span class="pt-label">At Your Door</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Shipping Method Switcher (Standard Free vs Express) -->
    <div v-if="!compact" class="shipping-methods">
      <label class="method-card" :class="{ selected: selectedMethod === 'standard' }">
        <input type="radio" name="shippingMethod" value="standard" v-model="selectedMethod" />
        <div class="method-meta">
          <div class="method-head">
            <strong>Standard Tracked Shipping</strong>
            <span class="badge-free">FREE</span>
          </div>
          <span class="method-sub">{{ standardDaysText }} &bull; Direct Carrier Tracking</span>
        </div>
      </label>

      <label class="method-card" :class="{ selected: selectedMethod === 'express' }">
        <input type="radio" name="shippingMethod" value="express" v-model="selectedMethod" />
        <div class="method-meta">
          <div class="method-head">
            <strong>Express Priority Air Line</strong>
            <span class="express-price">{{ format(4.99) }}</span>
          </div>
          <span class="method-sub">{{ expressDaysText }} &bull; Expedited Customs Clearance</span>
        </div>
      </label>
    </div>

    <!-- On-Time Guarantee Notice -->
    <div class="guarantee-footer">
      <span class="shield-icon"><i class="fa-solid fa-shield-halved"></i></span>
      <span><strong>Guaranteed On-Time Delivery:</strong> If package arrives late, receive a $5 credit.</span>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  compact: {
    type: Boolean,
    default: false
  },
  baseDays: {
    type: Number,
    default: 7
  }
})

const { format } = useCurrency()

const selectedMethod = ref('standard')
const showCountrySelect = ref(false)

const countries = [
  { code: 'US', name: 'United States', transit: '4–7 Days', offsetDays: 0 },
  { code: 'GB', name: 'United Kingdom', transit: '5–8 Days', offsetDays: 1 },
  { code: 'CA', name: 'Canada', transit: '5–9 Days', offsetDays: 1 },
  { code: 'AU', name: 'Australia', transit: '6–10 Days', offsetDays: 2 },
  { code: 'DE', name: 'Germany', transit: '4–8 Days', offsetDays: 1 },
  { code: 'FR', name: 'France', transit: '4–8 Days', offsetDays: 1 },
  { code: 'IN', name: 'India', transit: '5–9 Days', offsetDays: 1 }
]

const selectedCountry = ref(countries[0])

if (import.meta.client) {
  const savedCode = localStorage.getItem('dropship_dest_country')
  if (savedCode) {
    const found = countries.find(c => c.code === savedCode)
    if (found) selectedCountry.value = found
  }
}

function selectCountry(country) {
  selectedCountry.value = country
  showCountrySelect.value = false
  if (import.meta.client) {
    localStorage.setItem('dropship_dest_country', country.code)
  }
}

// ----------------------------------------------------------------------
// Countdown Timer Logic (Cutoff at 5:00 PM local time daily)
// ----------------------------------------------------------------------
const hours = ref('00')
const minutes = ref('00')
const seconds = ref('00')
let timerInterval = null

function updateCountdown() {
  const now = new Date()
  const cutoff = new Date(now)
  cutoff.setHours(17, 0, 0, 0) // 5:00 PM

  if (now.getTime() >= cutoff.getTime()) {
    cutoff.setDate(cutoff.getDate() + 1)
  }

  const diffMs = cutoff.getTime() - now.getTime()
  if (diffMs <= 0) {
    hours.value = '00'
    minutes.value = '00'
    seconds.value = '00'
    return
  }

  const h = Math.floor(diffMs / (1000 * 60 * 60))
  const m = Math.floor((diffMs % (1000 * 60 * 60)) / (1000 * 60))
  const s = Math.floor((diffMs % (1000 * 60)) / 1000)

  hours.value = String(h).padStart(2, '0')
  minutes.value = String(m).padStart(2, '0')
  seconds.value = String(s).padStart(2, '0')
}

onMounted(() => {
  updateCountdown()
  timerInterval = setInterval(updateCountdown, 1000)
})

onUnmounted(() => {
  if (timerInterval) clearInterval(timerInterval)
})

// ----------------------------------------------------------------------
// Estimated Delivery Range Calculations
// ----------------------------------------------------------------------
function addDays(date, days) {
  const result = new Date(date)
  result.setDate(result.getDate() + days)
  return result
}

function formatDateRange(startDate, endDate) {
  const optionsMonth = { month: 'short' }
  const optionsDay = { day: 'numeric' }
  const optionsWeekday = { weekday: 'short' }

  const startDay = startDate.toLocaleDateString('en-US', optionsDay)
  const startMonth = startDate.toLocaleDateString('en-US', optionsMonth)
  const startWk = startDate.toLocaleDateString('en-US', optionsWeekday)

  const endDay = endDate.toLocaleDateString('en-US', optionsDay)
  const endMonth = endDate.toLocaleDateString('en-US', optionsMonth)
  const endWk = endDate.toLocaleDateString('en-US', optionsWeekday)

  if (startMonth === endMonth) {
    return `${startWk}, ${startMonth} ${startDay} – ${endWk}, ${endDay}`
  }
  return `${startWk}, ${startMonth} ${startDay} – ${endWk}, ${endMonth} ${endDay}`
}

const standardDaysText = computed(() => {
  const min = 4 + selectedCountry.value.offsetDays
  const max = 8 + selectedCountry.value.offsetDays
  return `${min}–${max} Business Days`
})

const expressDaysText = computed(() => {
  const min = 2 + selectedCountry.value.offsetDays
  const max = 4 + selectedCountry.value.offsetDays
  return `${min}–${max} Business Days`
})

const activeDeliveryRange = computed(() => {
  const now = new Date()
  const offset = selectedCountry.value.offsetDays

  if (selectedMethod.value === 'express') {
    const start = addDays(now, 2 + offset)
    const end = addDays(now, 4 + offset)
    return formatDateRange(start, end)
  } else {
    const start = addDays(now, 4 + offset)
    const end = addDays(now, 8 + offset)
    return formatDateRange(start, end)
  }
})
</script>

<style scoped>
.delivery-estimator {
  background: #f8fafc;
  border: 1px solid var(--border-color);
  border-radius: var(--radius-md);
  padding: 1.15rem 1.25rem;
  margin: 1.25rem 0;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.delivery-estimator.is-compact {
  padding: 0.85rem 1rem;
  margin: 0.85rem 0;
  background: var(--bg-surface);
}

/* Header */
.estimator-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 0.65rem;
  padding-bottom: 0.75rem;
  border-bottom: 1px solid var(--border-color);
}

.countdown-row {
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  font-size: 0.84rem;
}

.live-dot-wrap {
  position: relative;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 12px;
  height: 12px;
}

.live-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #16a34a;
  box-shadow: 0 0 0 3px rgba(34, 197, 94, 0.25);
  animation: pulse 1.5s infinite;
}

@keyframes pulse {
  0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(34, 197, 94, 0.5); }
  70% { transform: scale(1); box-shadow: 0 0 0 5px rgba(34, 197, 94, 0); }
  100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(34, 197, 94, 0); }
}

.countdown-label {
  color: var(--text-muted);
  font-weight: 600;
}

.timer-display {
  display: inline-flex;
  align-items: center;
  gap: 0.15rem;
  background: #fef2f2;
  border: 1px solid #fee2e2;
  padding: 0.15rem 0.45rem;
  border-radius: var(--radius-sm);
  color: #b91c1c;
  font-family: monospace;
  font-size: 0.85rem;
}

.timer-display .num {
  font-weight: 800;
}

.colon {
  font-weight: 700;
  color: #ef4444;
}

.countdown-suffix {
  color: #475569;
  font-weight: 600;
}

/* Destination Picker */
.destination-picker {
  position: relative;
  display: inline-flex;
  align-items: center;
  gap: 0.35rem;
  font-size: 0.82rem;
}

.dest-label {
  color: var(--text-muted);
}

.btn-dest-change {
  display: inline-flex;
  align-items: center;
  gap: 0.3rem;
  background: #fff;
  border: 1px solid var(--border-color);
  padding: 0.25rem 0.55rem;
  border-radius: var(--radius-sm);
  font-weight: 700;
  font-size: 0.8rem;
  color: var(--text-main);
  cursor: pointer;
  transition: all 0.15s;
}

.btn-dest-change:hover {
  border-color: var(--primary);
  color: var(--primary);
}

.country-badge {
  display: inline-flex;
  align-items: center;
  gap: 0.25rem;
  color: var(--primary);
  font-weight: 700;
}

.country-pill {
  display: inline-block;
  padding: 0.1rem 0.35rem;
  background: var(--bg-subtle);
  border-radius: var(--radius-xs);
  font-size: 0.72rem;
  font-weight: 700;
  color: var(--text-muted);
}

.country-dropdown {
  position: absolute;
  top: calc(100% + 4px);
  right: 0;
  background: #fff;
  border: 1px solid var(--border-color);
  border-radius: var(--radius-md);
  box-shadow: var(--shadow-lg);
  padding: 0.35rem;
  min-width: 220px;
  z-index: 200;
  display: flex;
  flex-direction: column;
}

.country-opt {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.45rem 0.65rem;
  font-size: 0.82rem;
  font-weight: 600;
  background: transparent;
  border: none;
  border-radius: var(--radius-sm);
  cursor: pointer;
  text-align: left;
}

.country-opt:hover {
  background: #f1f5f9;
}

.country-opt.active {
  background: var(--primary-light);
  color: var(--primary);
}

.transit-tag {
  margin-left: auto;
  font-size: 0.72rem;
  color: var(--text-muted);
  font-weight: 500;
}

/* Arrival Highlight Box */
.arrival-box {
  background: #fff;
  border: 1px solid var(--border-color);
  border-radius: var(--radius-md);
  padding: 0.9rem 1.15rem;
}

.arrival-top {
  display: flex;
  align-items: center;
  gap: 0.85rem;
  margin-bottom: 0.85rem;
}

.truck-icon-wrap {
  width: 40px;
  height: 40px;
  border-radius: var(--radius-md);
  background: #eff6ff;
  color: var(--primary);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.arrival-title {
  font-size: 0.78rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.04em;
  color: var(--text-muted);
}

.arrival-dates {
  font-size: 1.15rem;
  font-weight: 800;
  color: #0f172a;
  letter-spacing: -0.01em;
}

/* Mini Stepper */
.mini-stepper {
  position: relative;
  padding: 0.25rem 0.5rem 0;
}

.stepper-line {
  position: absolute;
  top: 11px;
  left: 20px;
  right: 20px;
  height: 3px;
  background: #e2e8f0;
  z-index: 1;
}

.line-fill {
  width: 50%;
  height: 100%;
  background: #16a34a;
}

.stepper-points {
  position: relative;
  z-index: 2;
  display: flex;
  justify-content: space-between;
}

.step-point {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.35rem;
}

.pt-dot {
  width: 14px;
  height: 14px;
  border-radius: 50%;
  background: #cbd5e1;
  border: 2px solid #fff;
  box-shadow: 0 0 0 1px #cbd5e1;
}

.step-point.done .pt-dot {
  background: #16a34a;
  box-shadow: 0 0 0 1px #16a34a;
}

.step-point.current .pt-dot {
  background: #2563eb;
  box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.25);
}

.pt-label {
  font-size: 0.72rem;
  font-weight: 700;
  color: #64748b;
}

.step-point.current .pt-label {
  color: var(--primary);
}

/* Shipping Methods */
.shipping-methods {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 0.65rem;
}

.method-card {
  display: flex;
  align-items: flex-start;
  gap: 0.65rem;
  padding: 0.75rem 0.85rem;
  border: 1px solid var(--border-color);
  background: #fff;
  border-radius: var(--radius-sm);
  cursor: pointer;
  transition: all 0.15s;
}

.method-card:hover {
  border-color: #cbd5e1;
}

.method-card.selected {
  border-color: var(--primary);
  background: #f8faff;
  box-shadow: 0 0 0 1px var(--primary);
}

.method-card input {
  margin-top: 0.2rem;
  accent-color: var(--primary);
}

.method-meta {
  display: flex;
  flex-direction: column;
  gap: 0.15rem;
  flex: 1;
}

.method-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-size: 0.82rem;
}

.badge-free {
  font-size: 0.7rem;
  font-weight: 800;
  color: #16a34a;
  background: #dcfce7;
  padding: 0.1rem 0.4rem;
  border-radius: 4px;
}

.express-price {
  font-size: 0.8rem;
  font-weight: 800;
  color: var(--primary);
}

.method-sub {
  font-size: 0.73rem;
  color: var(--text-muted);
}

/* Guarantee Footer */
.guarantee-footer {
  display: flex;
  align-items: center;
  gap: 0.45rem;
  font-size: 0.78rem;
  color: #475569;
  background: #f1f5f9;
  padding: 0.5rem 0.75rem;
  border-radius: var(--radius-sm);
}

.shield-icon {
  font-size: 0.95rem;
}

@media (max-width: 640px) {
  .shipping-methods {
    grid-template-columns: 1fr;
  }
  .estimator-header {
    flex-direction: column;
    align-items: flex-start;
  }
}
</style>
