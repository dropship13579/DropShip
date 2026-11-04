<!-- frontend/app/pages/admin/products/index.vue -->
<template>
    <div class="admin-page">
        <div class="admin-container">
            <!-- Header -->
            <div class="admin-header">
                <div>
                    <div class="badge-tag">Inventory Operations</div>
                    <h1>Product Inventory & Pricing</h1>
                    <p class="subtitle">Quick-adjust stock levels, selling prices, and store catalog visibility.</p>
                </div>
                <button @click="fetchProducts" class="btn-refresh" :disabled="loading">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M23 4v6h-6"></path>
                        <path d="M1 20v-6h6"></path>
                        <path d="M3.51 9a9 9 0 0 1 14.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0 0 20.49 15"></path>
                    </svg>
                    <span>{{ loading ? 'Syncing...' : 'Reload Stock' }}</span>
                </button>
            </div>

            <!-- Navigation Tabs -->
            <nav class="admin-tabs">
                <NuxtLink to="/admin" class="tab-item">Website Status & Charts</NuxtLink>
                <NuxtLink to="/admin/products" class="tab-item active">Product Inventory</NuxtLink>
            </nav>

            <!-- Filters Bar -->
            <div class="filters-bar">
                <div class="search-input-wrap">
                    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <circle cx="11" cy="11" r="8"></circle>
                        <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
                    </svg>
                    <input v-model="searchQuery" type="text" placeholder="Search products by title or category..."
                        class="search-input" />
                </div>

                <div class="status-filters">
                    <button v-for="f in filterOptions" :key="f.key" type="button" class="filter-pill"
                        :class="{ 'active': activeFilter === f.key }" @click="activeFilter = f.key">
                        {{ f.label }}
                    </button>
                </div>
            </div>

            <!-- Loading Spinner -->
            <div v-if="loading && products.length === 0" class="loading-wrap">
                <LoadingSpinner text="Retrieving catalog inventory..." />
            </div>

            <!-- Error Banner -->
            <div v-else-if="error" class="error-banner">
                {{ error }}
            </div>

            <!-- Products Table Card -->
            <div v-else class="card table-card">
                <div class="table-meta-header">
                    <span>Showing <strong>{{ filteredProducts.length }}</strong> products</span>
                </div>

                <div class="table-responsive">
                    <table class="inventory-table">
                        <thead>
                            <tr>
                                <th>Product</th>
                                <th>Category</th>
                                <th>Price ($)</th>
                                <th>Stock Count</th>
                                <th>Active Status</th>
                                <th>Featured</th>
                                <th>Action</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="p in filteredProducts" :key="p.id" :class="{ 'row-modified': p._modified }">
                                <!-- Product Info -->
                                <td class="product-cell">
                                    <div class="prod-thumb">
                                        <img v-if="p.image" :src="p.image" :alt="p.name" />
                                        <div v-else class="thumb-fallback">{{ p.name.charAt(0) }}</div>
                                    </div>
                                    <div class="prod-details">
                                        <NuxtLink :to="`/products/${p.slug}`" target="_blank" class="prod-name"
                                            title="View storefront page">
                                            {{ p.name }}
                                            <span class="external-icon">&nearr;</span>
                                        </NuxtLink>
                                        <span class="prod-slug">/products/{{ p.slug }}</span>
                                    </div>
                                </td>

                                <!-- Category -->
                                <td>
                                    <span class="category-badge">{{ p.category_name }}</span>
                                </td>

                                <!-- Price Editor -->
                                <td>
                                    <div class="price-input-wrap">
                                        <span class="currency-prefix">$</span>
                                        <input v-model.number="p.current_price" type="number" step="0.01" min="0"
                                            class="inline-input price-input" @input="markModified(p)" />
                                    </div>
                                </td>

                                <!-- Stock Controls -->
                                <td>
                                    <div class="stock-control-wrap">
                                        <button type="button" @click="decrementStock(p)" class="btn-step"
                                            :disabled="p.stock_quantity <= 0">&minus;</button>

                                        <input v-model.number="p.stock_quantity" type="number" min="0"
                                            class="inline-input stock-input" @input="markModified(p)" />

                                        <button type="button" @click="incrementStock(p)"
                                            class="btn-step">&plus;</button>

                                        <span :class="['stock-pill', getStockPillClass(p.stock_quantity)]">
                                            {{ getStockLabel(p.stock_quantity) }}
                                        </span>
                                    </div>
                                </td>

                                <!-- Active Status -->
                                <td>
                                    <label class="switch-toggle">
                                        <input type="checkbox" v-model="p.is_active" @change="markModified(p)" />
                                        <span class="slider"></span>
                                    </label>
                                </td>

                                <!-- Featured Status -->
                                <td>
                                    <button type="button" @click="toggleFeatured(p)" class="btn-star"
                                        :class="{ 'starred': p.is_featured }" title="Toggle Featured">
                                        &#9733;
                                    </button>
                                </td>

                                <!-- Action -->
                                <td>
                                    <div class="action-cell">
                                        <button type="button" @click="saveProduct(p)" class="btn-save"
                                            :disabled="p._saving || !p._modified">
                                            <span v-if="p._saving">Saving...</span>
                                            <span v-else-if="p._saved" class="saved-text">&#10003; Saved</span>
                                            <span v-else>Save</span>
                                        </button>
                                    </div>
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
definePageMeta({
    middleware: 'admin'
})

