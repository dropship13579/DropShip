<script setup>
const route = useRoute()
const router = useRouter()

const { getCategories, getProducts } = useProducts()

const categories = ref([])
const products = ref([])
const totalCount = ref(0)
const loading = ref(true)

// Mobile Drawer State
const isMobileDrawerOpen = ref(false)

// Filter & Sort State (initialized from URL query)
const selectedCategory = ref(route.query.category || '')
const searchQuery = ref(route.query.search || '')
const selectedSort = ref(route.query.sort || 'newest')
const currentPage = ref(Number(route.query.page) || 1)

const minPrice = ref(route.query.min_price || '')
const maxPrice = ref(route.query.max_price || '')
const minRating = ref(route.query.min_rating || '')
const inStockOnly = ref(route.query.in_stock === 'true')
const onSaleOnly = ref(route.query.on_sale === 'true')

// Price presets helper
const pricePresets = [
    { id: 'all', label: 'All Prices', min: '', max: '' },
    { id: 'under_25', label: 'Under $25', min: '', max: '25' },
    { id: '25_50', label: '$25 to $50', min: '25', max: '50' },
    { id: '50_100', label: '$50 to $100', min: '50', max: '100' },
    { id: 'over_100', label: '$100 & Above', min: '100', max: '' },
]

const currentPricePreset = computed(() => {
    const min = minPrice.value ? String(minPrice.value) : ''
    const max = maxPrice.value ? String(maxPrice.value) : ''
    if (!min && !max) return 'all'
    const found = pricePresets.find(p => p.min === min && p.max === max)
    return found ? found.id : 'custom'
})

// Number of currently active filters (excluding sort and pagination)
const activeFilterCount = computed(() => {
    let count = 0
    if (selectedCategory.value) count++
    if (searchQuery.value) count++
    if (minPrice.value || maxPrice.value) count++
    if (minRating.value) count++
    if (inStockOnly.value) count++
    if (onSaleOnly.value) count++
    return count
})

// Sync state on URL change (e.g. Back/Forward button)
watch(() => route.query, (newQuery) => {
    selectedCategory.value = newQuery.category || ''
    searchQuery.value = newQuery.search || ''
    selectedSort.value = newQuery.sort || 'newest'
    currentPage.value = Number(newQuery.page) || 1
    minPrice.value = newQuery.min_price || ''
    maxPrice.value = newQuery.max_price || ''
    minRating.value = newQuery.min_rating || ''
    inStockOnly.value = newQuery.in_stock === 'true'
    onSaleOnly.value = newQuery.on_sale === 'true'
    fetchProducts()
})

async function fetchProducts() {
    loading.value = true
    try {
        const data = await getProducts({
            category: selectedCategory.value,
            search: searchQuery.value,
            sort: selectedSort.value,
            page: currentPage.value,
            min_price: minPrice.value,
            max_price: maxPrice.value,
            min_rating: minRating.value,
            in_stock: inStockOnly.value,
            on_sale: onSaleOnly.value,
        })
        products.value = data?.results || []
        totalCount.value = data?.count || 0
    } catch (err) {
        console.error('Failed to fetch products', err)
        products.value = []
        totalCount.value = 0
    } finally {
        loading.value = false
    }
}

function updateQuery() {
    const query = {}
    if (selectedCategory.value) query.category = selectedCategory.value
    if (searchQuery.value) query.search = searchQuery.value
    if (selectedSort.value && selectedSort.value !== 'newest') query.sort = selectedSort.value
    if (currentPage.value > 1) query.page = currentPage.value
    if (minPrice.value) query.min_price = minPrice.value
    if (maxPrice.value) query.max_price = maxPrice.value
    if (minRating.value) query.min_rating = minRating.value
    if (inStockOnly.value) query.in_stock = 'true'
    if (onSaleOnly.value) query.on_sale = 'true'

    router.push({
        path: '/shop',
        query
    })
}

