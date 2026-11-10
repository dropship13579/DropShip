<!-- frontend/app/pages/products/[slug].vue -->
<template>
  <div class="product-detail-page">
    <div class="container">
      <div v-if="loading" class="loading-wrap">
        <LoadingSpinner text="Loading product details..." />
      </div>

      <div v-else-if="error" class="error-wrap">
        <h2>Product Not Found</h2>
        <p>{{ error }}</p>
        <NuxtLink to="/shop" class="btn-back-nav">
          <span class="back-arrow-wrap">
            <i class="fa-solid fa-arrow-left"></i>
          </span>
          <span>Return to Shop</span>
        </NuxtLink>
      </div>

      <div v-else-if="product">
        <!-- Top Bar Navigation with Back Button & Breadcrumbs -->
        <div class="product-top-bar">
          <NuxtLink to="/shop" class="btn-back-nav" aria-label="Back to Shop Catalog">
            <span class="back-arrow-wrap">
              <i class="fa-solid fa-arrow-left"></i>
            </span>
            <span>Back to Shop</span>
          </NuxtLink>

          <nav class="breadcrumb-trail" aria-label="Breadcrumb">
            <NuxtLink to="/">Home</NuxtLink>
            <span class="bc-sep">/</span>
            <NuxtLink to="/shop">Shop</NuxtLink>
            <template v-if="product.category">
              <span class="bc-sep">/</span>
              <NuxtLink :to="`/shop?category=${product.category.slug}`">{{ product.category.name }}</NuxtLink>
            </template>
            <span class="bc-sep">/</span>
            <span class="bc-curr">{{ product.name }}</span>
          </nav>
        </div>

        <!-- Main Product Layout -->
        <div class="product-layout">
          <div class="product-gallery">
            <div class="main-image-wrap">
              <img v-if="currentSelectedImage || product.image" :src="currentSelectedImage || product.image" :alt="product.name" class="main-img">
              <div v-else class="image-fallback">
                <span>{{ product.category?.name || 'KyroKart' }}</span>
              </div>
            </div>

            <!-- Multi-Image Gallery Thumbnail Strip -->
            <div v-if="galleryImages.length > 1" class="gallery-thumbs">
              <button
                v-for="(imgUrl, idx) in galleryImages"
                :key="idx"
                type="button"
                class="thumb-box"
                :class="{ active: (currentSelectedImage || product.image) === imgUrl }"
                @click="currentSelectedImage = imgUrl"
                :aria-label="`View image ${idx + 1}`"
              >
                <img :src="imgUrl" :alt="`${product.name} thumbnail ${idx + 1}`" />
              </button>
            </div>
          </div>

          <div class="product-meta">
            <span class="category-name">{{ product.category?.name }}</span>
            <h1 class="title">{{ product.name }}</h1>

            <div class="rating-row" @click="scrollToReviews">
              <span class="stars">&#9733; {{ Number(product.rating).toFixed(1) }}</span>
              <span class="reviews">({{ product.review_count }} customer reviews)</span>
            </div>

            <div class="price-box">
              <PriceDisplay :current-price="product.current_price" :original-price="product.original_price"
                :discount-percentage="product.discount_percentage" />
            </div>

            <div class="stock-status"
              :class="{ 'in-stock': product.is_in_stock, 'out-of-stock': !product.is_in_stock }">
              <span class="stock-dot"></span>
              <span>{{ product.is_in_stock ? `In Stock (${product.stock_quantity} available)` : 'Out of Stock' }}</span>
            </div>

            <p class="description">{{ product.description }}</p>

            <!-- Add to Cart Controls -->
            <div class="purchase-controls">
              <div v-if="addSuccessMsg" class="success-banner">
                {{ addSuccessMsg }}
              </div>
              <div class="purchase-row">
                <QuantitySelector v-model="quantity" :min="1" :max="product.stock_quantity || 1" />
                <button @click="handleAddToCart" class="btn-add-cart" :disabled="!product.is_in_stock">
                  {{ product.is_in_stock ? 'Add to Cart' : 'Currently Unavailable' }}
                </button>
                <button type="button" class="btn-wishlist-toggle" :class="{ active: isWishlisted(product.id) }"
                  @click="toggleWishlist(product.id)"
                  :title="isWishlisted(product.id) ? 'Remove from Wishlist' : 'Add to Wishlist'">
                  <svg width="20" height="20" viewBox="0 0 24 24" :fill="isWishlisted(product.id) ? '#ef4444' : 'none'"
                    :stroke="isWishlisted(product.id) ? '#ef4444' : 'currentColor'" stroke-width="2">
                    <path
                      d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z">
                    </path>
                  </svg>
                  <span>{{ isWishlisted(product.id) ? 'Saved' : 'Wishlist' }}</span>
                </button>
              </div>

              <!-- Live Urgency Countdown & Estimated Delivery Calculator -->
              <DeliveryEstimator />

              <!-- Quick Trust Guarantees -->
              <div class="product-trust-strip">
                <div class="trust-item">
                  <span class="trust-icon"><i class="fa-solid fa-truck-fast"></i></span>
                  <span>Fast Tracked Delivery (4–9 Days)</span>
                </div>
                <div class="trust-item">
                  <span class="trust-icon"><i class="fa-solid fa-shield-halved"></i></span>
                  <span>30-Day Money-Back Guarantee</span>
                </div>
                <div class="trust-item">
                  <span class="trust-icon"><i class="fa-solid fa-lock"></i></span>
                  <span>SSL Encrypted Checkout</span>
                </div>
              </div>

              <!-- Customer Question Prompt -->
              <div class="product-support-action">
                <span>Have a question about this item?</span>
                <button type="button" @click="isSupportModalOpen = true" class="btn-product-ask">
                  <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path>
                  </svg>
                  <span>Ask Customer Support</span>
                </button>
              </div>
            </div>

            <!-- Specifications Table -->
            <div v-if="hasSpecifications" class="specs-section">
              <h3>Specifications</h3>
              <table class="specs-table">
                <tbody>
                  <tr v-for="(val, key) in product.specifications" :key="key">
                    <td class="spec-label">{{ key }}</td>
                    <td class="spec-value">{{ val }}</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>

        <!-- REVIEWS & RATINGS SECTION -->
        <section id="reviews-section" class="reviews-section">
          <div class="section-header-row">
            <div>
              <h2>Customer Reviews & Ratings</h2>
              <p class="section-subtext">Real experiences shared by verified store shoppers.</p>
            </div>
            <button v-if="isAuthenticated && !showReviewForm" @click="showReviewForm = true" class="btn-write-review">
              Write a Review
            </button>
          </div>

          <!-- Rating Breakdown Card -->
          <div class="ratings-overview-card">
            <div class="score-summary">
              <div class="big-score">{{ Number(reviewData.average_rating || product.rating).toFixed(1) }}</div>
              <div class="star-display">
                <span v-for="s in 5" :key="s" class="star-icon"
                  :class="{ filled: s <= Math.round(reviewData.average_rating || product.rating) }">
                  &#9733;
                </span>
              </div>
              <p class="score-subtext">Based on {{ reviewData.review_count || product.review_count }} ratings</p>
            </div>

            <!-- Star Percentage Meters -->
            <div class="star-meters">
              <div v-for="star in [5, 4, 3, 2, 1]" :key="star" class="meter-row">
                <span class="meter-star-label">{{ star }} &#9733;</span>
                <div class="meter-track">
                  <div class="meter-fill" :style="{ width: `${reviewData.star_percentages?.[String(star)] || 0}%` }">
                  </div>
                </div>
                <span class="meter-pct">{{ reviewData.star_percentages?.[String(star)] || 0 }}%</span>
              </div>
            </div>
          </div>

          <!-- Review Submission Form -->
          <div v-if="showReviewForm" class="review-form-card">
            <h3>{{ reviewData.user_has_reviewd ? 'Update Your Review' : 'Write a Review' }}</h3>

            <form @submit.prevent="handleReviewSubmit" class="review-form">
              <!-- Interactive Star Picker -->
              <div class="form-group">
                <label>Overall Rating *</label>
                <div class="star-picker">
                  <button v-for="s in 5" :key="s" type="button" class="picker-star"
                    :class="{ active: s <= reviewForm.rating }" @click="reviewForm.rating = s"
                    @mouseenter="hoverRating = s" @mouseleave="hoverRating = 0">
                    &#9733;
                  </button>
                  <span class="rating-descriptor">{{ getRatingLabel(hoverRating || reviewForm.rating) }}</span>
                </div>
              </div>

              <div class="form-group">
                <label for="headline">Review Headline (Optional)</label>
                <input id="headline" v-model="reviewForm.headline" type="text"
                  placeholder="e.g. Exceeded my expectations, fast shipping!" />
              </div>

              <div class="form-group">
                <label for="comment">Detailed Experience *</label>
                <textarea id="comment" v-model="reviewForm.comment" rows="4" required
                  placeholder="What did you like or dislike about this product? How is the quality?"></textarea>
              </div>

              <div v-if="reviewError" class="error-msg">{{ reviewError }}</div>

              <div class="form-actions">
                <button type="button" @click="showReviewForm = false" class="btn-cancel">Cancel</button>
                <button type="submit" class="btn-submit" :disabled="submittingReview">
                  {{ submittingReview ? 'Publishing...' : 'Submit Review' }}
                </button>
              </div>
            </form>
          </div>

          <!-- Prompt for Guest Users -->
          <div v-else-if="!isAuthenticated" class="guest-review-prompt">
            <span>Want to share your thoughts?</span>
            <NuxtLink :to="`/login?redirect=${route.fullPath}`" class="link-sign-in">Sign in to write a review &rarr;
            </NuxtLink>
          </div>

          <!-- Reviews Feed List -->
          <div class="reviews-feed">
            <div v-if="loadingReviews" class="reviews-loading">
              <LoadingSpinner text="Loading customer reviews..." />
            </div>

            <div v-else-if="!reviewData.reviews?.length" class="empty-reviews">
              <p>No customer reviews yet. Be the first to review this product!</p>
            </div>

            <div v-else class="reviews-list">
              <div v-for="rev in reviewData.reviews" :key="rev.id" class="review-card">
                <div class="review-top">
                  <div class="reviewer-meta">
                    <div class="avatar-circle">
                      {{ (rev.user_username || 'U')[0].toUpperCase() }}
                    </div>
                    <div>
                      <div class="name-row">
                        <strong>{{ rev.user_username }}</strong>
                        <span v-if="rev.is_verified_purchase" class="badge-verified">
                          &#10003; Verified Buyer
                        </span>
                      </div>
                      <span class="review-date">{{ formatDate(rev.created_at) }}</span>
                    </div>
                  </div>

                  <!-- Star Rating Display -->
                  <div class="review-stars">
                    <span v-for="s in 5" :key="s" class="star-icon small" :class="{ filled: s <= rev.rating }">
                      &#9733;
                    </span>
                  </div>
                </div>

                <h4 v-if="rev.headline" class="review-headline">{{ rev.headline }}</h4>
                <p class="review-text">{{ rev.comment }}</p>

                <!-- Owner Delete Action -->
                <div v-if="rev.is_own_review" class="review-footer">
                  <button @click="handleDeleteReview(rev.id)" class="btn-delete-review">
                    Delete My Review
                  </button>
                </div>
              </div>
            </div>
          </div>
        </section>

        <!-- PRODUCT FAQS ACCORDION -->
        <ProductFaqAccordion @open-support="isSupportModalOpen = true" />

        <!-- Related Products Section -->
        <section v-if="product?.related_products?.length" class="related-section">
          <h2>You Might Also Like</h2>
          <ProductGrid :products="product.related_products" />
        </section>

        <!-- CUSTOMER SUPPORT MODAL -->
        <CustomerSupportModal
          :is-open="isSupportModalOpen"
          :product-context="product"
          @close="isSupportModalOpen = false"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
