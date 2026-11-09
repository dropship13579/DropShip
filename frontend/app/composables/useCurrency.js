// frontend/app/composables/useCurrency.js

export const useCurrency = () => {
  // Locked to standard store currency (USD)
  const defaultCurrency = {
    code: 'USD',
    symbol: '$',
    rate: 1.0,
    name: 'US Dollar'
  }

  const selectedCurrency = useState('selectedCurrency', () => 'USD')

  if (import.meta.client) {
    // Clean up any previously stored currency overrides
    if (localStorage.getItem('dropship_currency')) {
      localStorage.removeItem('dropship_currency')
    }
    selectedCurrency.value = 'USD'
  }

  const currentCurrency = computed(() => defaultCurrency)

  /**
   * Formats USD price with dollar sign
   */
  const format = (amountInUsd) => {
    const num = Number(amountInUsd)
    if (isNaN(num)) return '$0.00'
    return `$${num.toFixed(2)}`
  }

  return {
    selectedCurrency,
    currentCurrency,
    format
  }
}
