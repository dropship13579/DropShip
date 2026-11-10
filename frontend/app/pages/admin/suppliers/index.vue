<!-- frontend/app/pages/admin/suppliers/index.vue -->
<script setup>
definePageMeta({
  middleware: [
    () => navigateTo('/admin/products', { replace: true })
  ]
})
</script>

<template>
  <div class="p-8 text-center text-slate-500">
    <p>Redirecting to Products Inventory...</p>
  </div>
</template>