const route = useRoute()
const { getProductBySlug, getProductReviews, submitProductReview, deleteProductReview } = useProducts()
const { addToCart } = useCartState()
const { isAuthenticated } = useAuthState()
const { isWishlisted, toggleWishlist } = useWishlist()

const product = ref(null)
const currentSelectedImage = ref('')

const galleryImages = computed(() => {
  const list = []
  if (product.value?.image) list.push(product.value.image)
  if (Array.isArray(product.value?.images)) {
    product.value.images.forEach(img => {
      const url = typeof img === 'string' ? img : img.image
      if (url && !list.includes(url)) list.push(url)
    })
  }
  return list
})
const loading = ref(true)
const error = ref('')
const quantity = ref(1)
const addingToCart = ref(false)
const addSuccessMsg = ref('')
const isSupportModalOpen = ref(false)

// Reviews State
const reviewData = ref({
  average_rating: 0,
  review_count: 0,
  star_percentages: {},
  reviews: []
})
const loadingReviews = ref(false)
const showReviewForm = ref(false)
const submittingReview = ref(false)
const reviewError = ref('')
const hoverRating = ref(0)

const reviewForm = reactive({
  rating: 5,
  headline: '',
  comment: ''
})

const hasSpecifications = computed(() => {
  return product.value?.specifications && Object.keys(product.value.specifications).length > 0
})

