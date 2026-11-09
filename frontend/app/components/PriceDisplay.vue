<!-- frontend/app/components/PriceDisplay.vue -->
<script setup>
const props = defineProps({
  currentPrice: {
    type: [Number, String],
    required: true
  },
  originalPrice: {
    type: [Number, String],
    default: null
  },
  discountPercentage: {
    type: [Number, String],
    default: 0
  }
})

const { format } = useCurrency()

const hasDiscount = computed(() => {
  return Number(props.discountPercentage) > 0 && props.originalPrice
})
</script>

<template>
  <div class="price-container">
    <span class="current-price">{{ format(currentPrice) }}</span>
    <span v-if="hasDiscount" class="original-price">{{ format(originalPrice) }}</span>
    <span v-if="hasDiscount" class="discount-badge">-{{ discountPercentage }}%</span>
  </div>
</template>

<style scoped>
.price-container {
  display: flex;
  align-items: baseline;
  gap: 0.45rem;
  flex-wrap: wrap;
}

.current-price {
  font-family: 'Outfit', 'Plus Jakarta Sans', sans-serif;
  font-size: 1.25rem;
  font-weight: 800;
  color: var(--text-main);
  letter-spacing: -0.02em;
  font-variant-numeric: tabular-nums;
}

.original-price {
  font-family: 'Outfit', sans-serif;
  font-size: 0.88rem;
  color: var(--text-subtle);
  text-decoration: line-through;
  font-variant-numeric: tabular-nums;
}

.discount-badge {
  background: #fef2f2;
  color: #ef4444;
  border: 1px solid #fee2e2;
  font-size: 0.72rem;
  font-weight: 800;
  padding: 0.12rem 0.4rem;
  border-radius: var(--radius-xs);
  letter-spacing: 0.02em;
}
</style>
