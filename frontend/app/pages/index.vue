<script setup>
definePageMeta({
  middleware: [
    async () => {
      const { user, initialized, refreshUser } = useAuthState()
      if (!initialized.value) {
        await refreshUser()
      }
      if (user.value?.is_staff) {
        return navigateTo('/admin')
      }
    }
  ]
})

const { getCategories, getProducts } = useProducts()

const categories = ref([])
const products = ref([])
const loadingCategories = ref(true)
const loadingProducts = ref(true)
const activeFilter = ref('all')

// Newsletter state
const newsletterEmail = ref('')
const newsletterSuccess = ref(false)

onMounted(async () => {
  try {
    const [catData, prodData] = await Promise.all([
      getCategories(),
      getProducts({ featured: true })
    ])

    categories.value = catData || []
    products.value = prodData?.results || []
  } catch (err) {
    console.error("Failed to load homepage data: ", err)
  } finally {
    loadingCategories.value = false
    loadingProducts.value = false
  }
})

const filteredProducts = computed(() => {
  if (activeFilter.value === 'all') return products.value
  if (activeFilter.value === 'deals') {
    return products.value.filter(p => p.discount_percentage > 0)
  }
  return products.value.filter(p => p.category?.slug === activeFilter.value)
})

function handleNewsletterSubmit() {
  if (newsletterEmail.value.includes('@')) {
    newsletterSuccess.value = true
  }
}

const categoryIcons = {
  'smart-tech-gadgets': 'fa-solid fa-headphones',
  'home-lifestyle': 'fa-solid fa-house',
  'fitness-outdoors': 'fa-solid fa-dumbbell',
}

function getCategoryIcon(slug) {
  return categoryIcons[slug] || 'fa-solid fa-wand-magic-sparkles'
}
</script>

