// frontend/app/middleware/guest.js
export default defineNuxtRouteMiddleware(async () => {
    const { user, initialized, refreshUser } = useAuthState()

    if (!initialized.value) {
        await refreshUser()
    }

    if (user.value) {
        return navigateTo(user.value.is_staff ? '/admin' : '/')
    }
})