async function loadProduct() {
  loading.value = true
  error.value = ''
  try {
    const data = await getProductBySlug(route.params.slug)
    product.value = data
    await loadReviews()
  } catch (err) {
    error.value = 'We could not locate this product. It may have been removed or updated.'
  } finally {
    loading.value = false
  }
}

async function loadReviews() {
  loadingReviews.value = true
  try {
    const data = await getProductReviews(route.params.slug)
    reviewData.value = data
  } catch (err) {
    console.error('Failed to load reviews:', err)
  } finally {
    loadingReviews.value = false
  }
}

async function handleAddToCart() {
  if (!product.value) return
  addingToCart.value = true
  addSuccessMsg.value = ''
  const res = await addToCart(product.value.id, quantity.value)
  if (res.success) {
    addSuccessMsg.value = `Added ${quantity.value} item(s) to your cart!`
    setTimeout(() => { addSuccessMsg.value = '' }, 3500)
  } else {
    alert(res.error || 'Failed to add item to cart.')
  }
  addingToCart.value = false
}

async function handleReviewSubmit() {
  submittingReview.value = true
  reviewError.value = ''
  try {
    await submitProductReview(route.params.slug, reviewForm)
    showReviewForm.value = false
    reviewForm.headline = ''
    reviewForm.comment = ''
    // Reload both product (for updated rating/review_count) and reviews list
    const [pData] = await Promise.all([
      getProductBySlug(route.params.slug),
      loadReviews()
    ])
    product.value = pData
  } catch (err) {
    reviewError.value = err.message || err.data?.detail || 'Failed to submit review.'
  } finally {
    submittingReview.value = false
  }
}

