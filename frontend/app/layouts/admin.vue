<!-- frontend/app/layouts/admin.vue -->
<script setup>
import AdminSidebar from '~/components/AdminSidebar.vue'

const route = useRoute()
const { user, logout } = useAuthState()

const isMobileSidebarOpen = ref(false)

// Close mobile sidebar on route change
watch(
  () => route.fullPath,
  () => {
    isMobileSidebarOpen.value = false
  }
)

const currentSectionTitle = computed(() => {
  if (route.path.startsWith('/admin/products')) return 'Product Inventory'
  if (route.path.startsWith('/admin/orders')) return 'Order Packaging & Tracking'
  if (route.path.startsWith('/admin/support')) return 'Customer Inquiries'
  return 'Website Status & Analytics'
})
</script>

<template>
  <div class="admin-layout">
    <!-- Backdrop overlay for mobile drawer -->
    <transition name="fade">
      <div
        v-if="isMobileSidebarOpen"
        class="sidebar-backdrop"
        @click="isMobileSidebarOpen = false"
      />
    </transition>

    <!-- Admin Sidebar -->
    <AdminSidebar
      :is-mobile-open="isMobileSidebarOpen"
      @close="isMobileSidebarOpen = false"
    />

    <!-- Main Viewport -->
    <div class="admin-main-viewport">
      <!-- Admin Topbar -->
      <header class="admin-topbar">
        <div class="topbar-left">
          <button
            type="button"
            class="btn-hamburger"
            @click="isMobileSidebarOpen = !isMobileSidebarOpen"
            aria-label="Toggle navigation menu"
          >
            <i class="fa-solid fa-bars"></i>
          </button>

          <nav class="topbar-breadcrumb" aria-label="Admin breadcrumb">
            <NuxtLink to="/admin" class="bc-root">
              <i class="fa-solid fa-gauge-high"></i>
              <span>Admin Console</span>
            </NuxtLink>
            <span class="bc-sep">/</span>
            <span class="bc-current">{{ currentSectionTitle }}</span>
          </nav>
        </div>

        <div class="topbar-right">
          <!-- View Storefront -->
          <NuxtLink to="/" target="_blank" class="btn-topbar-store" title="Preview customer store in new tab">
            <i class="fa-solid fa-store"></i>
            <span class="store-label">Live Store</span>
            <i class="fa-solid fa-arrow-up-right-from-square ext-arrow"></i>
          </NuxtLink>

          <!-- Staff User Pill -->
          <div class="topbar-user-pill">
            <span class="staff-badge">Staff</span>
            <span class="staff-name">{{ user?.username || 'Admin' }}</span>
          </div>

          <!-- Sign Out -->
          <button
            type="button"
            @click="logout"
            class="btn-topbar-logout"
            title="Sign out of Admin Session"
          >
            <i class="fa-solid fa-right-from-bracket"></i>
            <span class="logout-label">Logout</span>
          </button>
        </div>
      </header>

      <!-- Main Admin Page Content -->
      <main class="admin-content-stage">
        <slot />
      </main>
    </div>
  </div>
</template>

<style scoped>
.admin-layout {
  display: flex;
  min-height: 100vh;
  background: var(--bg-page);
  position: relative;
}

/* Backdrop */
.sidebar-backdrop {
  position: fixed;
  inset: 0;
  background: rgba(11, 15, 25, 0.6);
  backdrop-filter: blur(3px);
  z-index: 1040;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* Main Viewport */
.admin-main-viewport {
  flex: 1;
  display: flex;
  flex-direction: column;
  min-width: 0;
}

/* Topbar */
.admin-topbar {
  height: 68px;
  background: #ffffff;
  border-bottom: 1px solid var(--border-color);
  padding: 0 2rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
  position: sticky;
  top: 0;
  z-index: 1000;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.03);
}

.topbar-left {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.btn-hamburger {
  display: none;
  background: transparent;
  border: 1px solid var(--border-color);
  color: var(--text-body);
  width: 36px;
  height: 36px;
  border-radius: var(--radius-sm);
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.15s;
  font-size: 1rem;
}

.btn-hamburger:hover {
  background: var(--bg-subtle);
  border-color: var(--border-hover);
  color: var(--primary);
}

.topbar-breadcrumb {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.88rem;
}

.bc-root {
  display: inline-flex;
  align-items: center;
  gap: 0.45rem;
  color: var(--text-muted);
  text-decoration: none;
  font-weight: 600;
  transition: color 0.15s;
}

.bc-root:hover {
  color: var(--primary);
}

.bc-sep {
  color: var(--border-hover);
  font-size: 0.8rem;
}

.bc-current {
  color: var(--text-main);
  font-weight: 700;
}

/* Topbar Right Actions */
.topbar-right {
  display: flex;
  align-items: center;
  gap: 0.85rem;
}

.btn-topbar-store {
  display: inline-flex;
  align-items: center;
  gap: 0.45rem;
  padding: 0.45rem 0.85rem;
  background: #f8fafc;
  border: 1px solid var(--border-color);
  border-radius: var(--radius-md);
  color: var(--text-body);
  font-size: 0.82rem;
  font-weight: 600;
  text-decoration: none;
  transition: all 0.15s;
}

.btn-topbar-store:hover {
  background: #eff6ff;
  border-color: #93c5fd;
  color: var(--primary);
}

.ext-arrow {
  font-size: 0.7rem;
  opacity: 0.7;
}

.topbar-user-pill {
  display: inline-flex;
  align-items: center;
  gap: 0.45rem;
  background: #f1f5f9;
  border: 1px solid var(--border-color);
  padding: 0.35rem 0.75rem;
  border-radius: var(--radius-full);
}

.staff-badge {
  background: #2563eb;
  color: #ffffff;
  font-size: 0.65rem;
  font-weight: 800;
  text-transform: uppercase;
  padding: 0.15rem 0.45rem;
  border-radius: var(--radius-xs);
  letter-spacing: 0.04em;
}

.staff-name {
  font-size: 0.82rem;
  font-weight: 700;
  color: var(--text-main);
}

.btn-topbar-logout {
  display: inline-flex;
  align-items: center;
  gap: 0.45rem;
  padding: 0.45rem 0.85rem;
  background: #ffffff;
  border: 1px solid var(--border-color);
  border-radius: var(--radius-md);
  color: var(--text-muted);
  font-size: 0.82rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.15s;
}

.btn-topbar-logout:hover {
  background: #fee2e2;
  border-color: #fecaca;
  color: #dc2626;
}

/* Page Content Stage */
.admin-content-stage {
  flex: 1;
  width: 100%;
}

@media (max-width: 1024px) {
  .btn-hamburger {
    display: inline-flex;
  }

  .admin-topbar {
    padding: 0 1rem;
  }

  .store-label,
  .logout-label {
    display: none;
  }

  .btn-topbar-logout,
  .btn-topbar-store {
    padding: 0.45rem 0.65rem;
  }
}
</style>

