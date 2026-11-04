// frontend/app/middleware/auth.js
export default defineNuxtRouteMiddleware(async () => {
    const { user, initialized, refreshUser } = useAuthState()

    if (!initialized.value) {
        await refreshUser()
    }

    if (!user.value) {
        return navigateTo('/login')
    }
})
