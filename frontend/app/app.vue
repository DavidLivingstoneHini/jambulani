<template>
  <div>
    <NuxtLayout>
      <NuxtPage />
    </NuxtLayout>
  </div>
</template>

<script setup lang="ts">
const cartStore = useCartStore()

onMounted(() => {
  cartStore.fetchCart()
})
</script>