const { getProducts, updateProduct } = useAdminApi()

const products = ref([])
const loading = ref(true)
const error = ref('')
const searchQuery = ref('')
const activeFilter = ref('all')

const filterOptions = [
    { key: 'all', label: 'All Products' },
    { key: 'in_stock', label: 'In Stock (> 5)' },
    { key: 'low_stock', label: 'Low Stock (1-5)' },
    { key: 'out_of_stock', label: 'Out of Stock' },
    { key: 'featured', label: 'Featured Only' },
]

async function fetchProducts() {
    loading.value = true
    error.value = ''
    try {
        const data = await getProducts()
        products.value = (data || []).map(p => ({
            ...p,
            _modified: false,
            _saving: false,
            _saved: false
        }))
    } catch (err) {
        error.value = err.message || 'Failed to retrieve products.'
    } finally {
        loading.value = false
    }
}

function markModified(p) {
    p._modified = true
    p._saved = false
}

function incrementStock(p) {
    p.stock_quantity = (p.stock_quantity || 0) + 1
    markModified(p)
}

function decrementStock(p) {
    if (p.stock_quantity > 0) {
        p.stock_quantity -= 1
        markModified(p)
    }
}

function toggleFeatured(p) {
    p.is_featured = !p.is_featured
    markModified(p)
}

function getStockLabel(qty) {
    if (qty <= 0) return 'Out'
    if (qty <= 5) return 'Low'
    return 'OK'
}

function getStockPillClass(qty) {
    if (qty <= 0) return 'pill-out'
    if (qty <= 5) return 'pill-low'
    return 'pill-ok'
}

const filteredProducts = computed(() => {
    let result = products.value

    // Search filter
    if (searchQuery.value.trim()) {
        const q = searchQuery.value.toLowerCase()
        result = result.filter(p =>
            p.name.toLowerCase().includes(q) ||
            p.category_name.toLowerCase().includes(q) ||
            p.slug.toLowerCase().includes(q)
        )
    }

    // Status filter
    if (activeFilter.value === 'in_stock') {
        result = result.filter(p => p.stock_quantity > 5)
    } else if (activeFilter.value === 'low_stock') {
        result = result.filter(p => p.stock_quantity > 0 && p.stock_quantity <= 5)
    } else if (activeFilter.value === 'out_of_stock') {
        result = result.filter(p => p.stock_quantity <= 0)
    } else if (activeFilter.value === 'featured') {
        result = result.filter(p => p.is_featured)
    }

    return result
})

async function saveProduct(p) {
    p._saving = true
    try {
        await updateProduct(p.id, {
            stock_quantity: p.stock_quantity,
            current_price: p.current_price,
            is_active: p.is_active,
            is_featured: p.is_featured
        })
        p._modified = false
        p._saved = true
        setTimeout(() => {
            p._saved = false
        }, 2500)
    } catch (err) {
        alert(err.message || 'Failed to update product.')
    } finally {
        p._saving = false
    }
}

onMounted(() => {
    fetchProducts()
})
</script>

