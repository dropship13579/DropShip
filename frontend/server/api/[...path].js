export default defineEventHandler(async (event) => {
    const config = useRuntimeConfig(event)

    let path = getRouterParam(event, 'path') || ''
    const query = getRequestURL(event).search

    // Preserve Django's trailing-slash API convention
    if (path && !path.endsWith('/')) {
        path += '/'
    }

    const upstream = config.apiUpstream.replace(/\/+$/, '')
    const target = `${upstream}/api/${path}${query}`

    return proxyRequest(event, target)
})
