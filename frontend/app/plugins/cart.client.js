// frontend/app/plugins/cart.client.js
export default defineNuxtPlugin(async () => {
    const { refreshCart } = useCartState()
    await refreshCart()
})
