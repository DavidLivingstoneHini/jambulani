<template>
  <NuxtLink :to="`/products/${product?.slug || '#'}`" class="product-card group block">
    <!-- Image container -->
    <div class="relative bg-gray-100 overflow-hidden" style="aspect-ratio: 1/1;">
      <img
        v-if="product?.primary_image"
        :src="product.primary_image"
        :alt="product?.name || 'Product image'"
        class="w-full h-full object-cover transition-transform duration-500 group-hover:scale-105"
        loading="lazy"
      />

      <div v-else class="w-full h-full flex items-center justify-center bg-gray-100">
        <svg class="w-14 h-14 text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
        </svg>
      </div>

      <div
        v-if="product?.discount_percentage && product.discount_percentage > 0"
        class="absolute top-2 left-2 bg-green-500 text-white text-[10px] font-bold px-1.5 py-0.5 uppercase font-display"
      >
        Save {{ product.discount_percentage }}%
      </div>
    </div>

    <div class="pt-2 pb-1">
      <p class="font-display font-semibold text-[12px] leading-[1.3] text-gray-800 line-clamp-2 mb-1">
        {{ product?.name || 'Product' }}
      </p>
      <div class="flex items-baseline gap-1.5 flex-wrap">
        <span class="font-display font-bold text-[16px] text-gray-900">€{{ product?.price || '0.00' }}</span>
        <span v-if="product?.original_price" class="text-red-500 line-through text-[12px] font-body">
          €{{ product.original_price }}
        </span>
      </div>
    </div>
  </NuxtLink>
</template>

<script setup lang="ts">
import type { ProductList } from '~/app/types'

defineProps<{ 
  product?: ProductList | null 
}>()
</script>