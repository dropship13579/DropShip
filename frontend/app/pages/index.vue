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
const featuredProducts = ref([])
const loadingCategories = ref(true)
const loadingProducts = ref(true)

onMounted(async () => {
  try {
    const [catData, prodData] = await Promise.all([
      getCategories(),
      getProducts({ featured: true })
    ])

    categories.value = catData || []
    featuredProducts.value = prodData?.results || []
  } catch (err) {
    console.error("Failed to load homepage data: ", err)
  } finally {
    loadingCategories.value = false
    loadingProducts.value = false
  }
})

</script>

<template>
  <div class="home-page">
    <section class="hero-section">
      <div class="hero-inner">
        <span class="hero-badge">Direct From Verified Suppliers</span>
        <h1>Trending Tech & Lifestyle Gear, Delivered Fast</h1>
        <p class="hero-subtext">
          Discover handpicked, high-quality products at direct-to-consumer prices. Enjoy seamless ordering and
          dependable tracking.
        </p>

        <div class="hero-actions">
          <NuxtLink to="/shop" class="btn-primary">Browse All Products</NuxtLink>
          <NuxtLink to="/shop?sort=popular" class="btn-secondary">Popular Items</NuxtLink>
        </div>
      </div>
    </section>

    <section class="categories-section">
      <div class="section-container">
        <div class="section-header">
          <h2>Shop by Category</h2>
          <NuxtLink to="/shop" class="see-all">View all &rarr;</NuxtLink>
        </div>

        <div v-if="loadingCategories" class="loading-wrap">
          <LoadingSpinner text="Loading categories..." />
        </div>

        <div v-else class="category-cards">
          <NuxtLink v-for="cat in categories" :key="cat.id" :to="`/shop?category=${cat.slug}`" class="cat-card">
            <h3>{{ cat.name }}</h3>
            <span class="cat-count">{{ cat.product_count }}</span>
          </NuxtLink>
        </div>
      </div>
    </section>

    <section class="featured-section">
      <div class="section-container">
        <div class="section-header">
          <h2>Featured Products</h2>
          <NuxtLink to="/shop?featured=true" class="see-all">See more &rarr;</NuxtLink>
        </div>

        <div v-if="loadingProducts" class="loading-wrap">
          <LoadingSpinner text="Fetching products..." />
        </div>

        <ProductGrid v-else-if="featuredProducts.length" :products="featuredProducts" />

        <EmptyState v-else title="No featured products yet." description="Check back soon for new arrival." />
      </div>
    </section>
  </div>
</template>

<style scoped>
.hero-section {
  background: linear-gradient(180deg, var(--bg-surface) 0%, var(--bg-page) 100%);
  border-bottom: 1px solid var(--border-color);
  padding: 5rem 1.5rem;
  text-align: center;
}

.hero-inner {
  max-width: 750px;
  margin: 0 auto;
}

.hero-badge {
  display: inline-block;
  background: var(--primary-light);
  color: var(--primary);
  font-weight: 700;
  font-size: 0.8rem;
  padding: 0.35rem 0.85rem;
  border-radius: 9999px;
  margin-bottom: 1.25rem;
  text-transform: uppercase;
  letter-spacing: 0.04em;
}

h1 {
  font-size: 2.75rem;
  font-weight: 800;
  line-height: 1.2;
  letter-spacing: -0.03em;
  margin-bottom: 1.25rem;
}

.hero-subtext {
  color: var(--text-muted);
  font-size: 1.1rem;
  line-height: 1.6;
  margin-bottom: 2rem;
}

.hero-actions {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 1rem;
  flex-wrap: wrap;
}

.btn-primary {
  background: var(--primary);
  color: #fff;
  font-weight: 700;
  font-size: 0.95rem;
  padding: 0.85rem 1.75rem;
  border-radius: var(--radius-md);
  transition: background 0.15s;
}

.btn-primary:hover {
  background: var(--primary-hover);
}

.btn-secondary {
  background: var(--bg-surface);
  border: 1px solid var(--border-color);
  color: var(--text-main);
  font-weight: 700;
  font-size: 0.95rem;
  padding: 0.85rem 1.75rem;
  border-radius: var(--radius-md);
  transition: all 0.15s;
}

.btn-secondary:hover {
  border-color: var(--text-main);
}

.section-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 3.5rem 1.5rem;
}

.section-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 1.75rem;
}

.section-header h2 {
  font-size: 1.6rem;
  font-weight: 800;
  letter-spacing: -0.02em;
}

.see-all {
  color: var(--primary);
  font-weight: 600;
  font-size: 0.9rem;
}

.category-cards {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
  gap: 1rem;
}

.cat-card {
  background: var(--bg-surface);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-md);
  padding: 1.5rem;
  transition: transform 0.15s, border-color 0.15s;
}

.cat-card:hover {
  transform: translateY(-2px);
  border-color: var(--primary);
}

.cat-card h3 {
  font-size: 1.05rem;
  font-weight: 700;
  margin-bottom: 0.25rem;
}

.cat-count {
  font-size: 0.85rem;
  color: var(--text-muted);
}

@media (max-width: 640px) {
  h1 {
    font-size: 2rem;
  }

  .hero-section {
    padding: 3rem 1.25rem;
  }
}
</style>