<style scoped>
.admin-page {
    padding: 2.5rem 1.5rem 5rem;
    max-width: 1200px;
    margin: 0 auto;
}

.badge-tag {
    display: inline-block;
    font-size: 0.75rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    background: #0f172a;
    color: #fff;
    padding: 0.2rem 0.5rem;
    border-radius: var(--radius-sm);
    margin-bottom: 0.5rem;
}

.admin-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    flex-wrap: wrap;
    gap: 1.5rem;
    margin-bottom: 1.5rem;
}

.admin-header h1 {
    font-size: 2.1rem;
    font-weight: 800;
    letter-spacing: -0.02em;
    color: var(--text-main);
}

.subtitle {
    color: var(--text-muted);
    font-size: 0.95rem;
    margin-top: 0.25rem;
}

.btn-refresh {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    background: var(--bg-surface);
    border: 1px solid var(--border-color);
    padding: 0.6rem 1.25rem;
    border-radius: var(--radius-md);
    font-size: 0.9rem;
    font-weight: 600;
    color: var(--text-main);
    box-shadow: var(--shadow-sm);
    transition: all 0.15s;
}

.btn-refresh:hover:not(:disabled) {
    background: #f8fafc;
    border-color: #cbd5e1;
}

/* Tabs */
.admin-tabs {
    display: flex;
    gap: 0.5rem;
    border-bottom: 2px solid var(--border-color);
    margin-bottom: 1.75rem;
}

.tab-item {
    font-size: 0.95rem;
    font-weight: 600;
    color: var(--text-muted);
    padding: 0.75rem 1.25rem;
    border-bottom: 2px solid transparent;
    margin-bottom: -2px;
    transition: all 0.15s;
}

.tab-item:hover {
    color: var(--text-main);
}

.tab-item.active {
    color: var(--primary);
    border-bottom-color: var(--primary);
}

/* Filters */
.filters-bar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 1rem;
    margin-bottom: 1.5rem;
}

.search-input-wrap {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    background: var(--bg-surface);
    border: 1px solid var(--border-color);
    border-radius: var(--radius-md);
    padding: 0.55rem 0.85rem;
    width: 380px;
    color: var(--text-muted);
}

.search-input {
    border: none;
    outline: none;
    width: 100%;
    font-size: 0.9rem;
    background: transparent;
}

.status-filters {
    display: flex;
    gap: 0.4rem;
    flex-wrap: wrap;
}

.filter-pill {
    font-size: 0.8rem;
    font-weight: 600;
    color: var(--text-muted);
    background: var(--bg-surface);
    border: 1px solid var(--border-color);
    padding: 0.45rem 0.85rem;
    border-radius: 999px;
    transition: all 0.15s;
}

.filter-pill:hover {
    color: var(--text-main);
    border-color: #cbd5e1;
}

.filter-pill.active {
    background: #0f172a;
    color: #fff;
    border-color: #0f172a;
}

/* Table Card */
.card {
    background: var(--bg-surface);
    border: 1px solid var(--border-color);
    border-radius: var(--radius-lg);
    box-shadow: var(--shadow-sm);
    overflow: hidden;
}

.table-meta-header {
    padding: 1rem 1.5rem;
    background: #f8fafc;
    border-bottom: 1px solid var(--border-color);
    font-size: 0.85rem;
    color: var(--text-muted);
}

.table-responsive {
    overflow-x: auto;
}

.inventory-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 0.9rem;
    text-align: left;
}

.inventory-table th {
    padding: 0.85rem 1.25rem;
    font-size: 0.75rem;
    font-weight: 700;
    color: var(--text-muted);
    text-transform: uppercase;
    letter-spacing: 0.03em;
    border-bottom: 1px solid var(--border-color);
}

.inventory-table td {
    padding: 1rem 1.25rem;
    border-bottom: 1px solid var(--border-color);
    vertical-align: middle;
}

.inventory-table tr:last-child td {
    border-bottom: none;
}

.row-modified {
    background: #fffbeb;
}

/* Product Info Cell */
.product-cell {
    display: flex;
    align-items: center;
    gap: 0.85rem;
    min-width: 260px;
}