async function handleDeleteReview(reviewId) {
  if (confirm('Are you sure you want to delete your review?')) {
    try {
      await deleteProductReview(route.params.slug, reviewId)
      const [pData] = await Promise.all([
        getProductBySlug(route.params.slug),
        loadReviews()
      ])
      product.value = pData
    } catch (err) {
      alert(err.message || 'Failed to delete review.')
    }
  }
}

function getRatingLabel(val) {
  const map = { 5: 'Excellent', 4: 'Very Good', 3: 'Average', 2: 'Below Average', 1: 'Poor' }
  return map[val] || ''
}

function formatDate(isoStr) {
  if (!isoStr) return ''
  const d = new Date(isoStr)
  return d.toLocaleDateString('en-US', { year: 'numeric', month: 'short', day: 'numeric' })
}

function scrollToReviews() {
  const el = document.getElementById('reviews-section')
  if (el) el.scrollIntoView({ behavior: 'smooth' })
}

watch(() => route.params.slug, () => {
  loadProduct()
})

onMounted(() => {
  loadProduct()
})
</script>

<style scoped>
.product-detail-page {
  padding: 3rem 1.5rem 5rem;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
}

.product-top-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1.5rem;
  margin-bottom: 2rem;
  flex-wrap: wrap;
}

.breadcrumb-trail {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.85rem;
  color: var(--text-muted);
}

.breadcrumb-trail a {
  color: var(--text-muted);
  text-decoration: none;
  transition: color 0.15s;
}

.breadcrumb-trail a:hover {
  color: var(--primary);
}

