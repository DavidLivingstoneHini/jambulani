<template>
  <footer class="bg-gray-900 text-white pt-10 pb-6 mt-16">
    <div class="max-w-screen-xl mx-auto px-4">
      <div class="grid grid-cols-1 md:grid-cols-4 gap-8 mb-8">
        <div>
          <h3 class="font-display font-bold uppercase text-base tracking-wider mb-4">Main Menu</h3>
          <ul class="space-y-2">
            <li><NuxtLink to="/" class="footer-link">Home</NuxtLink></li>
            <li><NuxtLink to="/products" class="footer-link">T-shirts</NuxtLink></li>
            <li><NuxtLink to="/products" class="footer-link">NBA</NuxtLink></li>
            <li><NuxtLink to="/products" class="footer-link">Tracksuits</NuxtLink></li>
            <li><span class="footer-link">Products Delivery · 1–2 days</span></li>
            <li><NuxtLink to="/" class="footer-link">Contact</NuxtLink></li>
            <li><NuxtLink to="/" class="footer-link">Reviews</NuxtLink></li>
          </ul>
        </div>

        <div>
          <h3 class="font-display font-bold uppercase text-base tracking-wider mb-4">Secondary Menu</h3>
          <ul class="space-y-2">
            <li><NuxtLink to="/products" class="footer-link">Search</NuxtLink></li>
            <li><NuxtLink to="/" class="footer-link">Privacy policy</NuxtLink></li>
            <li><NuxtLink to="/" class="footer-link">Shipping Policy</NuxtLink></li>
            <li><NuxtLink to="/" class="footer-link">Returns Policy</NuxtLink></li>
            <li><NuxtLink to="/" class="footer-link">Terms of Service</NuxtLink></li>
          </ul>
        </div>

        <div>
          <h3 class="font-display font-bold uppercase text-base tracking-wider mb-4">Subscribe</h3>
          <p class="text-gray-400 text-sm mb-4 font-body">Subscribe to our mailing list to receive the latest news.</p>
          <form class="flex" @submit.prevent="handleSubscribe">
            <input
              v-model="email"
              type="email"
              placeholder="Email Address"
              class="flex-1 bg-gray-800 border border-gray-700 px-3 py-2 text-sm font-body text-white placeholder-gray-500 focus:outline-none focus:border-gray-500"
            />
            <button type="submit" class="bg-primary px-3 py-2 text-black hover:bg-primary-600 transition-colors">
              <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M10.293 3.293a1 1 0 011.414 0l6 6a1 1 0 010 1.414l-6 6a1 1 0 01-1.414-1.414L14.586 11H3a1 1 0 110-2h11.586l-4.293-4.293a1 1 0 010-1.414z" clip-rule="evenodd" />
              </svg>
            </button>
          </form>
          <p v-if="subscribeMsg" class="text-sm mt-2" :class="subscribeError ? 'text-red-400' : 'text-green-400'">
            {{ subscribeMsg }}
          </p>
        </div>

        <div>
          <h3 class="font-display font-bold uppercase text-base tracking-wider mb-4">Follow Us</h3>
          <div class="flex gap-2">
            <a href="#" class="bg-blue-600 p-2 hover:bg-blue-700 transition-colors">
              <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 24 24">
                <path d="M18 2h-3a5 5 0 00-5 5v3H7v4h3v8h4v-8h3l1-4h-4V7a1 1 0 011-1h3z" />
              </svg>
            </a>
            <a href="#" class="bg-sky-500 p-2 hover:bg-sky-600 transition-colors">
              <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 24 24">
                <path d="M23 3a10.9 10.9 0 01-3.14 1.53 4.48 4.48 0 00-7.86 3v1A10.66 10.66 0 013 4s-4 9 5 13a11.64 11.64 0 01-7 2c9 5 20 0 20-11.5a4.5 4.5 0 00-.08-.83A7.72 7.72 0 0023 3z" />
              </svg>
            </a>
            <a href="#" class="bg-gradient-to-br from-purple-600 via-pink-500 to-orange-400 p-2 hover:opacity-90 transition-opacity">
              <svg class="w-4 h-4 text-white" fill="currentColor" viewBox="0 0 24 24">
                <rect x="2" y="2" width="20" height="20" rx="5" ry="5" />
                <path fill="white" d="M16 11.37A4 4 0 1112.63 8 4 4 0 0116 11.37zm1.5-4.87h.01" />
              </svg>
            </a>
          </div>
        </div>
      </div>

      <div class="border-t border-gray-800 pt-6 flex flex-col md:flex-row items-center justify-between gap-4">
        <p class="text-gray-500 text-sm font-body">© 2021 Jambulani · All rights reserved</p>
        <div class="flex items-center gap-3 flex-wrap justify-center">
          <span class="text-gray-400 font-display text-xs font-bold">ApplePay</span>
          <span class="text-gray-400 font-display text-xs font-bold">BANK TRANSFER</span>
          <span class="text-gray-400 font-display text-xs font-bold">bitpay</span>
          <span class="text-gray-400 font-display text-xs font-bold">⬤⬤</span>
          <span class="text-gray-400 font-display text-xs font-bold">SEPA</span>
          <span class="text-gray-400 font-display text-xs font-bold">VISA</span>
        </div>
      </div>
    </div>
  </footer>
</template>

<script setup lang="ts">
const { apiFetch } = useApi()
const email = ref('')
const subscribeMsg = ref('')
const subscribeError = ref(false)

async function handleSubscribe() {
  if (!email.value) return
  subscribeMsg.value = ''
  subscribeError.value = false
  try {
    await apiFetch('/newsletter/subscribe/', {
      method: 'POST',
      body: JSON.stringify({ email: email.value }),
    })
    subscribeMsg.value = 'Successfully subscribed!'
    email.value = ''
  } catch (e: any) {
    subscribeError.value = true
    subscribeMsg.value = e?.data?.email?.[0] || 'Something went wrong.'
  }
}
</script>
