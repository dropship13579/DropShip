<script setup>

const props = defineProps({
    placeholder: {
        type: String,
        default: 'Search products, gadgets, home...'
    },
    initialQuery: {
        type: String,
        default: ''
    }
})

const emit = defineEmits(['search'])
const query = ref(props.initialQuery)

watch(() => props.initialQuery, (newVal) => {
    query.value = newVal
})

function handleSearch(){
    emit('search', query.value.trim())
}

function clearSearch(){
    query.value = ''
    emit('search', '')
}

</script>

<template>
    <form @submit.prevent="handleSearch" class="search-form">
        <div class="search-input-wrap">
            <svg class="search-icon" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="11" cy="11" r="8"></circle>
                <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
            </svg>
            <input v-model="query" type="text" :placeholder="placeholder" class="search-input" />
            <button v-if="query" type="button" @click="clearSearch" class="clear-btn">x</button>
        </div>
        <button type="submit" class="search-btn">Search</button>
    </form>
</template>

<style scoped>

.search-form{
    display: flex;
    align-items: center;
    gap: 0.5rem;
    width: 100%;
    max-width: 550px;
}

.search-input-wrap{
    position: relative;
    flex: 1;
    display: flex;
    align-items: center;
}

.search-icon{
    position: absolute;
    left: 0.85rem;
    color: var(--text-muted);
    pointer-events: none;
}

.search-input{
    width: 100%;
    padding: 0.65rem 2rem 0.65rem 2.5rem;
    background: var(--bg-page);
    border: 1px solid var(--border-color);
    border-radius: var(--radius-md);
    font-size: 0.9rem;
    outline: none;
    transition: all 0.15s;
}

.search-input:focus{
    background: var(--bg-surface);
    border-color: var(--primary);
    box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1);
}

.clear-btn{
    position: absolute;
    right: 0.75rem;
    color: var(--text-muted);
    font-size: 0.8rem;
    padding: 0.2rem;
}

.search-btn{
    background: var(--primary);
    color: #fff;
    padding: 0.65rem 1.25rem;
    border-radius: var(--radius-md);
    font-weight: 600;
    font-size: 0.9rem;
    white-space: nowrap;
    transition: background 0.15s;
}

.search-btn:hover{
    background: var(--primary-hover);
}

</style>