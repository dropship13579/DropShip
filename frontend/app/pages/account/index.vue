<!-- frontend/app/pages/account/index.vue -->
<template>
    <div class="account-page">
        <div class="account-container">
            <!-- Page Header -->
            <div class="page-header">
                <div>
                    <h1>My Account</h1>
                    <p class="subtitle">Manage your personal information, delivery addresses, and security settings.</p>
                </div>
                <button @click="logout" class="btn-logout-header">Sign Out</button>
            </div>

            <div class="account-layout">
                <!-- Sidebar Navigation Card -->
                <aside class="account-sidebar">
                    <div class="user-card">
                        <div class="user-avatar">
                            {{ (profileForm.first_name || user?.username || 'U')[0].toUpperCase() }}
                        </div>
                        <div class="user-details">
                            <h3>{{ displayName }}</h3>
                            <p>{{ user?.email }}</p>
                        </div>
                    </div>

                    <nav class="sidebar-nav">
                        <button class="nav-item" :class="{ active: currentTab === 'profile' }"
                            @click="switchTab('profile')">
                            Profile & Details
                        </button>
                        <button class="nav-item" :class="{ active: currentTab === 'security' }"
                            @click="switchTab('security')">
                            Login & Security
                        </button>
                        <button class="nav-item" :class="{ active: currentTab === 'addresses' }"
                            @click="switchTab('addresses')">
                            Delivery Addresses ({{ addresses.length }})
                        </button>
                        <NuxtLink to="/account/wishlist" class="nav-item link-item">
                            My Wishlist &rarr;
                        </NuxtLink>
                        <NuxtLink to="/account/orders" class="nav-item link-item">
                            Order History &rarr;
                        </NuxtLink>
                    </nav>
                </aside>

                <!-- Main Content Area -->
                <main class="account-main">
                    <!-- TAB 1: Profile & Details -->
                    <section v-if="currentTab === 'profile'" class="tab-card">
                        <h2>Personal Information</h2>
                        <p class="section-desc">Update your personal details and contact number.</p>

                        <div v-if="profileMsg" class="success-banner">{{ profileMsg }}</div>
                        <div v-if="profileError" class="error-banner">{{ profileError }}</div>

                        <form @submit.prevent="handleUpdateProfile" class="profile-form">
                            <div class="form-row">
                                <div class="form-group">
                                    <label for="prof-first-name">First Name</label>
                                    <input id="prof-first-name" v-model="profileForm.first_name" type="text"
                                        placeholder="e.g. Alex" />
                                </div>
                                <div class="form-group">
                                    <label for="prof-last-name">Last Name</label>
                                    <input id="prof-last-name" v-model="profileForm.last_name" type="text"
                                        placeholder="e.g. Johnson" />
                                </div>
                            </div>

                            <div class="form-row">
                                <div class="form-group">
                                    <label>Username</label>
                                    <input type="text" :value="user?.username" disabled class="input-disabled" />
                                    <span class="field-hint">Usernames cannot be changed.</span>
                                </div>

                                <div class="form-group">
                                    <label>Email Address</label>
                                    <input type="email" :value="user?.email" disabled class="input-disabled" />
                                    <span class="field-hint">Primary account email.</span>
                                </div>
                            </div>

                            <div class="form-group">
                                <label for="prof-phone">Phone Number</label>
                                <input id="prof-phone" v-model="profileForm.phone" type="tel"
                                    placeholder="e.g. +1 (555) 019-2834" />
                            </div>

                            <button type="submit" class="btn-primary" :disabled="savingProfile">
                                {{ savingProfile ? 'Saving Changes...' : 'Save Profile Changes' }}
                            </button>
                        </form>
                    </section>

                    <!-- TAB 2: Login & Security (Password Change) -->
                    <section v-if="currentTab === 'security'" class="tab-card">
                        <div class="tab-header">
                            <div>
                                <h2>Login & Password Security</h2>
                                <p class="section-desc">Ensure your KyroKart customer account stays protected.</p>
                            </div>
                        </div>

                        <!-- Account Summary Card -->
                        <div class="security-meta-box">
                            <div class="meta-item">
                                <span class="meta-label">Username</span>
                                <span class="meta-val">{{ user?.username }}</span>
                            </div>
                            <div class="meta-item">
                                <span class="meta-label">Email</span>
                                <span class="meta-val">{{ user?.email }}</span>
                            </div>
                            <div class="meta-item">
                                <span class="meta-label">Account Status</span>
                                <span class="meta-badge-active">Protected</span>
                            </div>
                        </div>

                        <div v-if="passwordSuccess" class="success-banner">{{ passwordSuccess }}</div>
                        <div v-if="passwordError" class="error-banner">{{ passwordError }}</div>

                        <form @submit.prevent="handleChangePassword" class="profile-form">
                            <!-- Current Password -->
                            <div class="form-group">
                                <label for="old-pass">Current Password</label>
                                <div class="password-input-wrap">
                                    <input id="old-pass" :type="showOldPassword ? 'text' : 'password'"
                                        v-model="passwordForm.old_password" required
                                        placeholder="Enter your current password" />
                                    <button type="button" class="btn-toggle-eye"
                                        @click="showOldPassword = !showOldPassword">
                                        {{ showOldPassword ? 'Hide' : 'Show' }}
                                    </button>
                                </div>
                            </div>

                            <!-- New Password -->
                            <div class="form-group">
                                <label for="new-pass">New Password</label>
                                <div class="password-input-wrap">
                                    <input id="new-pass" :type="showNewPassword ? 'text' : 'password'"
                                        v-model="passwordForm.new_password" required
                                        placeholder="At least 8 characters" />
                                    <button type="button" class="btn-toggle-eye"
                                        @click="showNewPassword = !showNewPassword">
                                        {{ showNewPassword ? 'Hide' : 'Show' }}
                                    </button>
                                </div>
                            </div>

                            <!-- Confirm New Password -->
                            <div class="form-group">
                                <label for="confirm-pass">Confirm New Password</label>
                                <input id="confirm-pass" type="password" v-model="passwordForm.confirm_password"
                                    required placeholder="Re-type your new password" />
                            </div>

                            <!-- Security Checklist -->
                            <div class="password-rules">
                                <div class="rule-item" :class="{ valid: isLengthValid }">
                                    <span class="rule-icon"><i :class="isLengthValid ? 'fa-solid fa-circle-check' : 'fa-regular fa-circle'"></i></span>
                                    <span>At least 8 characters</span>
                                </div>
                                <div class="rule-item"
                                    :class="{ valid: isMatchValid && passwordForm.confirm_password }">
                                    <span class="rule-icon"><i :class="(isMatchValid && passwordForm.confirm_password) ? 'fa-solid fa-circle-check' : 'fa-regular fa-circle'"></i></span>
                                    <span>Passwords match</span>
                                </div>
                            </div>

                            <button type="submit" class="btn-primary"
                                :disabled="savingPassword || !isLengthValid || !isMatchValid">
                                {{ savingPassword ? 'Updating Password...' : 'Update Password' }}
                            </button>
                        </form>
                    </section>

                    <!-- TAB 3: Delivery Addresses -->
                    <section v-if="currentTab === 'addresses'" class="tab-card">
                        <div class="tab-header">
                            <div>
                                <h2>Delivery Addresses</h2>
                                <p class="section-desc">Manage your addresses for 1-click checkout.</p>
                            </div>
                            <button @click="openAddModal" class="btn-primary">+ Add New Address</button>
                        </div>

                        <div v-if="loadingAddresses" class="loading-wrap">
                            <LoadingSpinner text="Loading addresses..." />
                        </div>

                        <EmptyState v-else-if="addresses.length === 0" title="No delivery addresses saved"
                            description="Add an address now to speed up checkout on your future orders.">
                            <template #action>
                                <button @click="openAddModal" class="btn-primary">+ Add Address</button>
                            </template>
                        </EmptyState>

                        <div v-else class="address-grid">
                            <div v-for="addr in addresses" :key="addr.id" class="address-card"
                                :class="{ 'is-default': addr.is_default }">
                                <div class="card-top">
                                    <span v-if="addr.is_default" class="badge-default">Default</span>
                                    <span class="recipient">{{ addr.recipient_name }}</span>
                                </div>

                                <div class="addr-lines">
                                    <p>{{ addr.address_line_1 }}</p>
                                    <p v-if="addr.address_line_2">{{ addr.address_line_2 }}</p>
                                    <p>{{ addr.city }}, {{ addr.state }} {{ addr.postal_code }}</p>
                                    <p>{{ addr.country }}</p>
                                    <p class="phone-line">Phone: {{ addr.phone }}</p>
                                </div>

                                <div class="card-actions">
                                    <button @click="openEditModal(addr)" class="btn-action">Edit</button>
                                    <button @click="handleDeleteAddress(addr.id)"
                                        class="btn-action delete">Delete</button>
                                </div>
                            </div>
                        </div>
                    </section>
                </main>
            </div>

            <!-- Address Modal -->
            <AddressFormModal :is-open="modalOpen" :initial-data="selectedAddress" @close="modalOpen = false"
                @saved="loadAddresses" />
        </div>
    </div>
