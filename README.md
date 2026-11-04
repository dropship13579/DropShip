# DropShip — Full-Stack E-Commerce & Dropshipping Platform

A modern, high-performance Dropshipping platform powered by **Django REST Framework** (Python / MySQL) on the backend and **Nuxt 4 / Vue 3** on the frontend.

---

## 🚀 Key Features

### 🛒 Storefront & Customer Experience
- **Interactive Product Catalog**: Real-time filtering by category, price ranges (presets & custom min/max), customer rating threshold, in-stock availability, and deals.
- **Product Details & Gallery**: High-resolution image preview, specifications table, and stock status indicators.
- **Customer Reviews & Ratings**: 5-star rating system with percentage distribution bars and **Verified Purchase** badges.
- **Customer Wishlist**: Instant wishlist bookmarking with live navigation badges and dedicated wishlist manager.
- **Guest & Authenticated Cart**: Session-based cart with automatic merging on login, live quantity steppers, and stock limits.
- **3-Step Checkout**: Saved address picker, inline delivery address creation modal, promotional coupon validation (`WELCOME10`, `SAVE20`, `FLASH50`), and multiple payment methods (COD, Sandbox Card, Bank Transfer).
- **Public Parcel Tracking**: Live order lookup by Order Number & Email with a 4-stage visual timeline stepper and carrier tracking code copying.
- **Customer Account Dashboard**: Profile editing, saved shipping addresses, and full order history with per-order tracking.

### 💼 Dropship Backoffice & Admin Portal
- **Role-Based Dynamic Header**: Automatically converts the store navigation into the Admin Command Center for staff accounts (`is_staff=True`).
- **Real-Time Analytics & KPIs**: Gross revenue, 30-day sales, average order value (AOV), 7-day revenue trend chart, and order status distribution.
- **Order Fulfillment & Tracking**: Filter orders by status, change fulfillment stages (`pending` → `confirmed` → `processing` → `shipped` → `delivered`), and assign carrier tracking numbers.
- **Supplier & Margin Management**: Connect products with wholesale dropshipping suppliers (AliExpress, CJ Dropshipping, Spocket), track supplier costs, and monitor profit margin percentages.
- **Inventory Control**: Quick-edit retail pricing and inventory stock levels directly from the dashboard.

---

## 🛠️ Tech Stack

- **Backend**: Python 3.12, Django 5.x, Django REST Framework, MySQL / PyMySQL, Django CORS Headers.
- **Frontend**: Nuxt 4, Vue 3 (Composition API), Vite 8, Vanilla CSS Design System with Google Fonts (`Plus Jakarta Sans`).
- **Database**: MySQL database (`dropship_db`).

---

## ⚡ Quick Start & Development

### 1. Launch with One Click
Double-click `run_dev.bat` or run:
```cmd
.\run_dev.bat
```

### 2. Manual Server Startup

#### Backend (Django REST API):
```powershell
cd backend
..\venv\Scripts\activate
python manage.py runserver 127.0.0.1:8000
```
- API Base URL: `http://127.0.0.1:8000/api/`
- Django Admin: `http://127.0.0.1:8000/admin/`

#### Frontend (Nuxt 4 Storefront):
```powershell
cd frontend
npm run dev
```
- Storefront URL: `http://localhost:3000`

---

## 📦 Seeded Data & Coupons

- **Promotional Coupons**:
  - `WELCOME10`: 10% off (up to $25 off)
  - `SAVE20`: $20 off on orders over $50
  - `FLASH50`: 50% off (up to $30 off)
- **Wholesale Dropship Suppliers**:
  - CJ Dropshipping (Avg. 8 days delivery)
  - AliExpress Direct (Avg. 12 days delivery)
  - Spocket Global (Avg. 4 days delivery)
