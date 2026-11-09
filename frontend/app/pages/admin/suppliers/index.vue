<!-- frontend/app/pages/admin/suppliers/index.vue -->
<template>
    <div class="admin-suppliers-page">
        <div class="workstation-container">
            <!-- Header Section -->
            <div class="header-section">
                <div>
                    <span class="badge-staff">Dropship Sourcing Hub</span>
                    <h1>Suppliers & Profit Margin Workstation</h1>
                    <p class="subtitle">Manage wholesale supplier partners, supplier SKUs, and monitor product profit
                        margins.</p>
                </div>

                <div class="header-actions">
                    <button @click="openAddSupplierModal" class="btn-primary">
                        + Register Supplier
                    </button>
                </div>
            </div>

            <!-- Telemetry Profit Metrics Strip -->
            <div class="metrics-grid">
                <div class="metric-card">
                    <span class="metric-title">Average Store Margin</span>
                    <div class="metric-val text-green">
                        {{ analytics.average_margin ?? 0 }}%
                    </div>
                    <span class="metric-sub">Across all active catalog items</span>
                </div>

                <div class="metric-card">
                    <span class="metric-title">Potential Inventory Profit</span>
                    <div class="metric-val text-blue">
                        ${{ Number(analytics.total_potential_profit || 0).toFixed(2) }}
                    </div>
                    <span class="metric-sub">Expected gross profit if stock clears</span>
                </div>

                <div class="metric-card">
                    <span class="metric-title">Active Suppliers</span>
                    <div class="metric-val">
                        {{ suppliers.length }}
                    </div>
                    <span class="metric-sub">Connected fulfillment partners</span>
                </div>

                <div class="metric-card">
                    <span class="metric-title">Catalog SKUs Tracked</span>
                    <div class="metric-val">
                        {{ analytics.total_products || products.length }}
                    </div>
                    <span class="metric-sub">Products with supplier mapping</span>
                </div>
            </div>

            <!-- Navigation Tabs -->
            <div class="tab-switcher">
                <button class="tab-btn" :class="{ active: currentTab === 'sourcing' }" @click="currentTab = 'sourcing'">
                    Product Sourcing & Margins ({{ products.length }})
                </button>
                <button class="tab-btn" :class="{ active: currentTab === 'directory' }"
                    @click="currentTab = 'directory'">
                    Supplier Partner Directory ({{ suppliers.length }})
                </button>
            </div>

            <!-- TAB 1: PRODUCT SOURCING & PROFIT MARGIN TABLE -->
            <div v-if="currentTab === 'sourcing'" class="tab-content">
                <!-- Filter Toolbar -->
                <div class="toolbar-card">
                    <div class="search-box">
                        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor"
                            stroke-width="2">
                            <circle cx="11" cy="11" r="8"></circle>
                            <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
                        </svg>
                        <input v-model="searchQuery" type="text"
                            placeholder="Search by Product name, Supplier SKU, or Supplier name..."
                            @input="debounceSearch" />
                    </div>

                    <div class="filter-group">
                        <label>Filter Supplier:</label>
                        <select v-model="selectedSupplierFilter" @change="loadSourcing">
                            <option value="">All Suppliers</option>
                            <option v-for="sup in suppliers" :key="sup.id" :value="sup.id">
                                {{ sup.name }}
                            </option>
                        </select>
                    </div>
                </div>

                <!-- Feedback Notification -->
                <div v-if="feedback" class="feedback-banner">
                    {{ feedback }}
                </div>

                <!-- Sourcing Table -->
                <div class="table-card">
                    <table class="sourcing-table">
                        <thead>
                            <tr>
                                <th>Product Item</th>
                                <th>Supplier Partner</th>
                                <th>Supplier SKU</th>
                                <th>Wholesale Cost ($)</th>
                                <th>Retail Price ($)</th>
                                <th>Net Profit ($)</th>
                                <th>Profit Margin (%)</th>
                                <th>Actions</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="p in products" :key="p.id" class="table-row">
                                <!-- Product Thumbnail & Title -->
                                <td class="col-product">
                                    <div class="product-cell">
                                        <img v-if="p.image" :src="p.image" :alt="p.name" class="p-thumb" />
                                        <div v-else class="thumb-fallback">{{ p.name[0] }}</div>
                                        <div>
                                            <strong class="p-name">{{ p.name }}</strong>
                                            <span class="p-cat">{{ p.category_name }}</span>
                                        </div>
                                    </div>
                                </td>

                                <!-- Supplier Select -->
                                <td class="col-supplier">
                                    <select :value="editing[p.id]?.supplier_id ?? p.supplier"
                                        @change="onFieldChange(p.id, 'supplier_id', $event.target.value)"
                                        class="supplier-select">
                                        <option :value="null">Unassigned</option>
                                        <option v-for="sup in suppliers" :key="sup.id" :value="sup.id">
                                            {{ sup.name }}
                                        </option>
                                    </select>
                                </td>

                                <!-- Supplier SKU -->
                                <td class="col-sku">
                                    <input type="text" :value="editing[p.id]?.supplier_sku ?? p.supplier_sku"
                                        @input="onFieldChange(p.id, 'supplier_sku', $event.target.value)"
                                        placeholder="e.g. CJ-0012" class="input-sku" />
                                </td>

                                <!-- Wholesale Cost -->
                                <td class="col-cost">
                                    <div class="input-money-wrap">
                                        <span class="money-prefix">$</span>
                                        <input type="number" step="0.01"
                                            :value="editing[p.id]?.supplier_cost ?? p.supplier_cost"
                                            @input="onFieldChange(p.id, 'supplier_cost', $event.target.value)"
                                            class="input-money" />
                                    </div>
                                </td>

                                <!-- Retail Price -->
                                <td class="col-retail">
                                    <strong>${{ Number(p.current_price).toFixed(2) }}</strong>
                                </td>

                                <!-- Net Profit -->
                                <td class="col-profit">
                                    <strong class="text-green">${{ Number(p.net_profit).toFixed(2) }}</strong>
                                </td>

                                <!-- Margin Badge -->
                                <td class="col-margin">
                                    <span class="margin-badge" :class="{
                                        'margin-high': p.profit_margin_percentage >= 50,
                                        'margin-med': p.profit_margin_percentage >= 30 && p.profit_margin_percentage < 50,
                                        'margin-low': p.profit_margin_percentage < 30
                                    }">
                                        {{ p.profit_margin_percentage }}%
                                    </span>
                                </td>

                                <!-- Actions -->
                                <td class="col-action">
                                    <button v-if="hasChanges(p.id)" @click="saveProductSourcing(p)" class="btn-save-row"
                                        title="Save Changes">
                                        Save
                                    </button>
                                    <span v-else class="text-synced">&#10003; Synced</span>
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>

            <!-- TAB 2: SUPPLIER PARTNER DIRECTORY -->
            <div v-else class="tab-content">
                <div class="suppliers-grid">
                    <div v-for="sup in suppliers" :key="sup.id" class="supplier-card">
                        <div class="supplier-top">
                            <div>
                                <h3>{{ sup.name }}</h3>
                                <span class="shipping-pill"><i class="fa-solid fa-bolt"></i> Avg Shipping: {{ sup.average_shipping_days }} days</span>
                            </div>
                            <span class="prod-count-badge">{{ sup.products_count || 0 }} products</span>
                        </div>

                        <div class="supplier-info-list">
                            <p v-if="sup.contact_name"><strong>Contact:</strong> {{ sup.contact_name }}</p>
                            <p v-if="sup.email"><strong>Email:</strong> {{ sup.email }}</p>
                            <p v-if="sup.website_url">
                                <strong>Portal:</strong>
                                <a :href="sup.website_url" target="_blank" rel="noopener" class="link-ext">
                                    {{ sup.website_url }} &nearr;
                                </a>
                            </p>
                            <p v-if="sup.notes" class="supplier-notes">{{ sup.notes }}</p>
                        </div>

                        <div class="supplier-actions">
                            <button @click="openEditSupplierModal(sup)" class="btn-edit-sup">Edit</button>
                            <button @click="handleDeleteSupplier(sup)" class="btn-del-sup">Remove</button>
                        </div>
                    </div>
                </div>
            </div>

            <!-- ADD / EDIT SUPPLIER MODAL -->
            <div v-if="isSupplierModalOpen" class="modal-overlay" @click.self="isSupplierModalOpen = false">
                <div class="modal-card">
                    <div class="modal-header">
                        <h2>{{ editingSupplierId ? 'Edit Supplier' : 'Register New Supplier' }}</h2>
                        <button @click="isSupplierModalOpen = false" class="btn-close">&times;</button>
                    </div>

                    <form @submit.prevent="handleSaveSupplier" class="supplier-form">
                        <div class="form-group">
                            <label>Company Name *</label>
                            <input v-model="supplierForm.name" type="text" required
                                placeholder="e.g. CJ Dropshipping, Spocket" />
                        </div>

                        <div class="form-row">
                            <div class="form-group">
                                <label>Contact Rep</label>
                                <input v-model="supplierForm.contact_name" type="text"
                                    placeholder="e.g. Logistics Account Manager" />
                            </div>
                            <div class="form-group">
                                <label>Email Address</label>
                                <input v-model="supplierForm.email" type="email" placeholder="e.g. vendor@supply.com" />
                            </div>
                        </div>

                        <div class="form-row">
                            <div class="form-group">
                                <label>Catalog / Portal URL</label>
                                <input v-model="supplierForm.website_url" type="url" placeholder="https://..." />
                            </div>
                            <div class="form-group">
                                <label>Avg Shipping (Days)</label>
                                <input v-model.number="supplierForm.average_shipping_days" type="number" min="1"
                                    max="60" />
                            </div>
                        </div>

                        <div class="form-group">
                            <label>Sourcing & Integration Notes</label>
                            <textarea v-model="supplierForm.notes" rows="3"
                                placeholder="Notes about shipping carriers, fulfillment policies, or discounts..."></textarea>
                        </div>

                        <div class="modal-actions">
                            <button type="button" @click="isSupplierModalOpen = false"
                                class="btn-cancel">Cancel</button>
                            <button type="submit" class="btn-submit" :disabled="savingSupplier">
                                {{ savingSupplier ? 'Saving...' : 'Save Supplier' }}
                            </button>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
