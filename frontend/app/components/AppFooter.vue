<!-- frontend/app/components/AppFooter.vue -->
<template>
  <footer class="app-footer">
    <div class="footer-container">
      <!-- Column 1: Brand Info -->
      <div class="footer-col brand-col">
        <NuxtLink to="/" class="footer-logo">
          <div class="footer-logo-mark">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.3">
              <path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"></path>
              <polyline points="3.27 6.96 12 12.01 20.73 6.96"></polyline>
              <line x1="12" y1="22.08" x2="12" y2="12"></line>
            </svg>
          </div>
          <span><span class="brand-text">Drop</span><span class="accent-text">Ship</span></span>
        </NuxtLink>

        <p class="brand-desc">
          Your trusted destination for curated tech, smart lifestyle accessories, and daily essentials delivered directly
          from audited global suppliers with zero retail markups.
        </p>

        <div class="footer-guarantee-badge">
          <span class="shield-icon"><i class="fa-solid fa-shield-halved"></i></span>
          <span>Verified Direct Supplier Network</span>
        </div>
      </div>

      <!-- Column 2: Shop Links -->
      <div class="footer-col">
        <h4>Catalog</h4>
        <ul class="footer-links">
          <li><NuxtLink to="/shop">All Products</NuxtLink></li>
          <li><NuxtLink to="/shop?sort=popular">Popular Items</NuxtLink></li>
          <li><NuxtLink to="/shop?sort=newest">New Arrivals</NuxtLink></li>
          <li><NuxtLink to="/shop?on_sale=true">Special Deals & Offers</NuxtLink></li>
          <li><NuxtLink to="/account/wishlist">Saved Wishlist</NuxtLink></li>
        </ul>
      </div>

      <!-- Column 3: Customer Care & Tracking -->
      <div class="footer-col">
        <h4>Customer Care</h4>
        <ul class="footer-links">
          <li><NuxtLink to="/track">Track Order Status</NuxtLink></li>
          <li><NuxtLink to="/cart">View Shopping Cart</NuxtLink></li>
          <li><NuxtLink to="/account">My Account & Orders</NuxtLink></li>
          <li><NuxtLink to="/shipping-policy">Shipping & Delivery Times</NuxtLink></li>
          <li><NuxtLink to="/returns-policy">30-Day Money-Back Policy</NuxtLink></li>
        </ul>
      </div>

      <!-- Column 4: Trust & Payment Badges -->
      <div class="footer-col payment-col">
        <h4>Safe & Secure Checkout</h4>
        <p class="payment-desc">
          All transactions are encrypted with 256-bit bank-grade SSL security. We partner with PCI-DSS compliant
          gateways.
        </p>

        <!-- Payment Method Badges -->
        <div class="payment-badges-grid">
          <span class="pay-chip">VISA</span>
          <span class="pay-chip">MC</span>
          <span class="pay-chip">AMEX</span>
          <span class="pay-chip">Apple Pay</span>
          <span class="pay-chip">PayPal</span>
          <span class="pay-chip">COD</span>
        </div>

        <div class="ssl-seal">
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
            <rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect>
            <path d="M7 11V7a5 5 0 0 1 10 0v4"></path>
          </svg>
          <span>256-Bit SSL Encrypted Verification</span>
        </div>
      </div>
    </div>

    <!-- Bottom Bar -->
    <div class="footer-bottom">
      <div class="footer-bottom-inner">
        <p class="copyright-text">
          &copy; {{ new Date().getFullYear() }} DropShip E-Commerce Platform. All rights reserved.
        </p>

        <div class="status-indicator">
          <span class="status-dot"></span>
          <span>Fulfillment Systems Online & Operating</span>
        </div>
      </div>
    </div>
  </footer>
</template>

<style scoped>
.app-footer {
  background: #0b0f19;
  color: #94a3b8;
  border-top: 1px solid #1e293b;
  margin-top: auto;
  font-size: 0.9rem;
}

.footer-container {
  max-width: 1240px;
  margin: 0 auto;
  padding: 4.5rem 1.5rem 3rem;
  display: grid;
  grid-template-columns: 2fr 1fr 1fr 1.5fr;
  gap: 3.5rem;
}

.footer-col h4 {
  font-family: 'Outfit', sans-serif;
  font-size: 1rem;
  font-weight: 700;
  color: #ffffff;
  margin-bottom: 1.25rem;
  letter-spacing: -0.01em;
}

/* Brand Col */
.footer-logo {
  display: inline-flex;
  align-items: center;
  gap: 0.6rem;
  font-family: 'Outfit', sans-serif;
  font-size: 1.45rem;
  font-weight: 800;
  color: #ffffff;
  margin-bottom: 1rem;
}

.footer-logo-mark {
  width: 32px;
  height: 32px;
  border-radius: var(--radius-xs);
  background: linear-gradient(135deg, #1d4ed8 0%, #2563eb 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
}

.accent-text {
  color: #38bdf8;
}

.brand-desc {
  color: #94a3b8;
  font-size: 0.88rem;
  line-height: 1.65;
  margin-bottom: 1.25rem;
  max-width: 340px;
}

.footer-guarantee-badge {
  display: inline-flex;
  align-items: center;
  gap: 0.45rem;
  background: rgba(30, 41, 59, 0.7);
  border: 1px solid #334155;
  padding: 0.4rem 0.75rem;
  border-radius: var(--radius-sm);
  font-size: 0.78rem;
  font-weight: 600;
  color: #cbd5e1;
}

/* Links */
.footer-links {
  list-style: none;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.footer-links li a {
  color: #94a3b8;
  font-size: 0.88rem;
  transition: all var(--transition-fast);
}

.footer-links li a:hover {
  color: #38bdf8;
  transform: translateX(2px);
  display: inline-block;
}

/* Payment Col */
.payment-desc {
  font-size: 0.84rem;
  color: #94a3b8;
  line-height: 1.55;
  margin-bottom: 1rem;
}

.payment-badges-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 0.4rem;
  margin-bottom: 1.25rem;
}

.pay-chip {
  background: #1e293b;
  border: 1px solid #334155;
  color: #f1f5f9;
  font-size: 0.72rem;
  font-weight: 700;
  padding: 0.25rem 0.55rem;
  border-radius: var(--radius-xs);
  letter-spacing: 0.04em;
}

.ssl-seal {
  display: inline-flex;
  align-items: center;
  gap: 0.45rem;
  color: #10b981;
  font-size: 0.78rem;
  font-weight: 600;
}

/* Bottom Bar */
.footer-bottom {
  border-top: 1px solid #1e293b;
  padding: 1.5rem 1.5rem;
  background: #070a12;
}

.footer-bottom-inner {
  max-width: 1240px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 1rem;
}

.copyright-text {
  font-size: 0.82rem;
  color: #64748b;
}

.status-indicator {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.78rem;
  color: #94a3b8;
}

.status-dot {
  width: 7px;
  height: 7px;
  border-radius: 50%;
  background: #10b981;
  box-shadow: 0 0 0 2px rgba(16, 185, 129, 0.25);
}

@media (max-width: 1024px) {
  .footer-container {
    grid-template-columns: 1fr 1fr;
    gap: 2.5rem;
  }
}

@media (max-width: 640px) {
  .footer-container {
    grid-template-columns: 1fr;
    padding: 3rem 1.25rem 2rem;
  }
  .footer-bottom-inner {
    flex-direction: column;
    align-items: flex-start;
  }
}
</style>
