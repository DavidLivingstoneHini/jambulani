<template>
  <footer class="bg-[#f5f5f6]">

    <div class="md:grid grid-cols-4 gap-4 py-16 flex flex-col px-[34px]">

      <!-- Main Menu -->
      <div>
        <p class="text-[12px] text-[#111112] font-bold mb-5 capitalize">Main Menu</p>
        <ul class="text-[12px] font-medium text-[#111112] cursor-pointer">
          <li class="mb-3"><NuxtLink to="/" class="hover:underline">Home</NuxtLink></li>
          <li class="mb-3"><NuxtLink to="/products" class="hover:underline">T-shirts</NuxtLink></li>
          <li class="mb-3"><NuxtLink to="/products" class="hover:underline">NBA</NuxtLink></li>
          <li class="mb-3"><NuxtLink to="/products" class="hover:underline">Tracksuits</NuxtLink></li>
          <li class="mb-3">Products Delivery · 1–2 days</li>
          <li class="mb-3"><NuxtLink to="/" class="hover:underline">Contact</NuxtLink></li>
          <li class="mb-3"><NuxtLink to="/" class="hover:underline">Reviews</NuxtLink></li>
        </ul>
      </div>

      <!-- Secondary Menu -->
      <div>
        <p class="text-[12px] text-[#111112] font-bold mb-5 capitalize">Secondary Menu</p>
        <ul class="text-[12px] font-medium text-[#111112] cursor-pointer">
          <li class="mb-3"><NuxtLink to="/products" class="hover:underline">Search</NuxtLink></li>
          <li class="mb-3"><NuxtLink to="/" class="hover:underline">Privacy policy</NuxtLink></li>
          <li class="mb-3"><NuxtLink to="/" class="hover:underline">Shipping Policy</NuxtLink></li>
          <li class="mb-3"><NuxtLink to="/" class="hover:underline">Returns Policy</NuxtLink></li>
          <li class="mb-3"><NuxtLink to="/" class="hover:underline">Terms of Services</NuxtLink></li>
        </ul>
      </div>

      <!-- Subscribe -->
      <div>
        <p class="text-[12px] text-[#111112] font-bold mb-5 capitalize">Subscribe</p>
        <p class="text-[12px] font-medium text-[#111112] cursor-pointer">
          Subscribe to our mailing list to receive the latest news.
        </p>
        <div class="mt-3 flex items-center">
          <input
            v-model="email"
            type="email"
            class="bg-white outline-none border-[lightgray] border-[0.5px] py-2 px-7 placeholder:text-[13px]"
            placeholder="Email address"
            @keydown.enter="handleSubscribe"
          />
          <button class="bg-primary py-3 px-4 mr-2" @click="handleSubscribe">
            <svg width="16" height="16" viewBox="0 0 12 12" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M0.00571428 12L12 6L0.00571428 0L0 4.66667L8.57143 6L0 7.33333L0.00571428 12Z" fill="#111112" />
            </svg>
          </button>
        </div>
        <p v-if="subscribeMsg" class="text-[12px] mt-1.5" :class="subscribeError ? 'text-red-500' : 'text-green-600'">
          {{ subscribeMsg }}
        </p>
      </div>

      <!-- Follow Us -->
      <div class="md:pl-12">
        <p class="text-[12px] text-[#111112] font-bold mb-5 capitalize">Follow Us</p>
        <div class="flex items-center mt-3">
          <a href="#" aria-label="Facebook" class="bg-black py-2 px-3 mr-2 hover:opacity-80 transition-opacity">
            <svg width="9" height="18" viewBox="0 0 9 18" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path fill-rule="evenodd" clip-rule="evenodd" d="M5.66764 17.4077V8.70281H8.07056L8.389 5.70307H5.66764L5.67172 4.20167C5.67172 3.41929 5.74606 3.00008 6.86978 3.00008H8.37198V0H5.96873C3.08203 0 2.06598 1.4552 2.06598 3.90238V5.70341H0.266602V8.70315H2.06598V17.4077H5.66764Z" fill="white" />
            </svg>
          </a>
          <a href="#" aria-label="Twitter" class="bg-black py-2 px-2 mr-2 hover:opacity-80 transition-opacity">
            <svg width="18" height="18" viewBox="0 0 18 14" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M8.32769 4.32321L8.36126 4.87685L7.80168 4.80906C5.7648 4.54919 3.98532 3.66789 2.47444 2.18776L1.73579 1.45334L1.54554 1.99568C1.14264 3.20464 1.40004 4.4814 2.23942 5.3401C2.68709 5.81464 2.58636 5.88243 1.81414 5.59997C1.54554 5.50958 1.31051 5.44178 1.28813 5.47568C1.20979 5.55477 1.47839 6.58295 1.69103 6.98971C1.98201 7.55464 2.57517 8.10828 3.22429 8.43594L3.77268 8.69581L3.12356 8.70711C2.49683 8.70711 2.47444 8.71841 2.54159 8.95568C2.76543 9.69009 3.64957 10.4697 4.63444 10.8087L5.32832 11.0459L4.72397 11.4075C3.82864 11.9272 2.77662 12.221 1.7246 12.2436C1.22098 12.2549 0.806885 12.3001 0.806885 12.334C0.806885 12.447 2.17227 13.0797 2.96688 13.3283C5.3507 14.0627 8.1822 13.7463 10.3086 12.4922C11.8195 11.5996 13.3304 9.82568 14.0354 8.10828C14.416 7.19308 14.7965 5.52088 14.7965 4.71867C14.7965 4.19893 14.83 4.13114 15.4568 3.50971C15.8261 3.14815 16.173 2.7527 16.2402 2.63971C16.3521 2.42503 16.3409 2.42503 15.7702 2.61711C14.8189 2.95607 14.6846 2.91088 15.1546 2.40244C15.5015 2.04088 15.9156 1.38555 15.9156 1.19347C15.9156 1.15958 15.7478 1.21607 15.5575 1.31776C15.3561 1.43075 14.9084 1.60023 14.5726 1.70192L13.9683 1.89399L13.4199 1.52114C13.1177 1.31776 12.6924 1.09179 12.4686 1.02399C11.8978 0.865812 11.0249 0.88841 10.5101 1.06919C9.1111 1.57763 8.22696 2.88828 8.32769 4.32321Z" fill="white" />
            </svg>
          </a>
          <a href="#" aria-label="Instagram" class="bg-black py-2 px-2 mr-2 hover:opacity-80 transition-opacity">
            <svg width="18" height="18" viewBox="0 0 18 18" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path fill-rule="evenodd" clip-rule="evenodd" d="M5.48232 0.518231C6.39255 0.476809 6.6834 0.466675 9.00093 0.466675H8.99827C11.3165 0.466675 11.6063 0.476809 12.5165 0.518231C13.425 0.559832 14.0454 0.703655 14.5894 0.914679C15.1512 1.13246 15.6259 1.42402 16.1006 1.89869C16.5752 2.37301 16.8668 2.8491 17.0855 3.41035C17.2952 3.95293 17.4392 4.57303 17.4819 5.48148C17.5228 6.39171 17.5335 6.68256 17.5335 9.0001C17.5335 11.3176 17.5228 11.6078 17.4819 12.518C17.4392 13.4261 17.2952 14.0464 17.0855 14.5891C16.8668 15.1502 16.5752 15.6263 16.1006 16.1006C15.6264 16.5753 15.151 16.8676 14.59 17.0855C14.047 17.2965 13.4262 17.4404 12.5178 17.482C11.6075 17.5234 11.3176 17.5335 8.99986 17.5335C6.68251 17.5335 6.39184 17.5234 5.48161 17.482C4.57333 17.4404 3.95306 17.2965 3.41012 17.0855C2.84922 16.8676 2.37313 16.5753 1.89899 16.1006C1.4245 15.6263 1.13294 15.1502 0.914801 14.589C0.703955 14.0464 0.560132 13.4263 0.518353 12.5178C0.477108 11.6076 0.466797 11.3176 0.466797 9.0001C0.466797 6.68256 0.477464 6.39154 0.518175 5.4813C0.559064 4.57321 0.703066 3.95293 0.914624 3.41017C1.13329 2.8491 1.42485 2.37301 1.89952 1.89869C2.37384 1.4242 2.84993 1.13264 3.41118 0.914679C3.95377 0.703655 4.57386 0.559832 5.48232 0.518231ZM8.23541 2.00447C8.38405 2.00424 8.54396 2.00431 8.71652 2.00439L9.00093 2.00447C11.2794 2.00447 11.5494 2.01265 12.4491 2.05354C13.2812 2.09158 13.7327 2.2306 14.0335 2.34741C14.4317 2.50207 14.7157 2.68696 15.0142 2.98563C15.3128 3.2843 15.4977 3.56875 15.6527 3.96698C15.7695 4.26743 15.9087 4.71899 15.9466 5.55099C15.9875 6.45056 15.9964 6.72079 15.9964 8.99814C15.9964 11.2755 15.9875 11.5457 15.9466 12.4453C15.9086 13.2773 15.7695 13.7289 15.6527 14.0293C15.4981 14.4275 15.3128 14.7111 15.0142 15.0096C14.7155 15.3083 14.4319 15.4931 14.0335 15.6478C13.7331 15.7651 13.2812 15.9038 12.4491 15.9419C11.5496 15.9827 11.2794 15.9916 9.00093 15.9916C6.72233 15.9916 6.45228 15.9827 5.55272 15.9419C4.72071 15.9035 4.26915 15.7644 3.96817 15.6476C3.56994 15.493 3.28549 15.3081 2.98682 15.0094C2.68815 14.7107 2.50326 14.427 2.34824 14.0286C2.23144 13.7281 2.09224 13.2766 2.05437 12.4446C2.01348 11.545 2.0053 11.2748 2.0053 8.99601C2.0053 6.71723 2.01348 6.44843 2.05437 5.54886C2.09241 4.71685 2.23144 4.26529 2.34824 3.96449C2.50291 3.56626 2.68815 3.28182 2.98682 2.98315C3.28549 2.68448 3.56994 2.49959 3.96817 2.34456C4.26897 2.22723 4.72071 2.08856 5.55272 2.05034C6.33993 2.01478 6.645 2.00411 8.23541 2.00234V2.00447ZM12.532 4.44503C12.532 3.87951 12.9907 3.42137 13.556 3.42137C14.1213 3.42137 14.58 3.87969 14.58 4.44503C14.58 5.01037 14.1213 5.46904 13.556 5.46904C12.9907 5.46904 12.532 5.01037 12.532 4.44503ZM4.61866 9.0001C4.61866 6.57998 6.58082 4.61783 9.00093 4.61783C11.421 4.61783 13.3825 6.57998 13.3825 9.0001C13.3825 11.4202 11.421 13.3815 9.00093 13.3815C6.58082 13.3815 4.61866 11.4202 4.61866 9.0001ZM11.8454 9.0001C11.8454 7.42906 10.5718 6.15562 9.00093 6.15562C7.42989 6.15562 6.15646 7.42906 6.15646 9.0001C6.15646 10.571 7.42989 11.8446 9.00093 11.8446C10.5718 11.8446 11.8454 10.571 11.8454 9.0001Z" fill="white" />
            </svg>
          </a>
        </div>
      </div>

    </div>

    <!-- Bottom bar -->
    <div class="px-[34px] grid grid-cols-1 md:flex items-center justify-between py-2 bg-[#f5f5f6]">
      <p class="text-[12px] text-[#111112]">© 2021 Jambulani · All rights reserved</p>
      <img src="/assets/images/partners.png" alt="partners" />
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