definePageMeta({
    middleware: 'auth'
})

const {
    getSuppliers,
    createSupplier,
    updateSupplier,
    deleteSupplier,
    getProductSourcing,
    updateProductSourcing
} = useAdminApi()

const currentTab = ref('sourcing')
const suppliers = ref([])
const products = ref([])
const analytics = ref({})
const loading = ref(true)

const searchQuery = ref('')
const selectedSupplierFilter = ref('')
const feedback = ref('')

// Sourcing edits map: { [productId]: { supplier_id, supplier_cost, supplier_sku } }
const editing = reactive({})

// Supplier modal
const isSupplierModalOpen = ref(false)
const editingSupplierId = ref(null)
const savingSupplier = ref(false)
const supplierForm = reactive({
    name: '',
    contact_name: '',
    email: '',
    website_url: '',
    average_shipping_days: 7,
    notes: ''
})

let searchTimer = null

async function loadData() {
    loading.value = true
    await Promise.all([loadSuppliers(), loadSourcing()])
    loading.value = false
}

async function loadSuppliers() {
    try {
        const data = await getSuppliers()
        suppliers.value = Array.isArray(data) ? data : []
    } catch (err) {
        console.error('Failed to load suppliers:', err)
    }
}

async function loadSourcing() {
    try {
        const params = {}
        if (selectedSupplierFilter.value) params.supplier = selectedSupplierFilter.value
        if (searchQuery.value.trim()) params.search = searchQuery.value.trim()

        const res = await getProductSourcing(params)
        products.value = res.products || []
        analytics.value = res.analytics || {}
    } catch (err) {
        console.error('Failed to load product sourcing:', err)
    }
}