// Filter Action Handlers
function onCategorySelect(slug) {
    selectedCategory.value = slug
    currentPage.value = 1
    updateQuery()
}

function selectPricePreset(preset) {
    minPrice.value = preset.min
    maxPrice.value = preset.max
    currentPage.value = 1
    updateQuery()
}

function applyCustomPrice() {
    currentPage.value = 1
    updateQuery()
}

function selectRating(val) {
    minRating.value = minRating.value === String(val) ? '' : String(val)
    currentPage.value = 1
    updateQuery()
}

function toggleInStock() {
    inStockOnly.value = !inStockOnly.value
    currentPage.value = 1
    updateQuery()
}

function toggleOnSale() {
    onSaleOnly.value = !onSaleOnly.value
    currentPage.value = 1
    updateQuery()
}

function onSortChange() {
    currentPage.value = 1
    updateQuery()
}

function clearSearch() {
    searchQuery.value = ''
    currentPage.value = 1
    updateQuery()
}

function clearPrice() {
    minPrice.value = ''
    maxPrice.value = ''
    currentPage.value = 1
    updateQuery()
}

function resetAllFilters() {
    selectedCategory.value = ''
    searchQuery.value = ''
    selectedSort.value = 'newest'
    minPrice.value = ''
    maxPrice.value = ''
    minRating.value = ''
    inStockOnly.value = false
    onSaleOnly.value = false
    currentPage.value = 1
    isMobileDrawerOpen.value = false
    updateQuery()
}

function onPageChange(page) {
    currentPage.value = page
    updateQuery()
    window.scrollTo({ top: 0, behavior: 'smooth' })
}

function getCategoryName(slug) {
    const cat = categories.value.find(c => c.slug === slug)
    return cat ? cat.name : slug
}

onMounted(async () => {
    try {
        categories.value = await getCategories() || []
    } catch (err) {
        console.error('Failed to load categories', err)
    }
    await fetchProducts()
})
</script>

