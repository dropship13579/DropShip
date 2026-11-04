// frontend/app/middleware/admin.js
export default defineNuxtRouteMiddleware(async (to) => {
    const { user, initialized, refreshUser } = useAuthState()

    if (!initialized.value) {
        await refreshUser()
    }

    if (!user.value) {
        return navigateTo({
            path: '/login',
            query: { redirect: to.fullPath }
        })
    }

    if (!user.value.is_staff) {
        return navigateTo('/')
    }
})
