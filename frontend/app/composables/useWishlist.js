// frontend/app/composables/useWishlist.js
import { useApi } from './useApi'
import { useAuthState } from './useAuthState'

export const useWishlist = () => {
    const { fetchWithAuth } = useApi()
    const { isAuthenticated } = useAuthState()

    // Global reactive state shared across components
    const wishlistItems = useState('wishlist_items', () => [])
    const wishlistIds = useState('wishlist_ids', () => [])
    const loading = useState('wishlist_loading', () => false)

    const totalWishlist = computed(() => wishlistIds.value.length)

    const isWishlisted = (productId) => {
        return wishlistIds.value.includes(productId)
    }

    const fetchWishlist = async () => {
        if (!isAuthenticated.value) {
            wishlistItems.value = []
            wishlistIds.value = []
            return
        }

        loading.value = true
        try {
            const data = await fetchWithAuth('/products/wishlist/')
            wishlistItems.value = data.items || []
            wishlistIds.value = data.ids || []
        } catch (err) {
            console.error('Failed to load wishlist:', err)
        } finally {
            loading.value = false
        }
    }

    const toggleWishlist = async (productId) => {
        if (!isAuthenticated.value) {
            // Redirect to login if guest clicks heart
            const route = useRoute()
            return navigateTo(`/login?redirect=${encodeURIComponent(route.fullPath)}`)
        }

        const currentlyWishlisted = isWishlisted(productId)

        // Optimistic UI update for instant feedback
        if (currentlyWishlisted) {
            wishlistIds.value = wishlistIds.value.filter(id => id !== productId)
            wishlistItems.value = wishlistItems.value.filter(item => item.product?.id !== productId)
        } else {
            wishlistIds.value = [...wishlistIds.value, productId]
        }

        try {
            const res = await fetchWithAuth('/products/wishlist/toggle/', {
                method: 'POST',
                body: JSON.stringify({ product_id: productId })
            })

            // Sync with server confirmation
            if (res.wishlisted) {
                if (!wishlistIds.value.includes(productId)) {
                    wishlistIds.value.push(productId)
                }
            } else {
                wishlistIds.value = wishlistIds.value.filter(id => id !== productId)
            }
        } catch (err) {
            console.error('Wishlist toggle error:', err)
            // Revert on error
            await fetchWishlist()
        }
    }

    return {
        wishlistItems,
        wishlistIds,
        totalWishlist,
        loading,
        isWishlisted,
        fetchWishlist,
        toggleWishlist
    }
}