<template>
    <div class="shop-page">
        <div class="shop-container">
            <!-- Header Banner -->
            <div class="shop-header">
                <div>
                    <h1 class="shop-title">Explore Store Catalog</h1>
                    <p class="results-count" v-if="!loading">
                        Showing {{ products.length }} of {{ totalCount }} available products
                    </p>
                </div>

                <!-- Mobile Filter Trigger -->
                <button class="btn-mobile-filter" @click="isMobileDrawerOpen = true">
                    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <polygon points="22 3 2 3 10 12.46 10 19 14 21 14 12.46 22 3"></polygon>
                    </svg>
                    <span>Filters</span>
                    <span v-if="activeFilterCount > 0" class="filter-count-badge">{{ activeFilterCount }}</span>
                </button>
            </div>

            <!-- Top Horizontal Category Navigation Bar -->
            <CategoryNav :categories="categories" :selected-category="selectedCategory" @select="onCategorySelect" />

            <!-- Main Layout: Sidebar Filters + Products Area -->
            <div class="shop-layout">
                <!-- Desktop Sidebar Filters -->
                <aside class="shop-sidebar">
                    <div class="sidebar-header">
                        <h2 class="sidebar-title">Filters</h2>
                        <button v-if="activeFilterCount > 0" class="btn-clear-all" @click="resetAllFilters">
                            Reset All
                        </button>
                    </div>

                    <!-- Category Facet List -->
                    <div class="filter-group">
                        <h3 class="filter-heading">Categories</h3>
                        <div class="filter-options">
                            <label class="filter-radio-row" :class="{ 'selected': selectedCategory === '' }">
                                <input type="radio" name="desktop-category" :checked="selectedCategory === ''"
                                    @change="onCategorySelect('')">
                                <span class="radio-label">All Categories</span>
                            </label>
                            <label v-for="cat in categories" :key="cat.id" class="filter-radio-row"
                                :class="{ 'selected': selectedCategory === cat.slug }">
                                <input type="radio" name="desktop-category" :checked="selectedCategory === cat.slug"
                                    @change="onCategorySelect(cat.slug)">
                                <span class="radio-label">{{ cat.name }}</span>
                                <span v-if="cat.product_count" class="facet-badge">{{ cat.product_count }}</span>
                            </label>
                        </div>
                    </div>

                    <!-- Price Range Facet -->
                    <div class="filter-group">
                        <h3 class="filter-heading">Price Range</h3>
                        <div class="price-presets">
                            <button v-for="preset in pricePresets" :key="preset.id" type="button"
                                class="price-preset-btn" :class="{ 'active': currentPricePreset === preset.id }"
                                @click="selectPricePreset(preset)">
                                {{ preset.label }}
                            </button>
                        </div>

                        <!-- Custom Min / Max Inputs -->
                        <div class="custom-price-inputs">
                            <div class="price-input-box">
                                <span class="currency-symbol">$</span>
                                <input type="number" min="0" placeholder="Min" v-model="minPrice"
                                    @keydown.enter="applyCustomPrice" />
                            </div>
                            <span class="range-divider">-</span>
                            <div class="price-input-box">
                                <span class="currency-symbol">$</span>
                                <input type="number" min="0" placeholder="Max" v-model="maxPrice"
                                    @keydown.enter="applyCustomPrice" />
                            </div>
                            <button type="button" class="btn-apply-price" @click="applyCustomPrice">Go</button>
                        </div>
                    </div>

                    <!-- Customer Reviews / Star Rating Facet -->
                    <div class="filter-group">
                        <h3 class="filter-heading">Customer Rating</h3>
                        <div class="rating-options">
                            <button type="button" class="rating-row-btn" :class="{ 'active': minRating === '4' }"
                                @click="selectRating(4)">
                                <span class="gold-stars">
                                    <i class="fa-solid fa-star"></i><i class="fa-solid fa-star"></i><i class="fa-solid fa-star"></i><i class="fa-solid fa-star"></i><i class="fa-regular fa-star"></i>
                                </span>
                                <span class="rating-text">4.0 & Up</span>
                            </button>
                            <button type="button" class="rating-row-btn" :class="{ 'active': minRating === '3' }"
                                @click="selectRating(3)">
                                <span class="gold-stars">
                                    <i class="fa-solid fa-star"></i><i class="fa-solid fa-star"></i><i class="fa-solid fa-star"></i><i class="fa-regular fa-star"></i><i class="fa-regular fa-star"></i>
                                </span>
                                <span class="rating-text">3.0 & Up</span>
                            </button>
                            <button type="button" class="rating-row-btn" :class="{ 'active': minRating === '2' }"
                                @click="selectRating(2)">
                                <span class="gold-stars">
                                    <i class="fa-solid fa-star"></i><i class="fa-solid fa-star"></i><i class="fa-regular fa-star"></i><i class="fa-regular fa-star"></i><i class="fa-regular fa-star"></i>
                                </span>
                                <span class="rating-text">2.0 & Up</span>
                            </button>
                        </div>
                    </div>

                    <!-- Availability & Deals Switches -->
                    <div class="filter-group">
                        <h3 class="filter-heading">Preferences</h3>
                        <div class="toggle-list">
                            <label class="toggle-row">
                                <span class="toggle-label">In Stock Only</span>
                                <div class="switch" :class="{ 'active': inStockOnly }" @click.prevent="toggleInStock">
                                    <span class="slider"></span>
                                </div>
                            </label>

                            <label class="toggle-row">
                                <span class="toggle-label">
                                    On Sale Deals
                                    <span class="deal-pill">SALE</span>
                                </span>
                                <div class="switch" :class="{ 'active': onSaleOnly }" @click.prevent="toggleOnSale">
                                    <span class="slider"></span>
                                </div>
                            </label>
                        </div>
                    </div>
                </aside>

                <!-- Products Display Area -->
                <main class="shop-main">
                    <!-- Toolbar: Active Filter Chips & Sort Selector -->
                    <div class="shop-toolbar">
                        <div class="active-chips-area">
                            <span v-if="searchQuery" class="filter-chip">
                                Search: "{{ searchQuery }}"
                                <button type="button" @click="clearSearch" class="chip-remove" title="Remove"><i class="fa-solid fa-xmark"></i></button>
                            </span>

                            <span v-if="selectedCategory" class="filter-chip">
                                Category: {{ getCategoryName(selectedCategory) }}
                                <button type="button" @click="onCategorySelect('')" class="chip-remove"
                                    title="Remove"><i class="fa-solid fa-xmark"></i></button>
                            </span>

                            <span v-if="minPrice || maxPrice" class="filter-chip">
                                Price: {{ minPrice ? `$${minPrice}` : '$0' }} - {{ maxPrice ? `$${maxPrice}` : 'Above'
                                }}
                                <button type="button" @click="clearPrice" class="chip-remove" title="Remove"><i class="fa-solid fa-xmark"></i></button>
                            </span>

                            <span v-if="minRating" class="filter-chip">
                                Rating: {{ minRating }} <i class="fa-solid fa-star"></i> & Up
                                <button type="button" @click="selectRating(minRating)" class="chip-remove"
                                    title="Remove"><i class="fa-solid fa-xmark"></i></button>
                            </span>

                            <span v-if="inStockOnly" class="filter-chip">
                                In Stock
                                <button type="button" @click="toggleInStock" class="chip-remove"
                                    title="Remove"><i class="fa-solid fa-xmark"></i></button>
                            </span>

                            <span v-if="onSaleOnly" class="filter-chip">
                                On Sale
                                <button type="button" @click="toggleOnSale" class="chip-remove"
                                    title="Remove"><i class="fa-solid fa-xmark"></i></button>
                            </span>

                            <button v-if="activeFilterCount > 0" type="button" class="btn-clear-chips"
                                @click="resetAllFilters">
                                Clear All
                            </button>
                        </div>

                        <!-- Sort Dropdown -->
                        <div class="sort-box">
                            <label for="sort-select" class="sort-label">Sort by:</label>
                            <select id="sort-select" v-model="selectedSort" @change="onSortChange" class="sort-select">
                                <option value="newest">Newest Arrivals</option>
                                <option value="price_asc">Price: Low to High</option>
                                <option value="price_desc">Price: High to Low</option>
                                <option value="rating_desc">Highest Rated</option>
                                <option value="popular">Most Popular</option>
                            </select>
                        </div>
                    </div>

                    <!-- Loading State -->
                    <div v-if="loading" class="loading-container">
                        <LoadingSpinner text="Refreshing catalog items..." />
                    </div>

                    <!-- Empty State -->
                    <EmptyState v-else-if="products.length === 0" title="No matching products found"
                        description="Try widening your price range, clearing some filters, or searching for a different keyword.">
                        <template #action>
                            <button @click="resetAllFilters" class="btn-reset-large">Reset All Filters</button>
                        </template>
                    </EmptyState>

                    <!-- Product Grid & Pagination -->
                    <template v-else>
                        <ProductGrid :products="products" />
                        <div class="pagination-wrap">
                            <Pagination :current-page="currentPage" :total-count="totalCount" :page-size="12"
                                @change="onPageChange" />
                        </div>
                    </template>
                </main>
            </div>
        </div>

        <!-- Mobile Filter Off-Canvas Drawer -->
        <Teleport to="body">
            <div v-if="isMobileDrawerOpen" class="mobile-drawer-overlay" @click="isMobileDrawerOpen = false">
                <div class="mobile-drawer-sheet" @click.stop>
                    <div class="drawer-header">
                        <h2>Filter & Refine</h2>
                        <button type="button" class="btn-close-drawer" @click="isMobileDrawerOpen = false"><i class="fa-solid fa-xmark"></i></button>
                    </div>

                    <div class="drawer-content">
                        <!-- Mobile Category List -->
                        <div class="drawer-section">
                            <h3>Categories</h3>
                            <div class="drawer-radio-group">
                                <label class="drawer-radio-label">
                                    <input type="radio" name="mobile-cat" :checked="selectedCategory === ''"
                                        @change="onCategorySelect('')">
                                    <span>All Categories</span>
                                </label>
                                <label v-for="cat in categories" :key="'mob-' + cat.id" class="drawer-radio-label">
                                    <input type="radio" name="mobile-cat" :checked="selectedCategory === cat.slug"
                                        @change="onCategorySelect(cat.slug)">
                                    <span>{{ cat.name }}</span>
                                    <span v-if="cat.product_count" class="facet-badge">{{ cat.product_count }}</span>
                                </label>
                            </div>
                        </div>

                        <!-- Mobile Price Range -->
                        <div class="drawer-section">
                            <h3>Price Brackets</h3>
                            <div class="price-presets">
                                <button v-for="preset in pricePresets" :key="'mob-' + preset.id" type="button"
                                    class="price-preset-btn" :class="{ 'active': currentPricePreset === preset.id }"
                                    @click="selectPricePreset(preset)">
                                    {{ preset.label }}
                                </button>
                            </div>
                            <div class="custom-price-inputs">
                                <div class="price-input-box">
                                    <span class="currency-symbol">$</span>
                                    <input type="number" min="0" placeholder="Min" v-model="minPrice" />
                                </div>
                                <span class="range-divider">-</span>
                                <div class="price-input-box">
                                    <span class="currency-symbol">$</span>
                                    <input type="number" min="0" placeholder="Max" v-model="maxPrice" />
                                </div>
                                <button type="button" class="btn-apply-price" @click="applyCustomPrice">Go</button>
                            </div>
                        </div>

                        <!-- Mobile Rating -->
                        <div class="drawer-section">
                            <h3>Rating</h3>
                            <div class="rating-options">
                                <button type="button" class="rating-row-btn" :class="{ 'active': minRating === '4' }"
                                    @click="selectRating(4)">
                                    <span class="gold-stars">
                                        <i class="fa-solid fa-star"></i><i class="fa-solid fa-star"></i><i class="fa-solid fa-star"></i><i class="fa-solid fa-star"></i><i class="fa-regular fa-star"></i>
                                    </span>
                                    <span class="rating-text">4.0 & Up</span>
                                </button>
                                <button type="button" class="rating-row-btn" :class="{ 'active': minRating === '3' }"
                                    @click="selectRating(3)">
                                    <span class="gold-stars">
                                        <i class="fa-solid fa-star"></i><i class="fa-solid fa-star"></i><i class="fa-solid fa-star"></i><i class="fa-regular fa-star"></i><i class="fa-regular fa-star"></i>
                                    </span>
                                    <span class="rating-text">3.0 & Up</span>
                                </button>
                            </div>
                        </div>

                        <!-- Mobile Toggles -->
                        <div class="drawer-section">
                            <h3>Availability</h3>
                            <div class="toggle-list">
                                <label class="toggle-row">
                                    <span class="toggle-label">In Stock Only</span>
                                    <div class="switch" :class="{ 'active': inStockOnly }"
                                        @click.prevent="toggleInStock">
                                        <span class="slider"></span>
                                    </div>
                                </label>
                                <label class="toggle-row">
                                    <span class="toggle-label">On Sale Deals</span>
                                    <div class="switch" :class="{ 'active': onSaleOnly }" @click.prevent="toggleOnSale">
                                        <span class="slider"></span>
                                    </div>
                                </label>
                            </div>
                        </div>
                    </div>

                    <div class="drawer-footer">
                        <button type="button" class="btn-drawer-reset" @click="resetAllFilters">Reset All</button>
                        <button type="button" class="btn-drawer-apply" @click="isMobileDrawerOpen = false">
                            Show Results ({{ totalCount }})
                        </button>
                    </div>
                </div>
            </div>
        </Teleport>
    </div>
