// frontend/app/plugins/auth.client.js
export default defineNuxtPlugin(async () => {
    const { refreshUser, initialized } = useAuthState()
    if (!initialized.value) {
        await refreshUser()
    }
})
