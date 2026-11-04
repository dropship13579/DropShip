// frontend/app/composables/useAuthState.js
import { useAuthApi } from './useAuthApi'

export const useAuthState = () => {
    const user = useState('auth_user', () => null)
    const initialized = useState('auth_initialized', () => false)
    const loading = useState('auth_loading', () => false)

    const authApi = useAuthApi()

    const setUser = (userData) => {
        user.value = userData
    }

    const refreshUser = async () => {
        try {
            loading.value = true
            const res = await authApi.fetchMe()
            user.value = res?.user || null
        } catch (err) {
            user.value = null
        } finally {
            initialized.value = true
            loading.value = false
        }
    }

    const login = async (credentials) => {
        await authApi.initCsrf()
        const res = await authApi.login(credentials)
        user.value = res.user
        return res
    }

    const register = async (userData) => {
        await authApi.initCsrf()
        const res = await authApi.register(userData)
        user.value = res.user
        return res
    }

    const logout = async () => {
        try {
            await authApi.logout()
        } finally {
            user.value = null
            navigateTo('/login')
        }
    }

    return {
        user,
        initialized,
        loading,
        setUser,
        refreshUser,
        login,
        register,
        logout,
        isAuthenticated: computed(() => !!user.value),
        isAdmin: computed(() => !!user.value?.is_staff)
    }
}
