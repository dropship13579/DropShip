<!-- frontend/app/components/ProductGrid.vue -->
<script setup>
defineProps({
  products: {
    type: Array,
    required: true
  }
})
</script>

<template>
  <div class="product-grid">
    <ProductCard v-for="product in products" :key="product.id" :product="product" />
  </div>
</template>

<style scoped>
.product-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(270px, 1fr));
  gap: 1.75rem;
}

@media (max-width: 640px) {
  .product-grid {
    grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
    gap: 1rem;
  }
}
</style>
