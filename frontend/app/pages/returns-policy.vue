<!-- frontend/app/pages/returns-policy.vue -->
<template>
  <div class="policy-page">
    <div class="policy-container">
      <div class="policy-header">
        <span class="policy-tag">Risk-Free Shopping</span>
        <h1>30-Day Money-Back & Returns Policy</h1>
        <p class="policy-sub">Simple, straightforward returns and prompt refunds with zero hidden restock fees.</p>
      </div>

      <div class="policy-card">
        <section class="policy-section">
          <h2><i class="fa-solid fa-arrows-rotate icon-accent"></i> 1. 30-Day Happiness Guarantee</h2>
          <p>
            We want you to love your purchase. If you are not completely satisfied with any item ordered from <strong>KyroKart</strong>,
            you may initiate a return or exchange within <strong>30 days of receiving your parcel</strong>.
          </p>
        </section>

        <section class="policy-section">
          <h2><i class="fa-solid fa-clipboard-check icon-accent"></i> 2. Return Eligibility Criteria</h2>
          <ul class="criteria-list">
            <li>Item must be in its original packaging with all included accessories, manuals, and protective cables.</li>
            <li>Item must be undamaged, unworn, and in like-new functional condition.</li>
            <li>Proof of purchase (order number or email confirmation) is required.</li>
          </ul>
        </section>

        <section class="policy-section">
          <h2><i class="fa-solid fa-shield-heart icon-accent"></i> 3. Defective, Damaged, or Incorrect Items</h2>
          <p>
            In the rare event that an item arrives damaged or malfunctions within the 1-year store warranty period,
            we will dispatch an immediate free replacement or issue a 100% refund — no return shipment required in most cases.
          </p>
        </section>

        <section class="policy-section">
          <h2><i class="fa-solid fa-headset icon-accent"></i> 4. How to Initiate a Return or Refund</h2>
          <p>
            Simply open our support desk or submit a ticket with your order number. Our team will review your inquiry
            and provide a prepaid return slip or instant resolution within <strong>2 business hours</strong>.
          </p>
          <div class="cta-box">
            <NuxtLink to="/track" class="btn-policy-cta">
              <i class="fa-solid fa-box-open"></i> Check Order Status
            </NuxtLink>
            <button type="button" @click="isGlobalSupportOpen = true" class="btn-policy-secondary">
              <i class="fa-solid fa-envelope"></i> Contact Customer Support
            </button>
          </div>
        </section>
      </div>
    </div>
  </div>
</template>

<script setup>
// Uses global layout support modal if available
</script>

<style scoped>
.policy-page {
  background: var(--bg-page);
  padding: 3.5rem 1.5rem 5rem;
  min-height: 80vh;
}

.policy-container {
  max-width: 860px;
  margin: 0 auto;
}

.policy-header {
  text-align: center;
  margin-bottom: 2.5rem;
}

.policy-tag {
  display: inline-block;
  background: #ecfdf5;
  color: #065f46;
  font-size: 0.75rem;
  font-weight: 800;
  text-transform: uppercase;
  padding: 0.3rem 0.8rem;
  border-radius: var(--radius-full);
  margin-bottom: 0.75rem;
  letter-spacing: 0.05em;
}

.policy-header h1 {
  font-size: 2.4rem;
  font-weight: 800;
  color: var(--text-main);
  margin-bottom: 0.65rem;
  letter-spacing: -0.02em;
}

.policy-sub {
  color: var(--text-muted);
  font-size: 1.05rem;
  line-height: 1.6;
}

.policy-card {
  background: #ffffff;
  border: 1px solid var(--border-color);
  border-radius: var(--radius-xl);
  padding: 3rem;
  box-shadow: var(--shadow-sm);
  display: flex;
  flex-direction: column;
  gap: 2.5rem;
}

.policy-section h2 {
  font-size: 1.25rem;
  font-weight: 800;
  color: var(--text-main);
  margin-bottom: 1rem;
  display: flex;
  align-items: center;
  gap: 0.65rem;
}

.icon-accent {
  color: var(--primary);
  font-size: 1.15rem;
}

.policy-section p {
  color: var(--text-body);
  font-size: 0.98rem;
  line-height: 1.75;
}

.criteria-list {
  padding-left: 1.35rem;
  color: var(--text-body);
  font-size: 0.95rem;
  line-height: 1.8;
}

.cta-box {
  display: flex;
  gap: 1rem;
  margin-top: 1.5rem;
  flex-wrap: wrap;
}

.btn-policy-cta {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  background: var(--primary);
  color: #ffffff;
  padding: 0.8rem 1.4rem;
  border-radius: var(--radius-md);
  font-weight: 700;
  font-size: 0.92rem;
  text-decoration: none;
}

.btn-policy-secondary {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  background: #ffffff;
  color: var(--text-main);
  border: 1px solid var(--border-color);
  padding: 0.8rem 1.4rem;
  border-radius: var(--radius-md);
  font-weight: 700;
  font-size: 0.92rem;
  cursor: pointer;
}

@media (max-width: 640px) {
  .policy-card { padding: 1.75rem 1.25rem; }
  .policy-header h1 { font-size: 1.85rem; }
}
</style>

