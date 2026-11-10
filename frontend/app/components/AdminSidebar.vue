<!-- frontend/app/components/AdminSidebar.vue -->
<script setup>
const props = defineProps({
  isMobileOpen: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['close'])

const route = useRoute()
const { user, logout } = useAuthState()
const { getSupportTickets } = useAdminApi()

const openTickets = ref(0)

// Quick fetch open ticket count for live badge
onMounted(async () => {
  try {
    const res = await getSupportTickets({ status: 'open' })
    if (res?.count !== undefined) {
      openTickets.value = res.count
    } else if (Array.isArray(res?.results)) {
      openTickets.value = res.results.length
    }
  } catch (e) {
    // Silent fallback
  }
})

function handleLinkClick() {
  emit('close')
}
</script>

<template>
  <aside class="admin-sidebar" :class="{ 'mobile-open': isMobileOpen }">
    <!-- Sidebar Header / Branding -->
    <div class="sidebar-header">
      <NuxtLink to="/admin" class="brand-link" @click="handleLinkClick">
        <div class="brand-logo-wrap">
          <img src="/images/logo.png" alt="KyroKart Logo" class="brand-logo-img" />
        </div>
        <span class="admin-badge">Admin</span>
      </NuxtLink>

      <button
        type="button"
        class="btn-close-drawer"
        @click="$emit('close')"
        aria-label="Close sidebar menu"
      >
        <i class="fa-solid fa-xmark"></i>
      </button>
    </div>

    <!-- Navigation Scroll Area -->
    <div class="sidebar-scrollable">
      <!-- Section: Core Operations -->
      <div class="nav-group">
        <div class="nav-group-title">Command Center</div>
        <nav class="nav-items">
          <NuxtLink
            to="/admin"
            class="sidebar-nav-item"
            :class="{ active: route.path === '/admin' }"
            @click="handleLinkClick"
          >
            <span class="item-icon"><i class="fa-solid fa-chart-line"></i></span>
            <span class="item-label">Website Status</span>
          </NuxtLink>

          <NuxtLink
            to="/admin/products"
            class="sidebar-nav-item"
            :class="{ active: route.path.startsWith('/admin/products') }"
            @click="handleLinkClick"
          >
            <span class="item-icon"><i class="fa-solid fa-boxes-stacked"></i></span>
            <span class="item-label">Product Inventory</span>
          </NuxtLink>

          <NuxtLink
            to="/admin/orders"
            class="sidebar-nav-item"
            :class="{ active: route.path.startsWith('/admin/orders') }"
            @click="handleLinkClick"
          >
            <span class="item-icon"><i class="fa-solid fa-truck-fast"></i></span>
            <span class="item-label">Order Packaging</span>
          </NuxtLink>

          <NuxtLink
            to="/admin/support"
            class="sidebar-nav-item"
            :class="{ active: route.path.startsWith('/admin/support') }"
            @click="handleLinkClick"
          >
            <span class="item-icon"><i class="fa-solid fa-headset"></i></span>
            <span class="item-label">Customer Inquiries</span>
            <span v-if="openTickets > 0" class="badge-alert">{{ openTickets }}</span>
          </NuxtLink>
        </nav>
      </div>

      <!-- Section: Storefront Shortcut -->
      <div class="nav-group">
        <div class="nav-group-title">Live Storefront</div>
        <nav class="nav-items">
          <NuxtLink to="/" target="_blank" class="sidebar-nav-item external-link">
            <span class="item-icon"><i class="fa-solid fa-store"></i></span>
            <span class="item-label">View Live Store</span>
            <span class="ext-icon"><i class="fa-solid fa-arrow-up-right-from-square"></i></span>
          </NuxtLink>

          <NuxtLink to="/track" target="_blank" class="sidebar-nav-item external-link">
            <span class="item-icon"><i class="fa-solid fa-location-crosshairs"></i></span>
            <span class="item-label">Customer Tracking</span>
            <span class="ext-icon"><i class="fa-solid fa-arrow-up-right-from-square"></i></span>
          </NuxtLink>
        </nav>
      </div>
    </div>

    <!-- Sidebar Footer / Staff Profile -->
    <div class="sidebar-footer">
      <div class="user-card">
        <div class="user-avatar-circle">
          {{ (user?.username || 'A')[0].toUpperCase() }}
        </div>
        <div class="user-details">
          <span class="user-display-name">{{ user?.username || 'Admin Staff' }}</span>
          <span class="user-role-label">Administrator</span>
        </div>
      </div>

      <button
        type="button"
        @click="logout"
        class="btn-sidebar-logout"
        title="Sign out of Admin Session"
      >
        <i class="fa-solid fa-right-from-bracket"></i>
      </button>
    </div>
  </aside>
</template>

<style scoped>
.admin-sidebar {
  width: 260px;
  min-width: 260px;
  height: 100vh;
  position: sticky;
  top: 0;
  left: 0;
  background: #0b1120;
  border-right: 1px solid #1e293b;
  display: flex;
  flex-direction: column;
  z-index: 1050;
  color: #f1f5f9;
  user-select: none;
  transition: transform 0.25s cubic-bezier(0.16, 1, 0.3, 1);
}

/* Header */
.sidebar-header {
  height: 68px;
  padding: 0 1.25rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
  border-bottom: 1px solid #1e293b;
  background: #0b1120;
}

.brand-link {
  display: flex;
  align-items: center;
  gap: 0.65rem;
  text-decoration: none;
}

.brand-logo-wrap {
  background: #ffffff;
  padding: 0.3rem 0.55rem;
  border-radius: var(--radius-sm);
  display: flex;
  align-items: center;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.3);
}

