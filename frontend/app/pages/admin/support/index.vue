<!-- frontend/app/pages/admin/support/index.vue -->
<template>
  <div class="admin-support-page">
    <div class="workstation-container">
      <!-- Header -->
      <div class="header-section">
        <div>
          <span class="badge-staff">Support Desk</span>
          <h1>Customer Inquiries & Support Tickets</h1>
          <p class="subtitle">Review, track, and resolve customer messages, product questions, and return requests.</p>
        </div>

        <div class="header-actions">
          <button @click="loadTickets" class="btn-refresh" :disabled="loading">
            <i class="fa-solid fa-arrows-rotate" :class="{ 'fa-spin': loading }"></i>
            <span>{{ loading ? 'Syncing...' : 'Refresh Feed' }}</span>
          </button>
        </div>
      </div>

      <!-- Quick Metrics Filter Ribbon -->
      <div class="metrics-ribbon">
        <div class="metric-chip" :class="{ active: currentStatus === '' }" @click="setStatusFilter('')">
          <span class="chip-label">All Inquiries</span>
          <span class="chip-count">{{ counts.all }}</span>
        </div>
        <div class="metric-chip open-chip" :class="{ active: currentStatus === 'open' }" @click="setStatusFilter('open')">
          <span class="chip-label">Awaiting Reply</span>
          <span class="chip-count">{{ counts.open }}</span>
        </div>
        <div class="metric-chip progress-chip" :class="{ active: currentStatus === 'in_progress' }" @click="setStatusFilter('in_progress')">
          <span class="chip-label">In Progress</span>
          <span class="chip-count">{{ counts.in_progress }}</span>
        </div>
        <div class="metric-chip resolved-chip" :class="{ active: currentStatus === 'resolved' }" @click="setStatusFilter('resolved')">
          <span class="chip-label">Resolved</span>
          <span class="chip-count">{{ counts.resolved }}</span>
        </div>
      </div>

      <!-- Filters & Search Toolbar -->
      <div class="toolbar-card">
        <div class="search-box">
          <i class="fa-solid fa-magnifying-glass search-icon"></i>
          <input
            v-model="searchQuery"
            type="text"
            placeholder="Search by Ticket #, Customer Name, Email, Product, or Order #..."
            @input="debounceSearch"
          />
          <button v-if="searchQuery" @click="searchQuery = ''; loadTickets()" class="btn-clear-search">
            <i class="fa-solid fa-xmark"></i>
          </button>
        </div>

        <div class="filter-controls">
          <div class="filter-group">
            <label>Inquiry Type</label>
            <select v-model="inquiryFilter" @change="loadTickets">
              <option value="">All Topics</option>
              <option value="product">Product Inquiries</option>
              <option value="order">Order & Shipping Status</option>
              <option value="return">Returns & Refunds</option>
              <option value="general">General Questions</option>
            </select>
          </div>
        </div>
      </div>

      <!-- Loading State -->
      <div v-if="loading" class="loading-state-card">
        <LoadingSpinner text="Loading customer inquiries..." />
      </div>

      <!-- Empty State -->
      <div v-else-if="tickets.length === 0" class="empty-state-card">
        <div class="empty-icon-box">
          <i class="fa-solid fa-envelope-open-text"></i>
        </div>
        <h3>No support inquiries found</h3>
        <p>No customer messages matched your current search or status filter.</p>
        <button @click="resetFilters" class="btn-reset">Reset Filters</button>
      </div>

      <!-- Tickets Workstation Table -->
      <div v-else class="tickets-table-card">
        <table class="workstation-table">
          <thead>
            <tr>
              <th>Ticket ID & Date</th>
              <th>Customer</th>
              <th>Topic & Context</th>
              <th>Subject & Message</th>
              <th>Status</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="t in tickets" :key="t.id" class="ticket-row" :class="{ 'row-open': t.status === 'open' }">
              <!-- Ticket Number & Date -->
              <td class="col-id">
                <strong class="ticket-number">{{ t.ticket_number }}</strong>
                <span class="ticket-date">{{ formatDate(t.created_at) }}</span>
              </td>

              <!-- Customer Details -->
              <td class="col-customer">
                <strong class="cust-name">{{ t.name }}</strong>
                <a :href="`mailto:${t.email}?subject=Regarding inquiry ${t.ticket_number}: ${t.subject}`" class="cust-email">
                  <i class="fa-solid fa-envelope"></i> {{ t.email }}
                </a>
              </td>

              <!-- Topic & Context -->
              <td class="col-topic">
                <span class="topic-tag" :class="t.inquiry_type">
                  {{ formatInquiryType(t.inquiry_type) }}
                </span>
                <span v-if="t.product_name" class="context-pill" :title="t.product_name">
                  <i class="fa-solid fa-box"></i> {{ t.product_name }}
                </span>
                <span v-if="t.order_number" class="context-pill" :title="t.order_number">
                  <i class="fa-solid fa-receipt"></i> {{ t.order_number }}
                </span>
              </td>

              <!-- Subject & Message Snippet -->
              <td class="col-message" @click="openModal(t)">
                <strong class="msg-subject">{{ t.subject }}</strong>
                <p class="msg-snippet">{{ t.message }}</p>
              </td>

              <!-- Status Pill & Quick Change -->
              <td class="col-status">
                <span class="status-badge" :class="t.status">
                  <span class="status-dot"></span>
                  {{ formatStatus(t.status) }}
                </span>
              </td>

              <!-- Actions -->
              <td class="col-actions">
                <button
                  type="button"
                  @click="openModal(t)"
                  class="btn-inspect"
                  title="View full inquiry"
                >
                  Inspect &rarr;
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Ticket Detail Modal -->
    <Teleport to="body">
      <div v-if="inspectModalTicket" class="modal-backdrop" @click="inspectModalTicket = null">
        <div class="modal-card" @click.stop>
          <div class="modal-head">
            <div class="modal-title-wrap">
              <span class="modal-ticket-num">{{ inspectModalTicket.ticket_number }}</span>
              <h2>{{ inspectModalTicket.subject }}</h2>
            </div>
            <button type="button" @click="inspectModalTicket = null" class="btn-close-modal">
              <i class="fa-solid fa-xmark"></i>
            </button>
          </div>

          <div class="modal-body">
            <!-- Meta Bar -->
            <div class="modal-meta-grid">
              <div class="meta-item">
                <span class="m-label">Customer Name:</span>
                <strong>{{ inspectModalTicket.name }}</strong>
              </div>
              <div class="meta-item">
                <span class="m-label">Email Address:</span>
                <a :href="`mailto:${inspectModalTicket.email}`" class="m-link">
                  {{ inspectModalTicket.email }} &nearr;
                </a>
              </div>
              <div class="meta-item">
                <span class="m-label">Date Submitted:</span>
                <span>{{ formatDate(inspectModalTicket.created_at) }}</span>
              </div>
              <div class="meta-item">
                <span class="m-label">Inquiry Category:</span>
                <span class="topic-tag" :class="inspectModalTicket.inquiry_type">
                  {{ formatInquiryType(inspectModalTicket.inquiry_type) }}
                </span>
              </div>
              <div v-if="inspectModalTicket.product_name" class="meta-item full-width">
                <span class="m-label">Referenced Product:</span>
                <strong>{{ inspectModalTicket.product_name }}</strong>
              </div>
              <div v-if="inspectModalTicket.order_number" class="meta-item full-width">
                <span class="m-label">Referenced Order:</span>
                <strong>{{ inspectModalTicket.order_number }}</strong>
              </div>
            </div>

            <!-- Message Content -->
            <div class="modal-msg-box">
              <h3>Customer Message:</h3>
              <div class="msg-content-text">{{ inspectModalTicket.message }}</div>
            </div>

            <!-- Status Controls -->
            <div class="status-action-row">
              <span class="status-change-label">Change Ticket Status:</span>
              <div class="status-btn-group">
                <button
                  type="button"
                  class="btn-status-toggle open"
                  :class="{ active: inspectModalTicket.status === 'open' }"
                  :disabled="updatingStatus"
                  @click="updateStatus(inspectModalTicket, 'open')"
                >
                  Awaiting Reply (Open)
                </button>
                <button
                  type="button"
                  class="btn-status-toggle in_progress"
                  :class="{ active: inspectModalTicket.status === 'in_progress' }"
                  :disabled="updatingStatus"
                  @click="updateStatus(inspectModalTicket, 'in_progress')"
                >
                  In Progress
                </button>
                <button
                  type="button"
                  class="btn-status-toggle resolved"
                  :class="{ active: inspectModalTicket.status === 'resolved' }"
                  :disabled="updatingStatus"
                  @click="updateStatus(inspectModalTicket, 'resolved')"
                >
                  Resolved
                </button>
              </div>
            </div>
          </div>

          <div class="modal-foot">
            <a
              :href="`mailto:${inspectModalTicket.email}?subject=Regarding inquiry ${inspectModalTicket.ticket_number}: ${inspectModalTicket.subject}`"
              class="btn-reply-email"
            >
              <i class="fa-solid fa-reply"></i> Reply via Email
            </a>
            <button type="button" @click="inspectModalTicket = null" class="btn-done">
              Close
            </button>
          </div>
        </div>
      </div>
    </Teleport>
  </div>
