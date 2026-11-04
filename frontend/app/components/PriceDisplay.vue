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

.price-container{
    display: flex;
    align-items: center;
    gap: 0.5rem;
    flex-wrap: wrap;
}

.current-price{
    font-size: 1.25rem;
    font-weight: 800;
    color: var(--text-main);
    letter-spacing: -0.02rem;
}

.original-price{
    font-size: 0.9rem;
    color: var(--text-muted);
    text-decoration: line-through;
}

.discount-badge{
    background: #fef2f2;
    color: #dc2626;
    font-size: 0.75rem;
    font-weight: 700;
    padding: 0.15rem 0.45rem;
    border-radius: var(--radius-sm);
}

</style>