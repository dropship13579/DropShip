<!-- frontend/app/pages/admin/products/index.vue -->
<template>
    <div class="admin-page">
        <div class="admin-container">
            <!-- Header Section -->
            <div class="admin-header">
                <div>
                    <div class="badge-tag">Catalog Operations</div>
                    <h1>Products & Categories Hub</h1>
                    <p class="subtitle">Upload new products with multi-image gallery, manage store categories, and
                        adjust live pricing.</p>
                </div>
                <div class="header-action-group">
                    <button type="button" @click="openAddCategoryModal" class="btn-action btn-add-cat">
                        <i class="fa-solid fa-folder-plus"></i>
                        <span>+ Add Category</span>
                    </button>
                    <button type="button" @click="openAddProductModal" class="btn-action btn-add-prod">
                        <i class="fa-solid fa-plus"></i>
                        <span>+ Add Product</span>
                    </button>
                    <button type="button" @click="fetchInitialData" class="btn-refresh" :disabled="loading"
                        title="Refresh catalog data">
                        <i class="fa-solid fa-arrows-rotate" :class="{ 'fa-spin': loading }"></i>
                        <span>{{ loading ? 'Syncing...' : 'Refresh' }}</span>
                    </button>
                </div>
            </div>

            <!-- Tab Switcher (Products vs Categories) -->
            <div class="view-tabs-strip">
                <button type="button" class="view-tab-btn" :class="{ active: activeViewTab === 'products' }"
                    @click="activeViewTab = 'products'">
                    <i class="fa-solid fa-boxes-stacked"></i>
                    <span>Products Inventory</span>
                    <span class="tab-count-pill">{{ products.length }}</span>
                </button>
                <button type="button" class="view-tab-btn" :class="{ active: activeViewTab === 'categories' }"
                    @click="activeViewTab = 'categories'">
                    <i class="fa-solid fa-layer-group"></i>
                    <span>Store Categories</span>
                    <span class="tab-count-pill">{{ categories.length }}</span>
                </button>
            </div>

            <!-- TAB 1: PRODUCTS INVENTORY -->
            <div v-if="activeViewTab === 'products'">
                <!-- Filters Bar -->
                <div class="filters-bar">
                    <div class="search-input-wrap">
                        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor"
                            stroke-width="2">
                            <circle cx="11" cy="11" r="8"></circle>
                            <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
                        </svg>
                        <input v-model="searchQuery" type="text"
                            placeholder="Search products by title, category, or slug..." class="search-input" />
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

                <!-- Empty State -->
                <div v-else-if="filteredProducts.length === 0" class="empty-roster-card">
                    <div class="empty-icon-circle"><i class="fa-solid fa-box-open"></i></div>
                    <h3>No products match your criteria</h3>
                    <p>Adjust your search filters or click "+ Add Product" above to publish your first item.</p>
                    <button type="button" @click="openAddProductModal" class="btn-action btn-add-prod">
                        <i class="fa-solid fa-plus"></i> Add New Product
                    </button>
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
                                    <th>Actions</th>
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
                                            <div class="meta-row">
                                                <span class="prod-slug">/products/{{ p.slug }}</span>
                                                <span v-if="p.images && p.images.length > 1" class="gallery-badge"
                                                    title="Multiple gallery images attached">
                                                    <i class="fa-solid fa-images"></i> {{ p.images.length }}
                                                </span>
                                            </div>
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

                                    <!-- Actions -->
                                    <td>
                                        <div class="action-cell">
                                            <button type="button" @click="saveProduct(p)" class="btn-save"
                                                :disabled="p._saving || !p._modified" title="Save in-table changes">
                                                <span v-if="p._saving">Saving...</span>
                                                <span v-else-if="p._saved" class="saved-text">&#10003; Saved</span>
                                                <span v-else>Save</span>
                                            </button>

                                            <button type="button" @click="confirmDeleteProduct(p)" class="btn-delete"
                                                title="Delete Product">
                                                <i class="fa-solid fa-trash-can"></i>
                                            </button>
                                        </div>
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>

            <!-- TAB 2: STORE CATEGORIES -->
            <div v-else-if="activeViewTab === 'categories'">
                <div class="categories-header-card">
                    <div>
                        <h2>Store Categories ({{ categories.length }})</h2>
                        <p>Categories group your products and display visual thumbnail badges across the shop catalog.
                        </p>
                    </div>
                    <button type="button" @click="openAddCategoryModal" class="btn-action btn-add-cat">
                        <i class="fa-solid fa-plus"></i> Create New Category
                    </button>
                </div>

                <div v-if="categories.length === 0" class="empty-roster-card">
                    <div class="empty-icon-circle"><i class="fa-solid fa-folder-open"></i></div>
                    <h3>No categories created yet</h3>
                    <p>Create your first store category with a banner/thumbnail image.</p>
                    <button type="button" @click="openAddCategoryModal" class="btn-action btn-add-cat">
                        + Add First Category
                    </button>
                </div>

                <div v-else class="categories-grid">
                    <div v-for="cat in categories" :key="cat.id" class="category-admin-card">
                        <div class="cat-card-img">
                            <img v-if="cat.image" :src="cat.image" :alt="cat.name" />
                            <div v-else class="cat-img-fallback">
                                <i class="fa-solid fa-folder"></i>
                            </div>
                            <span class="cat-status-pill" :class="cat.is_active ? 'active' : 'inactive'">
                                {{ cat.is_active ? 'Active' : 'Hidden' }}
                            </span>
                        </div>

                        <div class="cat-card-body">
                            <div class="cat-card-top">
                                <h3>{{ cat.name }}</h3>
                                <span class="cat-count">{{ cat.product_count ?? 0 }} Products</span>
                            </div>
                            <span class="cat-slug-pill">/shop?category={{ cat.slug }}</span>
                            <p class="cat-desc">{{ cat.description || 'No description provided.' }}</p>

                            <div class="cat-card-actions">
                                <NuxtLink :to="`/shop?category=${cat.slug}`" target="_blank" class="btn-view-cat">
                                    View Storefront &rarr;
                                </NuxtLink>
                                <button type="button" @click="confirmDeleteCategory(cat)" class="btn-delete-cat"
                                    title="Delete Category">
                                    <i class="fa-solid fa-trash-can"></i>
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- ============================================================= -->
            <!-- MODAL 1: ADD PRODUCT FORM (WITH MULTIPLE IMAGE UPLOAD)        -->
            <!-- ============================================================= -->
            <div v-if="isAddProductModalOpen" class="modal-overlay" @click.self="closeAddProductModal">
                <div class="modal-card modal-lg">
                    <div class="modal-header">
                        <div>
                            <div class="modal-badge-row">
                                <span class="badge-staff">Catalog Manager</span>
                                <span class="badge-accent"><i class="fa-solid fa-images"></i> Multi-Image Gallery</span>
                            </div>
                            <h2>Register New Product</h2>
                        </div>
                        <button type="button" @click="closeAddProductModal" class="btn-close-modal"
                            aria-label="Close modal">&times;</button>
                    </div>

                    <form @submit.prevent="submitCreateProduct" class="modal-body-scrollable">
                        <!-- Error Alert -->
                        <div v-if="productFormError" class="modal-error-banner">
                            <i class="fa-solid fa-circle-exclamation"></i>
                            <span>{{ productFormError }}</span>
                        </div>

                        <div class="form-grid-2">
                            <!-- Product Name -->
                            <div class="form-group span-2">
                                <label for="prod-name">Product Name *</label>
                                <input id="prod-name" v-model="productForm.name" type="text" required
                                    placeholder="e.g. UltraFit Wireless Noise Cancelling Earbuds"
                                    class="form-control" />
                            </div>

                            <!-- Category Selection -->
                            <div class="form-group span-2">
                                <div class="label-with-action">
                                    <label for="prod-cat">Category *</label>
                                    <button type="button" @click="openAddCategoryModal" class="link-btn-subtle">
                                        + New Category
                                    </button>
                                </div>
                                <select id="prod-cat" v-model="productForm.category" required class="form-control">
                                    <option value="" disabled>Select Category</option>
                                    <option v-for="cat in categories" :key="cat.id" :value="cat.id">
                                        {{ cat.name }}
                                    </option>
                                </select>
                            </div>

                            <!-- Current Retail Price -->
                            <div class="form-group">
                                <label for="prod-price">Retail Selling Price ($) *</label>
                                <div class="input-dollar-wrap">
                                    <span class="currency-symbol">$</span>
                                    <input id="prod-price" v-model.number="productForm.current_price" type="number"
                                        step="0.01" min="0" required placeholder="49.99" class="form-control" />
                                </div>
                            </div>

                            <!-- Original / Compare-at Price -->
                            <div class="form-group">
                                <label for="prod-orig-price">Original / Compare Price ($)</label>
                                <div class="input-dollar-wrap">
                                    <span class="currency-symbol">$</span>
                                    <input id="prod-orig-price" v-model.number="productForm.original_price"
                                        type="number" step="0.01" min="0" placeholder="79.99 (for sale strike-through)"
                                        class="form-control" />
                                </div>
                            </div>

                            <!-- Sourcing Cost -->
                            <div class="form-group">
                                <label for="prod-cost">Unit / Wholesale Cost ($)</label>
                                <div class="input-dollar-wrap">
                                    <span class="currency-symbol">$</span>
                                    <input id="prod-cost" v-model.number="productForm.supplier_cost" type="number"
                                        step="0.01" min="0" placeholder="18.50" class="form-control" />
                                </div>
                            </div>

                            <!-- Initial Stock -->
                            <div class="form-group">
                                <label for="prod-stock">Initial Inventory Stock *</label>
                                <input id="prod-stock" v-model.number="productForm.stock_quantity" type="number" min="0"
                                    required placeholder="50" class="form-control" />
                            </div>

                            <!-- Product SKU -->
                            <div class="form-group span-2">
                                <label for="prod-sku">Product SKU / Inventory Code</label>
                                <input id="prod-sku" v-model="productForm.supplier_sku" type="text"
                                    placeholder="e.g. KYRO-AUDIO-9982-BLK" class="form-control" />
                            </div>

                            <!-- Description -->
                            <div class="form-group span-2">
                                <label for="prod-desc">Product Description & Specs</label>
                                <textarea id="prod-desc" v-model="productForm.description" rows="3"
                                    placeholder="High-converting product description, key highlights, materials, and package contents..."
                                    class="form-control"></textarea>
                            </div>

                            <!-- Storefront Status Checkboxes -->
                            <div class="form-group span-2 toggles-row">
                                <label class="checkbox-label">
                                    <input type="checkbox" v-model="productForm.is_active" />
                                    <span>Active on Storefront (Customers can view and buy)</span>
                                </label>
                                <label class="checkbox-label">
                                    <input type="checkbox" v-model="productForm.is_featured" />
                                    <span>Feature on Storefront Homepage</span>
                                </label>
                            </div>

                            <!-- MULTIPLE IMAGES UPLOAD SECTION -->
                            <div class="form-group span-2 image-upload-section">
                                <div class="upload-section-header">
                                    <label>Product Images & Photo Gallery *</label>
                                    <span class="upload-tip">Upload several photos (first image will be primary
                                        cover)</span>
                                </div>

                                <!-- Hidden File Input -->
                                <input type="file" ref="productImagesFileInput" multiple accept="image/*"
                                    @change="handleProductFilesSelected" class="visually-hidden-file-input" />

                                <!-- Drag-and-drop / Click Area -->
                                <div class="drop-zone-box" @click="$refs.productImagesFileInput.click()">
                                    <div class="drop-zone-icon">
                                        <i class="fa-solid fa-cloud-arrow-up"></i>
                                    </div>
                                    <div class="drop-zone-text">
                                        <strong>Click to Browse or Drag Several Images Here</strong>
                                        <span>PNG, JPG, JPEG, WEBP accepted (Select multiple images at once)</span>
                                    </div>
                                </div>

                                <!-- Previews Grid -->
                                <div v-if="productImagePreviews.length > 0" class="previews-container">
                                    <div class="previews-header">
                                        <span><strong>{{ productImagePreviews.length }}</strong> images selected</span>
                                        <button type="button" @click="clearAllProductImages" class="btn-clear-images">
                                            Clear All
                                        </button>
                                    </div>

                                    <div class="images-preview-grid">
                                        <div v-for="(item, idx) in productImagePreviews" :key="idx"
                                            class="preview-card">
                                            <img :src="item.url" :alt="item.name" />
                                            <span v-if="idx === 0" class="cover-tag">Primary Cover</span>
                                            <div class="preview-info">
                                                <span class="preview-name">{{ item.name }}</span>
                                                <span class="preview-size">{{ item.size }}</span>
                                            </div>
                                            <button type="button" @click.stop="removeProductFile(idx)"
                                                class="btn-remove-thumb" title="Remove this image">
                                                &times;
                                            </button>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <!-- Footer Actions -->
                        <div class="modal-footer">
                            <button type="button" @click="closeAddProductModal" class="btn-cancel"
                                :disabled="savingProduct">
                                Cancel
                            </button>
                            <button type="submit" class="btn-submit" :disabled="savingProduct">
                                <i v-if="savingProduct" class="fa-solid fa-spinner fa-spin"></i>
                                <span>{{ savingProduct ? 'Creating Product...' : 'Create Product & Upload Gallery'
                                    }}</span>
                            </button>
                        </div>
                    </form>
                </div>
            </div>

            <!-- ============================================================= -->
            <!-- MODAL 2: ADD CATEGORY FORM (WITH SINGLE IMAGE UPLOAD)         -->
            <!-- ============================================================= -->
            <div v-if="isAddCategoryModalOpen" class="modal-overlay" @click.self="closeAddCategoryModal">
                <div class="modal-card modal-md">
                    <div class="modal-header">
                        <div>
                            <div class="modal-badge-row">
                                <span class="badge-staff">Category Manager</span>
                                <span class="badge-emerald"><i class="fa-solid fa-image"></i> Single Thumbnail</span>
                            </div>
                            <h2>Create Store Category</h2>
                        </div>
                        <button type="button" @click="closeAddCategoryModal" class="btn-close-modal"
                            aria-label="Close modal">&times;</button>
                    </div>

                    <form @submit.prevent="submitCreateCategory" class="modal-body-scrollable">
                        <!-- Error Alert -->
                        <div v-if="categoryFormError" class="modal-error-banner">
                            <i class="fa-solid fa-circle-exclamation"></i>
                            <span>{{ categoryFormError }}</span>
                        </div>

                        <div class="form-grid-1">
                            <!-- Category Name -->
                            <div class="form-group">
                                <label for="cat-name">Category Name *</label>
                                <input id="cat-name" v-model="categoryForm.name" type="text" required
                                    placeholder="e.g. Smart Wearables & Audio" class="form-control" />
                            </div>

                            <!-- Description -->
                            <div class="form-group">
                                <label for="cat-desc">Description</label>
                                <textarea id="cat-desc" v-model="categoryForm.description" rows="2"
                                    placeholder="Brief category summary for storefront catalog banner..."
                                    class="form-control"></textarea>
                            </div>

                            <!-- Active Status -->
                            <div class="form-group">
                                <label class="checkbox-label">
                                    <input type="checkbox" v-model="categoryForm.is_active" />
                                    <span>Active (Visible on Storefront Navigation & Filters)</span>
                                </label>
                            </div>

                            <!-- SINGLE IMAGE UPLOAD SECTION -->
                            <div class="form-group image-upload-section">
                                <div class="upload-section-header">
                                    <label>Category Thumbnail / Banner (Single Image)</label>
                                    <span class="upload-tip">Square or 4:3 image recommended</span>
                                </div>

                                <!-- Hidden File Input -->
                                <input type="file" ref="categoryImageFileInput" accept="image/*"
                                    @change="handleCategoryFileSelected" class="visually-hidden-file-input" />

                                <!-- Drop / Click Zone if no image selected -->
                                <div v-if="!categoryImagePreview" class="drop-zone-box single-box"
                                    @click="$refs.categoryImageFileInput.click()">
                                    <div class="drop-zone-icon">
                                        <i class="fa-solid fa-image"></i>
                                    </div>
                                    <div class="drop-zone-text">
                                        <strong>Click to Browse Category Image</strong>
                                        <span>PNG, JPG, WEBP accepted (Single image)</span>
                                    </div>
                                </div>

                                <!-- Live Single Preview Card -->
                                <div v-else class="single-preview-card">
                                    <div class="preview-thumb-box">
                                        <img :src="categoryImagePreview.url" :alt="categoryImagePreview.name" />
                                    </div>
                                    <div class="single-preview-details">
                                        <strong>{{ categoryImagePreview.name }}</strong>
                                        <span>{{ categoryImagePreview.size }}</span>
                                        <button type="button" @click="$refs.categoryImageFileInput.click()"
                                            class="btn-change-image">
                                            Change Image
                                        </button>
                                    </div>
                                    <button type="button" @click="clearCategoryImage" class="btn-remove-single"
                                        title="Remove Image">
                                        &times;
                                    </button>
                                </div>
                            </div>
                        </div>

                        <!-- Footer Actions -->
                        <div class="modal-footer">
                            <button type="button" @click="closeAddCategoryModal" class="btn-cancel"
                                :disabled="savingCategory">
                                Cancel
                            </button>
                            <button type="submit" class="btn-submit" :disabled="savingCategory">
                                <i v-if="savingCategory" class="fa-solid fa-spinner fa-spin"></i>
                                <span>{{ savingCategory ? 'Creating Category...' : 'Create Category' }}</span>
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
    middleware: 'admin',
    layout: 'admin'
})

