<!-- frontend/app/pages/admin/index.vue -->
<template>
    <div class="admin-page">
        <div class="admin-container">
            <!-- Header & Title -->
            <div class="admin-header">
                <div>
                    <div class="badge-tag">Command Center</div>
                    <h1>Website Status & Operational Analytics</h1>
                    <p class="subtitle">Complete real-time monitoring of site revenue, order lifecycle, and catalog
                        health.</p>
                </div>
                <button @click="refreshData" class="btn-refresh" :disabled="loading">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M23 4v6h-6"></path>
                        <path d="M1 20v-6h6"></path>
                        <path d="M3.51 9a9 9 0 0 1 14.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0 0 20.49 15"></path>
                    </svg>
                    <span>{{ loading ? 'Updating...' : 'Live Refresh' }}</span>
                </button>
            </div>

            <!-- Operational System Health Strip -->
            <div v-if="stats" class="system-health-strip">
                <div class="health-pill">
                    <span class="status-dot dot-green"></span>
                    <span>API Engine: <strong>{{ stats.system.api_status }}</strong></span>
                </div>
                <div class="health-pill">
                    <span class="status-dot dot-green"></span>
                    <span>Database: <strong>{{ stats.system.db_engine }}</strong></span>
                </div>
                <div class="health-pill">
                    <span class="status-dot dot-blue"></span>
                    <span>Framework: <strong>Django {{ stats.system.django_version }} &bull; Nuxt 4</strong></span>
                </div>
                <div class="health-pill time-pill">
                    <span>Server UTC: <strong>{{ stats.system.server_time }}</strong></span>
                </div>
            </div>

            <!-- Navigation Tabs (Only Admin Sections) -->
            <nav class="admin-tabs">
                <NuxtLink to="/admin" class="tab-item active">Website Status & Charts</NuxtLink>
                <NuxtLink to="/admin/products" class="tab-item">Product Inventory</NuxtLink>
            </nav>

            <!-- Loading Spinner -->
            <div v-if="loading && !stats" class="loading-wrap">
                <LoadingSpinner text="Compiling website telemetry..." />
            </div>

            <!-- Error Banner -->
            <div v-else-if="error" class="error-banner">
                {{ error }}
            </div>

            <!-- Dashboard Analytics Content -->
            <div v-else-if="stats" class="dashboard-content">
                <!-- 4 KPI High-Level Cards -->
                <section class="kpi-grid">
                    <div class="kpi-card">
                        <div class="kpi-top">
                            <span class="kpi-label">Gross Lifetime Revenue</span>
                            <div class="kpi-icon icon-revenue">
                                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor"
                                    stroke-width="2">
                                    <line x1="12" y1="1" x2="12" y2="23"></line>
                                    <path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"></path>
                                </svg>
                            </div>
                        </div>
                        <div class="kpi-value">${{ stats.revenue.total.toFixed(2) }}</div>
                        <div class="kpi-footer">
                            <span>Past 30 Days: <strong>${{ stats.revenue.monthly.toFixed(2) }}</strong></span>
                        </div>
                    </div>

                    <div class="kpi-card">
                        <div class="kpi-top">
                            <span class="kpi-label">Average Order Value (AOV)</span>
                            <div class="kpi-icon icon-aov">
                                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor"
                                    stroke-width="2">
                                    <polygon
                                        points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2">
                                    </polygon>
                                </svg>
                            </div>
                        </div>
                        <div class="kpi-value">${{ stats.revenue.aov.toFixed(2) }}</div>
                        <div class="kpi-footer">
                            <span>Across {{ stats.orders.valid }} fulfilled orders</span>
                        </div>
                    </div>

                    <div class="kpi-card">
                        <div class="kpi-top">
                            <span class="kpi-label">Customer Orders Volume</span>
                            <div class="kpi-icon icon-orders">
                                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor"
                                    stroke-width="2">
                                    <path d="M6 2L3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4z"></path>
                                    <line x1="3" y1="6" x2="21" y2="6"></line>
                                    <path d="M16 10a4 4 0 0 1-8 0"></path>
                                </svg>
                            </div>
                        </div>
                        <div class="kpi-value">{{ stats.orders.total }}</div>
                        <div class="kpi-footer">
                            <span>Active Orders in System</span>
                        </div>
                    </div>

                    <div class="kpi-card">
                        <div class="kpi-top">
                            <span class="kpi-label">Customer Accounts</span>
                            <div class="kpi-icon icon-customers">
                                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor"
                                    stroke-width="2">
                                    <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path>
                                    <circle cx="9" cy="7" r="4"></circle>
                                    <path d="M23 21v-2a4 4 0 0 0-3-3.87"></path>
                                    <path d="M16 3.13a4 4 0 0 1 0 7.75"></path>
                                </svg>
                            </div>
                        </div>
                        <div class="kpi-value">{{ stats.customers.total }}</div>
                        <div class="kpi-footer">
                            <span>Registered Buyer Profiles</span>
                        </div>
                    </div>
                </section>

                <!-- Charts Section 1: Revenue Velocity & Order Lifecycle -->
                <section class="charts-row">
                    <!-- CHART 1: 7-Day Revenue Trend -->
                    <div class="card chart-card">
                        <div class="card-header">
                            <div>
                                <h3>7-Day Sales & Revenue Velocity</h3>
                                <p class="card-subtitle">Daily dropship order volume</p>
                            </div>
                        </div>

                        <div class="chart-container">
                            <div class="chart-bars">
                                <div v-for="day in stats.daily_sales" :key="day.date" class="bar-column">
                                    <div class="bar-track">
                                        <div class="bar-fill" :style="{ height: getBarHeight(day.total) }">
                                            <span class="bar-tooltip">${{ day.total.toFixed(2) }}</span>
                                        </div>
                                    </div>
                                    <span class="bar-label">{{ day.date }}</span>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- CHART 2: Order Lifecycle & Status Distribution -->
                    <div class="card chart-card">
                        <div class="card-header">
                            <div>
                                <h3>Order Lifecycle Distribution</h3>
                                <p class="card-subtitle">Breakdown of orders by fulfillment stage</p>
                            </div>
                        </div>

                        <!-- Segmented Progress Bar -->
                        <div class="segmented-bar">
                            <div v-for="seg in stats.orders.distribution" :key="seg.status" v-show="seg.count > 0"
                                class="segment" :style="{ width: `${seg.pct}%`, backgroundColor: seg.color }"
                                :title="`${seg.label}: ${seg.count} (${seg.pct}%)`"></div>
                        </div>

                        <!-- Status Legend & Metrics -->
                        <div class="status-legend-grid">
                            <div v-for="item in stats.orders.distribution" :key="item.status" class="legend-item">
                                <div class="legend-color-dot" :style="{ backgroundColor: item.color }"></div>
                                <div class="legend-label-group">
                                    <span class="legend-name">{{ item.label }}</span>
                                    <strong class="legend-count">{{ item.count }} ({{ item.pct }}%)</strong>
                                </div>
                            </div>
                        </div>
                    </div>
                </section>

                <!-- Charts Section 2: Inventory Health & Category Share -->
                <section class="charts-row">
                    <!-- CHART 3: Stock Health Distribution -->
                    <div class="card chart-card">
                        <div class="card-header space-between">
                            <div>
                                <h3>Catalog Stock Health</h3>
                                <p class="card-subtitle">{{ stats.inventory.total_products }} Total Store SKUs</p>
                            </div>
                            <NuxtLink to="/admin/products" class="link-manage">Manage Stock &rarr;</NuxtLink>
                        </div>

                        <div class="inventory-meter-container">
                            <!-- In Stock Meter -->
                            <div class="meter-item">
                                <div class="meter-header">
                                    <span class="meter-title">Healthy In-Stock (> 5 units)</span>
                                    <strong class="meter-val text-green">{{ stats.inventory.in_stock }} SKUs ({{
                                        stats.inventory.in_stock_pct }}%)</strong>
                                </div>
                                <div class="meter-track">
                                    <div class="meter-fill fill-green"
                                        :style="{ width: `${stats.inventory.in_stock_pct}%` }"></div>
                                </div>
                            </div>

                            <!-- Low Stock Meter -->
                            <div class="meter-item">
                                <div class="meter-header">
                                    <span class="meter-title">Low Stock Warning (&le; 5 units)</span>
                                    <strong class="meter-val text-amber">{{ stats.inventory.low_stock }} SKUs ({{
                                        stats.inventory.low_stock_pct }}%)</strong>
                                </div>
                                <div class="meter-track">
                                    <div class="meter-fill fill-amber"
                                        :style="{ width: `${stats.inventory.low_stock_pct}%` }"></div>
                                </div>
                            </div>

                            <!-- Out of Stock Meter -->
                            <div class="meter-item">
                                <div class="meter-header">
                                    <span class="meter-title">Out of Stock (0 units)</span>
                                    <strong class="meter-val text-red">{{ stats.inventory.out_of_stock }} SKUs ({{
                                        stats.inventory.out_of_stock_pct }}%)</strong>
                                </div>
                                <div class="meter-track">
                                    <div class="meter-fill fill-red"
                                        :style="{ width: `${stats.inventory.out_of_stock_pct}%` }"></div>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- CHART 4: Category Distribution Breakdown -->
                    <div class="card chart-card">
                        <div class="card-header">
                            <div>
                                <h3>Catalog Category Balance</h3>
                                <p class="card-subtitle">Product allocation across categories</p>
                            </div>
                        </div>

                        <div class="categories-list">
                            <div v-for="cat in stats.categories" :key="cat.id" class="category-stat-row">
                                <div class="cat-stat-info">
                                    <span class="cat-stat-name">{{ cat.name }}</span>
                                    <span class="cat-stat-count">{{ cat.count }} products ({{ cat.pct }}%)</span>
                                </div>
                                <div class="cat-stat-track">
                                    <div class="cat-stat-fill" :style="{ width: `${cat.pct}%` }"></div>
                                </div>
                            </div>
                        </div>
                    </div>
                </section>
            </div>
        </div>
    </div>
