<template>
  <NuxtLink :to="`/products/${product?.slug || '#'}`" v-bind="$attrs" class="product-card group block border border-gray-200 hover:border-gray-300 transition-colors">
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
        class="absolute bottom-2 left-2 bg-green-500 text-white text-[10px] font-bold px-[8px] py-[4px] uppercase font-body"
      >
        Save {{ product.discount_percentage }}%
      </div>
    </div>

    <div class="px-2 py-3 pt-4 pb-3">
      <p class="font-body font-[400] text-[14px] leading-[1.3] text-[#393A38] line-clamp-2 mb-1">
        {{ product?.name || 'Product' }}
      </p>
      <div class="flex items-baseline gap-1.5 flex-wrap">
        <span class="font-body font-bold text-[20px] text-gray-900">€{{ product?.price || '0.00' }}</span>
        <span v-if="product?.original_price" class="text-red-500 line-through text-[12px] font-body">
          €{{ product.original_price }}
        </span>
      </div>
    </div>
  </NuxtLink>
</template>

<script setup lang="ts">
import type { ProductList } from '~/app/types'

defineOptions({ inheritAttrs: false })

defineProps<{
  product?: ProductList | null
}>()
</script>