const {
    getProducts,
    createProduct,
    updateProduct,
    deleteProduct,
    getCategories,
    createCategory,
    deleteCategory
} = useAdminApi()

const activeViewTab = ref('products') // 'products' | 'categories'

const products = ref([])
const categories = ref([])
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

// ==========================================
// Product Creation State & Handlers
// ==========================================
const isAddProductModalOpen = ref(false)
const savingProduct = ref(false)
const productFormError = ref('')
const productImagesFileInput = ref(null)

const productForm = reactive({
    name: '',
    category: '',
    current_price: '',
    original_price: '',
    supplier_cost: '',
    supplier_sku: '',
    stock_quantity: 25,
    description: '',
    is_active: true,
    is_featured: false
})

const selectedProductFiles = ref([]) // Array of File objects
const productImagePreviews = ref([]) // Array of { name, size, url, file }

function openAddProductModal() {
    productFormError.value = ''
    resetProductForm()
    isAddProductModalOpen.value = true
}

function closeAddProductModal() {
    isAddProductModalOpen.value = false
    clearAllProductImages()
}

function resetProductForm() {
    productForm.name = ''
    productForm.category = categories.value.length > 0 ? categories.value[0].id : ''
    productForm.current_price = ''
    productForm.original_price = ''
    productForm.supplier_cost = ''
    productForm.supplier_sku = ''
    productForm.stock_quantity = 25
    productForm.description = ''
    productForm.is_active = true
    productForm.is_featured = false
    clearAllProductImages()
}

