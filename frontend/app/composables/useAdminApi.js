// frontend/app/composables/useAdminApi.js
import { useApi } from './useApi'

export const useAdminApi = () => {
    const { fetchWithAuth } = useApi()

    // 1. Analytics & Business Metrics
    const getStats = () => fetchWithAuth('/admin/stats/')

    // 2. Orders Management
    const getOrders = (params = {}) => {
        const query = new URLSearchParams()
        if (params.status) query.append('status', params.status)
        if (params.payment_status) query.append('payment_status', params.payment_status)
        if (params.search) query.append('search', params.search)

        const qs = query.toString()
        return fetchWithAuth(`/admin/orders/${qs ? `?${qs}` : ''}`)
    }

    const getOrder = (orderNumber) => fetchWithAuth(`/admin/orders/${orderNumber}/`)

    const updateOrder = (orderNumber, data) =>
        fetchWithAuth(`/admin/orders/${orderNumber}/`, {
            method: 'PATCH',
            body: JSON.stringify(data)
        })

    // 3. Inventory Management
    const getProducts = () => fetchWithAuth('/admin/products/')

    const updateProduct = (id, data) =>
        fetchWithAuth(`/admin/products/${id}/`, {
            method: 'PATCH',
            body: JSON.stringify(data)
        })

    // 4. Supplier & Dropship Profit Margins
    const getSuppliers = () => fetchWithAuth('/admin/suppliers/')

    const createSupplier = (data) =>
        fetchWithAuth('/admin/suppliers/', {
            method: 'POST',
            body: JSON.stringify(data)
        })

    const updateSupplier = (id, data) =>
        fetchWithAuth(`/admin/suppliers/${id}/`, {
            method: 'PATCH',
            body: JSON.stringify(data)
        })

    const deleteSupplier = (id) =>
        fetchWithAuth(`/admin/suppliers/${id}/`, {
            method: 'DELETE'
        })

    const getProductSourcing = (params = {}) => {
        const query = new URLSearchParams()
        if (params.supplier) query.append('supplier', params.supplier)
        if (params.search) query.append('search', params.search)
        const qs = query.toString()
        return fetchWithAuth(`/admin/suppliers/sourcing/${qs ? `?${qs}` : ''}`)
    }

    const updateProductSourcing = (id, data) =>
        fetchWithAuth(`/admin/suppliers/sourcing/${id}/`, {
            method: 'PATCH',
            body: JSON.stringify(data)
        })

    return {
        getStats,
        getOrders,
        getOrder,
        updateOrder,
        getProducts,
        updateProduct,
        getSuppliers,
        createSupplier,
        updateSupplier,
        deleteSupplier,
        getProductSourcing,
        updateProductSourcing
    }
}