</template>

<script setup>
definePageMeta({
    middleware: 'admin'
})

const { getStats } = useAdminApi()

const stats = ref(null)
const loading = ref(true)
const error = ref('')

async function refreshData() {
    loading.value = true
    error.value = ''
    try {
        const data = await getStats()
        stats.value = data
    } catch (err) {
        error.value = err.message || 'Unable to retrieve dashboard statistics.'
    } finally {
        loading.value = false
    }
}

function getBarHeight(dayTotal) {
    if (!stats.value?.daily_sales) return '5%'
    const maxVal = Math.max(...stats.value.daily_sales.map(d => d.total), 1)
    const pct = Math.max(8, (dayTotal / maxVal) * 100)
    return `${pct}%`
}

onMounted(() => {
    refreshData()
})
</script>

<style scoped>
.admin-page {
    padding: 2.5rem 1.5rem 5rem;
    max-width: 1200px;
    margin: 0 auto;
}

.badge-tag {
    display: inline-block;
    font-size: 0.75rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    background: #0f172a;
    color: #fff;
    padding: 0.2rem 0.5rem;
    border-radius: var(--radius-sm);
    margin-bottom: 0.5rem;
}

.admin-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    flex-wrap: wrap;
    gap: 1.5rem;
    margin-bottom: 1.5rem;
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

