<!-- frontend/app/components/AppHeader.vue -->
<template>
  <header class="app-header-wrapper">
    <!-- Top Announcement Ticker (Storefront only) -->
    <PromoTopBar v-if="!isAdmin" />

    <div class="app-header" :class="{ 'admin-header-bar': isAdmin }">
      <div class="header-inner">
        <!-- Logo: directs admin to /admin and customers to / -->
        <NuxtLink :to="isAdmin ? '/admin' : '/'" class="logo" aria-label="DropShip Home">
          <div class="logo-mark">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.3">
              <path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"></path>
              <polyline points="3.27 6.96 12 12.01 20.73 6.96"></polyline>
              <line x1="12" y1="22.08" x2="12" y2="12"></line>
            </svg>
          </div>
          <span class="logo-text">
            <span class="logo-primary">Drop</span><span class="logo-accent">Ship</span>
          </span>
          <span v-if="isAdmin" class="admin-chip">Admin</span>
        </NuxtLink>

        <!-- Customer Search Bar (Hidden for Admins, visible on Desktop) -->
        <div v-if="!isAdmin" class="search-area desktop-only">
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
        <nav v-else class="nav-actions desktop-only">
          <NuxtLink to="/shop" class="nav-link" active-class="active-link">
            <span>Shop</span>
          </NuxtLink>
          <NuxtLink to="/track" class="nav-link" active-class="active-link">
            <span>Track Order</span>
          </NuxtLink>


          <!-- Customer Wishlist Link with Count Badge -->
          <NuxtLink to="/account/wishlist" class="action-icon-btn" aria-label="Wishlist">
            <div class="icon-wrap">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"></path>
              </svg>
              <span v-if="totalWishlist > 0" class="badge-count wishlist-badge">{{ totalWishlist }}</span>
            </div>
          </NuxtLink>

          <!-- Customer Cart Link with Dynamic Count Badge -->
          <NuxtLink to="/cart" class="action-icon-btn" aria-label="Cart">
            <div class="icon-wrap">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M6 2L3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4z"></path>
                <line x1="3" y1="6" x2="21" y2="6"></line>
                <path d="M16 10a4 4 0 0 1-8 0"></path>
              </svg>
              <span v-if="totalItems > 0" class="badge-count cart-badge">{{ totalItems }}</span>
            </div>
          </NuxtLink>

          <!-- User State -->
          <div v-if="!initialized" class="auth-loading">
            <span class="loading-dot"></span>
          </div>

          <div v-else-if="isAuthenticated" class="auth-user">
            <NuxtLink to="/account" class="user-pill-btn">
              <span class="user-avatar-small">{{ (user?.username || 'U')[0].toUpperCase() }}</span>
              <span class="user-name">Account</span>
            </NuxtLink>
            <button @click="logout" class="btn-logout" title="Sign out">
              <svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"></path>
                <polyline points="16 17 21 12 16 7"></polyline>
                <line x1="21" y1="12" x2="9" y2="12"></line>
              </svg>
            </button>
          </div>

          <div v-else class="auth-guest">
            <NuxtLink to="/login" class="btn-signin">Sign In</NuxtLink>
            <NuxtLink to="/register" class="btn-register">Get Started</NuxtLink>
          </div>
        </nav>

        <!-- Mobile Controls (Search Icon + Cart + Hamburger) -->
        <div v-if="!isAdmin" class="mobile-controls mobile-only">
          <NuxtLink to="/cart" class="action-icon-btn" aria-label="Cart">
            <div class="icon-wrap">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M6 2L3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4z"></path>
                <line x1="3" y1="6" x2="21" y2="6"></line>
                <path d="M16 10a4 4 0 0 1-8 0"></path>
              </svg>
              <span v-if="totalItems > 0" class="badge-count cart-badge">{{ totalItems }}</span>
            </div>
          </NuxtLink>

          <button @click="isMobileMenuOpen = !isMobileMenuOpen" class="btn-hamburger" aria-label="Toggle navigation">
            <svg v-if="!isMobileMenuOpen" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <line x1="3" y1="12" x2="21" y2="12"></line>
              <line x1="3" y1="6" x2="21" y2="6"></line>
              <line x1="3" y1="18" x2="21" y2="18"></line>
            </svg>
            <svg v-else width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <line x1="18" y1="6" x2="6" y2="18"></line>
              <line x1="6" y1="6" x2="18" y2="18"></line>
            </svg>
          </button>
        </div>
      </div>

      <!-- Mobile Search Row -->
      <div v-if="!isAdmin" class="mobile-search-row mobile-only">
        <SearchBar @search="onSearch" />
      </div>

      <!-- Mobile Slide-out Drawer Navigation -->
      <div v-if="!isAdmin && isMobileMenuOpen" class="mobile-drawer">
        <div class="mobile-drawer-links">
          <NuxtLink to="/shop" class="mobile-nav-item" @click="isMobileMenuOpen = false">
            <span class="m-icon"><i class="fa-solid fa-bag-shopping"></i></span>
            <span>Shop Catalog</span>
          </NuxtLink>
          <NuxtLink to="/shop?sort=popular" class="mobile-nav-item" @click="isMobileMenuOpen = false">
            <span class="m-icon"><i class="fa-solid fa-fire"></i></span>
            <span>Trending Deals</span>
          </NuxtLink>
          <NuxtLink to="/track" class="mobile-nav-item" @click="isMobileMenuOpen = false">
            <span class="m-icon"><i class="fa-solid fa-box-open"></i></span>
            <span>Track Order Status</span>
          </NuxtLink>
          <NuxtLink to="/account/wishlist" class="mobile-nav-item" @click="isMobileMenuOpen = false">
            <span class="m-icon"><i class="fa-solid fa-heart"></i></span>
            <span>Saved Wishlist ({{ totalWishlist }})</span>
          </NuxtLink>
        </div>

        <div class="mobile-drawer-footer">

          <div v-if="isAuthenticated" class="mobile-user-box">
            <NuxtLink to="/account" class="btn-mobile-account" @click="isMobileMenuOpen = false">
              My Profile & Orders
            </NuxtLink>
            <button @click="logout(); isMobileMenuOpen = false" class="btn-mobile-logout">
              Sign Out
            </button>
          </div>
          <div v-else class="mobile-auth-actions">
            <NuxtLink to="/login" class="btn-signin-mobile" @click="isMobileMenuOpen = false">
              Sign In
            </NuxtLink>
            <NuxtLink to="/register" class="btn-register-mobile" @click="isMobileMenuOpen = false">
              Create Account
            </NuxtLink>
          </div>
        </div>
      </div>
    </div>
  </header>
