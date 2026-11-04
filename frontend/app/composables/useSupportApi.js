// frontend/app/composables/useSupportApi.js
export const useSupportApi = () => {
  const { fetchWithAuth } = useApi()

  /**
   * Submit a customer support inquiry/ticket.
   * payload: {
   *   name: string,
   *   email: string,
   *   subject: string,
   *   inquiry_type: 'product' | 'order' | 'return' | 'general',
   *   product_name?: string,
   *   order_number?: string,
   *   message: string
   * }
   */
  const submitInquiry = async (payload) => {
    return await fetchWithAuth('/accounts/support/', {
      method: 'POST',
      body: JSON.stringify(payload)
    })
  }

  return {
    submitInquiry
  }
}