</template>

<script setup>
definePageMeta({
  middleware: 'admin',
  layout: 'admin'
})

const { getSupportTickets, updateSupportTicket } = useAdminApi()

const loading = ref(false)
const tickets = ref([])
const counts = ref({
  all: 0,
  open: 0,
  in_progress: 0,
  resolved: 0
})

const currentStatus = ref('')
const inquiryFilter = ref('')
const searchQuery = ref('')
let searchTimeout = null

const inspectModalTicket = ref(null)
const updatingStatus = ref(false)

async function loadTickets() {
  loading.value = true
  try {
    const res = await getSupportTickets({
      status: currentStatus.value,
      inquiry_type: inquiryFilter.value,
      search: searchQuery.value
    })
    tickets.value = res.tickets || []
    if (res.counts) {
      counts.value = res.counts
    }
  } catch (err) {
    console.error('Failed to load support inquiries:', err)
  } finally {
    loading.value = false
  }
}

function setStatusFilter(status) {
  currentStatus.value = status
  loadTickets()
}

function resetFilters() {
  currentStatus.value = ''
  inquiryFilter.value = ''
  searchQuery.value = ''
  loadTickets()
}

function debounceSearch() {
  clearTimeout(searchTimeout)
  searchTimeout = setTimeout(() => {
    loadTickets()
  }, 350)
}

