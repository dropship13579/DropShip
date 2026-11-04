// frontend/app/composables/useAuthApi.js
import { useApi } from './useApi'

export const useAuthApi = () => {
    const { fetchWithAuth } = useApi()

    const initCsrf = () => fetchWithAuth('/accounts/csrf/')
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
