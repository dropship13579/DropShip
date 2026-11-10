// frontend/app/composables/useAuthApi.js
import { useApi } from './useApi'

export const useAuthApi = () => {
    const { fetchWithAuth, setCsrfToken } = useApi()

    const initCsrf = async () => {
        try {
            const res = await fetchWithAuth('/accounts/csrf/')
            if (res?.csrfToken) {
                setCsrfToken(res.csrfToken)
            }
            return res
        } catch (e) {
            return null
        }
    }
    const register = (payload) => fetchWithAuth('/accounts/register/', { method: 'POST', body: JSON.stringify(payload) })
    const login = (payload) => fetchWithAuth('/accounts/login/', { method: 'POST', body: JSON.stringify(payload) })
    const logout = () => fetchWithAuth('/accounts/logout/', { method: 'POST' })
    const fetchMe = () => fetchWithAuth('/accounts/me/')

    return {
        initCsrf,
        register,
        login,
        logout,
        fetchMe
    }
}
