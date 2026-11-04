// frontend/app/composables/useOrdersApi.js
import { useApi } from './useApi'

export const useOrdersApi = () => {
    const { fetchWithAuth } = useApi()

    const checkout = (payload) =>
        fetchWithAuth('/orders/checkout/', {
            method: 'POST',
            body: JSON.stringify(payload)
        })

    const validateCoupon = (code, subtotal) =>
        fetchWithAuth('/orders/coupons/validate/', {
            method: 'POST',
            body: JSON.stringify({ code, subtotal })
        })

    const getOrders = () => fetchWithAuth('/orders/')

    const getOrder = (orderNumber) => fetchWithAuth(`/orders/${orderNumber}/`)

    // Public shipment tracking lookup (order number + customer email)
    const trackOrderPublic = (orderNumber, email) =>
        fetchWithAuth('/orders/track/', {
            method: 'POST',
            body: JSON.stringify({ order_number: orderNumber, email })
        })

    return {
        checkout,
        validateCoupon,
        getOrders,
        getOrder,
        trackOrderPublic
    }
}