.bc-sep {
  color: var(--border-color);
  font-size: 0.8rem;
}

.bc-curr {
  color: var(--text-main);
  font-weight: 600;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 280px;
}

.product-layout {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 3.5rem;
  margin-bottom: 4rem;
}

.main-image-wrap {
  width: 100%;
  padding-top: 100%;
  position: relative;
  background: #f1f5f9;
  border-radius: var(--radius-lg);
  overflow: hidden;
  border: 1px solid var(--border-color);
}

.main-img {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: opacity 0.2s ease;
}

.gallery-thumbs {
  display: flex;
  gap: 0.75rem;
  margin-top: 1rem;
  overflow-x: auto;
  padding-bottom: 0.35rem;
}

.thumb-box {
  width: 68px;
  height: 68px;
  border-radius: var(--radius-md);
  border: 2px solid var(--border-color);
  background: #f1f5f9;
  overflow: hidden;
  padding: 0;
  cursor: pointer;
  flex-shrink: 0;
  transition: all 0.15s ease;
}

.thumb-box:hover {
  border-color: var(--primary);
  transform: translateY(-2px);
}

.thumb-box.active {
  border-color: var(--primary);
  box-shadow: 0 0 0 2px rgba(37, 99, 235, 0.25);
}

.thumb-box img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.image-fallback {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--text-muted);
}

.product-meta {
  display: flex;
  flex-direction: column;
}

.category-name {
  color: var(--primary);
  font-weight: 700;
  font-size: 0.85rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  margin-bottom: 0.5rem;
}

.title {
  font-size: 2.25rem;
  font-weight: 800;
  line-height: 1.2;
  letter-spacing: -0.02em;
  margin-bottom: 1rem;
}

.rating-row {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 1.5rem;
  cursor: pointer;
}

.stars {
  color: #f59e0b;
  font-weight: 700;
}

.reviews {
  color: var(--text-muted);
  font-size: 0.9rem;
}

.price-box {
  margin-bottom: 1.5rem;
}

.stock-status {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.9rem;
  font-weight: 600;
  margin-bottom: 1.5rem;
}

.stock-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
}

.in-stock {
  color: #16a34a;
}

.in-stock .stock-dot {
  background: #16a34a;
}

.out-of-stock {
  color: #dc2626;
}

.out-of-stock .stock-dot {
  background: #dc2626;
}

.description {
  color: var(--text-muted);
  line-height: 1.6;
  margin-bottom: 2rem;
}

.purchase-controls {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  margin-bottom: 2.5rem;
}

.success-banner {
  background: #f0fdf4;
  border: 1px solid #bbf7d0;
  color: #166534;
  padding: 0.75rem 1rem;
  border-radius: var(--radius-md);
  font-size: 0.9rem;
  font-weight: 600;
}

.btn-add-cart {
  background: var(--primary);
  color: #fff;
  font-weight: 700;
  font-size: 1.05rem;
  padding: 1rem;
  border-radius: var(--radius-md);
  transition: background 0.15s;
}

.btn-add-cart:hover:not(:disabled) {
  background: var(--primary-hover);
}

.btn-add-cart:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.specs-section {
  border-top: 1px solid var(--border-color);
  padding-top: 1.5rem;
}

.specs-section h3 {
  font-size: 1.1rem;
  font-weight: 700;
  margin-bottom: 1rem;
}

.specs-table {
  width: 100%;
  border-collapse: collapse;
}

.specs-table td {
  padding: 0.6rem 0;
  border-bottom: 1px solid var(--border-color);
  font-size: 0.9rem;
}

.spec-label {
  color: var(--text-muted);
  font-weight: 500;
  width: 40%;
}

.spec-value {
  font-weight: 600;
}

/* ==================== REVIEWS SECTION ==================== */
.reviews-section {
  border-top: 2px solid var(--border-color);
  padding-top: 3.5rem;
  margin-bottom: 5rem;
}

.section-header-row {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  margin-bottom: 2rem;
}

.section-header-row h2 {
  font-size: 1.75rem;
  font-weight: 800;
  letter-spacing: -0.02em;
}

.section-subtext {
  color: var(--text-muted);
  font-size: 0.95rem;
  margin-top: 0.25rem;
}

