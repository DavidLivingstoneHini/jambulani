<template>
  <footer class="bg-[#f4f4f0] text-gray-800 border-t border-gray-200 mt-10">
    <div class="max-w-screen-xl mx-auto px-4 pt-10 pb-6">

      <!-- 4-column grid -->
      <div class="grid grid-cols-2 md:grid-cols-4 gap-8 mb-8">

        <!-- Main Menu -->
        <div>
          <h3 class="font-display font-bold uppercase text-[13px] tracking-[0.1em] text-gray-900 mb-4">Main Menu</h3>
          <ul class="space-y-2">
            <li><NuxtLink to="/" class="footer-link-dark">Home</NuxtLink></li>
            <li><NuxtLink to="/products" class="footer-link-dark">T-shirts</NuxtLink></li>
            <li><NuxtLink to="/products" class="footer-link-dark">NBA</NuxtLink></li>
            <li><NuxtLink to="/products" class="footer-link-dark">Tracksuits</NuxtLink></li>
            <li><span class="footer-link-dark">Products Delivery · 1–2 days</span></li>
            <li><NuxtLink to="/" class="footer-link-dark">Contact</NuxtLink></li>
            <li><NuxtLink to="/" class="footer-link-dark">Reviews</NuxtLink></li>
          </ul>
        </div>

        <!-- Secondary Menu -->
        <div>
          <h3 class="font-display font-bold uppercase text-[13px] tracking-[0.1em] text-gray-900 mb-4">Secondary Menu</h3>
          <ul class="space-y-2">
            <li><NuxtLink to="/products" class="footer-link-dark">Search</NuxtLink></li>
            <li><NuxtLink to="/" class="footer-link-dark">Privacy policy</NuxtLink></li>
            <li><NuxtLink to="/" class="footer-link-dark">Shipping Policy</NuxtLink></li>
            <li><NuxtLink to="/" class="footer-link-dark">Returns Policy</NuxtLink></li>
            <li><NuxtLink to="/" class="footer-link-dark">Terms of Service</NuxtLink></li>
          </ul>
        </div>

        <!-- Subscribe -->
        <div>
          <h3 class="font-display font-bold uppercase text-[13px] tracking-[0.1em] text-gray-900 mb-4">Subscribe</h3>
          <p class="text-gray-500 text-[13px] mb-3 font-body leading-snug">
            Subscribe to our mailing list to receive the latest news.
          </p>
          <div class="flex">
            <input
              v-model="email"
              type="email"
              placeholder="Email Address"
              class="flex-1 border border-gray-300 bg-white px-3 py-2 text-[13px] font-body text-gray-800 placeholder-gray-400 focus:outline-none focus:border-gray-500 min-w-0"
              @keydown.enter="handleSubscribe"
            />
            <button
              class="bg-primary px-3 py-2 text-black hover:bg-primary-600 transition-colors shrink-0"
              @click="handleSubscribe"
            >
              <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M10.293 3.293a1 1 0 011.414 0l6 6a1 1 0 010 1.414l-6 6a1 1 0 01-1.414-1.414L14.586 11H3a1 1 0 110-2h11.586l-4.293-4.293a1 1 0 010-1.414z" clip-rule="evenodd" />
              </svg>
            </button>
          </div>
          <p v-if="subscribeMsg" class="text-[12px] mt-1.5" :class="subscribeError ? 'text-red-500' : 'text-green-600'">
            {{ subscribeMsg }}
          </p>
        </div>

        <!-- Follow Us -->
        <div>
          <h3 class="font-display font-bold uppercase text-[13px] tracking-[0.1em] text-gray-900 mb-4">Follow Us</h3>
          <div class="flex gap-2">
            <a href="#" aria-label="Facebook" class="bg-[#1877f2] p-2 hover:brightness-110 transition-all">
              <svg class="w-4 h-4 text-white" fill="currentColor" viewBox="0 0 24 24">
                <path d="M18 2h-3a5 5 0 00-5 5v3H7v4h3v8h4v-8h3l1-4h-4V7a1 1 0 011-1h3z" />
              </svg>
            </a>
            <a href="#" aria-label="Twitter" class="bg-[#1da1f2] p-2 hover:brightness-110 transition-all">
              <svg class="w-4 h-4 text-white" fill="currentColor" viewBox="0 0 24 24">
                <path d="M23 3a10.9 10.9 0 01-3.14 1.53 4.48 4.48 0 00-7.86 3v1A10.66 10.66 0 013 4s-4 9 5 13a11.64 11.64 0 01-7 2c9 5 20 0 20-11.5a4.5 4.5 0 00-.08-.83A7.72 7.72 0 0023 3z" />
              </svg>
            </a>
            <a href="#" aria-label="Instagram" class="p-2 hover:brightness-110 transition-all" style="background:linear-gradient(45deg,#f09433,#e6683c,#dc2743,#cc2366,#bc1888)">
              <svg class="w-4 h-4 text-white" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                <rect x="2" y="2" width="20" height="20" rx="5" ry="5" />
                <circle cx="12" cy="12" r="4" />
                <circle cx="17.5" cy="6.5" r="1" fill="white" stroke="none" />
              </svg>
            </a>
          </div>
        </div>

      </div>

      <!-- Bottom bar: copyright + payment icons -->
      <div class="border-t border-gray-200 pt-5 flex flex-col md:flex-row items-center justify-between gap-4">
        <p class="text-gray-500 text-[12px] font-body">© 2021 Jambulani · All rights reserved</p>

        <!-- Payment logos (text-based matching the design) -->
        <div class="flex items-center gap-4 flex-wrap justify-center">
          <span class="text-gray-500 text-[11px] font-body font-semibold tracking-wide">Apple Pay</span>
          <span class="text-gray-500 text-[11px] font-body font-semibold tracking-wide uppercase">Bank Transfer</span>
          <span class="text-gray-500 text-[11px] font-body font-semibold">bitpay</span>
          <!-- Mastercard circles -->
          <div class="flex items-center -space-x-1.5">
            <div class="w-6 h-6 rounded-full bg-red-500 opacity-90" />
            <div class="w-6 h-6 rounded-full bg-yellow-400 opacity-90" />
          </div>
          <span class="text-gray-500 text-[11px] font-body font-semibold tracking-wide uppercase">SEPA</span>
          <span class="text-gray-500 text-[11px] font-body font-semibold tracking-wide">VISA</span>
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
  if (!email.value.trim()) return
  subscribeMsg.value = ''
  subscribeError.value = false
  try {
    await apiFetch('/newsletter/subscribe/', {
      method: 'POST',
      body: JSON.stringify({ email: email.value }),
    })
    subscribeMsg.value = 'Successfully subscribed!'
    email.value = ''
  } catch (e: unknown) {
    subscribeError.value = true
    const err = e as Record<string, unknown>
    const emailErrors = (err?.data as Record<string, string[]>)?.email
    subscribeMsg.value = emailErrors?.[0] ?? 'Something went wrong.'
  }
}
</script>

<style scoped>
.footer-link-dark {
  @apply text-gray-500 text-[13px] font-body hover:text-gray-900 transition-colors duration-150;
}
</style>
