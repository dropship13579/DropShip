// frontend/app/composables/useCartApi.js
import { useApi } from './useApi'

export const useCartApi = () => {
    const { fetchWithAuth } = useApi()

    // Fetch the current user or guest cart
    const getCart = () => fetchWithAuth('/cart/')

    // Add product to cart
    const addItem = (productId, quantity = 1) =>
        fetchWithAuth('/cart/items/', {
            method: 'POST',
            body: JSON.stringify({ product_id: productId, quantity })
        })

    // Update item quantity
    const updateItem = (itemId, quantity) =>
        fetchWithAuth(`/cart/items/${itemId}/`, {
            method: 'PATCH',
            body: JSON.stringify({ quantity })
        })

    // Remove single item
    const removeItem = (itemId) =>
        fetchWithAuth(`/cart/items/${itemId}/remove/`, {
            method: 'DELETE'
        })

    // Clear all items
    const clearCart = () =>
        fetchWithAuth('/cart/clear/', {
            method: 'POST'
        })

    return {
        getCart,
        addItem,
        updateItem,
        removeItem,
        clearCart
    }
}