.btn-write-review {
  background: #0f172a;
  color: #fff;
  font-weight: 600;
  font-size: 0.9rem;
  padding: 0.65rem 1.25rem;
  border-radius: var(--radius-md);
  transition: background 0.15s;
}

.btn-write-review:hover {
  background: var(--primary);
}

/* Ratings Overview Card */
.ratings-overview-card {
  background: var(--bg-surface);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-lg);
  padding: 2rem;
  display: grid;
  grid-template-columns: 240px 1fr;
  gap: 3rem;
  align-items: center;
  margin-bottom: 2.5rem;
  box-shadow: var(--shadow-sm);
}

.score-summary {
  text-align: center;
  border-right: 1px solid var(--border-color);
  padding-right: 2rem;
}

.big-score {
  font-size: 3.5rem;
  font-weight: 800;
  line-height: 1;
  color: var(--text-main);
  margin-bottom: 0.5rem;
}

.star-display {
  display: flex;
  justify-content: center;
  gap: 0.2rem;
  margin-bottom: 0.5rem;
}

.star-icon {
  font-size: 1.35rem;
  color: #e2e8f0;
}

.star-icon.filled {
  color: #f59e0b;
}

.star-icon.small {
  font-size: 1rem;
}

.score-subtext {
  font-size: 0.85rem;
  color: var(--text-muted);
}

.star-meters {
  display: flex;
  flex-direction: column;
  gap: 0.6rem;
}

.meter-row {
  display: flex;
  align-items: center;
  gap: 1rem;
  font-size: 0.85rem;
}

.meter-star-label {
  width: 45px;
  font-weight: 600;
  color: var(--text-muted);
}

.meter-track {
  flex: 1;
  height: 8px;
  background: #f1f5f9;
  border-radius: 999px;
  overflow: hidden;
}

.meter-fill {
  height: 100%;
  background: #f59e0b;
  border-radius: 999px;
  transition: width 0.3s ease;
}

.meter-pct {
  width: 40px;
  text-align: right;
  font-weight: 600;
  color: var(--text-muted);
  font-size: 0.8rem;
}

/* Review Form Card */
.review-form-card {
  background: var(--bg-surface);
  border: 1.5px solid var(--primary);
  border-radius: var(--radius-lg);
  padding: 2rem;
  margin-bottom: 2.5rem;
  box-shadow: var(--shadow-md);
}

.review-form-card h3 {
  font-size: 1.25rem;
  font-weight: 700;
  margin-bottom: 1.25rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
  margin-bottom: 1.25rem;
}

.form-group label {
  font-size: 0.85rem;
  font-weight: 600;
}

.star-picker {
  display: flex;
  align-items: center;
  gap: 0.35rem;
}

.picker-star {
  font-size: 1.75rem;
  color: #cbd5e1;
  transition: color 0.1s, transform 0.1s;
}

.picker-star:hover,
.picker-star.active {
  color: #f59e0b;
  transform: scale(1.15);
}

.rating-descriptor {
  margin-left: 0.75rem;
  font-size: 0.9rem;
  font-weight: 600;
  color: var(--text-muted);
}

.form-group input,
.form-group textarea {
  border: 1px solid var(--border-color);
  border-radius: var(--radius-md);
  padding: 0.75rem 0.85rem;
  font-size: 0.95rem;
  outline: none;
  transition: border-color 0.15s;
}

.form-group input:focus,
.form-group textarea:focus {
  border-color: var(--primary);
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 0.75rem;
}

.btn-cancel {
  padding: 0.65rem 1.25rem;
  font-size: 0.9rem;
  font-weight: 600;
  color: var(--text-muted);
}

.btn-submit {
  background: var(--primary);
  color: #fff;
  font-size: 0.9rem;
  font-weight: 700;
  padding: 0.65rem 1.5rem;
  border-radius: var(--radius-md);
  transition: background 0.15s;
}

.btn-submit:hover:not(:disabled) {
  background: var(--primary-hover);
}

.guest-review-prompt {
  background: #f8fafc;
  border: 1px dashed var(--border-color);
  border-radius: var(--radius-md);
  padding: 1.25rem;
  text-align: center;
  margin-bottom: 2rem;
  font-size: 0.95rem;
  color: var(--text-muted);
}