</template>

<script setup>
definePageMeta({
    middleware: 'auth'
})

const { user, logout } = useAuthState()
const { getProfile, updateProfile, changePassword, getAddresses, deleteAddress } = useAccountApi()

const currentTab = ref('profile')

// Profile State
const savingProfile = ref(false)
const profileMsg = ref('')
const profileError = ref('')

const profileForm = reactive({
    first_name: '',
    last_name: '',
    phone: ''
})

// Password Security State
const savingPassword = ref(false)
const passwordSuccess = ref('')
const passwordError = ref('')
const showOldPassword = ref(false)
const showNewPassword = ref(false)

const passwordForm = reactive({
    old_password: '',
    new_password: '',
    confirm_password: ''
})

// Live Password Validation Computeds
const isLengthValid = computed(() => {
    return passwordForm.new_password.length >= 8
})

const isMatchValid = computed(() => {
    return Boolean(
        passwordForm.new_password &&
        passwordForm.confirm_password &&
        passwordForm.new_password === passwordForm.confirm_password
    )
})

// Computed Display Name for Sidebar Header
const displayName = computed(() => {
    if (profileForm.first_name || profileForm.last_name) {
        return `${profileForm.first_name} ${profileForm.last_name}`.trim()
    }
    return user.value?.username || 'Customer'
})

