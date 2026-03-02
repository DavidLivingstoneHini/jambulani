<template>
  <header class="sticky top-0 z-50 bg-white shadow-sm">

    <!-- ① Announcement bar: black, full-width -->
    <div class="bg-black text-white text-xs py-1.5">
      <div class="flex items-center justify-between px-4 max-w-screen-xl mx-auto">
        <!-- Language selector -->
        <div class="flex items-center gap-1 cursor-pointer shrink-0 select-none">
          <svg class="w-3.5 h-3.5 text-white/80" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM4.332 8.027a6.012 6.012 0 011.912-2.706C6.512 5.73 6.5 5.862 6.5 6c0 1.105.8 2 2 2 .26 0 .52-.052.76-.164A7.01 7.01 0 019.5 8c0 1.664-.805 3.126-2.037 4.016a4 4 0 01-.63-2.366 4.007 4.007 0 01-.501-1.623zM10 16a5.99 5.99 0 01-3.377-1.038A4.006 4.006 0 0110 12c1.007 0 1.918.373 2.614.985A5.99 5.99 0 0110 16z" clip-rule="evenodd" />
          </svg>
          <span class="font-body font-medium text-xs">EN</span>
          <svg class="w-2.5 h-2.5 text-white/70" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" clip-rule="evenodd" />
          </svg>
        </div>

        <!-- Center announcement text -->
        <div class="flex-1 text-center font-body text-[11px] uppercase tracking-[0.15em] font-medium">
          SALES BEGIN · FREE SHIPPING ON ALL ORDERS
        </div>

        <!-- WhatsApp CTA -->
        <a
          href="https://wa.me/"
          target="_blank"
          class="bg-green-500 text-white px-3 py-1 flex items-center gap-1.5 font-body text-[11px] uppercase font-semibold shrink-0 hover:bg-green-600 transition-colors tracking-wide"
        >
          <svg class="w-3 h-3" fill="currentColor" viewBox="0 0 24 24">
            <path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51a9.928 9.928 0 00-.57-.01c-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413z" />
            <path d="M12 0C5.373 0 0 5.373 0 12c0 2.127.557 4.124 1.528 5.856L.057 24l6.303-1.649A11.935 11.935 0 0012 24c6.627 0 12-5.373 12-12S18.627 0 12 0zm0 21.818a9.8 9.8 0 01-4.998-1.366l-.358-.212-3.742.979 1.001-3.638-.233-.374A9.791 9.791 0 012.182 12C2.182 6.57 6.57 2.182 12 2.182S21.818 6.57 21.818 12 17.43 21.818 12 21.818z" />
          </svg>
          Chat with us
        </a>
      </div>
    </div>

    <!-- ② Desktop nav row: logo, category, search, cart, account -->
    <div class="hidden md:block bg-white border-b border-gray-200">
      <div class="max-w-screen-xl mx-auto px-4">

        <!-- Top utility row -->
        <div class="flex items-center h-[54px] gap-3">
          <!-- Logo -->
          <NuxtLink to="/" class="shrink-0">
            <div class="bg-primary px-3 py-2 h-full flex items-center">
              <span class="font-heading text-black text-xl leading-none tracking-wider">JAMBULANI</span>
            </div>
          </NuxtLink>

          <!-- Category dropdown -->
          <div class="relative shrink-0">
            <select class="border border-gray-300 text-[13px] pl-3 pr-8 py-2 font-body appearance-none cursor-pointer bg-white focus:outline-none h-[36px]">
              <option>All Categories</option>
              <option>T-Shirts</option>
              <option>Tracksuits</option>
              <option>NBA</option>
            </select>
            <div class="absolute right-2 top-1/2 -translate-y-1/2 pointer-events-none">
              <svg class="w-3 h-3 text-gray-500" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" clip-rule="evenodd" />
              </svg>
            </div>
          </div>

          <!-- Search bar -->
          <div class="flex flex-1">
            <input
              v-model="searchQuery"
              type="text"
              placeholder="What are you looking for?"
              class="flex-1 border border-gray-300 border-r-0 px-4 py-2 text-[13px] font-body focus:outline-none h-[36px]"
              @keydown.enter="handleSearch"
            />
            <button
              class="bg-primary px-5 py-2 font-display font-bold text-[13px] uppercase h-[36px] hover:bg-primary-600 transition-colors"
              @click="handleSearch"
            >Search</button>
            <button class="bg-black px-3 py-2 text-white h-[36px] hover:bg-gray-800 transition-colors" @click="handleSearch">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
              </svg>
            </button>
          </div>

          <!-- Spacer -->
          <div class="flex-1 max-w-[120px]" />

          <!-- Cart -->
          <button class="relative p-2 hover:text-primary transition-colors" @click="cartStore.isOpen = !cartStore.isOpen">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.75" d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 11-4 0 2 2 0 014 0z" />
            </svg>
            <span
              v-if="cartStore.itemCount > 0"
              class="absolute -top-0.5 -right-0.5 bg-primary text-black text-[10px] font-bold w-4 h-4 rounded-full flex items-center justify-center"
            >{{ cartStore.itemCount }}</span>
          </button>

          <!-- Account dropdown -->
          <div ref="accountMenuRef" class="relative">
            <button
              class="p-2 flex items-center gap-1 hover:text-primary transition-colors"
              @click="accountMenuOpen = !accountMenuOpen"
            >
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.75" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
              </svg>
              <svg class="w-3 h-3 text-gray-500" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" clip-rule="evenodd" />
              </svg>
            </button>

            <Transition name="fade-down">
              <div v-if="accountMenuOpen" class="absolute right-0 top-full mt-1 w-48 bg-white border border-gray-200 shadow-lg z-50 py-1">
                <template v-if="authStore.isAuthenticated">
                  <div class="px-4 py-2 border-b border-gray-100">
                    <p class="text-[11px] font-body text-gray-400">Signed in as</p>
                    <p class="text-sm font-display font-semibold truncate">{{ authStore.user?.email }}</p>
                  </div>
                  <NuxtLink to="/account" class="block px-4 py-2 text-sm font-body hover:bg-gray-50 transition-colors" @click="accountMenuOpen = false">My Account</NuxtLink>
                  <button class="w-full text-left px-4 py-2 text-sm font-body text-red-500 hover:bg-red-50 transition-colors border-t border-gray-100" @click="handleLogout">Sign Out</button>
                </template>
                <template v-else>
                  <NuxtLink to="/login" class="block px-4 py-2 text-sm font-body hover:bg-gray-50 transition-colors" @click="accountMenuOpen = false">Sign In</NuxtLink>
                  <NuxtLink to="/register" class="block px-4 py-2 text-sm font-body hover:bg-gray-50 transition-colors" @click="accountMenuOpen = false">Create Account</NuxtLink>
                </template>
              </div>
            </Transition>
          </div>
        </div>

        <!-- Bottom nav links -->
        <nav class="flex items-center gap-6 pb-2">
          <NuxtLink to="/" class="nav-link font-medium" exact-active-class="text-black font-semibold">Home</NuxtLink>
          <NuxtLink to="/products" class="nav-link font-medium flex items-center gap-0.5">
            T-Shirts
            <svg class="w-3 h-3 mt-0.5 text-gray-400" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" clip-rule="evenodd" /></svg>
          </NuxtLink>
          <NuxtLink to="/products" class="nav-link font-medium flex items-center gap-0.5">
            NBA
            <svg class="w-3 h-3 mt-0.5 text-gray-400" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" clip-rule="evenodd" /></svg>
          </NuxtLink>
          <NuxtLink to="/products" class="nav-link font-medium flex items-center gap-0.5">
            Tracksuits
            <svg class="w-3 h-3 mt-0.5 text-gray-400" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" clip-rule="evenodd" /></svg>
          </NuxtLink>
          <NuxtLink to="/products" class="nav-link font-medium">Products Delivery · 1–2 days</NuxtLink>
          <NuxtLink to="/" class="nav-link font-medium">Contact</NuxtLink>
          <NuxtLink to="/" class="nav-link font-medium">Reviews</NuxtLink>
        </nav>

      </div>
    </div>

    <!-- ③ Mobile nav -->
    <div class="md:hidden bg-white border-b border-gray-200">
      <div class="flex items-center justify-between px-4 h-12 relative">
        <button class="p-1" @click="mobileMenuOpen = !mobileMenuOpen">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
          </svg>
        </button>

        <NuxtLink to="/" class="absolute left-1/2 -translate-x-1/2">
          <div class="bg-primary px-2 py-1.5">
            <span class="font-heading text-black text-base tracking-wider">JAMBULANI</span>
          </div>
        </NuxtLink>

        <div class="flex items-center gap-2">
          <!-- Mobile search icon -->
          <button class="p-1" @click="mobileSearchOpen = !mobileSearchOpen">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
            </svg>
          </button>
          <!-- Cart -->
          <button class="relative p-1" @click="cartStore.isOpen = !cartStore.isOpen">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.75" d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 11-4 0 2 2 0 014 0z" />
            </svg>
            <span v-if="cartStore.itemCount > 0" class="absolute -top-0.5 -right-0.5 bg-primary text-black text-[10px] font-bold w-4 h-4 rounded-full flex items-center justify-center">{{ cartStore.itemCount }}</span>
          </button>
          <!-- Account -->
          <NuxtLink v-if="!authStore.isAuthenticated" to="/login" class="p-1">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.75" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
            </svg>
          </NuxtLink>
          <NuxtLink v-else to="/account" class="p-1">
            <div class="w-7 h-7 bg-primary flex items-center justify-center font-heading text-black text-sm">
              {{ authStore.user?.first_name?.[0]?.toUpperCase() ?? 'U' }}
            </div>
          </NuxtLink>
        </div>
      </div>

      <!-- Mobile search bar -->
      <div v-if="mobileSearchOpen" class="flex border-t border-gray-200 px-4 py-2 gap-2">
        <input
          v-model="searchQuery"
          type="text"
          placeholder="What are you looking for?"
          class="flex-1 border border-gray-300 px-3 py-1.5 text-sm font-body focus:outline-none"
          @keydown.enter="handleSearch"
        />
        <button class="bg-primary px-3 py-1.5 font-display font-bold text-xs uppercase" @click="handleSearch">Go</button>
      </div>

      <!-- Mobile menu -->
      <div v-if="mobileMenuOpen" class="border-t border-gray-200 bg-white">
        <NuxtLink to="/" class="flex items-center px-4 py-3 text-sm font-body border-b border-gray-100" @click="mobileMenuOpen = false">Home</NuxtLink>
        <NuxtLink to="/products" class="flex items-center justify-between px-4 py-3 text-sm font-body border-b border-gray-100" @click="mobileMenuOpen = false">
          T-shirts
          <svg class="w-3 h-3 text-gray-400" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z" clip-rule="evenodd" /></svg>
        </NuxtLink>
        <NuxtLink to="/products" class="flex items-center justify-between px-4 py-3 text-sm font-body border-b border-gray-100" @click="mobileMenuOpen = false">
          NBA
          <svg class="w-3 h-3 text-gray-400" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z" clip-rule="evenodd" /></svg>
        </NuxtLink>
        <NuxtLink to="/products" class="flex items-center justify-between px-4 py-3 text-sm font-body border-b border-gray-100" @click="mobileMenuOpen = false">
          Tracksuits
          <svg class="w-3 h-3 text-gray-400" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z" clip-rule="evenodd" /></svg>
        </NuxtLink>
        <NuxtLink to="/products" class="flex items-center px-4 py-3 text-sm font-body border-b border-gray-100" @click="mobileMenuOpen = false">Products Delivery · 1–2 days</NuxtLink>
        <NuxtLink to="/" class="flex items-center px-4 py-3 text-sm font-body border-b border-gray-100" @click="mobileMenuOpen = false">Contact</NuxtLink>
        <NuxtLink to="/" class="flex items-center px-4 py-3 text-sm font-body border-b border-gray-100" @click="mobileMenuOpen = false">Reviews</NuxtLink>
        <div class="border-t border-gray-200 mt-1">
          <template v-if="authStore.isAuthenticated">
            <NuxtLink to="/account" class="flex items-center px-4 py-3 text-sm font-body" @click="mobileMenuOpen = false">My Account</NuxtLink>
            <button class="flex items-center w-full px-4 py-3 text-sm font-body text-red-500" @click="handleLogout">Sign Out</button>
          </template>
          <template v-else>
            <NuxtLink to="/login" class="flex items-center px-4 py-3 text-sm font-body" @click="mobileMenuOpen = false">Sign In</NuxtLink>
            <NuxtLink to="/register" class="flex items-center px-4 py-3 text-sm font-body" @click="mobileMenuOpen = false">Create Account</NuxtLink>
          </template>
        </div>
      </div>
    </div>

  </header>
</template>

<script setup lang="ts">
import { onClickOutside } from '@vueuse/core'

const cartStore = useCartStore()
const authStore = useAuthStore()
const router = useRouter()

const searchQuery = ref('')
const mobileMenuOpen = ref(false)
const mobileSearchOpen = ref(false)
const accountMenuOpen = ref(false)
const accountMenuRef = ref<HTMLElement | null>(null)

onClickOutside(accountMenuRef, () => { accountMenuOpen.value = false })

function handleSearch() {
  const q = searchQuery.value.trim()
  if (q) {
    router.push(`/products?search=${encodeURIComponent(q)}`)
    mobileMenuOpen.value = false
    mobileSearchOpen.value = false
    searchQuery.value = ''
  }
}

async function handleLogout() {
  accountMenuOpen.value = false
  mobileMenuOpen.value = false
  await authStore.logout()
  router.push('/')
}
</script>

<style scoped>
.fade-down-enter-active, .fade-down-leave-active { transition: opacity 0.15s, transform 0.15s; }
.fade-down-enter-from, .fade-down-leave-to { opacity: 0; transform: translateY(-6px); }
</style>