</template>

<style scoped>
.shop-page {
    padding: 2rem 1.5rem 4rem;
}

.shop-container {
    max-width: 1280px;
    margin: 0 auto;
}

/* Header */
.shop-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 1.25rem;
    gap: 1rem;
}

.shop-title {
    font-size: 2rem;
    font-weight: 800;
    color: var(--text-main);
    letter-spacing: -0.025em;
}

.results-count {
    color: var(--text-muted);
    font-size: 0.9rem;
    margin-top: 0.25rem;
}

.btn-mobile-filter {
    display: none;
    align-items: center;
    gap: 0.5rem;
    background: var(--bg-surface);
    border: 1px solid var(--border-color);
    padding: 0.6rem 1rem;
    border-radius: var(--radius-md);
    font-weight: 600;
    font-size: 0.9rem;
    color: var(--text-main);
    box-shadow: var(--shadow-sm);
}

.filter-count-badge {
    background: var(--primary);
    color: #fff;
    font-size: 0.75rem;
    padding: 0.1rem 0.45rem;
    border-radius: 9999px;
    font-weight: 700;
}

/* Main Layout */
.shop-layout {
    display: grid;
    grid-template-columns: 260px 1fr;
    gap: 2rem;
    margin-top: 1.75rem;
    align-items: start;
}

