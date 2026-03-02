<template>
  <NuxtLink :to="`/products/${product.slug}`" class="product-card group block">
    <div class="relative aspect-square bg-gray-100 overflow-hidden">
      <img
        v-if="product.primary_image"
        :src="product.primary_image"
        :alt="product.name"
        class="w-full h-full object-cover transition-transform duration-500 group-hover:scale-105"
        loading="lazy"
      />
      <div v-else class="w-full h-full flex items-center justify-center text-gray-300">
        <svg class="w-16 h-16" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
        </svg>
      </div>
      <div v-if="product.discount_percentage > 0" class="absolute top-2 left-2 badge-save">
        Save {{ product.discount_percentage }}%
      </div>
    </div>
    <div class="p-3">
      <p class="font-display font-semibold text-sm leading-tight mb-1 line-clamp-2">{{ product.name }}</p>
      <div class="flex items-center gap-2 flex-wrap">
        <span class="price-current">€{{ product.price }}</span>
        <span v-if="product.original_price" class="price-original">€{{ product.original_price }}</span>
      </div>
    </div>
  </NuxtLink>
</template>

<script setup lang="ts">
import type { ProductList } from '~/app/types'

defineProps<{ product: ProductList }>()
</script>
