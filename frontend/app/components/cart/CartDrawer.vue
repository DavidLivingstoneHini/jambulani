<template>
  <Transition name="fade">
    <div
      v-if="cartStore.isOpen"
      class="fixed inset-0 bg-black/50 z-40"
      @click="cartStore.isOpen = false"
    />
  </Transition>

  <Transition name="slide-right">
    <div
      v-if="cartStore.isOpen"
      class="fixed right-0 top-0 h-full w-full max-w-md bg-white z-50 flex flex-col shadow-2xl"
    >
      <!-- Header -->
      <div class="flex items-center justify-between px-4 py-4 border-b border-gray-200">
        <h2 class="font-body font-bold uppercase text-lg tracking-wider">
          Cart ({{ cartStore.itemCount }})
        </h2>
        <button class="p-2 hover:bg-gray-100 transition-colors" @click="cartStore.isOpen = false">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>

      <!-- Items -->
      <div class="flex-1 overflow-y-auto px-4 py-4">
        <div v-if="cartStore.cart.items.length === 0" class="text-center py-16 text-gray-400">
          <svg class="w-12 h-12 mx-auto mb-4 opacity-30" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 11-4 0 2 2 0 014 0z" />
          </svg>
          <p class="font-body font-semibold uppercase text-sm tracking-wide">Your cart is empty</p>
          <button class="mt-4 text-sm text-gray-500 underline font-body" @click="cartStore.isOpen = false">
            Continue Shopping
          </button>
        </div>

        <div v-else class="space-y-4">
          <div
            v-for="item in cartStore.cart.items"
            :key="item.id"
            class="flex gap-3 pb-4 border-b border-gray-100 last:border-0"
          >
            <div class="w-20 h-20 bg-gray-100 shrink-0 overflow-hidden">
              <img
                v-if="item.product.primary_image"
                :src="item.product.primary_image"
                :alt="item.product.name"
                class="w-full h-full object-cover"
              />
            </div>
            <div class="flex-1 min-w-0">
              <p class="font-body font-semibold text-sm leading-tight mb-1 line-clamp-2">{{ item.product.name }}</p>
              <p class="text-xs text-gray-500 font-body mb-0.5">Size: <span class="font-semibold">{{ item.size }}</span></p>
              <p v-if="item.custom_name" class="text-xs text-gray-500 font-body mb-0.5">Name: {{ item.custom_name }}</p>
              <p v-if="item.custom_number" class="text-xs text-gray-500 font-body mb-0.5">#{{ item.custom_number }}</p>
              <p v-if="item.patch" class="text-xs text-gray-500 font-body mb-1">Patch: {{ item.patch.name }}</p>
              <p class="font-body font-bold text-sm">€{{ item.subtotal }}</p>
            </div>
            <div class="flex flex-col items-end justify-between shrink-0">
              <button
                class="text-gray-400 hover:text-red-500 transition-colors p-1"
                @click="cartStore.removeItem(item.id)"
              >
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
              <div class="flex items-center border border-gray-200">
                <button
                  class="px-2 py-1 text-gray-500 hover:bg-gray-100 transition-colors text-sm"
                  @click="cartStore.updateQuantity(item.id, item.quantity - 1)"
                >−</button>
                <span class="px-3 py-1 text-sm font-body border-x border-gray-200 min-w-[2rem] text-center">{{ item.quantity }}</span>
                <button
                  class="px-2 py-1 text-gray-500 hover:bg-gray-100 transition-colors text-sm"
                  @click="cartStore.updateQuantity(item.id, item.quantity + 1)"
                >+</button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Footer -->
      <div v-if="cartStore.cart.items.length > 0" class="border-t border-gray-200 px-4 py-4 space-y-3">
        <div class="flex justify-between font-body font-bold uppercase text-base">
          <span>Total</span>
          <span>€{{ cartStore.cartTotal }}</span>
        </div>
        <NuxtLink
          to="/checkout"
          class="btn-primary w-full block text-center"
          @click="cartStore.isOpen = false"
        >
          Proceed to Checkout
        </NuxtLink>
        <button
          class="w-full text-center text-sm text-gray-500 underline font-body hover:text-gray-700 transition-colors"
          @click="cartStore.isOpen = false"
        >
          Continue Shopping
        </button>
      </div>
    </div>
  </Transition>
</template>

<script setup lang="ts">
const cartStore = useCartStore()
</script>

<style scoped>
.fade-enter-active, .fade-leave-active { transition: opacity 0.2s; }
.fade-enter-from, .fade-leave-to { opacity: 0; }

.slide-right-enter-active, .slide-right-leave-active { transition: transform 0.3s ease; }
.slide-right-enter-from, .slide-right-leave-to { transform: translateX(100%); }
</style>