.prod-thumb {
    width: 44px;
    height: 44px;
    background: #f1f5f9;
    border-radius: var(--radius-sm);
    overflow: hidden;
    flex-shrink: 0;
}

.prod-thumb img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.thumb-fallback {
    width: 100%;
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 700;
    color: var(--text-muted);
}

.prod-details {
    display: flex;
    flex-direction: column;
}

.prod-name {
    font-weight: 600;
    color: var(--text-main);
    display: flex;
    align-items: center;
    gap: 0.25rem;
}

.prod-name:hover {
    color: var(--primary);
}

.external-icon {
    font-size: 0.8rem;
    color: var(--text-muted);
}

.prod-slug {
    font-size: 0.75rem;
    color: var(--text-muted);
    font-family: monospace;
}

.category-badge {
    font-size: 0.8rem;
    background: #f1f5f9;
    padding: 0.25rem 0.55rem;
    border-radius: var(--radius-sm);
    color: var(--text-muted);
}

/* Price Input */
.price-input-wrap {
    display: flex;
    align-items: center;
    border: 1px solid var(--border-color);
    border-radius: var(--radius-sm);
    padding: 0.25rem 0.5rem;
    width: 110px;
    background: #fff;
}

.currency-prefix {
    color: var(--text-muted);
    font-weight: 600;
    margin-right: 0.2rem;
}

.price-input {
    width: 100%;
    border: none;
    outline: none;
    font-weight: 700;
    font-size: 0.9rem;
}

/* Stock Controls */
.stock-control-wrap {
    display: flex;
    align-items: center;
    gap: 0.35rem;
}

.btn-step {
    width: 26px;
    height: 26px;
    background: #f1f5f9;
    border-radius: var(--radius-sm);
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 700;
    font-size: 1rem;
    color: var(--text-main);
    transition: background 0.15s;
}

.btn-step:hover:not(:disabled) {
    background: #e2e8f0;
}

.btn-step:disabled {
    opacity: 0.4;
    cursor: not-allowed;
}

.stock-input {
    width: 55px;
    text-align: center;
    border: 1px solid var(--border-color);
    border-radius: var(--radius-sm);
    padding: 0.25rem;
    font-weight: 700;
    font-size: 0.9rem;
    outline: none;
}

.stock-pill {
    font-size: 0.7rem;
    font-weight: 700;
    padding: 0.15rem 0.45rem;
    border-radius: 4px;
    text-transform: uppercase;
}

.pill-ok {
    background: #dcfce7;
    color: #166534;
}

.pill-low {
    background: #fef3c7;
    color: #92400e;
}

.pill-out {
    background: #fee2e2;
    color: #991b1b;
}

/* Switch Toggle */
.switch-toggle {
    position: relative;
    display: inline-block;
    width: 38px;
    height: 22px;
}

.switch-toggle input {
    opacity: 0;
    width: 0;
    height: 0;
}

.slider {
    position: absolute;
    cursor: pointer;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-color: #cbd5e1;
    transition: 0.2s;
    border-radius: 22px;
}

.slider:before {
    position: absolute;
    content: "";
    height: 16px;
    width: 16px;
    left: 3px;
    bottom: 3px;
    background-color: white;
    transition: 0.2s;
    border-radius: 50%;
}

input:checked+.slider {
    background-color: #16a34a;
}

input:checked+.slider:before {
    transform: translateX(16px);
}

/* Star Button */
.btn-star {
    font-size: 1.35rem;
    color: #cbd5e1;
    transition: color 0.15s;
}

.btn-star.starred {
    color: #f59e0b;
}

/* Action Save Button */
.btn-save {
    background: #0f172a;
    color: #fff;
    font-size: 0.8rem;
    font-weight: 600;
    padding: 0.4rem 0.95rem;
    border-radius: var(--radius-sm);
    transition: all 0.15s;
}

.btn-save:hover:not(:disabled) {
    background: var(--primary);
}

.btn-save:disabled {
    opacity: 0.35;
    cursor: not-allowed;
}

.saved-text {
    color: #86efac;
}

.loading-wrap {
    padding: 5rem 0;
}

.error-banner {
    background: #fef2f2;
    border: 1px solid #fecaca;
    color: #dc2626;
    padding: 1.25rem;
    border-radius: var(--radius-md);
}
</style>