// Address State
const addresses = ref([])
const loadingAddresses = ref(true)
const modalOpen = ref(false)
const selectedAddress = ref(null)

function switchTab(tab) {
    currentTab.value = tab
    profileMsg.value = ''
    profileError.value = ''
    passwordSuccess.value = ''
    passwordError.value = ''
}

async function loadProfile() {
    try {
        const data = await getProfile()
        if (data) {
            profileForm.first_name = data.first_name || ''
            profileForm.last_name = data.last_name || ''
            profileForm.phone = data.phone || ''
        }
    } catch (err) {
        console.error('Failed to load profile:', err)
    }
}

async function handleUpdateProfile() {
    savingProfile.value = true
    profileMsg.value = ''
    profileError.value = ''
    try {
        await updateProfile({
            first_name: profileForm.first_name,
            last_name: profileForm.last_name,
            phone: profileForm.phone
        })
        profileMsg.value = 'Profile details updated successfully.'
        setTimeout(() => { profileMsg.value = '' }, 4000)
    } catch (err) {
        profileError.value = err.message || 'Failed to update profile.'
    } finally {
        savingProfile.value = false
    }
}

async function handleChangePassword() {
    if (!isLengthValid.value) {
        passwordError.value = 'New password must be at least 8 characters long.'
        return
    }
    if (!isMatchValid.value) {
        passwordError.value = 'New passwords do not match.'
        return
    }

    savingPassword.value = true
    passwordSuccess.value = ''
    passwordError.value = ''

    try {
        const res = await changePassword({
            old_password: passwordForm.old_password,
            new_password: passwordForm.new_password,
            confirm_password: passwordForm.confirm_password
        })
        passwordSuccess.value = res?.message || 'Password changed successfully.'
        // Reset inputs on success
        passwordForm.old_password = ''
        passwordForm.new_password = ''
        passwordForm.confirm_password = ''
        setTimeout(() => { passwordSuccess.value = '' }, 5000)
    } catch (err) {
        passwordError.value = err.message || 'Failed to change password. Please check your current password.'
    } finally {
        savingPassword.value = false
    }
}

async function loadAddresses() {
    loadingAddresses.value = true
    try {
        const data = await getAddresses()
        addresses.value = Array.isArray(data) ? data : (data?.results || [])
    } catch (err) {
        console.error('Failed to load addresses:', err)
    } finally {
        loadingAddresses.value = false
    }
}

