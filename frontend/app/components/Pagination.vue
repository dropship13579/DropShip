<script setup>

const props = defineProps({
    currentPage: {
        type: Number,
        required: true
    },
    totalCount: {
        type: Number,
        required: true
    },
    pageSize: {
        type: Number,
        default: 12
    }
})

const emit = defineEmits(['change'])

const totalPages = computed(() => {
    return Math.ceil(props.totalCount / props.pageSize) || 1
})

function goToPage(page){
    if(page >= 1 && page <= totalPages.value && page !== props.currentPage){
        emit('change', page)
    }
}

</script>

<template>
    <div v-if="totalPages > 1" class="pagination-wrapper">
        <button class="page-btn" :disabled="currentPage <= 1" @click="goToPage(currentPage - 1)">Previous</button>
        <div class="page-numbers">
            <button v-for="page in totalPages" :key="page" class="number-btn" :class="{ active: page === currentPage}" @click="goToPage(page)">{{ page }}</button>            
        </div>
        <button class="page-btn" :disabled="currentPage >= totalPages" @click="goToPage(currentPage + 1)">Next</button>
    </div>
</template>

<style scoped>

.pagination-wrapper{
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0.5rem;
    margin: 3rem 0;
}

.page-btn{
    padding: 0.5rem 1rem;
    background: var(--bg-surface);
    border: 1px solid var(--border-color);
    border-radius: var(--radius-sm);
    font-size: 0.875rem;
    font-weight: 600;
    transition: all 0.15s;
}

.page-btn:hover:not(:disabled){
    border-color: var(--primary);
    color: var(--primary);
}

.page-btn:disabled{
    opacity: 0.4;
    cursor: not-allowed;
}

.page-numbers{
    display: flex;
    gap: 0.35rem;
}

.number-btn{
    width: 36px;
    height: 36px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: var(--bg-surface);
    border: 1px solid var(--border-color);
    border-radius: var(--radius-sm);
    font-size: 0.875rem;
    font-weight: 600;
    transition: all 0.15s;
}

.number-btn:hover{
    border-color: var(--primary);
    color: var(--primary);
}

.number-btn.active{
    background: var(--primary);
    border-color: var(--primary);
    color: #fff;
}

</style>