.link-sign-in {
  color: var(--primary);
  font-weight: 700;
  margin-left: 0.5rem;
}

/* Reviews List */
.reviews-list {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

.review-card {
  background: var(--bg-surface);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-lg);
  padding: 1.5rem;
  box-shadow: var(--shadow-sm);
}

.review-top {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 0.75rem;
}

.reviewer-meta {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.avatar-circle {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: #0f172a;
  color: #fff;
  font-weight: 700;
  display: flex;
  align-items: center;
  justify-content: center;
}

.name-row {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.badge-verified {
  font-size: 0.7rem;
  font-weight: 700;
  background: #dcfce7;
  color: #166534;
  padding: 0.15rem 0.45rem;
  border-radius: 4px;
}

.review-date {
  font-size: 0.75rem;
  color: var(--text-muted);
}

.review-headline {
  font-size: 1rem;
  font-weight: 700;
  margin-bottom: 0.4rem;
}

.review-text {
  color: var(--text-muted);
  font-size: 0.95rem;
  line-height: 1.5;
}

.review-footer {
  margin-top: 1rem;
  padding-top: 0.75rem;
  border-top: 1px dashed var(--border-color);
  display: flex;
  justify-content: flex-end;
}

.btn-delete-review {
  font-size: 0.8rem;
  color: #dc2626;
  font-weight: 600;
  transition: opacity 0.15s;
}

.btn-delete-review:hover {
  opacity: 0.75;
}

.empty-reviews {
  padding: 3rem;
  text-align: center;
  color: var(--text-muted);
}

/* Related Products */
.related-section {
  border-top: 1px solid var(--border-color);
  padding-top: 3rem;
}

.related-section h2 {
  font-size: 1.5rem;
  font-weight: 800;
  margin-bottom: 2rem;
}

.purchase-row {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  flex-wrap: wrap;
}

.btn-wishlist-toggle {
  display: flex;
  align-items: center;
  gap: 0.4rem;
  padding: 0.85rem 1.25rem;
  background: var(--bg-surface);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-md);
  font-weight: 600;
  font-size: 0.95rem;
  color: var(--text-main);
  cursor: pointer;
  transition: all 0.15s ease;
}

.btn-wishlist-toggle:hover {
  border-color: #ef4444;
  color: #ef4444;
}

.btn-wishlist-toggle.active {
  background: #fef2f2;
  border-color: #fecaca;
  color: #ef4444;
}

/* Product Trust Strip */
.product-trust-strip {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  margin-top: 1.25rem;
  padding: 0.85rem 1rem;
  background: #f8fafc;
  border: 1px solid var(--border-color);
  border-radius: var(--radius-md);
}

.trust-item {
  display: flex;
  align-items: center;
  gap: 0.65rem;
  font-size: 0.85rem;
  font-weight: 600;
  color: #475569;
}

.trust-icon {
  font-size: 1.05rem;
}

/* Product Support Action */
.product-support-action {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-top: 0.85rem;
  padding: 0.65rem 0.85rem;
  border-radius: var(--radius-sm);
  background: #eff6ff;
  border: 1px dashed #bfdbfe;
  font-size: 0.85rem;
  color: #1e40af;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.btn-product-ask {
  display: inline-flex;
  align-items: center;
  gap: 0.35rem;
  background: #fff;
  border: 1px solid #93c5fd;
  color: var(--primary);
  font-weight: 700;
  font-size: 0.8rem;
  padding: 0.35rem 0.75rem;
  border-radius: var(--radius-sm);
  cursor: pointer;
  transition: all 0.15s;
}

.btn-product-ask:hover {
  background: var(--primary);
  color: #fff;
  border-color: var(--primary);
}


@media (max-width: 860px) {
  .product-layout {
    grid-template-columns: 1fr;
    gap: 2rem;
  }

  .ratings-overview-card {
    grid-template-columns: 1fr;
    gap: 1.5rem;
  }

  .score-summary {
    border-right: none;
    border-bottom: 1px solid var(--border-color);
    padding-right: 0;
    padding-bottom: 1.5rem;
  }
}
</style>