</template>

<script setup>
import PromoTopBar from '~/components/PromoTopBar.vue'

const { user, initialized, isAuthenticated, isAdmin, logout } = useAuthState()
const { totalItems } = useCartState()
const { totalWishlist, fetchWishlist } = useWishlist()

const isMobileMenuOpen = ref(false)

onMounted(() => {
  fetchWishlist()
})

function onSearch(query) {
  isMobileMenuOpen.value = false
  navigateTo({
    path: '/shop',
    query: query ? { search: query } : {}
  })
}
</script>

<style scoped>
.app-header-wrapper {
  position: sticky;
  top: 0;
  z-index: 50;
  width: 100%;
}

.app-header {
  background: rgba(255, 255, 255, 0.94);
  backdrop-filter: blur(14px);
  -webkit-backdrop-filter: blur(14px);
  border-bottom: 1px solid var(--border-color);
  box-shadow: 0 1px 3px 0 rgba(11, 15, 25, 0.03);
  transition: all var(--transition-fast);
}

.admin-header-bar {
  background: #0b0f19;
  border-bottom-color: #1e293b;
  color: #fff;
}

.header-inner {
  max-width: 1240px;
  margin: 0 auto;
  padding: 0.85rem 1.5rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1.5rem;
}

/* Logo */
.logo {
  display: flex;
  align-items: center;
  gap: 0.65rem;
  text-decoration: none;
}