function openAddModal() {
    selectedAddress.value = null
    modalOpen.value = true
}

function openEditModal(addr) {
    selectedAddress.value = { ...addr }
    modalOpen.value = true
}

async function handleDeleteAddress(id) {
    if (confirm('Are you sure you want to delete this delivery address?')) {
        try {
            await deleteAddress(id)
            await loadAddresses()
        } catch (err) {
            alert(err.message || 'Failed to delete address.')
        }
    }
}

onMounted(async () => {
    await Promise.all([
        loadProfile(),
        loadAddresses()
    ])
})
</script>

<style scoped>
.account-page {
    padding: 3rem 1.5rem 5rem;
}

.account-container {
    max-width: 1100px;
    margin: 0 auto;
}

.page-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 2.5rem;
    border-bottom: 1px solid var(--border-color);
    padding-bottom: 1.5rem;
}

h1 {
    font-size: 2rem;
    font-weight: 800;
    letter-spacing: -0.02em;
}

.subtitle {
    color: var(--text-muted);
    font-size: 0.95rem;
    margin-top: 0.25rem;
}

.btn-logout-header {
    background: #f1f5f9;
    border: 1px solid var(--border-color);
    color: #475569;
    font-weight: 600;
    font-size: 0.85rem;
    padding: 0.5rem 1.1rem;
    border-radius: var(--radius-sm);
    transition: all 0.15s;
}

.btn-logout-header:hover {
    color: #dc2626;
    background: #fee2e2;
}

.account-layout {
    display: grid;
    grid-template-columns: 280px 1fr;
    gap: 2.5rem;
    align-items: start;
}

.account-sidebar {
    background: var(--bg-surface);
    border: 1px solid var(--border-color);
    border-radius: var(--radius-lg);
    overflow: hidden;
    box-shadow: var(--shadow-sm);
}

.user-card {
    padding: 1.75rem 1.25rem;
    border-bottom: 1px solid var(--border-color);
    display: flex;
    align-items: center;
    gap: 1rem;
}

.user-avatar {
    width: 48px;
    height: 48px;
    background: var(--primary);
    color: #fff;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.25rem;
    font-weight: 800;
    flex-shrink: 0;
}

.user-details h3 {
    font-size: 1rem;
    font-weight: 700;
    line-height: 1.25;
}

.user-details p {
    font-size: 0.8rem;
    color: var(--text-muted);
    word-break: break-all;
    margin-top: 0.2rem;
}

.sidebar-nav {
    display: flex;
    flex-direction: column;
}

.nav-item {
    text-align: left;
    padding: 0.9rem 1.25rem;
    font-size: 0.9rem;
    font-weight: 600;
    color: var(--text-main);
    border-bottom: 1px solid var(--border-color);
    transition: all 0.15s;
    display: block;
}

.nav-item:last-child {
    border-bottom: none;
}

.nav-item:hover {
    background: var(--bg-page);
    color: var(--primary);
}

.nav-item.active {
    background: var(--primary-light);
    color: var(--primary);
    border-left: 3px solid var(--primary);
}

.tab-card {
    background: var(--bg-surface);
    border: 1px solid var(--border-color);
    border-radius: var(--radius-lg);
    padding: 2.25rem;
    box-shadow: var(--shadow-sm);
}

.tab-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 1.5rem;
}

h2 {
    font-size: 1.35rem;
    font-weight: 800;
}

.section-desc {
    font-size: 0.875rem;
    color: var(--text-muted);
    margin-top: 0.25rem;
}

.success-banner {
    background: #f0fdf4;
    border: 1px solid #bbf7d0;
    color: #16a34a;
    padding: 0.75rem 1rem;
    border-radius: var(--radius-md);
    font-size: 0.875rem;
    font-weight: 600;
    margin-bottom: 1.5rem;
}

.error-banner {
    background: #fef2f2;
    border: 1px solid #fecaca;
    color: #dc2626;
    padding: 0.75rem 1rem;
    border-radius: var(--radius-md);
    font-size: 0.875rem;
    font-weight: 600;
    margin-bottom: 1.5rem;
}

/* Security Meta Box */
.security-meta-box {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
    gap: 1rem;
    background: var(--bg-page);
    border: 1px solid var(--border-color);
    border-radius: var(--radius-md);
    padding: 1rem 1.25rem;
    margin-bottom: 1.75rem;
}

