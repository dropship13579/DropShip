// frontend/app/composables/useAccountApi.js
import { useApi } from './useApi'

export const useAccountApi = () => {
    const { fetchWithAuth } = useApi()

    // Profile endpoints
    const getProfile = () => fetchWithAuth('/accounts/profile/')

    const updateProfile = (data) =>
        fetchWithAuth('/accounts/profile/', {
            method: 'PATCH',
            body: JSON.stringify(data)
        })

    const changePassword = (passwordData) => fetchWithAuth('/accounts/change/password/', {
        method: 'POST',
        body: JSON.stringify(passwordData)
    })

    // Address endpoints
    const getAddresses = () => fetchWithAuth('/accounts/addresses/')

    const addAddress = (addressData) =>
        fetchWithAuth('/accounts/addresses/', {
            method: 'POST',
            body: JSON.stringify(addressData)
        })

    const updateAddress = (id, addressData) =>
        fetchWithAuth(`/accounts/addresses/${id}/`, {
            method: 'PATCH',
            body: JSON.stringify(addressData)
        })

    const deleteAddress = (id) =>
        fetchWithAuth(`/accounts/addresses/${id}/`, {
            method: 'DELETE'
        })

    return {
        getProfile,
        updateProfile,
        changePassword,
        getAddresses,
        addAddress,
        updateAddress,
        deleteAddress
    }
}