function openModal(ticket) {
  inspectModalTicket.value = ticket
}

async function updateStatus(ticket, newStatus) {
  if (ticket.status === newStatus) return
  updatingStatus.value = true
  try {
    const res = await updateSupportTicket(ticket.id, { status: newStatus })
    ticket.status = newStatus
    if (inspectModalTicket.value && inspectModalTicket.value.id === ticket.id) {
      inspectModalTicket.value.status = newStatus
    }
    // Update local counters
    await loadTickets()
  } catch (err) {
    alert('Failed to update ticket status: ' + (err.message || 'Error'))
  } finally {
    updatingStatus.value = false
  }
}

function formatDate(iso) {
  if (!iso) return ''
  return new Date(iso).toLocaleDateString('en-US', {
    month: 'short',
    day: 'numeric',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

function formatInquiryType(type) {
  const map = {
    product: 'Product Inquiry',
    order: 'Order & Shipping',
    return: 'Return & Refund',
    general: 'General Question'
  }
  return map[type] || type || 'General'
}

function formatStatus(status) {
  const map = {
    open: 'Open',
    in_progress: 'In Progress',
    resolved: 'Resolved'
  }
  return map[status] || status
}

onMounted(() => {
  loadTickets()
})
</script>

<style scoped>
.admin-support-page {
  background: #f8fafc;
  min-height: calc(100vh - 70px);
  padding: 2rem 1.5rem 4rem;
}

.workstation-container {
  max-width: 1320px;
  margin: 0 auto;
}

/* Header */
.header-section {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 2rem;
  gap: 1.5rem;
}

.badge-staff {
  display: inline-block;
  background: var(--primary-light);
  color: var(--primary);
  font-size: 0.72rem;
  font-weight: 800;
  text-transform: uppercase;
  padding: 0.25rem 0.65rem;
  border-radius: var(--radius-full);
  margin-bottom: 0.5rem;
  letter-spacing: 0.05em;
}

.header-section h1 {
  font-size: 1.85rem;
  font-weight: 800;
  color: var(--text-main);
  margin-bottom: 0.35rem;
  letter-spacing: -0.02em;
}

.subtitle {
  color: var(--text-muted);
  font-size: 0.95rem;
}

.btn-refresh {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  background: #ffffff;
  border: 1px solid var(--border-color);
  padding: 0.65rem 1.15rem;
  border-radius: var(--radius-md);
  font-weight: 700;
  font-size: 0.88rem;
  color: var(--text-main);
  cursor: pointer;
  box-shadow: var(--shadow-xs);
  transition: all var(--transition-fast);
}

.btn-refresh:hover:not(:disabled) {
  border-color: var(--primary);
  color: var(--primary);
}

/* Metrics Ribbon */
.metrics-ribbon {
  display: flex;
  gap: 0.85rem;
  margin-bottom: 1.75rem;
  overflow-x: auto;
  padding-bottom: 0.35rem;
}

.metric-chip {
  display: flex;
  align-items: center;
  gap: 0.65rem;
  background: #ffffff;
  border: 1px solid var(--border-color);
  padding: 0.65rem 1.15rem;
  border-radius: var(--radius-md);
  font-size: 0.88rem;
  font-weight: 700;
  color: var(--text-body);
  cursor: pointer;
  transition: all var(--transition-fast);
  box-shadow: var(--shadow-xs);
  white-space: nowrap;
}

.metric-chip:hover {
  border-color: var(--border-hover);
  background: #f1f5f9;
}

.metric-chip.active {
  background: var(--text-main);
  color: #ffffff;
  border-color: var(--text-main);
}

.chip-count {
  background: rgba(0, 0, 0, 0.08);
  padding: 0.15rem 0.55rem;
  border-radius: var(--radius-full);
  font-size: 0.8rem;
}

.metric-chip.active .chip-count {
  background: rgba(255, 255, 255, 0.25);
  color: #ffffff;
}

.open-chip.active {
  background: #b91c1c;
  border-color: #b91c1c;
}

.progress-chip.active {
  background: #2563eb;
  border-color: #2563eb;
}

.resolved-chip.active {
  background: #059669;
  border-color: #059669;
}

/* Toolbar */
.toolbar-card {
  background: #ffffff;
  border: 1px solid var(--border-color);
  border-radius: var(--radius-lg);
  padding: 1.15rem 1.35rem;
  margin-bottom: 1.75rem;
  display: flex;
  align-items: center;
  gap: 1.25rem;
  flex-wrap: wrap;
  box-shadow: var(--shadow-xs);
}

.search-box {
  position: relative;
  flex: 1;
  min-width: 280px;
  display: flex;
  align-items: center;
}

.search-icon {
  position: absolute;
  left: 0.95rem;
  color: var(--text-subtle);
  font-size: 0.9rem;
}

.search-box input {
  width: 100%;
  padding: 0.65rem 2.2rem 0.65rem 2.4rem;
  border: 1px solid var(--border-color);
  border-radius: var(--radius-md);
  font-size: 0.9rem;
  outline: none;
  background: #f8fafc;
  transition: all var(--transition-fast);
}

.search-box input:focus {
  border-color: var(--primary);
  background: #ffffff;
}

.btn-clear-search {
  position: absolute;
  right: 0.75rem;
  background: transparent;
  border: none;
  color: var(--text-subtle);
  cursor: pointer;
  padding: 0.2rem;
}

.filter-controls {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.filter-group {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.85rem;
  font-weight: 600;
  color: var(--text-body);
}

.filter-group select {
  padding: 0.6rem 0.95rem;
  border: 1px solid var(--border-color);
  border-radius: var(--radius-md);
  font-size: 0.88rem;
  background: #ffffff;
  outline: none;
  cursor: pointer;
}

/* Table Card */
.tickets-table-card {
  background: #ffffff;
  border: 1px solid var(--border-color);
  border-radius: var(--radius-lg);
  overflow: hidden;
  box-shadow: var(--shadow-xs);
}

.workstation-table {
  width: 100%;
  border-collapse: collapse;
  text-align: left;
  font-size: 0.88rem;
}

.workstation-table th {
  background: #f8fafc;
  padding: 0.85rem 1.25rem;
  font-size: 0.78rem;
  font-weight: 800;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.05em;
  border-bottom: 1px solid var(--border-color);
}

.workstation-table td {
  padding: 1.15rem 1.25rem;
  border-bottom: 1px solid var(--border-color);
  vertical-align: top;
}

.ticket-row:hover {
  background: #f8fafc;
}

.ticket-row.row-open {
  background: #fffdfa;
}

.col-id {
  width: 160px;
}

.ticket-number {
  display: block;
  font-family: monospace;
  font-size: 0.88rem;
  color: var(--text-main);
}

.ticket-date {
  font-size: 0.75rem;
  color: var(--text-muted);
}

.col-customer {
  width: 200px;
}

.cust-name {
  display: block;
  font-size: 0.92rem;
  color: var(--text-main);
}

.cust-email {
  display: inline-flex;
  align-items: center;
  gap: 0.35rem;
  font-size: 0.8rem;
  color: var(--primary);
  text-decoration: none;
  margin-top: 0.2rem;
}

.cust-email:hover {
  text-decoration: underline;
}

.col-topic {
  width: 190px;
}

.topic-tag {
  display: inline-block;
  padding: 0.2rem 0.55rem;
  border-radius: var(--radius-xs);
  font-size: 0.72rem;
  font-weight: 700;
  text-transform: uppercase;
  margin-bottom: 0.35rem;
}

.topic-tag.product { background: #eff6ff; color: #1d4ed8; }
.topic-tag.order { background: #fef3c7; color: #b45309; }
.topic-tag.return { background: #fee2e2; color: #b91c1c; }
.topic-tag.general { background: #f1f5f9; color: #475569; }

.context-pill {
  display: block;
  font-size: 0.76rem;
  color: var(--text-muted);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 180px;
}

.col-message {
  cursor: pointer;
}

.msg-subject {
  display: block;
  font-size: 0.92rem;
  color: var(--text-main);
  margin-bottom: 0.25rem;
}

.msg-snippet {
  font-size: 0.82rem;
  color: var(--text-muted);
  line-height: 1.45;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.col-status {
  width: 140px;
}

.status-badge {
  display: inline-flex;
  align-items: center;
  gap: 0.45rem;
  padding: 0.35rem 0.75rem;
  border-radius: var(--radius-full);
  font-size: 0.76rem;
  font-weight: 700;
  text-transform: uppercase;
}

.status-dot {
  width: 7px;
  height: 7px;
  border-radius: 50%;
}

.status-badge.open {
  background: #fee2e2;
  color: #991b1b;
}
.status-badge.open .status-dot { background: #ef4444; }

.status-badge.in_progress {
  background: #eff6ff;
  color: #1e40af;
}
.status-badge.in_progress .status-dot { background: #3b82f6; }

.status-badge.resolved {
  background: #ecfdf5;
  color: #065f46;
}
.status-badge.resolved .status-dot { background: #10b981; }

.col-actions {
  width: 110px;
  text-align: right;
}

.btn-inspect {
  background: #ffffff;
  border: 1px solid var(--border-color);
  padding: 0.45rem 0.85rem;
  border-radius: var(--radius-sm);
  font-size: 0.82rem;
  font-weight: 700;
  color: var(--primary);
  cursor: pointer;
  transition: all var(--transition-fast);
}

.btn-inspect:hover {
  background: var(--primary);
  color: #ffffff;
  border-color: var(--primary);
}

/* Empty & Loading States */
.loading-state-card, .empty-state-card {
  background: #ffffff;
  border: 1px dashed var(--border-color);
  border-radius: var(--radius-lg);
  padding: 4rem 1.5rem;
  text-align: center;
}

.empty-icon-box {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  background: var(--bg-subtle);
  color: var(--text-muted);
  font-size: 1.6rem;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 1.25rem;
}

.btn-reset {
  margin-top: 1rem;
  background: var(--primary);
  color: #ffffff;
  border: none;
  padding: 0.55rem 1.25rem;
  border-radius: var(--radius-md);
  font-weight: 700;
  cursor: pointer;
}

/* Modal */
.modal-backdrop {
  position: fixed;
  inset: 0;
  background: rgba(15, 23, 42, 0.6);
  backdrop-filter: blur(4px);
  z-index: 10000;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 1.5rem;
}

.modal-card {
  background: #ffffff;
  border-radius: var(--radius-xl);
  max-width: 680px;
  width: 100%;
  max-height: 90vh;
  display: flex;
  flex-direction: column;
  box-shadow: 0 25px 60px -15px rgba(15, 23, 42, 0.25);
  overflow: hidden;
}

.modal-head {
  padding: 1.5rem 1.75rem;
  border-bottom: 1px solid var(--border-color);
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
}

.modal-ticket-num {
  display: inline-block;
  font-family: monospace;
  font-size: 0.82rem;
  color: var(--primary);
  font-weight: 700;
  margin-bottom: 0.35rem;
}

.modal-head h2 {
  font-size: 1.35rem;
  font-weight: 800;
  color: var(--text-main);
  line-height: 1.3;
}

.btn-close-modal {
  background: transparent;
  border: none;
  font-size: 1.25rem;
  color: var(--text-subtle);
  cursor: pointer;
  padding: 0.25rem;
}

.modal-body {
  padding: 1.75rem;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.modal-meta-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
  background: #f8fafc;
  padding: 1.15rem 1.25rem;
  border-radius: var(--radius-md);
  border: 1px solid var(--border-color);
  font-size: 0.88rem;
}

.meta-item.full-width {
  grid-column: span 2;
}

.m-label {
  display: block;
  font-size: 0.75rem;
  color: var(--text-muted);
  font-weight: 600;
  text-transform: uppercase;
  margin-bottom: 0.15rem;
}

.m-link {
  color: var(--primary);
  text-decoration: none;
  font-weight: 600;
}

.modal-msg-box {
  background: #ffffff;
  border: 1px solid var(--border-color);
  border-radius: var(--radius-md);
  padding: 1.25rem;
}

.modal-msg-box h3 {
  font-size: 0.85rem;
  text-transform: uppercase;
  color: var(--text-muted);
  font-weight: 800;
  margin-bottom: 0.75rem;
  letter-spacing: 0.05em;
}

.msg-content-text {
  font-size: 0.95rem;
  line-height: 1.65;
  color: var(--text-main);
  white-space: pre-wrap;
}

.status-action-row {
  display: flex;
  flex-direction: column;
  gap: 0.65rem;
}

.status-change-label {
  font-size: 0.82rem;
  font-weight: 700;
  color: var(--text-body);
}

.status-btn-group {
  display: flex;
  gap: 0.65rem;
  flex-wrap: wrap;
}

.btn-status-toggle {
  padding: 0.55rem 1rem;
  border-radius: var(--radius-md);
  font-size: 0.85rem;
  font-weight: 700;
  cursor: pointer;
  border: 1px solid var(--border-color);
  background: #ffffff;
  color: var(--text-body);
  transition: all var(--transition-fast);
}

.btn-status-toggle.open.active {
  background: #fee2e2;
  color: #991b1b;
  border-color: #ef4444;
}

.btn-status-toggle.in_progress.active {
  background: #eff6ff;
  color: #1e40af;
  border-color: #3b82f6;
}

.btn-status-toggle.resolved.active {
  background: #ecfdf5;
  color: #065f46;
  border-color: #10b981;
}

.modal-foot {
  padding: 1.25rem 1.75rem;
  border-top: 1px solid var(--border-color);
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: #f8fafc;
}

.btn-reply-email {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  background: var(--primary);
  color: #ffffff;
  padding: 0.65rem 1.25rem;
  border-radius: var(--radius-md);
  font-weight: 700;
  font-size: 0.88rem;
  text-decoration: none;
}

.btn-done {
  background: #ffffff;
  border: 1px solid var(--border-color);
  padding: 0.65rem 1.25rem;
  border-radius: var(--radius-md);
  font-weight: 700;
  font-size: 0.88rem;
  color: var(--text-body);
  cursor: pointer;
}
</style>