function debounceSearch() {
    clearTimeout(searchTimer)
    searchTimer = setTimeout(() => {
        loadSourcing()
    }, 300)
}

function onFieldChange(productId, field, value) {
    if (!editing[productId]) {
        editing[productId] = {}
    }
    editing[productId][field] = value
}

function hasChanges(productId) {
    return editing[productId] && Object.keys(editing[productId]).length > 0
}

async function saveProductSourcing(product) {
    const patchData = editing[product.id]
    if (!patchData) return

    try {
        const updated = await updateProductSourcing(product.id, patchData)
        // Replace with fresh updated row
        const idx = products.value.findIndex(p => p.id === product.id)
        if (idx !== -1) {
            products.value[idx] = updated
        }
        delete editing[product.id]
        showFeedback(`Saved sourcing for '${updated.name}' (Margin: ${updated.profit_margin_percentage}%)`)
        // Reload analytics
        await loadSourcing()
    } catch (err) {
        alert(err.message || 'Failed to update product sourcing.')
    }
}

function showFeedback(msg) {
    feedback.value = msg
    setTimeout(() => { feedback.value = '' }, 3500)
}

// Supplier Modal Methods
function openAddSupplierModal() {
    editingSupplierId.value = null
    supplierForm.name = ''
    supplierForm.contact_name = ''
    supplierForm.email = ''
    supplierForm.website_url = ''
    supplierForm.average_shipping_days = 7
    supplierForm.notes = ''
    isSupplierModalOpen.value = true
}

