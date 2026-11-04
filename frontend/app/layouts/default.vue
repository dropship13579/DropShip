<script setup>
import AppFooter from '~/components/AppFooter.vue';
import AppHeader from '~/components/AppHeader.vue';
import CustomerSupportModal from '~/components/CustomerSupportModal.vue';

const { isAdmin } = useAuthState();
const isGlobalSupportOpen = ref(false);
</script>

<template>
    <div class="site-wrapper">
        <AppHeader />
        <main class="page-content">
            <slot />
        </main>
        <AppFooter />

        <!-- Global Floating Help Trigger (Customer Storefront only) -->
        <button
            v-if="!isAdmin"
            type="button"
            class="floating-support-btn"
            @click="isGlobalSupportOpen = true"
            aria-label="Customer Support Help Desk"
        >
            <span class="floating-icon">💬</span>
            <span class="floating-text">Help & FAQ</span>
        </button>

        <!-- Global Customer Support Modal -->
        <CustomerSupportModal
            :is-open="isGlobalSupportOpen"
            @close="isGlobalSupportOpen = false"
        />
    </div>
</template>

<style scoped>

.site-wrapper{
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    position: relative;
}

.page-content{
    flex: 1;
}

/* Floating Help Button */
.floating-support-btn {
    position: fixed;
    bottom: 1.75rem;
    right: 1.75rem;
    z-index: 900;
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    background: var(--text-main);
    color: #fff;
    padding: 0.65rem 1.15rem;
    border-radius: 9999px;
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.2);
    font-size: 0.88rem;
    font-weight: 700;
    cursor: pointer;
    border: 1px solid rgba(255, 255, 255, 0.15);
    transition: transform 0.2s cubic-bezier(0.16, 1, 0.3, 1), background 0.2s, box-shadow 0.2s;
}

.floating-support-btn:hover {
    transform: translateY(-3px) scale(1.02);
    background: var(--primary);
    box-shadow: 0 12px 28px rgba(37, 99, 235, 0.35);
}

.floating-icon {
    font-size: 1.1rem;
}

@media (max-width: 640px) {
    .floating-support-btn {
        bottom: 1.25rem;
        right: 1.25rem;
        padding: 0.6rem 0.95rem;
    }
}


</style>