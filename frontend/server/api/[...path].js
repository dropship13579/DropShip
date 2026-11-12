export default defineEventHandler(async (event) => {
    const config = useRuntimeConfig(event)

    const path = getRouterParam(event, 'path') || ''
    const query = getRequestURL(event).search

    const upstream = config.apiUpstream.replace(/\/+$/, '')
    const target = `${upstream}/api/${path}${query}`

    return proxyRequest(event, target)
})