function openEditSupplierModal(sup) {
    editingSupplierId.value = sup.id
    supplierForm.name = sup.name
    supplierForm.contact_name = sup.contact_name
    supplierForm.email = sup.email
    supplierForm.website_url = sup.website_url
    supplierForm.average_shipping_days = sup.average_shipping_days
    supplierForm.notes = sup.notes
    isSupplierModalOpen.value = true
}

async function handleSaveSupplier() {
    savingSupplier.value = true
    try {
        if (editingSupplierId.value) {
            await updateSupplier(editingSupplierId.value, supplierForm)
            showFeedback(`Supplier '${supplierForm.name}' updated.`)
        } else {
            await createSupplier(supplierForm)
            showFeedback(`Supplier '${supplierForm.name}' created!`)
        }
        isSupplierModalOpen.value = false
        await loadSuppliers()
    } catch (err) {
        alert(err.message || 'Failed to save supplier.')
    } finally {
        savingSupplier.value = false
    }
}

async function handleDeleteSupplier(sup) {
    if (confirm(`Remove supplier partner '${sup.name}'? Existing assigned products will remain active.`)) {
        try {
            await deleteSupplier(sup.id)
            showFeedback(`Supplier '${sup.name}' removed.`)
            await loadSuppliers()
            await loadSourcing()
        } catch (err) {
            alert(err.message || 'Failed to delete supplier.')
        }
    }
}

onMounted(() => {
    loadData()
})
</script>

<style scoped>
.admin-suppliers-page {
    padding: 2.5rem 1.5rem 5rem;
    background: var(--bg-page);
    min-height: 90vh;
}

.workstation-container {
    max-width: 1400px;
    margin: 0 auto;
}

.header-section {
    display: flex;
    justify-content: space-between;
    align-items: flex-end;
    margin-bottom: 2rem;
}

.badge-staff {
    display: inline-block;
    background: #0284c7;
    color: #fff;
    font-size: 0.72rem;
    font-weight: 700;
    text-transform: uppercase;
    padding: 0.2rem 0.55rem;
    border-radius: 9999px;
    margin-bottom: 0.5rem;
}

.header-section h1 {
    font-size: 2rem;
    font-weight: 800;
    letter-spacing: -0.02em;
}

.subtitle {
    color: var(--text-muted);
    font-size: 0.95rem;
}

.btn-primary {
    background: var(--primary);
    color: #fff;
    border: none;
    padding: 0.75rem 1.5rem;
    border-radius: var(--radius-md);
    font-weight: 600;
    cursor: pointer;
    transition: background 0.15s;
}

.btn-primary:hover {
    background: var(--primary-hover, #4f46e5);
}

/* Metrics Grid */
.metrics-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 1.5rem;
    margin-bottom: 2rem;
}

.metric-card {
    background: var(--bg-surface);
    border: 1px solid var(--border-color);
    border-radius: var(--radius-lg);
    padding: 1.5rem;
}

.metric-title {
    display: block;
    font-size: 0.8rem;
    font-weight: 700;
    text-transform: uppercase;
    color: var(--text-muted);
    margin-bottom: 0.4rem;
}

.metric-val {
    font-size: 1.85rem;
    font-weight: 800;
    margin-bottom: 0.2rem;
}

.text-green {
    color: #10b981;
}

.text-blue {
    color: #3b82f6;
}

.metric-sub {
    font-size: 0.75rem;
    color: var(--text-muted);
}

/* Tab Switcher */
.tab-switcher {
    display: flex;
    gap: 0.5rem;
    border-bottom: 2px solid var(--border-color);
    margin-bottom: 1.5rem;
}

.tab-btn {
    padding: 0.75rem 1.5rem;
    background: transparent;
    border: none;
    font-size: 0.95rem;
    font-weight: 700;
    color: var(--text-muted);
    cursor: pointer;
    border-bottom: 2px solid transparent;
    margin-bottom: -2px;
    transition: all 0.15s;
}

.tab-btn:hover {
    color: var(--text-main);
}

.tab-btn.active {
    color: var(--primary);
    border-bottom-color: var(--primary);
}

