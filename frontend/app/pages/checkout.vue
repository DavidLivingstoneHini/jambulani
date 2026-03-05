<template>
  <div class="max-w-screen-xl mx-auto px-4 py-10">
    <nav class="text-sm font-body mb-6 text-gray-500">
      <NuxtLink to="/" class="hover:text-gray-900">Home</NuxtLink>
      <span class="mx-2">›</span>
      <span class="text-gray-900">Checkout</span>
    </nav>

    <h1 class="font-body font-bold uppercase text-2xl mb-8">Checkout</h1>

    <div class="grid grid-cols-1 md:grid-cols-2 gap-10">
      <div class="order-2 md:order-1">
        <h2 class="font-body font-bold uppercase text-base tracking-wider mb-4 border-b border-gray-200 pb-2">Order Summary</h2>
        <div v-if="cartStore.cart.items.length === 0" class="text-gray-400 text-sm font-body py-6 text-center">
          Your cart is empty. <NuxtLink to="/products" class="underline">Shop now</NuxtLink>
        </div>
        <div v-else>
          <div v-for="item in cartStore.cart.items" :key="item.id" class="flex items-center gap-3 mb-3 pb-3 border-b border-gray-100">
            <div class="w-16 h-16 bg-gray-100 shrink-0 overflow-hidden">
              <img v-if="item.product.primary_image" :src="item.product.primary_image" :alt="item.product.name" class="w-full h-full object-cover" />
            </div>
            <div class="flex-1 min-w-0">
              <p class="font-body font-semibold text-sm line-clamp-1">{{ item.product.name }}</p>
              <p class="text-xs text-gray-500 font-body">{{ item.size }} × {{ item.quantity }}</p>
            </div>
            <p class="font-body font-bold text-sm shrink-0">€{{ item.subtotal }}</p>
          </div>
          <div class="flex justify-between font-body font-bold text-base pt-2">
            <span>Total</span>
            <span>€{{ cartStore.cartTotal }}</span>
          </div>
        </div>
      </div>

      <div class="order-1 md:order-2">
        <h2 class="font-body font-bold uppercase text-base tracking-wider mb-4 border-b border-gray-200 pb-2">Contact Information</h2>
        <div class="bg-yellow-50 border border-yellow-200 p-3 mb-4 text-sm text-yellow-800 font-body">
          Demo checkout form
        </div>
        <div class="space-y-3">
          <input type="text" placeholder="Full Name" class="form-input" />
          <input type="email" placeholder="Email Address" class="form-input" />
          <input type="tel" placeholder="Phone Number" class="form-input" />
          <input type="text" placeholder="Shipping Address" class="form-input" />
          <input type="text" placeholder="City" class="form-input" />
          <input type="text" placeholder="Postal Code" class="form-input" />
          <button class="btn-primary w-full py-4 text-base mt-2">Place Order</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
const cartStore = useCartStore()
useHead({ title: 'Checkout — Jambulani' })
</script>
