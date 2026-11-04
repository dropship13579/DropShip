// frontend/app/composables/useApi.js
export const useApi = () => {
    const config = useRuntimeConfig()
    const baseURL = config.public.apiBase


    const getCsrfToken = () => {
        if (import.meta.server) {
            const reqHeaders = useRequestHeaders(['cookie'])
            const match = reqHeaders.cookie?.match(/csrftoken=([^;]+)/)
            return match ? match[1] : ''
        }
        const match = document.cookie.match(/csrftoken=([^;]+)/)
        return match ? match[1] : ''
    }

    const fetchWithAuth = async (endpoint, options = {}) => {
        const url = endpoint.startsWith('http') ? endpoint : `${baseURL}${endpoint}`
        const method = (options.method || 'GET').toUpperCase()

        const headers = {
            'Content-Type': 'application/json',
            Accept: 'application/json',
            ...(options.headers || {})
        }

        // Forward browser cookies during SSR requests to Django
        if (import.meta.server) {
            const reqHeaders = useRequestHeaders(['cookie'])
            if (reqHeaders.cookie) {
                headers['cookie'] = reqHeaders.cookie
            }
        }

        // Attach CSRF token on unsafe methods
        if (['POST', 'PUT', 'PATCH', 'DELETE'].includes(method)) {
            const csrfToken = getCsrfToken()
            if (csrfToken) {
                headers['X-CSRFToken'] = csrfToken
            }
        }

        const response = await fetch(url, {
            ...options,
            headers,
            credentials: 'include' // Always include session cookie
        })

        const data = await response.json().catch(() => null)

        if (!response.ok) {
            const error = new Error(data?.message || data?.detail || `HTTP Error ${response.status}`)
            error.status = response.status
            error.data = data
            throw error
        }

        return data
    }

    return {
        fetchWithAuth,
        getCsrfToken
    }
}