/* Sidebar */
.shop-sidebar {
    background: var(--bg-surface);
    border: 1px solid var(--border-color);
    border-radius: var(--radius-lg);
    padding: 1.5rem;
    box-shadow: var(--shadow-sm);
    position: sticky;
    top: 5rem;
}

.sidebar-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding-bottom: 1rem;
    border-bottom: 1px solid var(--border-color);
    margin-bottom: 1.25rem;
}

.sidebar-title {
    font-size: 1.15rem;
    font-weight: 800;
    color: var(--text-main);
}

.btn-clear-all {
    color: var(--primary);
    font-size: 0.825rem;
    font-weight: 700;
    background: none;
    border: none;
    cursor: pointer;
}

.btn-clear-all:hover {
    text-decoration: underline;
}

/* Filter Groups */
.filter-group {
    padding-bottom: 1.25rem;
    margin-bottom: 1.25rem;
    border-bottom: 1px solid var(--border-color);
}

.filter-group:last-child {
    border-bottom: none;
    margin-bottom: 0;
    padding-bottom: 0;
}

.filter-heading {
    font-size: 0.85rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: var(--text-muted);
    margin-bottom: 0.75rem;
}

/* Category Radios */
.filter-options {
    display: flex;
    flex-direction: column;
    gap: 0.45rem;
}