<template>
  <div class="home-page">
    <!-- HERO SECTION -->
    <section class="hero-section">
      <div class="hero-glow"></div>
      <div class="hero-container">
        <!-- Trust Rating Chip -->
        <div class="hero-rating-pill">
          <div class="star-group">
            <i class="fa-solid fa-star"></i><i class="fa-solid fa-star"></i><i class="fa-solid fa-star"></i><i class="fa-solid fa-star"></i><i class="fa-solid fa-star"></i>
          </div>
          <span class="rating-text">4.9/5 from 2,400+ verified shoppers</span>
          <span class="pill-divider">•</span>
          <span class="pill-badge">Factory Direct</span>
        </div>

        <!-- Headline & Subtitle -->
        <h1 class="hero-title">
          Curated Tech & Modern Essentials, <br class="title-break" />
          <span class="gradient-text">Direct to Your Doorstep.</span>
        </h1>

        <p class="hero-subtitle">
          Bypass retail markups. Explore rigorously tested audio, fast wireless docks, and smart lifestyle upgrades
          backed by direct factory sourcing and 30-day risk-free guarantees.
        </p>

        <!-- CTA Buttons -->
        <div class="hero-actions">
          <NuxtLink to="/shop" class="btn-primary-hero">
            <span>Explore Catalog</span>
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
              <line x1="5" y1="12" x2="19" y2="12"></line>
              <polyline points="12 5 19 12 12 19"></polyline>
            </svg>
          </NuxtLink>

          <NuxtLink to="/shop?on_sale=true" class="btn-secondary-hero">
            <span class="deal-flame"><i class="fa-solid fa-fire"></i></span>
            <span>View Flash Deals</span>
          </NuxtLink>
        </div>

        <!-- Hero Stats Counters -->
        <div class="hero-stats-grid">
          <div class="stat-card">
            <strong class="stat-num">15,000+</strong>
            <span class="stat-label">Orders Shipped</span>
          </div>
          <div class="stat-card">
            <strong class="stat-num">4–8 Days</strong>
            <span class="stat-label">Tracked Air Delivery</span>
          </div>
          <div class="stat-card">
            <strong class="stat-num">30 Days</strong>
            <span class="stat-label">Money-Back Trial</span>
          </div>
          <div class="stat-card">
            <strong class="stat-num">24 / 7</strong>
            <span class="stat-label">Dedicated Support</span>
          </div>
        </div>
      </div>
    </section>

    <!-- TRUST PILLARS / PERKS BAR -->
    <section class="trust-perks-section">
      <div class="section-container">
        <div class="perks-grid">
          <div class="perk-card">
            <div class="perk-icon-wrap blue">
              <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2">
                <rect x="1" y="3" width="15" height="13"></rect>
                <polygon points="16 8 20 8 23 11 23 16 16 16 16 8"></polygon>
                <circle cx="5.5" cy="18.5" r="2.5"></circle>
                <circle cx="18.5" cy="18.5" r="2.5"></circle>
              </svg>
            </div>
            <div class="perk-content">
              <h4>Direct Tracked Dispatch</h4>
              <p>Real-time carrier checkpoints from vetted supplier hubs.</p>
            </div>
          </div>

          <div class="perk-card">
            <div class="perk-icon-wrap green">
              <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2">
                <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path>
                <polyline points="9 12 11 14 15 10"></polyline>
              </svg>
            </div>
            <div class="perk-content">
              <h4>30-Day Money-Back</h4>
              <p>Zero risk shopping. Hassle-free refunds or replacements.</p>
            </div>
          </div>

          <div class="perk-card">
            <div class="perk-icon-wrap purple">
              <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2">
                <rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect>
                <path d="M7 11V7a5 5 0 0 1 10 0v4"></path>
              </svg>
            </div>
            <div class="perk-content">
              <h4>Bank-Grade Encryption</h4>
              <p>256-bit SSL encrypted PCI checkout & verified cards.</p>
            </div>
          </div>

          <div class="perk-card">
            <div class="perk-icon-wrap orange">
              <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2">
                <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path>
              </svg>
            </div>
            <div class="perk-content">
              <h4>2-Hour Support Response</h4>
              <p>Dedicated customer helpdesk available around the clock.</p>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- SHOP BY CATEGORY -->
    <section class="categories-section">
      <div class="section-container">
        <div class="section-header-row">
          <div>
            <span class="sub-header-tag">Curated Collections</span>
            <h2>Shop by Category</h2>
          </div>
          <NuxtLink to="/shop" class="view-all-link">
            <span>Explore all categories</span>
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
              <line x1="5" y1="12" x2="19" y2="12"></line>
              <polyline points="12 5 19 12 12 19"></polyline>
            </svg>
          </NuxtLink>
        </div>

        <div v-if="loadingCategories" class="loading-wrap">
          <LoadingSpinner text="Loading collections..." />
        </div>

        <div v-else class="category-grid">
          <NuxtLink
            v-for="cat in categories"
            :key="cat.id"
            :to="`/shop?category=${cat.slug}`"
            class="category-card"
          >
            <div class="cat-icon-bubble">
              <i :class="getCategoryIcon(cat.slug)"></i>
            </div>
            <div class="cat-details">
              <h3>{{ cat.name }}</h3>
              <p class="cat-desc">{{ cat.description }}</p>
              <span class="cat-count-pill">{{ cat.product_count }} Curated Items &rarr;</span>
            </div>
          </NuxtLink>
        </div>
      </div>
    </section>

    <!-- FEATURED PRODUCTS SHOWCASE -->
    <section class="featured-section">
      <div class="section-container">
        <div class="section-header-row">
          <div>
            <span class="sub-header-tag">Customer Favorites</span>
            <h2>Featured Products</h2>
          </div>

          <!-- Quick Filter Tabs -->
          <div class="filter-tab-pills">
            <button
              type="button"
              class="tab-pill"
              :class="{ active: activeFilter === 'all' }"
              @click="activeFilter = 'all'"
            >
              All Items
            </button>
            <button
              type="button"
              class="tab-pill"
              :class="{ active: activeFilter === 'deals' }"
              @click="activeFilter = 'deals'"
            >
              <i class="fa-solid fa-fire text-amber"></i> Special Deals
            </button>
            <button
              v-for="c in categories"
              :key="c.id"
              type="button"
              class="tab-pill"
              :class="{ active: activeFilter === c.slug }"
              @click="activeFilter = c.slug"
            >
              {{ c.name.split('&')[0].trim() }}
            </button>
          </div>
        </div>

        <div v-if="loadingProducts" class="loading-wrap">
          <LoadingSpinner text="Fetching products..." />
        </div>

        <ProductGrid v-else-if="filteredProducts.length" :products="filteredProducts" />

        <EmptyState
          v-else
          title="No products found in this category."
          description="Check back shortly or explore our full collection."
        />
      </div>
    </section>

    <!-- SPOTLIGHT PRODUCT BANNER -->
    <section class="spotlight-section">
      <div class="section-container">
        <div class="spotlight-card">
          <div class="spotlight-content">
            <span class="spotlight-tag"><i class="fa-solid fa-award"></i> DEAL OF THE WEEK</span>
            <h2>AeroPro Noise-Cancelling Earbuds</h2>
            <p>
              Engineered with active noise cancellation, custom high-excursion drivers, and 32-hour battery life.
              Factory direct pricing with zero brand markups.
            </p>
            <div class="spotlight-features">
              <div class="s-feat"><i class="fa-solid fa-circle-check"></i> 32-Hour Battery Case</div>
              <div class="s-feat"><i class="fa-solid fa-circle-check"></i> IPX7 Waterproofing</div>
              <div class="s-feat"><i class="fa-solid fa-circle-check"></i> Touch EQ Controls</div>
            </div>
            <div class="spotlight-action-row">
              <NuxtLink to="/products/aeropro-wireless-noise-cancelling-earbuds" class="btn-spotlight">
                Shop Product Details &rarr;
              </NuxtLink>
              <span class="spotlight-code">Use code <strong>WELCOME10</strong> for 10% off</span>
            </div>
          </div>
          <div class="spotlight-visual">
            <div class="visual-badge">
              <span class="badge-saving">Save 33%</span>
              <span class="badge-retail">Compared to $89.99</span>
            </div>
            <div class="audio-wave">
              <span class="wave-bar w1"></span>
              <span class="wave-bar w2"></span>
              <span class="wave-bar w3"></span>
              <span class="wave-bar w4"></span>
              <span class="wave-bar w5"></span>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- CUSTOMER REVIEWS & SOCIAL PROOF -->
    <section class="testimonials-section">
      <div class="section-container">
        <div class="section-header-center">
          <span class="sub-header-tag">Verified Experiences</span>
          <h2>Loved by Smart Shoppers Worldwide</h2>
          <p class="section-subtext">Real reviews from customers who made the switch to direct factory dropshipping.</p>
        </div>

        <div class="testimonials-grid">
          <div class="testimonial-card">
            <div class="review-stars">
              <i class="fa-solid fa-star"></i><i class="fa-solid fa-star"></i><i class="fa-solid fa-star"></i><i class="fa-solid fa-star"></i><i class="fa-solid fa-star"></i>
            </div>
            <p class="review-quote">
              "The AeroPro Earbuds sound comparable to $200 brand name headphones. Arrived in 5 days with clear tracking updates. Outstanding value!"
            </p>
            <div class="reviewer-footer">
              <div class="reviewer-avatar">M</div>
              <div>
                <strong>Marcus T.</strong>
                <span class="reviewer-loc">Austin, TX • Verified Buyer</span>
              </div>
            </div>
          </div>

          <div class="testimonial-card">
            <div class="review-stars">
              <i class="fa-solid fa-star"></i><i class="fa-solid fa-star"></i><i class="fa-solid fa-star"></i><i class="fa-solid fa-star"></i><i class="fa-solid fa-star"></i>
            </div>
            <p class="review-quote">
              "Ordered the MagCharge 3-in-1 station for my nightstand. Clean design, charges my phone, watch, and earbuds all at once. Super clean setup."
            </p>
            <div class="reviewer-footer">
              <div class="reviewer-avatar">S</div>
              <div>
                <strong>Sarah K.</strong>
                <span class="reviewer-loc">London, UK • Verified Buyer</span>
              </div>
            </div>
          </div>

          <div class="testimonial-card">
            <div class="review-stars">
              <i class="fa-solid fa-star"></i><i class="fa-solid fa-star"></i><i class="fa-solid fa-star"></i><i class="fa-solid fa-star"></i><i class="fa-solid fa-star"></i>
            </div>
            <p class="review-quote">
              "Super impressed with customer support when I asked a sizing question. Ticket was answered in 40 minutes and product quality is top notch."
            </p>
            <div class="reviewer-footer">
              <div class="reviewer-avatar">D</div>
              <div>
                <strong>David M.</strong>
                <span class="reviewer-loc">Toronto, CA • Verified Buyer</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- VIP NEWSLETTER SIGNUP -->
    <section class="newsletter-section">
      <div class="section-container">
        <div class="newsletter-card">
          <div class="newsletter-content">
            <span class="newsletter-badge">VIP Club Access</span>
            <h2>Get 10% Off Your First Order</h2>
            <p>Subscribe to receive exclusive drops, private warehouse clearance deals, and secret discount coupons.</p>

            <div v-if="newsletterSuccess" class="newsletter-success">
              <span class="check-icon"><i class="fa-solid fa-check"></i></span>
              <span>You're in! Use coupon <strong>WELCOME10</strong> during checkout.</span>
            </div>

            <form v-else @submit.prevent="handleNewsletterSubmit" class="newsletter-form">
              <input
                v-model="newsletterEmail"
                type="email"
                required
                placeholder="Enter your email address..."
                class="newsletter-input"
              />
              <button type="submit" class="btn-newsletter">
                Claim My 10% Off
              </button>
            </form>

            <span class="newsletter-note">Zero spam. Unsubscribe anytime with 1 click.</span>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<style scoped>