function formatFileSize(bytes) {
    if (bytes < 1024) return `${bytes} B`
    if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`
    return `${(bytes / (1024 * 1024)).toFixed(1)} MB`
}

function handleProductFilesSelected(event) {
    const files = Array.from(event.target.files || [])
    if (!files.length) return

    for (const file of files) {
        // avoid identical name duplication in current selection
        if (!selectedProductFiles.value.some(f => f.name === file.name && f.size === file.size)) {
            selectedProductFiles.value.push(file)
            productImagePreviews.value.push({
                name: file.name,
                size: formatFileSize(file.size),
                url: URL.createObjectURL(file),
                file
            })
        }
    }

    // Reset input value so re-selecting same file works
    if (productImagesFileInput.value) {
        productImagesFileInput.value.value = ''
    }
}

function removeProductFile(index) {
    if (index >= 0 && index < selectedProductFiles.value.length) {
        const item = productImagePreviews.value[index]
        if (item?.url) {
            URL.revokeObjectURL(item.url)
        }
        selectedProductFiles.value.splice(index, 1)
        productImagePreviews.value.splice(index, 1)
    }
}

function clearAllProductImages() {
    productImagePreviews.value.forEach(item => {
        if (item.url) URL.revokeObjectURL(item.url)
    })
    selectedProductFiles.value = []
    productImagePreviews.value = []
}

async function submitCreateProduct() {
    productFormError.value = ''

    if (!productForm.name.trim()) {
        productFormError.value = 'Please enter a product name.'
        return
    }
    if (!productForm.current_price || Number(productForm.current_price) <= 0) {
        productFormError.value = 'Please provide a valid selling price greater than 0.'
        return
    }
    if (!productForm.category) {
        productFormError.value = 'Please select a product category.'
        return
    }

    savingProduct.value = true

    try {
        const formData = new FormData()
        formData.append('name', productForm.name.trim())
        formData.append('category', productForm.category)
        formData.append('current_price', productForm.current_price)
        formData.append('stock_quantity', productForm.stock_quantity ?? 0)
        formData.append('is_active', productForm.is_active ? 'true' : 'false')
        formData.append('is_featured', productForm.is_featured ? 'true' : 'false')

        if (productForm.original_price) {
            formData.append('original_price', productForm.original_price)
        }
        if (productForm.supplier_cost) {
            formData.append('supplier_cost', productForm.supplier_cost)
        }
        if (productForm.supplier_sku) {
            formData.append('supplier_sku', productForm.supplier_sku.trim())
        }
        if (productForm.description) {
            formData.append('description', productForm.description.trim())
        }

        // Attach several images
        selectedProductFiles.value.forEach((file, idx) => {
            formData.append('images', file)
            // also set primary cover image
            if (idx === 0) {
                formData.append('image', file)
            }
        })

        const newProd = await createProduct(formData)

        // Add to local state
        products.value.unshift({
            ...newProd,
            _modified: false,
            _saving: false,
            _saved: false
        })

        closeAddProductModal()
        activeViewTab.value = 'products'
    } catch (err) {
        productFormError.value = err.message || 'Failed to create product.'
    } finally {
        savingProduct.value = false
    }
}

// ==========================================
// Category Creation State & Handlers
// ==========================================
const isAddCategoryModalOpen = ref(false)
const savingCategory = ref(false)
const categoryFormError = ref('')
const categoryImageFileInput = ref(null)

const categoryForm = reactive({
    name: '',
    description: '',
    is_active: true
})

const selectedCategoryFile = ref(null) // File object
const categoryImagePreview = ref(null) // { name, size, url, file }

function openAddCategoryModal() {
    categoryFormError.value = ''
    resetCategoryForm()
    isAddCategoryModalOpen.value = true
}

function closeAddCategoryModal() {
    isAddCategoryModalOpen.value = false
    clearCategoryImage()
}

function resetCategoryForm() {
    categoryForm.name = ''
    categoryForm.description = ''
    categoryForm.is_active = true
    clearCategoryImage()
}

function handleCategoryFileSelected(event) {
    const file = event.target.files?.[0]
    if (!file) return

    clearCategoryImage()
    selectedCategoryFile.value = file
    categoryImagePreview.value = {
        name: file.name,
        size: formatFileSize(file.size),
        url: URL.createObjectURL(file),
        file
    }

    if (categoryImageFileInput.value) {
        categoryImageFileInput.value.value = ''
    }
}

function clearCategoryImage() {
    if (categoryImagePreview.value?.url) {
        URL.revokeObjectURL(categoryImagePreview.value.url)
    }
    selectedCategoryFile.value = null
    categoryImagePreview.value = null
}

async function submitCreateCategory() {
    categoryFormError.value = ''

    if (!categoryForm.name.trim()) {
        categoryFormError.value = 'Please enter a category name.'
        return
    }

    savingCategory.value = true

    try {
        const formData = new FormData()
        formData.append('name', categoryForm.name.trim())
        formData.append('is_active', categoryForm.is_active ? 'true' : 'false')

        if (categoryForm.description) {
            formData.append('description', categoryForm.description.trim())
        }

        // Single image upload
        if (selectedCategoryFile.value) {
            formData.append('image', selectedCategoryFile.value)
        }

        const newCat = await createCategory(formData)
        categories.value.unshift(newCat)

        closeAddCategoryModal()
        // If product modal was open or needed category, set it
        if (productForm.category === '' && newCat.id) {
            productForm.category = newCat.id
        }
    } catch (err) {
        categoryFormError.value = err.message || 'Failed to create category.'
    } finally {
        savingCategory.value = false
    }
}

async function confirmDeleteCategory(cat) {
    const confirmed = window.confirm(`Are you sure you want to delete category "${cat.name}"? Products in this category will remain unassigned.`)
    if (!confirmed) return

    try {
        await deleteCategory(cat.slug)
        categories.value = categories.value.filter(c => c.id !== cat.id)
    } catch (err) {
        alert(err.message || 'Failed to delete category.')
    }
}

async function confirmDeleteProduct(p) {
    const confirmed = window.confirm(`Are you sure you want to delete "${p.name}"? This action cannot be undone.`)
    if (!confirmed) return

    try {
        await deleteProduct(p.id)
        products.value = products.value.filter(item => item.id !== p.id)
    } catch (err) {
        alert(err.message || 'Failed to delete product.')
    }
}

// ==========================================
// Roster Data Fetching & Table Handlers
// ==========================================
async function fetchInitialData() {
    loading.value = true
    error.value = ''
    try {
        const [prodsData, catsData] = await Promise.all([
            getProducts(),
            getCategories()
        ])

        products.value = (prodsData || []).map(p => ({
            ...p,
            _modified: false,
            _saving: false,
            _saved: false
        }))

        categories.value = Array.isArray(catsData) ? catsData : (catsData?.results || [])
    } catch (err) {
        error.value = err.message || 'Failed to retrieve catalog data.'
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

    if (searchQuery.value.trim()) {
        const q = searchQuery.value.toLowerCase()
        result = result.filter(p =>
            p.name.toLowerCase().includes(q) ||
            p.category_name.toLowerCase().includes(q) ||
            p.slug.toLowerCase().includes(q)
        )
    }

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
    fetchInitialData()
})
</script>

<style scoped>
.admin-page {
    padding: 2.5rem 1.5rem 5rem;
    max-width: 1280px;
    margin: 0 auto;
}

.badge-tag {
    display: inline-block;
    font-size: 0.72rem;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    background: #0f172a;
    color: #fff;
    padding: 0.2rem 0.55rem;
    border-radius: var(--radius-sm);
    margin-bottom: 0.5rem;
}

.admin-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    flex-wrap: wrap;
    gap: 1.5rem;
    margin-bottom: 1.75rem;
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

/* Header Action Buttons */
.header-action-group {
    display: flex;
    align-items: center;
    gap: 0.65rem;
    flex-wrap: wrap;
}

.btn-action {
    display: inline-flex;
    align-items: center;
    gap: 0.45rem;
    padding: 0.6rem 1.15rem;
    border-radius: var(--radius-md);
    font-size: 0.88rem;
    font-weight: 700;
    cursor: pointer;
    transition: all 0.15s ease;
    border: none;
    box-shadow: var(--shadow-sm);
}

.btn-add-prod {
    background: linear-gradient(135deg, #2563eb, #1d4ed8);
    color: #ffffff;
}

.btn-add-prod:hover {
    background: linear-gradient(135deg, #1d4ed8, #1e40af);
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(37, 99, 235, 0.3);
}

.btn-add-cat {
    background: #0f172a;
    color: #ffffff;
    border: 1px solid #334155;
}

.btn-add-cat:hover {
    background: #1e293b;
    border-color: #475569;
    transform: translateY(-1px);
}

.btn-refresh {
    display: inline-flex;
    align-items: center;
    gap: 0.45rem;
    background: #ffffff;
    border: 1px solid var(--border-color);
    padding: 0.6rem 1rem;
    border-radius: var(--radius-md);
    font-size: 0.88rem;
    font-weight: 600;
    color: var(--text-main);
    box-shadow: var(--shadow-sm);
    cursor: pointer;
    transition: all 0.15s;
}

.btn-refresh:hover:not(:disabled) {
    background: #f8fafc;
    border-color: #cbd5e1;
}

/* View Tabs Strip (Products vs Categories) */
.view-tabs-strip {
    display: flex;
    gap: 0.5rem;
    background: #e2e8f0;
    padding: 0.3rem;
    border-radius: var(--radius-md);
    margin-bottom: 2rem;
    width: fit-content;
}

.view-tab-btn {
    display: inline-flex;
    align-items: center;
    gap: 0.55rem;
    padding: 0.5rem 1rem;
    border-radius: var(--radius-sm);
    font-size: 0.88rem;
    font-weight: 600;
    color: var(--text-muted);
    background: transparent;
    border: none;
    cursor: pointer;
    transition: all 0.15s;
}

.view-tab-btn.active {
    background: #ffffff;
    color: var(--text-main);
    font-weight: 700;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08);
}

.tab-count-pill {
    background: rgba(15, 23, 42, 0.08);
    color: var(--text-body);
    font-size: 0.72rem;
    font-weight: 800;
    padding: 0.1rem 0.45rem;
    border-radius: 999px;
}

.view-tab-btn.active .tab-count-pill {
    background: var(--primary-light);
    color: var(--primary);
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
    position: relative;
    flex: 1;
    min-width: 280px;
    max-width: 480px;
}

.search-input-wrap svg {
    position: absolute;
    left: 0.95rem;
    top: 50%;
    transform: translateY(-50%);
    color: var(--text-muted);
}

.search-input {
    width: 100%;
    padding: 0.65rem 1rem 0.65rem 2.5rem;
    background: #ffffff;
    border: 1px solid var(--border-color);
    border-radius: var(--radius-md);
    font-size: 0.9rem;
    outline: none;
    transition: all 0.15s;
}

.search-input:focus {
    border-color: var(--primary);
    box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.12);
}

.status-filters {
    display: flex;
    gap: 0.4rem;
    flex-wrap: wrap;
}

.filter-pill {
    background: #ffffff;
    border: 1px solid var(--border-color);
    padding: 0.45rem 0.85rem;
    border-radius: var(--radius-full);
    font-size: 0.82rem;
    font-weight: 600;
    color: var(--text-body);
    cursor: pointer;
    transition: all 0.15s;
}

.filter-pill:hover {
    border-color: #94a3b8;
}

.filter-pill.active {
    background: #0f172a;
    color: #ffffff;
    border-color: #0f172a;
}

/* Table Card */
.table-card {
    background: #ffffff;
    border: 1px solid var(--border-color);
    border-radius: var(--radius-lg);
    box-shadow: var(--shadow-sm);
    overflow: hidden;
}

.table-meta-header {
    padding: 0.85rem 1.5rem;
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
    text-align: left;
    font-size: 0.9rem;
}

.inventory-table th {
    padding: 0.85rem 1.25rem;
    background: #f8fafc;
    font-weight: 700;
    color: var(--text-muted);
    font-size: 0.78rem;
    text-transform: uppercase;
    letter-spacing: 0.04em;
    border-bottom: 1px solid var(--border-color);
}

.inventory-table td {
    padding: 1rem 1.25rem;
    border-bottom: 1px solid var(--border-color);
    vertical-align: middle;
}

.inventory-table tr:hover {
    background: #fbfcfe;
}

.inventory-table tr.row-modified {
    background: #fffbeb;
}

/* Product Info Cell */
.product-cell {
    display: flex;
    align-items: center;
    gap: 1rem;
    min-width: 280px;
}

.prod-thumb {
    width: 48px;
    height: 48px;
    min-width: 48px;
    border-radius: var(--radius-md);
    background: #f1f5f9;
    border: 1px solid var(--border-color);
    overflow: hidden;
    display: flex;
    align-items: center;
    justify-content: center;
}

.prod-thumb img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.thumb-fallback {
    font-weight: 800;
    color: var(--text-muted);
    font-size: 1.1rem;
}

.prod-details {
    display: flex;
    flex-direction: column;
}

.prod-name {
    font-weight: 700;
    color: var(--text-main);
    text-decoration: none;
    line-height: 1.3;
    font-size: 0.92rem;
}

.prod-name:hover {
    color: var(--primary);
}

.external-icon {
    font-size: 0.8rem;
    opacity: 0.6;
}

.meta-row {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    margin-top: 0.2rem;
}

.prod-slug {
    font-size: 0.75rem;
    color: var(--text-muted);
    font-family: monospace;
}

.gallery-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.25rem;
    font-size: 0.7rem;
    font-weight: 700;
    background: #eff6ff;
    color: #2563eb;
    padding: 0.1rem 0.35rem;
    border-radius: var(--radius-xs);
    border: 1px solid #bfdbfe;
}

/* Category Badge */
.category-badge {
    display: inline-block;
    background: #f1f5f9;
    color: var(--text-body);
    font-size: 0.75rem;
    font-weight: 600;
    padding: 0.25rem 0.6rem;
    border-radius: var(--radius-sm);
    border: 1px solid var(--border-color);
}

/* Price Input */
.price-input-wrap {
    display: inline-flex;
    align-items: center;
    background: #ffffff;
    border: 1px solid var(--border-color);
    border-radius: var(--radius-sm);
    padding: 0 0.4rem;
}

.currency-prefix {
    color: var(--text-muted);
    font-weight: 600;
    font-size: 0.85rem;
}

.inline-input {
    border: none;
    outline: none;
    padding: 0.4rem 0.3rem;
    font-size: 0.9rem;
    font-weight: 600;
    color: var(--text-main);
}

.price-input {
    width: 75px;
}

/* Stock Stepper */
.stock-control-wrap {
    display: inline-flex;
    align-items: center;
    gap: 0.35rem;
}

.btn-step {
    width: 26px;
    height: 26px;
    border-radius: var(--radius-xs);
    background: #f1f5f9;
    border: 1px solid var(--border-color);
    color: var(--text-main);
    font-weight: 700;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    transition: all 0.15s;
}

.btn-step:hover:not(:disabled) {
    background: #e2e8f0;
}

.stock-input {
    width: 50px;
    text-align: center;
    border: 1px solid var(--border-color);
    border-radius: var(--radius-xs);
}

.stock-pill {
    font-size: 0.7rem;
    font-weight: 700;
    padding: 0.15rem 0.45rem;
    border-radius: 999px;
    text-transform: uppercase;
}

.pill-ok {
    background: #ecfdf5;
    color: #16a34a;
}

.pill-low {
    background: #fffbeb;
    color: #b45309;
}

.pill-out {
    background: #fef2f2;
    color: #dc2626;
}

/* Switch Toggle */
.switch-toggle {
    position: relative;
    display: inline-block;
    width: 36px;
    height: 20px;
}

.switch-toggle input {
    opacity: 0;
    width: 0;
    height: 0;
}

.slider {
    position: absolute;
    cursor: pointer;
    inset: 0;
    background-color: #cbd5e1;
    border-radius: 20px;
    transition: 0.2s;
}

.slider:before {
    position: absolute;
    content: "";
    height: 14px;
    width: 14px;
    left: 3px;
    bottom: 3px;
    background-color: white;
    border-radius: 50%;
    transition: 0.2s;
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
    background: transparent;
    border: none;
    cursor: pointer;
    transition: color 0.15s;
}

.btn-star.starred {
    color: #f59e0b;
}

/* Action Buttons in Table */
.action-cell {
    display: flex;
    align-items: center;
    gap: 0.45rem;
}

.btn-save {
    background: #0f172a;
    color: #fff;
    font-size: 0.8rem;
    font-weight: 600;
    padding: 0.35rem 0.85rem;
    border-radius: var(--radius-sm);
    border: none;
    cursor: pointer;
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

.btn-delete {
    background: transparent;
    border: 1px solid var(--border-color);
    color: var(--text-muted);
    width: 30px;
    height: 30px;
    border-radius: var(--radius-sm);
    display: inline-flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    transition: all 0.15s;
}

.btn-delete:hover {
    color: #dc2626;
    border-color: #fca5a5;
    background: #fef2f2;
}

/* Empty Card */
.empty-roster-card {
    text-align: center;
    padding: 4.5rem 2rem;
    background: #ffffff;
    border: 1px solid var(--border-color);
    border-radius: var(--radius-lg);
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 0.75rem;
}

.empty-icon-circle {
    width: 64px;
    height: 64px;
    border-radius: 50%;
    background: #f1f5f9;
    color: var(--text-muted);
    font-size: 1.75rem;
    display: flex;
    align-items: center;
    justify-content: center;
    margin-bottom: 0.5rem;
}

/* ============================================================= */
/* CATEGORIES TAB STYLES                                         */
/* ============================================================= */
.categories-header-card {
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 1rem;
    background: #ffffff;
    border: 1px solid var(--border-color);
    border-radius: var(--radius-lg);
    padding: 1.5rem 1.75rem;
    margin-bottom: 1.5rem;
}

.categories-header-card h2 {
    font-size: 1.35rem;
    font-weight: 800;
}

.categories-header-card p {
    color: var(--text-muted);
    font-size: 0.88rem;
    margin-top: 0.2rem;
}

.categories-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
    gap: 1.5rem;
}

.category-admin-card {
    background: #ffffff;
    border: 1px solid var(--border-color);
    border-radius: var(--radius-lg);
    box-shadow: var(--shadow-sm);
    overflow: hidden;
    display: flex;
    flex-direction: column;
    transition: transform 0.15s ease, box-shadow 0.15s ease;
}

.category-admin-card:hover {
    transform: translateY(-2px);
    box-shadow: var(--shadow-md);
}

.cat-card-img {
    width: 100%;
    height: 140px;
    background: #f1f5f9;
    position: relative;
    overflow: hidden;
    display: flex;
    align-items: center;
    justify-content: center;
}

.cat-card-img img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.cat-img-fallback {
    font-size: 2.5rem;
    color: #cbd5e1;
}

.cat-status-pill {
    position: absolute;
    top: 0.75rem;
    right: 0.75rem;
    font-size: 0.7rem;
    font-weight: 800;
    padding: 0.15rem 0.5rem;
    border-radius: 999px;
    text-transform: uppercase;
}

.cat-status-pill.active {
    background: #16a34a;
    color: #ffffff;
}

.cat-status-pill.inactive {
    background: #64748b;
    color: #ffffff;
}

.cat-card-body {
    padding: 1.25rem;
    display: flex;
    flex-direction: column;
    flex: 1;
}

.cat-card-top {
    display: flex;
    justify-content: space-between;
    align-items: baseline;
    gap: 0.5rem;
    margin-bottom: 0.35rem;
}

.cat-card-top h3 {
    font-size: 1.1rem;
    font-weight: 800;
    color: var(--text-main);
}

.cat-count {
    font-size: 0.78rem;
    font-weight: 700;
    color: var(--primary);
    background: #eff6ff;
    padding: 0.15rem 0.45rem;
    border-radius: var(--radius-xs);
}

.cat-slug-pill {
    font-size: 0.75rem;
    color: var(--text-muted);
    font-family: monospace;
    margin-bottom: 0.65rem;
}

.cat-desc {
    font-size: 0.85rem;
    color: var(--text-muted);
    line-height: 1.45;
    margin-bottom: 1.25rem;
    flex: 1;
}

.cat-card-actions {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding-top: 0.85rem;
    border-top: 1px solid var(--border-color);
}

.btn-view-cat {
    font-size: 0.82rem;
    font-weight: 700;
    color: var(--primary);
    text-decoration: none;
}

.btn-view-cat:hover {
    text-decoration: underline;
}

.btn-delete-cat {
    background: transparent;
    border: 1px solid var(--border-color);
    color: var(--text-muted);
    width: 28px;
    height: 28px;
    border-radius: var(--radius-sm);
    display: inline-flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    transition: all 0.15s;
}

.btn-delete-cat:hover {
    color: #dc2626;
    border-color: #fca5a5;
    background: #fef2f2;
}

/* ============================================================= */
/* MODAL STYLES (PRODUCT & CATEGORY FORMS)                       */
/* ============================================================= */
.modal-overlay {
    position: fixed;
    inset: 0;
    background: rgba(15, 23, 42, 0.65);
    backdrop-filter: blur(4px);
    z-index: 2000;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 1.5rem;
}

.modal-card {
    background: #ffffff;
    border-radius: var(--radius-xl);
    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.25);
    width: 100%;
    max-height: 90vh;
    display: flex;
    flex-direction: column;
    overflow: hidden;
    animation: modalSlide 0.2s cubic-bezier(0.16, 1, 0.3, 1);
}

@keyframes modalSlide {
    from {
        opacity: 0;
        transform: scale(0.96) translateY(10px);
    }

    to {
        opacity: 1;
        transform: scale(1) translateY(0);
    }
}

.modal-lg {
    max-width: 820px;
}

.modal-md {
    max-width: 540px;
}

.modal-header {
    padding: 1.5rem 1.75rem;
    background: #f8fafc;
    border-bottom: 1px solid var(--border-color);
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
}

.modal-header h2 {
    font-size: 1.35rem;
    font-weight: 800;
    color: var(--text-main);
    margin-top: 0.25rem;
}

.modal-badge-row {
    display: flex;
    align-items: center;
    gap: 0.45rem;
}

.badge-staff {
    background: #0f172a;
    color: #ffffff;
    font-size: 0.68rem;
    font-weight: 800;
    text-transform: uppercase;
    padding: 0.15rem 0.45rem;
    border-radius: var(--radius-xs);
}

.badge-accent {
    background: #eff6ff;
    color: #2563eb;
    border: 1px solid #bfdbfe;
    font-size: 0.68rem;
    font-weight: 800;
    padding: 0.15rem 0.45rem;
    border-radius: var(--radius-xs);
}

.badge-emerald {
    background: #ecfdf5;
    color: #059669;
    border: 1px solid #a7f3d0;
    font-size: 0.68rem;
    font-weight: 800;
    padding: 0.15rem 0.45rem;
    border-radius: var(--radius-xs);
}

.btn-close-modal {
    background: transparent;
    border: none;
    font-size: 1.75rem;
    color: var(--text-muted);
    cursor: pointer;
    line-height: 1;
    padding: 0 0.25rem;
}

.btn-close-modal:hover {
    color: var(--text-main);
}

.modal-body-scrollable {
    padding: 1.75rem;
    overflow-y: auto;
    flex: 1;
}

.modal-error-banner {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    background: #fef2f2;
    border: 1px solid #fecaca;
    color: #dc2626;
    padding: 0.75rem 1rem;
    border-radius: var(--radius-md);
    margin-bottom: 1.25rem;
    font-size: 0.88rem;
    font-weight: 600;
}

/* Form Grids */
.form-grid-2 {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 1.25rem;
}

.form-grid-1 {
    display: flex;
    flex-direction: column;
    gap: 1.25rem;
}

.span-2 {
    grid-column: span 2;
}

.form-group {
    display: flex;
    flex-direction: column;
    gap: 0.4rem;
}

.form-group label {
    font-size: 0.85rem;
    font-weight: 700;
    color: var(--text-main);
}

.label-with-action {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.link-btn-subtle {
    background: transparent;
    border: none;
    color: var(--primary);
    font-size: 0.78rem;
    font-weight: 700;
    cursor: pointer;
    padding: 0;
}

.link-btn-subtle:hover {
    text-decoration: underline;
}

.form-control {
    width: 100%;
    padding: 0.65rem 0.85rem;
    background: #ffffff;
    border: 1px solid var(--border-color);
    border-radius: var(--radius-md);
    font-size: 0.9rem;
    color: var(--text-main);
    outline: none;
    transition: all 0.15s;
    font-family: inherit;
}

.form-control:focus {
    border-color: var(--primary);
    box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.12);
}

.input-dollar-wrap {
    display: flex;
    align-items: center;
    position: relative;
}

.currency-symbol {
    position: absolute;
    left: 0.85rem;
    color: var(--text-muted);
    font-weight: 700;
    font-size: 0.9rem;
    pointer-events: none;
}

.input-dollar-wrap .form-control {
    padding-left: 1.85rem;
}

.toggles-row {
    display: flex;
    flex-wrap: wrap;
    gap: 1.5rem;
    padding: 0.5rem 0;
}

.checkbox-label {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    font-size: 0.88rem;
    font-weight: 600;
    color: var(--text-body);
    cursor: pointer;
}

.checkbox-label input {
    accent-color: var(--primary);
    width: 17px;
    height: 17px;
}

/* ============================================================= */
/* IMAGE UPLOAD & PREVIEW STYLES (MULTI & SINGLE)               */
/* ============================================================= */
.image-upload-section {
    background: #f8fafc;
    border: 1px dashed #cbd5e1;
    border-radius: var(--radius-lg);
    padding: 1.25rem;
}

.upload-section-header {
    display: flex;
    justify-content: space-between;
    align-items: baseline;
    flex-wrap: wrap;
    gap: 0.5rem;
    margin-bottom: 0.75rem;
}

.upload-tip {
    font-size: 0.78rem;
    color: var(--text-muted);
    font-weight: 500;
}

.visually-hidden-file-input {
    display: none;
}

.drop-zone-box {
    background: #ffffff;
    border: 2px dashed #94a3b8;
    border-radius: var(--radius-md);
    padding: 1.75rem 1.5rem;
    text-align: center;
    cursor: pointer;
    transition: all 0.15s ease;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 0.5rem;
}

.drop-zone-box:hover {
    border-color: var(--primary);
    background: #eff6ff;
}

.drop-zone-icon {
    font-size: 2.25rem;
    color: #2563eb;
}

.drop-zone-text {
    display: flex;
    flex-direction: column;
    gap: 0.2rem;
}

.drop-zone-text strong {
    font-size: 0.95rem;
    color: var(--text-main);
}

.drop-zone-text span {
    font-size: 0.78rem;
    color: var(--text-muted);
}

/* Multi-Images Preview Grid */
.previews-container {
    margin-top: 1.25rem;
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
}

.previews-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 0.82rem;
    color: var(--text-muted);
}

.btn-clear-images {
    background: transparent;
    border: none;
    color: #dc2626;
    font-size: 0.78rem;
    font-weight: 700;
    cursor: pointer;
}

.btn-clear-images:hover {
    text-decoration: underline;
}

.images-preview-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(130px, 1fr));
    gap: 0.85rem;
}

.preview-card {
    position: relative;
    background: #ffffff;
    border: 1px solid var(--border-color);
    border-radius: var(--radius-md);
    overflow: hidden;
    display: flex;
    flex-direction: column;
    box-shadow: var(--shadow-xs);
}

.preview-card img {
    width: 100%;
    height: 100px;
    object-fit: cover;
    background: #f1f5f9;
}

.cover-tag {
    position: absolute;
    top: 0.35rem;
    left: 0.35rem;
    background: #2563eb;
    color: #ffffff;
    font-size: 0.65rem;
    font-weight: 800;
    text-transform: uppercase;
    padding: 0.15rem 0.4rem;
    border-radius: var(--radius-xs);
    box-shadow: 0 1px 4px rgba(0, 0, 0, 0.25);
}

.preview-info {
    padding: 0.4rem 0.5rem;
    display: flex;
    flex-direction: column;
    overflow: hidden;
}

.preview-name {
    font-size: 0.72rem;
    font-weight: 700;
    color: var(--text-main);
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

.preview-size {
    font-size: 0.68rem;
    color: var(--text-muted);
}

.btn-remove-thumb {
    position: absolute;
    top: 0.35rem;
    right: 0.35rem;
    background: rgba(15, 23, 42, 0.75);
    color: #ffffff;
    border: none;
    width: 22px;
    height: 22px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.95rem;
    cursor: pointer;
    transition: background 0.15s;
}

.btn-remove-thumb:hover {
    background: #dc2626;
}

/* Single Image Preview Box */
.single-preview-card {
    display: flex;
    align-items: center;
    gap: 1rem;
    background: #ffffff;
    border: 1px solid var(--border-color);
    border-radius: var(--radius-md);
    padding: 0.75rem;
    position: relative;
}

.preview-thumb-box {
    width: 72px;
    height: 72px;
    min-width: 72px;
    border-radius: var(--radius-sm);
    overflow: hidden;
    background: #f1f5f9;
}

.preview-thumb-box img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.single-preview-details {
    display: flex;
    flex-direction: column;
    gap: 0.2rem;
    flex: 1;
    overflow: hidden;
}

.single-preview-details strong {
    font-size: 0.88rem;
    color: var(--text-main);
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

.single-preview-details span {
    font-size: 0.78rem;
    color: var(--text-muted);
}

.btn-change-image {
    background: transparent;
    border: none;
    color: var(--primary);
    font-size: 0.78rem;
    font-weight: 700;
    cursor: pointer;
    text-align: left;
    padding: 0;
    margin-top: 0.2rem;
}

.btn-change-image:hover {
    text-decoration: underline;
}

.btn-remove-single {
    background: #fee2e2;
    border: 1px solid #fecaca;
    color: #dc2626;
    width: 28px;
    height: 28px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.1rem;
    cursor: pointer;
    transition: all 0.15s;
}

.btn-remove-single:hover {
    background: #dc2626;
    color: #ffffff;
}

/* Modal Footer Actions */
.modal-footer {
    padding: 1.25rem 1.75rem;
    background: #f8fafc;
    border-top: 1px solid var(--border-color);
    display: flex;
    justify-content: flex-end;
    gap: 0.85rem;
}

.btn-cancel {
    padding: 0.6rem 1.25rem;
    background: #ffffff;
    border: 1px solid var(--border-color);
    border-radius: var(--radius-md);
    font-size: 0.88rem;
    font-weight: 600;
    color: var(--text-body);
    cursor: pointer;
    transition: all 0.15s;
}

.btn-cancel:hover:not(:disabled) {
    background: #f1f5f9;
}

.btn-submit {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.6rem 1.4rem;
    background: linear-gradient(135deg, #2563eb, #1d4ed8);
    color: #ffffff;
    border: none;
    border-radius: var(--radius-md);
    font-size: 0.88rem;
    font-weight: 700;
    cursor: pointer;
    box-shadow: 0 4px 12px rgba(37, 99, 235, 0.25);
    transition: all 0.15s;
}

.btn-submit:hover:not(:disabled) {
    background: linear-gradient(135deg, #1d4ed8, #1e40af);
    transform: translateY(-1px);
    box-shadow: 0 6px 16px rgba(37, 99, 235, 0.35);
}

.btn-submit:disabled {
    opacity: 0.6;
    cursor: not-allowed;
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

@media (max-width: 768px) {
    .form-grid-2 {
        grid-template-columns: 1fr;
    }

    .span-2 {
        grid-column: span 1;
    }

    .admin-header h1 {
        font-size: 1.6rem;
    }
}
</style>