.filter-radio-row {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    font-size: 0.875rem;
    color: var(--text-main);
    cursor: pointer;
    padding: 0.25rem 0.4rem;
    border-radius: var(--radius-sm);
    transition: background 0.15s;
}

.filter-radio-row:hover {
    background: var(--bg-page);
}

.filter-radio-row.selected {
    font-weight: 700;
    color: var(--primary);
}

.radio-label {
    flex: 1;
}

.facet-badge {
    background: rgba(0, 0, 0, 0.06);
    color: var(--text-muted);
    font-size: 0.75rem;
    font-weight: 700;
    padding: 0.1rem 0.45rem;
    border-radius: 9999px;
}

/* Price Presets */
.price-presets {
    display: flex;
    flex-wrap: wrap;
    gap: 0.4rem;
    margin-bottom: 0.75rem;
}

.price-preset-btn {
    font-size: 0.8rem;
    font-weight: 600;
    padding: 0.35rem 0.65rem;
    background: var(--bg-page);
    border: 1px solid var(--border-color);
    border-radius: var(--radius-sm);
    color: var(--text-main);
    transition: all 0.15s;
}

.price-preset-btn:hover {
    border-color: var(--primary);
    color: var(--primary);
}

.price-preset-btn.active {
    background: var(--primary);
    color: #fff;
    border-color: var(--primary);
}