/* Toolbar */
.toolbar-card {
    background: var(--bg-surface);
    border: 1px solid var(--border-color);
    border-radius: var(--radius-lg);
    padding: 1rem 1.5rem;
    display: flex;
    gap: 1.5rem;
    justify-content: space-between;
    margin-bottom: 1.5rem;
}

.search-box {
    display: flex;
    align-items: center;
    gap: 0.65rem;
    background: var(--bg-page);
    border: 1px solid var(--border-color);
    border-radius: var(--radius-md);
    padding: 0.55rem 0.95rem;
    flex: 1;
    max-width: 520px;
}

.search-box input {
    border: none;
    background: transparent;
    width: 100%;
    font-size: 0.9rem;
    outline: none;
    color: var(--text-main);
}

.filter-group {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    font-size: 0.85rem;
    color: var(--text-muted);
}

.filter-group select {
    padding: 0.5rem 0.85rem;
    border: 1px solid var(--border-color);
    border-radius: var(--radius-sm);
    background: var(--bg-page);
    color: var(--text-main);
    font-size: 0.85rem;
}

.feedback-banner {
    background: #ecfdf5;
    border: 1px solid #a7f3d0;
    color: #065f46;
    padding: 0.75rem 1.25rem;
    border-radius: var(--radius-md);
    margin-bottom: 1.5rem;
    font-size: 0.9rem;
    font-weight: 600;
}

/* Sourcing Table */
.table-card {
    background: var(--bg-surface);
    border: 1px solid var(--border-color);
    border-radius: var(--radius-lg);
    overflow-x: auto;
    box-shadow: var(--shadow-sm);
}

.sourcing-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 0.88rem;
    text-align: left;
}

.sourcing-table th {
    background: #f8fafc;
    padding: 1rem;
    font-size: 0.75rem;
    font-weight: 700;
    text-transform: uppercase;
    color: var(--text-muted);
    border-bottom: 1px solid var(--border-color);
}

.sourcing-table td {
    padding: 1rem;
    border-bottom: 1px solid var(--border-color);
    vertical-align: middle;
}

.product-cell {
    display: flex;
    align-items: center;
    gap: 0.75rem;
}

.p-thumb {
    width: 40px;
    height: 40px;
    border-radius: var(--radius-sm);
    object-fit: cover;
    background: #e2e8f0;
}

.thumb-fallback {
    width: 40px;
    height: 40px;
    border-radius: var(--radius-sm);
    background: #e2e8f0;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 700;
    color: var(--text-muted);
}

.p-name {
    display: block;
    font-weight: 700;
    line-height: 1.3;
}

.p-cat {
    font-size: 0.75rem;
    color: var(--text-muted);
}

.supplier-select {
    padding: 0.45rem 0.65rem;
    border: 1px solid var(--border-color);
    border-radius: var(--radius-sm);
    background: var(--bg-page);
    color: var(--text-main);
    font-size: 0.85rem;
    width: 160px;
}

.input-sku {
    padding: 0.45rem 0.65rem;
    border: 1px solid var(--border-color);
    border-radius: var(--radius-sm);
    background: var(--bg-page);
    color: var(--text-main);
    font-family: monospace;
    font-size: 0.85rem;
    width: 110px;
}

.input-money-wrap {
    display: flex;
    align-items: center;
    border: 1px solid var(--border-color);
    border-radius: var(--radius-sm);
    background: var(--bg-page);
    width: 100px;
    padding: 0 0.45rem;
}

.money-prefix {
    color: var(--text-muted);
    font-weight: 700;
    font-size: 0.85rem;
}

.input-money {
    border: none;
    background: transparent;
    width: 100%;
    padding: 0.45rem 0.25rem;
    font-size: 0.88rem;
    font-weight: 700;
    color: var(--text-main);
    outline: none;
}

.margin-badge {
    display: inline-block;
    padding: 0.25rem 0.6rem;
    border-radius: 9999px;
    font-size: 0.78rem;
    font-weight: 800;
}

.margin-high {
    background: #d1fae5;
    color: #065f46;
}

.margin-med {
    background: #fef3c7;
    color: #92400e;
}

.margin-low {
    background: #fee2e2;
    color: #991b1b;
}

.btn-save-row {
    background: #10b981;
    color: #fff;
    border: none;
    padding: 0.35rem 0.75rem;
    border-radius: var(--radius-sm);
    font-size: 0.78rem;
    font-weight: 700;
    cursor: pointer;
}

.text-synced {
    font-size: 0.75rem;
    color: var(--text-muted);
}

