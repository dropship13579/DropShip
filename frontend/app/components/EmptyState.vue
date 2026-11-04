<script setup>

defineProps({
    title: {
        type: String,
        default: 'No products found'
    },
    description: {
        type: String,
        default: 'Try adjusting your search or filter to find what you are looking for.'
    }
})

</script>

<template>
    <div class="empty-state">
        <div class="icon-circle">
            <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="11" cy="11" r="8"></circle>
                <line  x1="21" y1="21" x2="16.65" y2="16.65"></line>
            </svg>
        </div>

        <h3>{{ title }}</h3>
        <p>{{ description }}</p>
        <slot name="action" />
    </div>
</template>

<style scoped>

.empty-state {
    text-align: center;
    padding: 4rem 1.5rem;
    background: var(--bg-surface);
    border: 1px dashed var(--border-color);
    border-radius: var(--radius-lg);
    margin: 1.5rem 0;
}

.icon-circle {
    width: 60px;
    height: 60px;
    margin: 0 auto 1.25rem;
    background: var(--primary-light);
    color: var(--primary);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
}

h3{
    font-size: 1.25rem;
    font-weight: 700;
    margin-bottom: 0.5rem;
}

p{
    color: var(--text-muted);
    font-size: 0.95rem;
    min-width: 400px;
    margin: 0 auto 1.5rem;
}

</style>