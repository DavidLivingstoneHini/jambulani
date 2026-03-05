<template>
  <NuxtLink :to="`/products/${product?.slug || '#'}`" class="product-card group block border border-gray-200 hover:border-gray-300 transition-colors">
    <div class="relative bg-gray-100 overflow-hidden" style="aspect-ratio: 1/1;">
      <img
        v-if="product?.primary_image"
        :src="product.primary_image"
        :alt="product?.name || 'Product image'"
        class="w-full h-full object-cover transition-transform duration-500 group-hover:scale-105"
        loading="lazy"
      />

      <div v-else class="w-full h-full flex items-center justify-center bg-gray-100">
        <img src="/assets/icons/image-placeholder.svg" class="w-14 h-14 opacity-30" alt="" aria-hidden="true" />
      </div>

      <div
        v-if="product?.discount_percentage && product.discount_percentage > 0"
        class="absolute top-2 left-2 bg-green-500 text-white text-[10px] font-bold px-1.5 py-0.5 uppercase font-display"
      >
        Save {{ product.discount_percentage }}%
      </div>
    </div>

    <div class="px-2 py-3 pt-2 pb-3">
      <p class="font-display font-[400] text-[12px] md:text-[14px] leading-[1.3] text-[#393A38] line-clamp-2 mb-1">
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