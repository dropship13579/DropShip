<!-- frontend/app/components/SearchBar.vue -->
<script setup>
const props = defineProps({
  placeholder: {
    type: String,
    default: 'Search products, electronics, gear...'
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

function handleSearch() {
  emit('search', query.value.trim())
}

function clearSearch() {
  query.value = ''
  emit('search', '')
}
</script>

<template>
  <form @submit.prevent="handleSearch" class="search-form">
    <div class="search-input-wrap">
      <svg class="search-icon" width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.3">
        <circle cx="11" cy="11" r="8"></circle>
        <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
      </svg>
      <input
        v-model="query"
        type="text"
        :placeholder="placeholder"
        class="search-input"
        autocomplete="off"
      />
      <button v-if="query" type="button" @click="clearSearch" class="clear-btn" aria-label="Clear search">
        <i class="fa-solid fa-xmark"></i>
      </button>
    </div>
    <button type="submit" class="search-btn" aria-label="Search">
      <span>Search</span>
    </button>
  </form>
</template>

<style scoped>
.search-form {
  display: flex;
  align-items: center;
  gap: 0.4rem;
  width: 100%;
}

.search-input-wrap {
  position: relative;
  flex: 1;
  display: flex;
  align-items: center;
}

.search-icon {
  position: absolute;
  left: 0.95rem;
  color: var(--text-subtle);
  pointer-events: none;
  transition: color var(--transition-fast);
}

.search-input {
  width: 100%;
  padding: 0.62rem 2.25rem 0.62rem 2.45rem;
  background: var(--bg-page);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-full);
  font-size: 0.88rem;
  outline: none;
  color: var(--text-main);
  transition: all var(--transition-fast);
}

.search-input:focus {
  background: #ffffff;
  border-color: var(--primary);
  box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.12);
}

.search-input:focus + .search-icon {
  color: var(--primary);
}

.clear-btn {
  position: absolute;
  right: 0.75rem;
  color: var(--text-muted);
  font-size: 0.75rem;
  width: 20px;
  height: 20px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--bg-subtle);
  cursor: pointer;
  transition: all var(--transition-fast);
}

.clear-btn:hover {
  background: #e2e8f0;
  color: var(--text-main);
}

.search-btn {
  background: var(--primary);
  color: #ffffff;
  padding: 0.62rem 1.15rem;
  border-radius: var(--radius-full);
  font-weight: 700;
  font-size: 0.85rem;
  white-space: nowrap;
  transition: all var(--transition-fast);
  box-shadow: 0 2px 6px rgba(37, 99, 235, 0.2);
}

.search-btn:hover {
  background: var(--primary-hover);
  transform: translateY(-1px);
}
</style>