.custom-price-inputs {
    display: flex;
    align-items: center;
    gap: 0.35rem;
}

.price-input-box {
    display: flex;
    align-items: center;
    background: var(--bg-page);
    border: 1px solid var(--border-color);
    border-radius: var(--radius-sm);
    padding: 0.3rem 0.5rem;
    flex: 1;
}

.currency-symbol {
    font-size: 0.8rem;
    color: var(--text-muted);
    margin-right: 0.2rem;
    font-weight: 700;
}

.price-input-box input {
    width: 100%;
    border: none;
    background: transparent;
    font-size: 0.85rem;
    outline: none;
    color: var(--text-main);
}

.range-divider {
    color: var(--text-muted);
    font-weight: 700;
}

.btn-apply-price {
    background: var(--primary);
    color: #fff;
    font-size: 0.8rem;
    font-weight: 700;
    padding: 0.4rem 0.7rem;
    border-radius: var(--radius-sm);
    transition: background 0.15s;
}

.btn-apply-price:hover {
    background: var(--primary-hover);
}

/* Rating Rows */
.rating-options {
    display: flex;
    flex-direction: column;
    gap: 0.35rem;
}

.rating-row-btn {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.35rem 0.5rem;
    border-radius: var(--radius-sm);
    background: var(--bg-page);
    border: 1px solid transparent;
    cursor: pointer;
    text-align: left;
    transition: all 0.15s;
}

.rating-row-btn:hover {
    border-color: var(--border-color);
}

.rating-row-btn.active {
    background: #fffbeb;
    border-color: #f59e0b;
}

.gold-stars {
    color: #f59e0b;
    font-size: 0.85rem;
    display: inline-flex;
    align-items: center;
    gap: 0.15rem;
}

.rating-text {
    font-size: 0.85rem;
    font-weight: 600;
    color: var(--text-main);
}

/* Switches & Toggles */
.toggle-list {
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
}

.toggle-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    cursor: pointer;
}

.toggle-label {
    font-size: 0.875rem;
    font-weight: 600;
    color: var(--text-main);
    display: flex;
    align-items: center;
    gap: 0.4rem;
}

.deal-pill {
    background: #fee2e2;
    color: #ef4444;
    font-size: 0.65rem;
    font-weight: 800;
    padding: 0.1rem 0.35rem;
    border-radius: 4px;
}

.switch {
    width: 38px;
    height: 22px;
    background: #cbd5e1;
    border-radius: 9999px;
    position: relative;
    cursor: pointer;
    transition: background 0.2s;
}

.switch.active {
    background: var(--primary);
}

.switch .slider {
    width: 16px;
    height: 16px;
    background: #ffffff;
    border-radius: 50%;
    position: absolute;
    top: 3px;
    left: 3px;
    transition: transform 0.2s;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.2);
}

.switch.active .slider {
    transform: translateX(16px);
}

/* Main Content & Toolbar */
.shop-main {
    min-width: 0;
}

.shop-toolbar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 1.5rem;
    gap: 1rem;
    flex-wrap: wrap;
    background: var(--bg-surface);
    border: 1px solid var(--border-color);
    border-radius: var(--radius-lg);
    padding: 0.75rem 1.25rem;
    box-shadow: var(--shadow-sm);
}

.active-chips-area {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    flex-wrap: wrap;
    flex: 1;
}

.filter-chip {
    background: var(--primary-light);
    border: 1px solid rgba(37, 99, 235, 0.2);
    color: var(--primary);
    font-size: 0.8rem;
    font-weight: 600;
    padding: 0.3rem 0.65rem;
    border-radius: 9999px;
    display: flex;
    align-items: center;
    gap: 0.4rem;
}

