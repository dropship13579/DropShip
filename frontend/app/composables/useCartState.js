// frontend/app/composables/useCartState.js
import { useCartApi } from './useCartApi'

export const useCartState = () => {
    const cart = useState('cart_data', () => ({
        items: [],
        total_items: 0,
        subtotal: '0.00'
    }))
    const loading = useState('cart_loading', () => false)
    const cartApi = useCartApi()

    const refreshCart = async () => {
        try {
            loading.value = true
            const data = await cartApi.getCart()
            if (data) cart.value = data
        } catch (err) {
            console.error('Failed to fetch cart:', err)
        } finally {
            loading.value = false
        }
    }

    const addToCart = async (productId, quantity = 1) => {
        try {
            loading.value = true
            const updatedCart = await cartApi.addItem(productId, quantity)
            cart.value = updatedCart
            return { success: true }
        } catch (err) {
            return { success: false, error: err.message }
        } finally {
            loading.value = false
        }
    }

    const updateQuantity = async (itemId, quantity) => {
        try {
            loading.value = true
            const updatedCart = await cartApi.updateItem(itemId, quantity)
            cart.value = updatedCart
            return { success: true }
        } catch (err) {
            return { success: false, error: err.message }
        } finally {
            loading.value = false
        }
    }

    const removeItem = async (itemId) => {
        try {
            loading.value = true
            const updatedCart = await cartApi.removeItem(itemId)
            cart.value = updatedCart
            return { success: true }
        } catch (err) {
            return { success: false, error: err.message }
        } finally {
            loading.value = false
        }
    }

    return {
        cart,
        loading,
        totalItems: computed(() => cart.value?.total_items || 0),
        subtotal: computed(() => cart.value?.subtotal || '0.00'),
        items: computed(() => cart.value?.items || []),
        refreshCart,
        addToCart,
        updateQuantity,
        removeItem
    }
}