.logo-mark {
  width: 36px;
  height: 36px;
  border-radius: var(--radius-sm);
  background: linear-gradient(135deg, #1d4ed8 0%, #2563eb 60%, #6366f1 100%);
  color: #ffffff;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 12px rgba(37, 99, 235, 0.28);
  transition: transform var(--transition-fast);
}

.logo:hover .logo-mark {
  transform: scale(1.05);
}

.logo-text {
  font-family: 'Outfit', 'Plus Jakarta Sans', sans-serif;
  font-size: 1.45rem;
  font-weight: 800;
  letter-spacing: -0.03em;
  color: var(--text-main);
  line-height: 1;
}

.logo-primary {
  color: var(--text-main);
}

.logo-accent {
  background: linear-gradient(135deg, #2563eb 0%, #6366f1 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.admin-chip {
  font-size: 0.7rem;
  font-weight: 700;
  text-transform: uppercase;
  background: #2563eb;
  color: #fff;
  padding: 0.2rem 0.5rem;
  border-radius: var(--radius-xs);
  letter-spacing: 0.05em;
  margin-left: 0.25rem;
}

.search-area {
  flex: 1;
  max-width: 440px;
}

/* Nav Actions */
.nav-actions {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.nav-link {
  font-weight: 600;
  font-size: 0.92rem;
  color: var(--text-body);
  padding: 0.5rem 0.75rem;
  border-radius: var(--radius-sm);
  transition: all var(--transition-fast);
}

.nav-link:hover {
  color: var(--primary);
  background: var(--primary-subtle);
}

.active-link {
  color: var(--primary) !important;
  font-weight: 700;
  background: var(--primary-subtle);
}

/* Action Icon Buttons */
.action-icon-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  border-radius: var(--radius-md);
  color: var(--text-body);
  background: var(--bg-surface);
  border: 1px solid var(--border-color);
  transition: all var(--transition-fast);
}

.action-icon-btn:hover {
  color: var(--primary);
  border-color: var(--border-hover);
  background: var(--bg-subtle);
  transform: translateY(-1px);
}

.icon-wrap {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
}

.badge-count {
  position: absolute;
  top: -8px;
  right: -8px;
  color: #ffffff;
  font-size: 0.68rem;
  font-weight: 800;
  min-width: 18px;
  height: 18px;
  border-radius: var(--radius-full);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0 4px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.15);
}

.cart-badge {
  background-color: var(--primary);
}

.wishlist-badge {
  background-color: #ef4444;
}

/* Auth User Pill */
.auth-user {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.user-pill-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.35rem 0.75rem 0.35rem 0.4rem;
  background: var(--bg-surface);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-full);
  transition: all var(--transition-fast);
}

.user-pill-btn:hover {
  border-color: var(--border-hover);
  background: var(--bg-subtle);
}

.user-avatar-small {
  width: 26px;
  height: 26px;
  border-radius: 50%;
  background: linear-gradient(135deg, #2563eb, #6366f1);
  color: #fff;
  font-size: 0.78rem;
  font-weight: 700;
  display: flex;
  align-items: center;
  justify-content: center;
}

.user-name {
  font-size: 0.85rem;
  font-weight: 600;
  color: var(--text-main);
}

.btn-logout {
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--text-muted);
  border-radius: var(--radius-md);
  border: 1px solid var(--border-color);
  transition: all var(--transition-fast);
}

.btn-logout:hover {
  color: #dc2626;
  background: #fee2e2;
  border-color: #fecaca;
}

/* Guest Buttons */
.auth-guest {
  display: flex;
  align-items: center;
  gap: 0.65rem;
}