.chip-remove {
    font-size: 0.75rem;
    color: var(--primary);
    cursor: pointer;
    display: flex;
    align-items: center;
    line-height: 1;
}

.chip-remove:hover {
    color: #ef4444;
}

.btn-clear-chips {
    font-size: 0.8rem;
    font-weight: 700;
    color: var(--text-muted);
    cursor: pointer;
    margin-left: 0.25rem;
}

.btn-clear-chips:hover {
    color: #ef4444;
}

/* Sort Selector */
.sort-box {
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.sort-label {
    font-size: 0.85rem;
    font-weight: 600;
    color: var(--text-muted);
    white-space: nowrap;
}

.sort-select {
    padding: 0.45rem 0.75rem;
    border: 1px solid var(--border-color);
    border-radius: var(--radius-sm);
    background: var(--bg-surface);
    color: var(--text-main);
    font-size: 0.85rem;
    font-weight: 600;
    outline: none;
    cursor: pointer;
}

.loading-container {
    padding: 4rem 0;
    display: flex;
    justify-content: center;
}

.btn-reset-large {
    background: var(--primary);
    color: #fff;
    font-weight: 700;
    padding: 0.75rem 1.75rem;
    border-radius: var(--radius-md);
    font-size: 0.95rem;
    transition: background 0.15s;
}

.btn-reset-large:hover {
    background: var(--primary-hover);
}

.pagination-wrap {
    margin-top: 2.5rem;
}

/* Mobile Off-Canvas Drawer */
.mobile-drawer-overlay {
    position: fixed;
    inset: 0;
    background: rgba(15, 23, 42, 0.55);
    backdrop-filter: blur(4px);
    z-index: 9999;
    display: flex;
    justify-content: flex-end;
}

.mobile-drawer-sheet {
    width: 100%;
    max-width: 360px;
    background: var(--bg-surface);
    height: 100%;
    display: flex;
    flex-direction: column;
    box-shadow: -4px 0 20px rgba(0, 0, 0, 0.15);
}

.drawer-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 1.25rem;
    border-bottom: 1px solid var(--border-color);
}

.drawer-header h2 {
    font-size: 1.2rem;
    font-weight: 800;
    color: var(--text-main);
}

.btn-close-drawer {
    font-size: 1.25rem;
    color: var(--text-muted);
    padding: 0.25rem;
}

.drawer-content {
    flex: 1;
    overflow-y: auto;
    padding: 1.25rem;
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
}

.drawer-section h3 {
    font-size: 0.85rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: var(--text-muted);
    margin-bottom: 0.75rem;
}

.drawer-radio-group {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
}

.drawer-radio-label {
    display: flex;
    align-items: center;
    gap: 0.6rem;
    font-size: 0.9rem;
    color: var(--text-main);
    padding: 0.25rem 0;
}

.drawer-footer {
    display: flex;
    gap: 0.75rem;
    padding: 1rem 1.25rem;
    border-top: 1px solid var(--border-color);
}

.btn-drawer-reset {
    flex: 1;
    background: var(--bg-page);
    border: 1px solid var(--border-color);
    padding: 0.75rem;
    border-radius: var(--radius-md);
    font-weight: 700;
    font-size: 0.9rem;
    color: var(--text-muted);
}

.btn-drawer-apply {
    flex: 2;
    background: var(--primary);
    color: #fff;
    padding: 0.75rem;
    border-radius: var(--radius-md);
    font-weight: 700;
    font-size: 0.9rem;
}

/* Responsive Media Queries */
@media (max-width: 960px) {
    .shop-layout {
        grid-template-columns: 1fr;
    }

    .shop-sidebar {
        display: none;
    }

    .btn-mobile-filter {
        display: flex;
    }
}
</style>
