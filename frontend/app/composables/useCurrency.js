// frontend/app/composables/useCurrency.js

export const useCurrency = () => {
  const currencies = {
    USD: { code: 'USD', symbol: '$', rate: 1.0, flag: '🇺🇸', name: 'US Dollar' },
    EUR: { code: 'EUR', symbol: '€', rate: 0.92, flag: '🇪🇺', name: 'Euro' },
    GBP: { code: 'GBP', symbol: '£', rate: 0.79, flag: '🇬🇧', name: 'British Pound' },
    CAD: { code: 'CAD', symbol: 'CA$', rate: 1.36, flag: '🇨🇦', name: 'Canadian Dollar' },
    AUD: { code: 'AUD', symbol: 'AU$', rate: 1.52, flag: '🇦🇺', name: 'Australian Dollar' },
    INR: { code: 'INR', symbol: '₹', rate: 83.2, flag: '🇮🇳', name: 'Indian Rupee' }
  }

  const selectedCurrency = useState('selectedCurrency', () => 'USD')

  if (import.meta.client) {
    const saved = localStorage.getItem('dropship_currency')
    if (saved && currencies[saved]) {
      selectedCurrency.value = saved
    }
  }

  const setCurrency = (code) => {
    if (currencies[code]) {
      selectedCurrency.value = code
      if (import.meta.client) {
        localStorage.setItem('dropship_currency', code)
      }
    }
  }

  const currentCurrency = computed(() => {
    return currencies[selectedCurrency.value] || currencies.USD
  })

  /**
   * Converts a base USD price to the current currency and returns formatted string
   */
  const format = (amountInUsd) => {
    const num = Number(amountInUsd)
    if (isNaN(num)) return `${currentCurrency.value.symbol}0.00`
    const converted = num * currentCurrency.value.rate
    return `${currentCurrency.value.symbol}${converted.toFixed(2)}`
  }

  return {
    currencies,
    selectedCurrency,
    currentCurrency,
    setCurrency,
    format
  }
}