.meta-item {
    display: flex;
    flex-direction: column;
    gap: 0.2rem;
}

.meta-label {
    font-size: 0.75rem;
    font-weight: 700;
    text-transform: uppercase;
    color: var(--text-muted);
    letter-spacing: 0.05em;
}

.meta-val {
    font-size: 0.9rem;
    font-weight: 700;
    color: var(--text-main);
}

.meta-badge-active {
    font-size: 0.75rem;
    font-weight: 700;
    color: #16a34a;
    background: #dcfce7;
    padding: 0.15rem 0.5rem;
    border-radius: 9999px;
    align-self: flex-start;
}

.profile-form {
    display: flex;
    flex-direction: column;
    gap: 1.25rem;
    max-width: 540px;
}

.form-row {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 1rem;
}

.form-group {
    display: flex;
    flex-direction: column;
    gap: 0.35rem;
}

label {
    font-size: 0.85rem;
    font-weight: 700;
    color: var(--text-main);
}

input {
    border: 1px solid var(--border-color);
    padding: 0.65rem 0.85rem;
    border-radius: var(--radius-sm);
    font-size: 0.9rem;
    outline: none;
    transition: border-color 0.15s;
    color: var(--text-main);
}

input:focus:not(:disabled) {
    border-color: var(--primary);
}

.input-disabled {
    background: var(--bg-page);
    color: var(--text-muted);
    cursor: not-allowed;
}

.field-hint {
    font-size: 0.75rem;
    color: var(--text-muted);
}

.password-input-wrap {
    position: relative;
    display: flex;
    align-items: center;
}

.password-input-wrap input {
    width: 100%;
    padding-right: 3.5rem;
}

.btn-toggle-eye {
    position: absolute;
    right: 0.75rem;
    font-size: 0.8rem;
    font-weight: 700;
    color: var(--text-muted);
    cursor: pointer;
}

.btn-toggle-eye:hover {
    color: var(--primary);
}

.password-rules {
    display: flex;
    flex-direction: column;
    gap: 0.35rem;
    padding: 0.75rem 1rem;
    background: var(--bg-page);
    border-radius: var(--radius-sm);
    border: 1px solid var(--border-color);
}

.rule-item {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    font-size: 0.8rem;
    color: var(--text-muted);
}

.rule-item.valid {
    color: #16a34a;
    font-weight: 600;
}

.rule-icon {
    font-weight: 800;
    font-size: 0.85rem;
}

.btn-primary {
    background: var(--primary);
    color: #fff;
    font-weight: 700;
    font-size: 0.9rem;
    padding: 0.7rem 1.4rem;
    border-radius: var(--radius-md);
    align-self: flex-start;
    transition: background 0.15s;
}

.btn-primary:hover:not(:disabled) {
    background: var(--primary-hover);
}

.btn-primary:disabled {
    opacity: 0.55;
    cursor: not-allowed;
}

/* Addresses */
.address-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
    gap: 1.25rem;
}

.address-card {
    border: 1px solid var(--border-color);
    border-radius: var(--radius-md);
    padding: 1.25rem;
    background: var(--bg-surface);
    display: flex;
    flex-direction: column;
}

.address-card.is-default {
    border-color: var(--primary);
    box-shadow: 0 0 0 1px var(--primary);
}

.card-top {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 0.75rem;
}

.badge-default {
    background: var(--primary-light);
    color: var(--primary);
    font-size: 0.75rem;
    font-weight: 700;
    padding: 0.15rem 0.5rem;
    border-radius: var(--radius-sm);
}

.recipient {
    font-weight: 700;
    font-size: 1rem;
}

.addr-lines {
    font-size: 0.875rem;
    color: var(--text-muted);
    line-height: 1.5;
    margin-bottom: 1.25rem;
    flex: 1;
}

.phone-line {
    margin-top: 0.5rem;
}

.card-actions {
    display: flex;
    gap: 0.75rem;
    border-top: 1px solid var(--border-color);
    padding-top: 0.75rem;
}

.btn-action {
    font-size: 0.8rem;
    font-weight: 600;
    color: var(--primary);
}

.btn-action.delete {
    color: #dc2626;
}

@media (max-width: 800px) {
    .account-layout {
        grid-template-columns: 1fr;
    }
}
</style>