/* Supplier Directory Grid */
.suppliers-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(340px, 1fr));
    gap: 1.5rem;
}

.supplier-card {
    background: var(--bg-surface);
    border: 1px solid var(--border-color);
    border-radius: var(--radius-lg);
    padding: 1.75rem;
    display: flex;
    flex-direction: column;
}

.supplier-top {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: 1.25rem;
    padding-bottom: 1rem;
    border-bottom: 1px solid var(--border-color);
}

.supplier-top h3 {
    font-size: 1.25rem;
    font-weight: 700;
    margin-bottom: 0.25rem;
}

.shipping-pill {
    font-size: 0.75rem;
    color: #3b82f6;
    font-weight: 600;
}

.prod-count-badge {
    background: #f1f5f9;
    color: var(--text-muted);
    font-size: 0.75rem;
    font-weight: 700;
    padding: 0.2rem 0.55rem;
    border-radius: 9999px;
}

.supplier-info-list {
    font-size: 0.88rem;
    line-height: 1.6;
    margin-bottom: 1.5rem;
    flex: 1;
}

.supplier-info-list p {
    margin-bottom: 0.35rem;
}

.link-ext {
    color: var(--primary);
    text-decoration: none;
    font-weight: 600;
}

.supplier-notes {
    margin-top: 0.75rem;
    padding: 0.65rem;
    background: var(--bg-page);
    border-radius: var(--radius-sm);
    font-size: 0.8rem;
    color: var(--text-muted);
}

.supplier-actions {
    display: flex;
    gap: 0.75rem;
    margin-top: auto;
}

.btn-edit-sup {
    flex: 1;
    background: var(--bg-page);
    border: 1px solid var(--border-color);
    padding: 0.5rem;
    border-radius: var(--radius-sm);
    font-weight: 600;
    font-size: 0.85rem;
    cursor: pointer;
}

.btn-del-sup {
    background: #fef2f2;
    border: 1px solid #fecaca;
    color: #b91c1c;
    padding: 0.5rem 0.85rem;
    border-radius: var(--radius-sm);
    font-weight: 600;
    font-size: 0.85rem;
    cursor: pointer;
}

/* Modal Overlay */
.modal-overlay {
    position: fixed;
    inset: 0;
    background: rgba(15, 23, 42, 0.6);
    backdrop-filter: blur(4px);
    z-index: 100;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 1.5rem;
}

.modal-card {
    background: var(--bg-surface);
    border: 1px solid var(--border-color);
    border-radius: var(--radius-xl);
    width: 100%;
    max-width: 600px;
    box-shadow: var(--shadow-xl);
}

.modal-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1.5rem 2rem;
    border-bottom: 1px solid var(--border-color);
}

.btn-close {
    background: transparent;
    border: none;
    font-size: 1.5rem;
    color: var(--text-muted);
    cursor: pointer;
}

.supplier-form {
    padding: 2rem;
}

.form-row {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 1rem;
}

.form-group {
    margin-bottom: 1.25rem;
}

.form-group label {
    display: block;
    font-size: 0.85rem;
    font-weight: 600;
    margin-bottom: 0.35rem;
}

.form-group input,
.form-group textarea {
    width: 100%;
    padding: 0.65rem 0.85rem;
    border: 1px solid var(--border-color);
    border-radius: var(--radius-sm);
    background: var(--bg-page);
    color: var(--text-main);
    outline: none;
    font-size: 0.9rem;
}

.form-group input:focus,
.form-group textarea:focus {
    border-color: var(--primary);
}

.modal-actions {
    display: flex;
    justify-content: flex-end;
    gap: 0.75rem;
    margin-top: 1.5rem;
}

.btn-cancel {
    background: var(--bg-page);
    border: 1px solid var(--border-color);
    padding: 0.65rem 1.25rem;
    border-radius: var(--radius-sm);
    font-weight: 600;
    cursor: pointer;
}

.btn-submit {
    background: var(--primary);
    color: #fff;
    border: none;
    padding: 0.65rem 1.5rem;
    border-radius: var(--radius-sm);
    font-weight: 700;
    cursor: pointer;
}

@media (max-width: 1024px) {
    .metrics-grid {
        grid-template-columns: 1fr 1fr;
    }
}

@media (max-width: 640px) {
    .metrics-grid {
        grid-template-columns: 1fr;
    }

    .form-row {
        grid-template-columns: 1fr;
    }
}
</style>
