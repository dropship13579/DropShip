<script setup>

defineProps({
    categories: {
        type: Array,
        default: () => []
    },
    selectedCategory: {
        type: String,
        default: ''
    }
})

const emit = defineEmits(['select'])

function selectCategory(slug){
    emit('select', slug)
}

</script>

<template>
    <div class="category-nav">
        <button class="category-pill" :class="{ active: selectedCategory === '' }" @click="selectCategory('')">All Products</button>
        <button v-for="cat in categories" :key="cat.id" class="category-pill" :class="{ active: selectedCategory === cat.slug }" @click="selectCategory(cat.slug)">
            {{ cat.name }}
            <span v-if="cat.product_count" class="count-badge">{{ cat.product_count }}</span>
        </button>
    </div>
</template>

<style scoped>

.category-nav{
    display: flex;
    align-items: center;
    gap: 0.5rem;
    overflow-x: auto;
    padding: 0.25rem 0 0.75rem;
    scrollbar-width: none;
}

.category-nav::-webkit-scrollbar{
    display: none;
}

.category-pill{
    white-space: nowrap;
    padding: 0.45rem 1rem;
    border-radius: 9999px;
    background: var(--bg-surface);
    border: 1px solid var(--border-color);
    font-size: 0.85rem;
    font-weight: 600;
    color: var(--text-main);
    display: flex;
    align-items: center;
    gap: 0.4rem;
    transition: all 0.15s;
}

.category-pill:hover{
    border-color: var(--primary);
    color: var(--primary);
}

.category-pill.active{
    background: var(--primary);
    color: #fff;
    border-color: var(--primary);
}

.count-badge{
    font-size: 0.75rem;
    background: rgba(0, 0, 0, 0.08);
    padding: 0.1rem 0.4rem;
    border-radius: 9999px;
}

.category-pill.active .count-badge{
    background: rgba(255, 255, 255, 0.25);
    color: #fff;
}

</style>