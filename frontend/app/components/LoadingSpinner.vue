<script setup>

defineProps({
    text: {
        type: String,
        default: 'Loading...'
    }
})

</script>

<template>
    <div class="spinner-container">
        <div class="spinner"></div>
        <p v-if="text" class="spinner-text">{{ text }}</p>
    </div>
</template>

<style scoped>

.spinner-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 3rem 1rem;
    gap: 0.75rem;
}

.spinner {
    width: 36px;
    height: 36px;
    border: 3px solid var(--border-color);
    border-top-color: var(--primary);
    border-radius: 50%;
    animation: spin 0.8s linear infinite;
}

.spinner-text{
    font-size: 0.875rem;
    color: var(--text-muted);
}

@keyframes spin {
    to{ transform: rotate(360deg); }
}

</style>