<!-- frontend/app/pages/shipping-policy.vue -->
<template>
  <div class="policy-page">
    <div class="policy-container">
      <div class="policy-header">
        <span class="policy-tag">Direct Sourcing Guidelines</span>
        <h1>Shipping & Delivery Policy</h1>
        <p class="policy-sub">Transparent, tracked fulfillment direct from verified global manufacturers to your door.</p>
      </div>

      <div class="policy-card">
        <section class="policy-section">
          <h2><i class="fa-solid fa-truck-fast icon-accent"></i> 1. Order Processing & Dispatch Timelines</h2>
          <p>
            All orders placed on <strong>KyroKart</strong> undergo automated verification and quality inspection before dispatch.
            Our audited manufacturing hubs process and hand over parcels to direct air couriers within <strong>24 to 48 hours</strong>
            (Monday through Friday, excluding public holidays).
          </p>
          <div class="highlight-box">
            <i class="fa-solid fa-circle-check text-green"></i>
            <span>Orders submitted before <strong>2:00 PM EST</strong> qualify for same-day warehouse fulfillment queue.</span>
          </div>
        </section>

        <section class="policy-section">
          <h2><i class="fa-solid fa-earth-americas icon-accent"></i> 2. Estimated Transit Times by Destination</h2>
          <div class="table-wrap">
            <table class="transit-table">
              <thead>
                <tr>
                  <th>Destination Country</th>
                  <th>Standard Tracked Air</th>
                  <th>Express Priority Air</th>
                  <th>Carrier Partners</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td><strong>United States</strong></td>
                  <td>4–7 Business Days</td>
                  <td>2–4 Business Days</td>
                  <td>USPS, FedEx Air, YunExpress</td>
                </tr>
                <tr>
                  <td><strong>United Kingdom</strong></td>
                  <td>5–8 Business Days</td>
                  <td>3–5 Business Days</td>
                  <td>Royal Mail, Hermes, DPD</td>
                </tr>
                <tr>
                  <td><strong>Canada</strong></td>
                  <td>5–9 Business Days</td>
                  <td>3–5 Business Days</td>
                  <td>Canada Post, DHL Express</td>
                </tr>
                <tr>
                  <td><strong>Australia & NZ</strong></td>
                  <td>6–10 Business Days</td>
                  <td>4–6 Business Days</td>
                  <td>Australia Post, Toll Global</td>
                </tr>
                <tr>
                  <td><strong>European Union</strong></td>
                  <td>4–8 Business Days</td>
                  <td>3–5 Business Days</td>
                  <td>DHL Parcel, DPD, Colissimo</td>
                </tr>
              </tbody>
            </table>
          </div>
        </section>

        <section class="policy-section">
          <h2><i class="fa-solid fa-magnifying-glass icon-accent"></i> 3. Real-Time Tracking & Notifications</h2>
          <p>
            As soon as your package is dispatched from the fulfillment hub, you will receive an automated tracking code.
            You can monitor real-time customs checkpoints, air cargo status, and last-mile postal transfers anytime via our
            <NuxtLink to="/track" class="policy-link">Live Order Tracker</NuxtLink>.
          </p>
        </section>

        <section class="policy-section">
          <h2><i class="fa-solid fa-shield-halved icon-accent"></i> 4. Guaranteed On-Time Delivery Protection</h2>
          <p>
            We stand behind our direct logistics network. If your standard shipment takes longer than 15 business days to arrive
            due to carrier delays, we automatically issue a <strong>$5.00 store credit</strong> and expedite delivery follow-up.
          </p>
        </section>
      </div>
    </div>
  </div>
</template>

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
  background: var(--primary-light);
  color: var(--primary);
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

.highlight-box {
  display: flex;
  align-items: center;
  gap: 0.65rem;
  background: #f0fdf4;
  border: 1px solid #bbf7d0;
  border-radius: var(--radius-md);
  padding: 0.85rem 1.15rem;
  margin-top: 1rem;
  font-size: 0.92rem;
  color: #166534;
}

.text-green {
  color: #16a34a;
}

.table-wrap {
  overflow-x: auto;
  margin-top: 1rem;
}

.transit-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.92rem;
  text-align: left;
}

.transit-table th {
  background: var(--bg-subtle);
  padding: 0.75rem 1rem;
  font-weight: 700;
  color: var(--text-muted);
  border-bottom: 1px solid var(--border-color);
  font-size: 0.82rem;
  text-transform: uppercase;
}

.transit-table td {
  padding: 0.9rem 1rem;
  border-bottom: 1px solid var(--border-color);
  color: var(--text-body);
}

.policy-link {
  color: var(--primary);
  font-weight: 700;
  text-decoration: none;
}

.policy-link:hover {
  text-decoration: underline;
}

@media (max-width: 640px) {
  .policy-card { padding: 1.75rem 1.25rem; }
  .policy-header h1 { font-size: 1.85rem; }
}
</style>