.btn-signin {
  font-weight: 600;
  font-size: 0.88rem;
  color: var(--text-main);
  padding: 0.5rem 0.9rem;
  border-radius: var(--radius-sm);
  transition: all var(--transition-fast);
}

.btn-signin:hover {
  color: var(--primary);
  background: var(--bg-subtle);
}

.btn-register {
  background: linear-gradient(135deg, #1d4ed8 0%, #2563eb 100%);
  color: #ffffff;
  font-weight: 700;
  font-size: 0.88rem;
  padding: 0.55rem 1.15rem;
  border-radius: var(--radius-full);
  box-shadow: 0 4px 12px rgba(37, 99, 235, 0.25);
  transition: all var(--transition-fast);
}

.btn-register:hover {
  background: linear-gradient(135deg, #1e40af 0%, #1d4ed8 100%);
  box-shadow: 0 6px 16px rgba(37, 99, 235, 0.35);
  transform: translateY(-1px);
}

/* Admin Styles */
.admin-nav-actions {
  display: flex;
  align-items: center;
  gap: 0.85rem;
}

.admin-nav-link {
  font-size: 0.88rem;
  font-weight: 600;
  color: #94a3b8;
  padding: 0.4rem 0.75rem;
  border-radius: var(--radius-sm);
  transition: all 0.15s;
}

.admin-nav-link:hover {
  color: #fff;
  background: rgba(255, 255, 255, 0.08);
}

.active-admin-link {
  color: #fff !important;
  background: rgba(37, 99, 235, 0.35) !important;
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
  background: rgba(239, 68, 68, 0.12);
  padding: 0.4rem 0.85rem;
  border-radius: var(--radius-sm);
  transition: all 0.15s;
}

.btn-logout-admin:hover {
  background: rgba(239, 68, 68, 0.25);
}

/* Mobile Responsive */
.mobile-only {
  display: none;
}

.btn-hamburger {
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 1px solid var(--border-color);
  border-radius: var(--radius-md);
  color: var(--text-main);
  background: var(--bg-surface);
}

.mobile-search-row {
  padding: 0 1rem 0.75rem;
}

.mobile-drawer {
  background: #ffffff;
  border-top: 1px solid var(--border-color);
  padding: 1rem 1.25rem 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
  animation: slideDown 0.2s ease-out;
}

@keyframes slideDown {
  from { opacity: 0; transform: translateY(-8px); }
  to { opacity: 1; transform: translateY(0); }
}

.mobile-drawer-links {
  display: flex;
  flex-direction: column;
  gap: 0.45rem;
}

.mobile-nav-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem 0.85rem;
  border-radius: var(--radius-sm);
  font-weight: 600;
  font-size: 0.95rem;
  color: var(--text-main);
  background: var(--bg-page);
  border: 1px solid var(--border-color);
}

.mobile-drawer-footer {
  border-top: 1px solid var(--border-color);
  padding-top: 1rem;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}


.mobile-auth-actions {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 0.75rem;
}

.btn-signin-mobile {
  text-align: center;
  padding: 0.65rem;
  border: 1px solid var(--border-color);
  border-radius: var(--radius-sm);
  font-weight: 600;
  font-size: 0.9rem;
}

.btn-register-mobile {
  text-align: center;
  padding: 0.65rem;
  background: var(--primary);
  color: #fff;
  border-radius: var(--radius-sm);
  font-weight: 700;
  font-size: 0.9rem;
}

.mobile-user-box {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.btn-mobile-account {
  text-align: center;
  padding: 0.65rem;
  background: var(--bg-page);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-sm);
  font-weight: 600;
}

.btn-mobile-logout {
  text-align: center;
  padding: 0.5rem;
  color: #dc2626;
  font-weight: 600;
  font-size: 0.88rem;
}

@media (max-width: 860px) {
  .desktop-only {
    display: none !important;
  }
  .mobile-only {
    display: flex !important;
  }
  .mobile-controls {
    display: flex;
    align-items: center;
    gap: 0.5rem;
  }
}
</style>
