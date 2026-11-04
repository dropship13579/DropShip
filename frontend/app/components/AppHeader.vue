<!-- frontend/app/components/AppHeader.vue -->
<template>
  <div class="app-header" :class="{ 'admin-header-bar': isAdmin }">
    <div class="header-inner">
      <!-- Logo: directs admin to /admin and customers to / -->
      <NuxtLink :to="isAdmin ? '/admin' : '/'" class="logo">
        <span class="logo-accent">Drop</span>Ship
        <span v-if="isAdmin" class="admin-chip">Admin</span>
      </NuxtLink>

      <!-- Customer Search Bar (Hidden for Admins) -->
      <div v-if="!isAdmin" class="search-area">
        <SearchBar @search="onSearch" />
      </div>

      <!-- ADMIN NAVIGATION (Displayed only for Staff) -->
      <nav v-if="isAdmin" class="admin-nav-actions">
        <NuxtLink to="/admin" class="admin-nav-link" active-class="active-admin-link">
          Website Status & Analytics
        </NuxtLink>
        <NuxtLink to="/admin/products" class="admin-nav-link" active-class="active-admin-link">
          Product Inventory
        </NuxtLink>
        <NuxtLink to="/admin/orders" class="admin-nav-link" active-class="active-admin-link">
          Order Packaging & Tracking
        </NuxtLink>
        <NuxtLink to="/admin/suppliers" class="admin-nav-link" active-class="active-admin-link">
          Suppliers & Margins
        </NuxtLink>
        <div class="admin-user-pill">
          <span class="staff-tag">Staff</span>
          <span class="staff-name">{{ user?.username }}</span>
        </div>
        <button @click="logout" class="btn-logout-admin">Logout</button>
      </nav>

      <!-- CUSTOMER NAVIGATION (Displayed for Regular Users & Guests) -->
      <nav v-else class="nav-actions">
        <NuxtLink to="/shop" class="nav-link">Shop</NuxtLink>
        <NuxtLink to="/track" class="nav-link">Track Order</NuxtLink>
        <CurrencySelector />
        <!-- Customer Wishlist Link with Dynamic Count Badge -->
        <NuxtLink to="/account/wishlist" class="cart-link" aria-label="Wishlist">
          <div class="cart-icon-wrap">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path
                d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z">
              </path>
            </svg>
            <span v-if="totalWishlist > 0" class="cart-badge wishlist-badge">{{ totalWishlist }}</span>
          </div>
        </NuxtLink>
        <!-- Customer Cart Link with Dynamic Badge -->
        <NuxtLink to="/cart" class="cart-link" aria-label="Cart">
          <div class="cart-icon-wrap">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M6 2L3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4z"></path>
              <line x1="3" y1="6" x2="21" y2="6"></line>
              <path d="M16 10a4 4 0 0 1-8 0"></path>
            </svg>
            <span v-if="totalItems > 0" class="cart-badge">{{ totalItems }}</span>
          </div>
        </NuxtLink>

        <div v-if="!initialized" class="auth-loading">...</div>

        <div v-else-if="isAuthenticated" class="auth-user">
          <NuxtLink to="/account" class="user-link">
            <span class="user-name">Hi, {{ user?.username }}</span>
          </NuxtLink>
          <button @click="logout" class="btn-logout">Logout</button>
        </div>

        <div v-else class="auth-guest">
          <NuxtLink to="/login" class="btn-text">Sign In</NuxtLink>
          <NuxtLink to="/register" class="btn-register">Register</NuxtLink>
        </div>
      </nav>
    </div>
  </div>
</template>

<script setup>
const { user, initialized, isAuthenticated, isAdmin, logout } = useAuthState()
const { totalItems } = useCartState()
const { totalWishlist, fetchWishlist } = useWishlist()

onMounted(() => {
  fetchWishlist()
})

function onSearch(query) {
  navigateTo({
    path: '/shop',
    query: query ? { search: query } : {}
  })
}
</script>

<style scoped>
.app-header {
  position: sticky;
  top: 0;
  z-index: 50;
  background-color: var(--bg-surface);
  border-bottom: 1px solid var(--border-color);
  backdrop-filter: blur(8px);
}

.admin-header-bar {
  background: #0f172a;
  border-bottom-color: #1e293b;
  color: #fff;
}