.btn-refresh {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    background: var(--bg-surface);
    border: 1px solid var(--border-color);
    padding: 0.6rem 1.25rem;
    border-radius: var(--radius-md);
    font-size: 0.9rem;
    font-weight: 600;
    color: var(--text-main);
    box-shadow: var(--shadow-sm);
    transition: all 0.15s;
}

.btn-refresh:hover:not(:disabled) {
    background: #f8fafc;
    border-color: #cbd5e1;
}

/* System Health Strip */
.system-health-strip {
    display: flex;
    flex-wrap: wrap;
    gap: 0.85rem;
    background: #f8fafc;
    border: 1px solid var(--border-color);
    border-radius: var(--radius-md);
    padding: 0.75rem 1rem;
    margin-bottom: 1.5rem;
    font-size: 0.85rem;
}

.health-pill {
    display: flex;
    align-items: center;
    gap: 0.45rem;
    color: var(--text-muted);
}

.time-pill {
    margin-left: auto;
}

.status-dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
}

.dot-green {
    background: #16a34a;
    box-shadow: 0 0 0 2px rgba(22, 163, 74, 0.2);
}

.dot-blue {
    background: #2563eb;
}

/* Tabs */
.admin-tabs {
    display: flex;
    gap: 0.5rem;
    border-bottom: 2px solid var(--border-color);
    margin-bottom: 2rem;
}