.home-page {
  display: flex;
  flex-direction: column;
}

/* HERO SECTION */
.hero-section {
  position: relative;
  background: radial-gradient(circle at 50% 20%, #eff6ff 0%, #f8fafc 85%, #f1f5f9 100%);
  border-bottom: 1px solid var(--border-color);
  padding: 5rem 1.5rem 4.5rem;
  overflow: hidden;
  text-align: center;
}

.hero-glow {
  position: absolute;
  top: -150px;
  left: 50%;
  transform: translateX(-50%);
  width: 700px;
  height: 400px;
  background: radial-gradient(circle, rgba(37, 99, 235, 0.15) 0%, rgba(99, 102, 241, 0.08) 50%, transparent 80%);
  filter: blur(60px);
  pointer-events: none;
}

.hero-container {
  max-width: 860px;
  margin: 0 auto;
  position: relative;
  z-index: 2;
}

/* Rating Pill */
.hero-rating-pill {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  background: #ffffff;
  border: 1px solid var(--border-color);
  padding: 0.35rem 0.95rem;
  border-radius: var(--radius-full);
  margin-bottom: 1.5rem;
  font-size: 0.82rem;
  font-weight: 600;
  box-shadow: var(--shadow-sm);
}

.star-group {
  color: #eab308;
  letter-spacing: 0.05em;
  font-size: 0.9rem;
}

.rating-text {
  color: var(--text-body);
}

.pill-divider {
  color: var(--text-subtle);
}

.pill-badge {
  color: var(--primary);
  font-weight: 700;
  text-transform: uppercase;
  font-size: 0.72rem;
}

/* Hero Title & Subtitle */
.hero-title {
  font-size: 3.4rem;
  font-weight: 800;
  line-height: 1.15;
  letter-spacing: -0.035em;
  color: var(--text-main);
  margin-bottom: 1.35rem;
}

.hero-subtitle {
  color: var(--text-muted);
  font-size: 1.15rem;
  line-height: 1.65;
  max-width: 680px;
  margin: 0 auto 2.25rem;
}

/* Hero Actions */
.hero-actions {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 1rem;
  flex-wrap: wrap;
  margin-bottom: 3.5rem;
}

.btn-primary-hero {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  background: linear-gradient(135deg, #1d4ed8 0%, #2563eb 100%);
  color: #ffffff;
  font-weight: 700;
  font-size: 1rem;
  padding: 0.95rem 2rem;
  border-radius: var(--radius-full);
  box-shadow: 0 8px 24px -4px rgba(37, 99, 235, 0.4);
  transition: all var(--transition-base);
}

.btn-primary-hero:hover {
  background: linear-gradient(135deg, #1e40af 0%, #1d4ed8 100%);
  transform: translateY(-2px);
  box-shadow: 0 12px 28px -4px rgba(37, 99, 235, 0.5);
}

.btn-secondary-hero {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  background: #ffffff;
  color: var(--text-main);
  border: 1px solid var(--border-color);
  font-weight: 700;
  font-size: 1rem;
  padding: 0.95rem 1.85rem;
  border-radius: var(--radius-full);
  box-shadow: var(--shadow-sm);
  transition: all var(--transition-base);
}

.btn-secondary-hero:hover {
  border-color: var(--border-hover);
  background: var(--bg-subtle);
  transform: translateY(-2px);
}

/* Hero Stats Grid */
.hero-stats-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1.5rem;
  padding-top: 2rem;
  border-top: 1px solid rgba(226, 232, 240, 0.8);
}

.stat-card {
  display: flex;
  flex-direction: column;
  gap: 0.2rem;
}

.stat-num {
  font-family: 'Outfit', sans-serif;
  font-size: 1.6rem;
  font-weight: 800;
  color: var(--text-main);
  letter-spacing: -0.02em;
}

.stat-label {
  font-size: 0.82rem;
  color: var(--text-muted);
  font-weight: 600;
}

/* SECTION CONTAINERS */
.section-container {
  max-width: 1240px;
  margin: 0 auto;
  padding: 4.5rem 1.5rem;
}

.section-header-row {
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  margin-bottom: 2.25rem;
  gap: 1.5rem;
  flex-wrap: wrap;
}

.section-header-row h2 {
  font-size: 2.1rem;
  font-weight: 800;
  letter-spacing: -0.03em;
  margin-top: 0.25rem;
}

.sub-header-tag {
  font-size: 0.78rem;
  font-weight: 800;
  text-transform: uppercase;
  color: var(--primary);
  letter-spacing: 0.08em;
}

.view-all-link {
  display: inline-flex;
  align-items: center;
  gap: 0.35rem;
  font-size: 0.92rem;
  font-weight: 700;
  color: var(--primary);
}

.view-all-link:hover {
  color: var(--primary-hover);
}

/* TRUST PERKS BAR */
.trust-perks-section {
  background: #ffffff;
  border-bottom: 1px solid var(--border-color);
}

.trust-perks-section .section-container {
  padding: 2.5rem 1.5rem;
}

.perks-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 2rem;
}

.perk-card {
  display: flex;
  align-items: flex-start;
  gap: 1rem;
}

.perk-icon-wrap {
  width: 44px;
  height: 44px;
  border-radius: var(--radius-md);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.perk-icon-wrap.blue { background: #eff6ff; color: #2563eb; }
.perk-icon-wrap.green { background: #ecfdf5; color: #10b981; }
.perk-icon-wrap.purple { background: #f5f3ff; color: #8b5cf6; }
.perk-icon-wrap.orange { background: #fff7ed; color: #f97316; }

.perk-content h4 {
  font-size: 0.98rem;
  font-weight: 700;
  margin-bottom: 0.2rem;
}

.perk-content p {
  font-size: 0.82rem;
  color: var(--text-muted);
  line-height: 1.45;
}

/* CATEGORY GRID */
.categories-section {
  background: var(--bg-page);
}

.category-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1.5rem;
}

.category-card {
  background: #ffffff;
  border: 1px solid var(--border-color);
  border-radius: var(--radius-lg);
  padding: 1.75rem;
  display: flex;
  gap: 1.25rem;
  transition: all var(--transition-base);
  box-shadow: var(--shadow-xs);
}

.category-card:hover {
  transform: translateY(-4px);
  border-color: var(--primary);
  box-shadow: var(--shadow-hover);
}

.cat-icon-bubble {
  width: 52px;
  height: 52px;
  border-radius: var(--radius-md);
  background: var(--bg-subtle);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.4rem;
  color: var(--primary);
  flex-shrink: 0;
}

.cat-details h3 {
  font-size: 1.15rem;
  font-weight: 700;
  margin-bottom: 0.35rem;
}

.cat-desc {
  font-size: 0.85rem;
  color: var(--text-muted);
  line-height: 1.45;
  margin-bottom: 0.85rem;
}

.cat-count-pill {
  font-size: 0.82rem;
  font-weight: 700;
  color: var(--primary);
}

/* FEATURED PRODUCTS & TABS */
.filter-tab-pills {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.tab-pill {
  padding: 0.45rem 1rem;
  border-radius: var(--radius-full);
  font-size: 0.85rem;
  font-weight: 600;
  background: #ffffff;
  border: 1px solid var(--border-color);
  color: var(--text-body);
  transition: all var(--transition-fast);
}

.tab-pill:hover {
  border-color: var(--primary);
  color: var(--primary);
}

.tab-pill.active {
  background: var(--primary);
  color: #ffffff;
  border-color: var(--primary);
  box-shadow: 0 4px 12px rgba(37, 99, 235, 0.25);
}

/* SPOTLIGHT CARD */
.spotlight-section {
  background: #ffffff;
}

.spotlight-card {
  background: linear-gradient(135deg, #0b0f19 0%, #1e293b 100%);
  border-radius: var(--radius-xl);
  padding: 3.5rem;
  color: #ffffff;
  display: grid;
  grid-template-columns: 1.2fr 0.8fr;
  gap: 3rem;
  align-items: center;
  box-shadow: var(--shadow-xl);
  overflow: hidden;
  position: relative;
}

.spotlight-tag {
  display: inline-block;
  background: rgba(37, 99, 235, 0.4);
  border: 1px solid rgba(96, 165, 250, 0.4);
  color: #93c5fd;
  font-size: 0.75rem;
  font-weight: 800;
  letter-spacing: 0.05em;
  padding: 0.35rem 0.85rem;
  border-radius: var(--radius-full);
  margin-bottom: 1rem;
}

.spotlight-content h2 {
  font-size: 2.3rem;
  color: #ffffff;
  margin-bottom: 1rem;
}

.spotlight-content p {
  color: #cbd5e1;
  font-size: 1.05rem;
  line-height: 1.6;
  margin-bottom: 1.5rem;
}

.spotlight-features {
  display: flex;
  gap: 1.5rem;
  margin-bottom: 2rem;
  flex-wrap: wrap;
}

.s-feat {
  font-size: 0.88rem;
  font-weight: 600;
  color: #93c5fd;
}

.spotlight-action-row {
  display: flex;
  align-items: center;
  gap: 1.5rem;
  flex-wrap: wrap;
}

.btn-spotlight {
  background: #2563eb;
  color: #fff;
  font-weight: 700;
  padding: 0.85rem 1.75rem;
  border-radius: var(--radius-full);
  box-shadow: 0 4px 14px rgba(37, 99, 235, 0.4);
  transition: all var(--transition-fast);
}

.btn-spotlight:hover {
  background: #1d4ed8;
  transform: translateY(-2px);
}

.spotlight-code {
  font-size: 0.85rem;
  color: #94a3b8;
}

.spotlight-visual {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 2rem;
}

.visual-badge {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(8px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  padding: 1.5rem 2rem;
  border-radius: var(--radius-lg);
  text-align: center;
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.badge-saving {
  font-size: 1.75rem;
  font-weight: 800;
  color: #38bdf8;
}

.badge-retail {
  font-size: 0.85rem;
  color: #94a3b8;
  text-decoration: line-through;
}

.audio-wave {
  display: flex;
  align-items: center;
  gap: 6px;
  height: 40px;
}

.wave-bar {
  width: 6px;
  background: #38bdf8;
  border-radius: 99px;
  animation: wave 1.2s ease-in-out infinite alternate;
}

.w1 { height: 16px; animation-delay: 0.1s; }
.w2 { height: 32px; animation-delay: 0.3s; }
.w3 { height: 24px; animation-delay: 0.2s; }
.w4 { height: 38px; animation-delay: 0.4s; }
.w5 { height: 20px; animation-delay: 0.25s; }

@keyframes wave {
  0% { transform: scaleY(0.4); }
  100% { transform: scaleY(1); }
}

/* TESTIMONIALS SECTION */
.testimonials-section {
  background: var(--bg-page);
}

.section-header-center {
  text-align: center;
  max-width: 650px;
  margin: 0 auto 3rem;
}

.section-header-center h2 {
  font-size: 2.1rem;
  margin: 0.35rem 0 0.5rem;
}

.section-subtext {
  color: var(--text-muted);
  font-size: 1rem;
}

.testimonials-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1.5rem;
}

.testimonial-card {
  background: #ffffff;
  border: 1px solid var(--border-color);
  border-radius: var(--radius-lg);
  padding: 1.75rem;
  display: flex;
  flex-direction: column;
  box-shadow: var(--shadow-xs);
}

.review-stars {
  color: #eab308;
  font-size: 1.1rem;
  margin-bottom: 0.85rem;
  letter-spacing: 0.1em;
}

.review-quote {
  color: var(--text-body);
  font-size: 0.95rem;
  line-height: 1.6;
  margin-bottom: 1.5rem;
  flex: 1;
}

.reviewer-footer {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.reviewer-avatar {
  width: 38px;
  height: 38px;
  border-radius: 50%;
  background: #eff6ff;
  color: var(--primary);
  font-weight: 700;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.95rem;
}

.reviewer-loc {
  display: block;
  font-size: 0.78rem;
  color: var(--text-muted);
}

/* NEWSLETTER SECTION */
.newsletter-section {
  background: #ffffff;
  border-top: 1px solid var(--border-color);
}

.newsletter-card {
  background: linear-gradient(135deg, #eff6ff 0%, #f8fafc 100%);
  border: 1px solid #bfdbfe;
  border-radius: var(--radius-xl);
  padding: 4rem 2rem;
  text-align: center;
}

.newsletter-content {
  max-width: 580px;
  margin: 0 auto;
}

.newsletter-badge {
  display: inline-block;
  background: var(--primary);
  color: #ffffff;
  font-size: 0.75rem;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  padding: 0.3rem 0.8rem;
  border-radius: var(--radius-full);
  margin-bottom: 1rem;
}

.newsletter-content h2 {
  font-size: 2.2rem;
  margin-bottom: 0.75rem;
}

.newsletter-content p {
  color: var(--text-muted);
  font-size: 1rem;
  margin-bottom: 1.75rem;
}

.newsletter-form {
  display: flex;
  gap: 0.65rem;
  max-width: 460px;
  margin: 0 auto 0.85rem;
}

.newsletter-input {
  flex: 1;
  padding: 0.85rem 1.15rem;
  border: 1px solid var(--border-color);
  border-radius: var(--radius-full);
  font-size: 0.95rem;
  outline: none;
  background: #ffffff;
}

.newsletter-input:focus {
  border-color: var(--primary);
}

.btn-newsletter {
  background: var(--primary);
  color: #ffffff;
  font-weight: 700;
  font-size: 0.95rem;
  padding: 0.85rem 1.65rem;
  border-radius: var(--radius-full);
  box-shadow: 0 4px 12px rgba(37, 99, 235, 0.25);
  transition: all var(--transition-fast);
  white-space: nowrap;
}

.btn-newsletter:hover {
  background: var(--primary-hover);
}

.newsletter-success {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  background: #dcfce7;
  color: #166534;
  padding: 0.75rem 1.25rem;
  border-radius: var(--radius-full);
  font-weight: 600;
  font-size: 0.95rem;
}

.newsletter-note {
  font-size: 0.8rem;
  color: var(--text-subtle);
}

/* RESPONSIVE QUERIES */
@media (max-width: 1024px) {
  .hero-title { font-size: 2.75rem; }
  .perks-grid { grid-template-columns: repeat(2, 1fr); }
  .category-grid { grid-template-columns: 1fr; }
  .testimonials-grid { grid-template-columns: 1fr; }
  .spotlight-card { grid-template-columns: 1fr; padding: 2.5rem; }
}

@media (max-width: 640px) {
  .hero-title { font-size: 2.15rem; }
  .title-break { display: none; }
  .hero-stats-grid { grid-template-columns: repeat(2, 1fr); gap: 1rem; }
  .perks-grid { grid-template-columns: 1fr; }
  .newsletter-form { flex-direction: column; }
  .btn-newsletter { width: 100%; }
}
</style>
