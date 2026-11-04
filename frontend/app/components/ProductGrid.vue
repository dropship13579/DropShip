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

.product-grid{
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
    gap: 1.5rem;
}

</style>