.tab-item {
    font-size: 0.95rem;
    font-weight: 600;
    color: var(--text-muted);
    padding: 0.75rem 1.25rem;
    border-bottom: 2px solid transparent;
    margin-bottom: -2px;
    transition: all 0.15s;
}

.tab-item:hover {
    color: var(--text-main);
}

.tab-item.active {
    color: var(--primary);
    border-bottom-color: var(--primary);
}

/* Loading & Error */
.loading-wrap {
    padding: 6rem 0;
}

.error-banner {
    background: #fef2f2;
    border: 1px solid #fecaca;
    color: #dc2626;
    padding: 1.25rem;
    border-radius: var(--radius-md);
    font-weight: 500;
}

/* KPI Grid */
.kpi-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(230px, 1fr));
    gap: 1.25rem;
    margin-bottom: 1.75rem;
}

.kpi-card {
    background: var(--bg-surface);
    border: 1px solid var(--border-color);
    border-radius: var(--radius-lg);
    padding: 1.35rem;
    box-shadow: var(--shadow-sm);
    transition: transform 0.15s;
}

.kpi-card:hover {
    transform: translateY(-2px);
}

.kpi-top {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 0.65rem;
}

.kpi-label {
    font-size: 0.8rem;
    font-weight: 700;
    color: var(--text-muted);
    text-transform: uppercase;
    letter-spacing: 0.04em;
}

.kpi-icon {
    width: 34px;
    height: 34px;
    border-radius: var(--radius-md);
    display: flex;
    align-items: center;
    justify-content: center;
}

.icon-revenue {
    background: #eff6ff;
    color: #2563eb;
}

.icon-aov {
    background: #fef3c7;
    color: #d97706;
}

.icon-orders {
    background: #f3e8ff;
    color: #9333ea;
}

.icon-customers {
    background: #f0fdf4;
    color: #16a34a;
}

.kpi-value {
    font-size: 1.85rem;
    font-weight: 800;
    letter-spacing: -0.02em;
    color: var(--text-main);
    margin-bottom: 0.35rem;
}

.kpi-footer {
    font-size: 0.8rem;
    color: var(--text-muted);
}

/* Charts Grid */
.charts-row {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 1.5rem;
    margin-bottom: 1.75rem;
}

.card {
    background: var(--bg-surface);
    border: 1px solid var(--border-color);
    border-radius: var(--radius-lg);
    padding: 1.5rem;
    box-shadow: var(--shadow-sm);
}

.card-header {
    margin-bottom: 1.25rem;
}

