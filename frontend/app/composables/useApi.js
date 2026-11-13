// frontend/app/composables/useApi.js
export const useApi = () => {
    const config = useRuntimeConfig()
    const baseURL = config.public.apiBase

    const csrfTokenState = useState('app_csrf_token', () => '')

    const setCsrfToken = (token) => {
        if (token) {
            csrfTokenState.value = token
        }
    }

    const getCsrfToken = () => {
        if (csrfTokenState.value) {
            return csrfTokenState.value
        }
        if (import.meta.server) {
            const reqHeaders = useRequestHeaders(['cookie'])
            const match = reqHeaders.cookie?.match(/csrftoken=([^;]+)/)
            return match ? match[1] : ''
        }
        if (typeof document !== 'undefined') {
            const match = document.cookie.match(/csrftoken=([^;]+)/)
            return match ? match[1] : ''
        }
        return ''
    }

    const fetchWithAuth = async (endpoint, options = {}) => {
        const url = endpoint.startsWith('http') ? endpoint : `${baseURL}${endpoint}`
        const method = (options.method || 'GET').toUpperCase()

        const isFormData = typeof FormData !== 'undefined' && options.body instanceof FormData

        const headers = {
            Accept: 'application/json',
            ...(options.headers || {})
        }

        if (!isFormData && !headers['Content-Type']) {
            headers['Content-Type'] = 'application/json'
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

	const requestFetch = useRequestFetch()

	try{
        	return await requestFetch(url, {
            	  ...options,
            	  headers,
            	  credentials: 'include' // Always include session cookie
        	})
	}catch(err){
        	const data = err.data || null

		const error = new Error(
			data?.message ||
			data?.detail ||
			err.message ||
			'API request failed'
		)

		error.status = err.statusCode || err.status
		error.data = data

		throw error
	}

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
        getCsrfToken,
        setCsrfToken
    }
}
