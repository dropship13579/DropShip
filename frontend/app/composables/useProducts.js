import { useApi } from './useApi'

export const useProducts = () => {
    const { fetchWithAuth } = useApi()

    const getCategories = async () => {
        return await fetchWithAuth('/categories/')
    }

    const getProducts = async (params = {}) => {
        const query = new URLSearchParams()

        if (params.search) query.append('search', params.search)
        if (params.category) query.append('category', params.category)
        if (params.sort) query.append('sort', params.sort)
        if (params.featured !== undefined && params.featured !== '') query.append('featured', params.featured)
        if (params.page) query.append('page', params.page)

        // Advanced Faceted Filters
        if (params.min_price !== undefined && params.min_price !== '') query.append('min_price', params.min_price)
        if (params.max_price !== undefined && params.max_price !== '') query.append('max_price', params.max_price)
        if (params.min_rating !== undefined && params.min_rating !== '') query.append('min_rating', params.min_rating)
        if (params.in_stock) query.append('in_stock', 'true')
        if (params.on_sale) query.append('on_sale', 'true')

        const queryString = query.toString() ? `?${query.toString()}` : ''
        return await fetchWithAuth(`/products/${queryString}`)
    }

    const getProductBySlug = async (slug) => {
        return await fetchWithAuth(`/products/${slug}/`)
    }

    const getProductReviews = async (slug) => {
        return await fetchWithAuth(`/products/${slug}/reviews/`)
    }

    // Alias for compatibility
    const getProductReview = getProductReviews

    const submitProductReview = async (slug, reviewData) => {
        return await fetchWithAuth(`/products/${slug}/reviews/`, {
            method: 'POST',
            body: JSON.stringify(reviewData)
        })
    }

    const deleteProductReview = async (slug, reviewId) => {
        return await fetchWithAuth(`/products/${slug}/reviews/${reviewId}/`, {
            method: 'DELETE'
        })
    }

    return {
        getCategories,
        getProducts,
        getProductBySlug,
        getProductReviews,
        getProductReview,
        submitProductReview,
        deleteProductReview
    }
}
