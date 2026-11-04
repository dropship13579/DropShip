<template>
    <footer class="app-footer">
        <div class="footer-container">
            <div class="footer-col brand">
                <span class="footer-logo">
                    <span class="accent">Drop</span>Ship
                </span>

                <p class="brand-sec">
                    Your modern destination for premium curated gadgets, smart lifestyle accessories, and essentials.
                </p>
            </div>

            <div class="footer-col">
                <h4>Shop</h4>
                <ul>
                    <li><NuxtLink to="/shop">All Products</NuxtLink></li>
                    <li><NuxtLink to="/shop?sort=popular">Popular</NuxtLink></li>
                    <li><NuxtLink to="/shop?sort=newest">New Arrivals</NuxtLink></li>
                </ul>
            </div>

            <div class="footer-col">
                <h4>Customer Care</h4>
                <ul>
                    <li><NuxtLink to="/shipping-policy">Shipping Policy</NuxtLink></li>
                    <li><NuxtLink to="/returns-policy">Returns & Refunds</NuxtLink></li>
                    <li><NuxtLink to="/contact">Contact</NuxtLink></li>
                </ul>
            </div>

            <div class="footer-col">
                <h4>Legal</h4>
                <ul>
                    <li><NuxtLink to="/privacy-policy">Privacy Policy</NuxtLink></li>
                    <li><NuxtLink to="/terms">Terms of service</NuxtLink></li>
                </ul>
            </div>
        </div>

        <div class="footer-bottom">
            <p>&copy; {{ new Date().getFullYear() }} DropShip E-Commerce. All rights reserved.</p>
        </div>
    </footer>
</template>

<style scoped>
    .app-footer{
        background: var(--bg-surface);
        border-top: 1px solid var(--border-color);
        margin-top: auto;
    }

    .footer-container{
        max-width: 1200px;
        margin: 0 auto;
        padding: 4rem 1.5rem 2.5rem;
        display: grid;
        grid-template-columns: 2fr repeat(3, 1fr);
        gap: 3rem;
    }

    .footer-logo{
        font-size: 1.35rem;
        font-weight: 800;
        color: var(--text-main);
        display: inline-block;
        margin-bottom: 0.75rem;
    }

    .accent{
        color: var(--primary);
    }

    .brand-desc{
        color: var(--text-muted);
        font-size: 0.9rem;
        line-height: 1.6;
        max-width: 320px;
    }

    h4{
        font-size: 0.95rem;
        font-weight: 700;
        margin-bottom: 1rem;
    }

    ul{
        list-style: none;
        display: flex;
        flex-direction: column;
        gap: 0.65rem;
    }

    li a{
        color: var(--text-muted);
        font-size: 0.9rem;
        transition: color 0.15s;
    }

    li a:hover{
        color: var(--primary);
    }

    .footer-bottom{
        border-top: 1px solid var(--border-color);
        text-align: center;
        padding: 1.5rem;
        color: var(--text-muted);
        font-size: 0.85rem;
    }

    @media (max-width: 768px){
        .footer-container{
            grid-template-columns: 1fr;
            gap: 2rem;
            padding: 2.5rem 1.5rem 1.5rem;
        }
    }

</style>