.card-header.space-between {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.card-header h3 {
    font-size: 1.1rem;
    font-weight: 700;
    color: var(--text-main);
}

.card-subtitle {
    font-size: 0.85rem;
    color: var(--text-muted);
    margin-top: 0.15rem;
}

.link-manage {
    font-size: 0.85rem;
    font-weight: 600;
    color: var(--primary);
}

.link-manage:hover {
    text-decoration: underline;
}

/* Chart 1: Revenue Bars */
.chart-container {
    height: 180px;
    padding-top: 0.5rem;
}

.chart-bars {
    display: flex;
    align-items: flex-end;
    justify-content: space-between;
    height: 140px;
    gap: 0.75rem;
}

.bar-column {
    flex: 1;
    display: flex;
    flex-direction: column;
    align-items: center;
    height: 100%;
}

.bar-track {
    flex: 1;
    width: 100%;
    max-width: 40px;
    display: flex;
    align-items: flex-end;
    background: #f8fafc;
    border-radius: var(--radius-sm);
    overflow: hidden;
}

.bar-fill {
    width: 100%;
    background: linear-gradient(180deg, #3b82f6 0%, #1d4ed8 100%);
    border-radius: var(--radius-sm) var(--radius-sm) 0 0;
    position: relative;
    transition: height 0.3s ease;
    cursor: pointer;
}

.bar-fill:hover {
    background: #1d4ed8;
}

.bar-tooltip {
    display: none;
    position: absolute;
    top: -24px;
    left: 50%;
    transform: translateX(-50%);
    background: #0f172a;
    color: #fff;
    font-size: 0.7rem;
    font-weight: 700;
    padding: 0.15rem 0.35rem;
    border-radius: 4px;
    white-space: nowrap;
}

.bar-fill:hover .bar-tooltip {
    display: block;
}

.bar-label {
    font-size: 0.75rem;
    color: var(--text-muted);
    margin-top: 0.5rem;
    font-weight: 600;
}

/* Chart 2: Segmented Bar & Legend */
.segmented-bar {
    height: 18px;
    background: #f1f5f9;
    border-radius: 999px;
    overflow: hidden;
    display: flex;
    margin-bottom: 1.5rem;
}

.segment {
    height: 100%;
    transition: width 0.3s ease;
}

.status-legend-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 0.85rem;
}

.legend-item {
    display: flex;
    align-items: center;
    gap: 0.6rem;
}

.legend-color-dot {
    width: 10px;
    height: 10px;
    border-radius: 50%;
    flex-shrink: 0;
}

.legend-label-group {
    display: flex;
    justify-content: space-between;
    width: 100%;
    font-size: 0.85rem;
}

.legend-name {
    color: var(--text-muted);
}

.legend-count {
    color: var(--text-main);
}

/* Chart 3: Inventory Meters */
.inventory-meter-container {
    display: flex;
    flex-direction: column;
    gap: 1.25rem;
}

.meter-header {
    display: flex;
    justify-content: space-between;
    font-size: 0.85rem;
    margin-bottom: 0.35rem;
}

.meter-title {
    color: var(--text-muted);
}

.meter-track {
    height: 10px;
    background: #f1f5f9;
    border-radius: 999px;
    overflow: hidden;
}

.meter-fill {
    height: 100%;
    border-radius: 999px;
    transition: width 0.3s ease;
}

.fill-green {
    background: #16a34a;
}

.fill-amber {
    background: #f59e0b;
}

.fill-red {
    background: #ef4444;
}

.text-green {
    color: #16a34a;
}

.text-amber {
    color: #d97706;
}

.text-red {
    color: #ef4444;
}

/* Chart 4: Categories List */
.categories-list {
    display: flex;
    flex-direction: column;
    gap: 1rem;
}

.cat-stat-info {
    display: flex;
    justify-content: space-between;
    font-size: 0.85rem;
    margin-bottom: 0.35rem;
}

.cat-stat-name {
    font-weight: 600;
    color: var(--text-main);
}

.cat-stat-count {
    color: var(--text-muted);
}

.cat-stat-track {
    height: 8px;
    background: #f1f5f9;
    border-radius: 999px;
    overflow: hidden;
}

.cat-stat-fill {
    height: 100%;
    background: var(--primary);
    border-radius: 999px;
    transition: width 0.3s ease;
}

@media (max-width: 900px) {
    .charts-row {
        grid-template-columns: 1fr;
    }

    .time-pill {
        margin-left: 0;
    }
}
</style>