.header-inner {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0.85rem 1.5rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1.5rem;
}

.logo {
  font-size: 1.35rem;
  font-weight: 800;
  letter-spacing: -0.03em;
  display: flex;
  align-items: center;
  gap: 0.4rem;
}

.logo-accent {
  color: var(--primary);
}

.admin-chip {
  font-size: 0.7rem;
  font-weight: 700;
  text-transform: uppercase;
  background: #2563eb;
  color: #fff;
  padding: 0.15rem 0.45rem;
  border-radius: 4px;
  letter-spacing: 0.05em;
}

.search-area {
  flex: 1;
  max-width: 440px;
}

/* Admin Nav Styles */
.admin-nav-actions {
  display: flex;
  align-items: center;
  gap: 1.25rem;
}

.admin-nav-link {
  font-size: 0.9rem;
  font-weight: 600;
  color: #94a3b8;
  padding: 0.4rem 0.75rem;
  border-radius: var(--radius-sm);
  transition: all 0.15s;
}

.admin-nav-link:hover {
  color: #fff;
  background: rgba(255, 255, 255, 0.06);
}

.active-admin-link {
  color: #fff !important;
  background: rgba(37, 99, 235, 0.3) !important;
}

.admin-user-pill {
  display: flex;
  align-items: center;
  gap: 0.4rem;
  background: #1e293b;
  padding: 0.3rem 0.65rem;
  border-radius: var(--radius-sm);
  font-size: 0.8rem;
}

.staff-tag {
  background: #334155;
  color: #94a3b8;
  padding: 0.1rem 0.35rem;
  border-radius: 3px;
  font-size: 0.7rem;
  font-weight: 700;
  text-transform: uppercase;
}

.staff-name {
  color: #f1f5f9;
  font-weight: 600;
}

.btn-logout-admin {
  font-size: 0.85rem;
  font-weight: 600;
  color: #f87171;
  background: rgba(239, 68, 68, 0.1);
  padding: 0.4rem 0.85rem;
  border-radius: var(--radius-sm);
  transition: all 0.15s;
}

.btn-logout-admin:hover {
  background: rgba(239, 68, 68, 0.2);
}

/* Customer Nav Styles */
.nav-actions {
  display: flex;
  align-items: center;
  gap: 1.25rem;
}

.nav-link {
  font-weight: 600;
  font-size: 0.95rem;
  color: var(--text-main);
  transition: color 0.15s;
}

.nav-link:hover {
  color: var(--primary);
}

.cart-link {
  display: flex;
  align-items: center;
  padding: 0.25rem;
  color: var(--text-main);
  transition: color 0.15s;
}

.cart-link:hover {
  color: var(--primary);
}

.cart-icon-wrap {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
}

.cart-badge {
  position: absolute;
  top: -8px;
  right: -8px;
  background-color: var(--primary);
  color: #ffffff;
  font-size: 0.7rem;
  font-weight: 700;
  min-width: 18px;
  height: 18px;
  border-radius: 9999px;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0 4px;
}

.auth-user {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.user-link {
  font-weight: 600;
  font-size: 0.9rem;
  color: var(--text-main);
}

.user-link:hover {
  color: var(--primary);
}

.btn-logout {
  font-size: 0.85rem;
  font-weight: 600;
  color: var(--text-muted);
  padding: 0.35rem 0.65rem;
  border-radius: var(--radius-sm);
  transition: all 0.15s;
}

.btn-logout:hover {
  color: #dc2626;
  background-color: #fee2e2;
}

.auth-guest {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.btn-text {
  font-weight: 600;
  font-size: 0.9rem;
  color: var(--text-main);
  padding: 0.4rem 0.65rem;
}

.btn-text:hover {
  color: var(--primary);
}

.btn-register {
  background: var(--primary);
  color: #ffffff;
  font-weight: 600;
  font-size: 0.9rem;
  padding: 0.45rem 0.95rem;
  border-radius: var(--radius-md);
  transition: background 0.15s;
}

.btn-register:hover {
  background: var(--primary-hover);
}

.wishlist-badge {
  background: #ef4444;
}


@media (max-width: 768px) {
  .header-inner {
    flex-wrap: wrap;
    gap: 0.75rem;
  }
}
</style>