.brand-logo-img {
  height: 24px;
  width: auto;
  max-width: 100px;
  object-fit: contain;
}

.admin-badge {
  font-size: 0.65rem;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
  color: #ffffff;
  padding: 0.2rem 0.5rem;
  border-radius: var(--radius-xs);
  box-shadow: 0 2px 8px rgba(37, 99, 235, 0.3);
}

.btn-close-drawer {
  display: none;
  background: transparent;
  border: 1px solid #334155;
  color: #94a3b8;
  width: 32px;
  height: 32px;
  border-radius: var(--radius-sm);
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.15s;
}

.btn-close-drawer:hover {
  color: #ffffff;
  border-color: #64748b;
  background: #1e293b;
}

/* Scroll Area */
.sidebar-scrollable {
  flex: 1;
  overflow-y: auto;
  padding: 1.25rem 0.85rem;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.sidebar-scrollable::-webkit-scrollbar {
  width: 5px;
}

.sidebar-scrollable::-webkit-scrollbar-thumb {
  background: #1e293b;
  border-radius: 999px;
}

/* Nav Groups */
.nav-group-title {
  font-size: 0.68rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: #64748b;
  padding: 0 0.65rem 0.5rem;
}

.nav-items {
  display: flex;
  flex-direction: column;
  gap: 0.3rem;
}

.sidebar-nav-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.68rem 0.85rem;
  border-radius: var(--radius-md);
  color: #94a3b8;
  font-size: 0.88rem;
  font-weight: 600;
  text-decoration: none;
  transition: all 0.15s ease;
  position: relative;
}

.item-icon {
  width: 20px;
  font-size: 0.95rem;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #64748b;
  transition: color 0.15s;
}

.item-label {
  flex: 1;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.ext-icon {
  font-size: 0.7rem;
  color: #475569;
  transition: transform 0.15s;
}

.sidebar-nav-item:hover {
  color: #ffffff;
  background: #1e293b;
}

.sidebar-nav-item:hover .item-icon {
  color: #60a5fa;
}

.sidebar-nav-item:hover .ext-icon {
  transform: translate(2px, -2px);
  color: #94a3b8;
}

/* Active State */
.sidebar-nav-item.active {
  color: #ffffff;
  background: linear-gradient(90deg, rgba(37, 99, 235, 0.22) 0%, rgba(37, 99, 235, 0.06) 100%);
  border-left: 3px solid #3b82f6;
  padding-left: calc(0.85rem - 3px);
  font-weight: 700;
}

.sidebar-nav-item.active .item-icon {
  color: #60a5fa;
}

/* Alert Badge */
.badge-alert {
  background: #ef4444;
  color: #ffffff;
  font-size: 0.7rem;
  font-weight: 800;
  padding: 0.15rem 0.45rem;
  border-radius: 999px;
  box-shadow: 0 2px 6px rgba(239, 68, 68, 0.4);
}

/* Footer / Staff Profile */
.sidebar-footer {
  padding: 0.85rem 1rem;
  background: #080d19;
  border-top: 1px solid #1e293b;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 0.5rem;
}

.user-card {
  display: flex;
  align-items: center;
  gap: 0.65rem;
  overflow: hidden;
}

.user-avatar-circle {
  width: 34px;
  height: 34px;
  min-width: 34px;
  border-radius: 50%;
  background: linear-gradient(135deg, #2563eb, #6366f1);
  color: #ffffff;
  font-weight: 700;
  font-size: 0.88rem;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 2px 6px rgba(37, 99, 235, 0.3);
}

.user-details {
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.user-display-name {
  font-size: 0.82rem;
  font-weight: 700;
  color: #f1f5f9;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.user-role-label {
  font-size: 0.68rem;
  color: #64748b;
  font-weight: 500;
}

.btn-sidebar-logout {
  width: 32px;
  height: 32px;
  min-width: 32px;
  background: transparent;
  border: 1px solid #334155;
  border-radius: var(--radius-sm);
  color: #94a3b8;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.15s ease;
  font-size: 0.85rem;
}

.btn-sidebar-logout:hover {
  background: #fee2e2;
  border-color: #fecaca;
  color: #dc2626;
}

/* Responsive Drawer on Tablet/Mobile */
@media (max-width: 1024px) {
  .admin-sidebar {
    position: fixed;
    top: 0;
    left: 0;
    bottom: 0;
    transform: translateX(-100%);
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
  }

  .admin-sidebar.mobile-open {
    transform: translateX(0);
  }

  .btn-close-drawer {
    display: inline-flex;
  }
}
</style>

