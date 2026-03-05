<template>
  <header class="sticky top-0 z-50 bg-white shadow-sm">
    <div class="topbar flex items-center justify-between p-0 w-full">
      <div class="lang-selector flex items-center cursor-pointer select-none px-5 py-2 md:px-12 shrink-0 z-10">
        <img src="/assets/icons/globe.svg" width="14" height="14" alt="" aria-hidden="true" />
        <span class="text-white uppercase mx-2 text-[10px] font-normal">EN</span>
        <img src="/assets/icons/chevron-down-white.svg" width="6" height="4" alt="" aria-hidden="true" />
      </div>

      <div class="flex-1 overflow-hidden">
        <p class="text-white text-center uppercase text-[8px] md:text-[10px] font-normal">
          SALES BEGIN · FREE SHIPPING ON ALL ORDERS
        </p>
      </div>

      <a
        href="https://wa.me/"
        target="_blank"
        class="whatsapp-btn bg-green-500 text-white flex items-center justify-center py-2 px-6 md:px-12 cursor-pointer shrink-0 relative md:relative hover:bg-green-600 transition-colors"
      >
        <img src="/assets/icons/whatsapp.svg" width="15" height="15" alt="" aria-hidden="true" />
        <span class="text-[10px] font-semibold mx-2 hidden md:block">Chat with us</span>
        <span class="text-[10px] font-semibold mx-2 md:hidden">Chat</span>
      </a>
    </div>

    <!-- Desktop nav -->
    <div class="hidden md:flex items-center w-full bg-white">
      <NuxtLink to="/" class="shrink-0 w-[145px] bg-primary flex items-center justify-center self-stretch">
        <span class="font-heading text-black text-lg leading-none tracking-wider"></span>
      </NuxtLink>

      <div class="flex-1">
        <div class="flex gap-px border-b border-gray-100">
          <div ref="collectionsMenuRef" class="relative flex items-center border-r border-slate-100 px-8 py-2 shrink-0 cursor-pointer hover:bg-slate-50" @click="collectionsMenuOpen = !collectionsMenuOpen">
            <span class="text-[12px] mr-2">All Collections</span>
            <img src="/assets/icons/chevron-down-dark.svg" width="6" height="4" alt="" aria-hidden="true" />
            <Transition name="fade-down">
              <div v-if="collectionsMenuOpen" class="absolute left-0 top-full mt-0 w-48 bg-white border border-gray-200 shadow-lg z-50 py-1">
                <NuxtLink to="/products" class="block px-4 py-2 text-sm font-body hover:bg-gray-50 transition-colors" @click="collectionsMenuOpen = false">All Categories</NuxtLink>
                <NuxtLink to="/products?category=tshirts" class="block px-4 py-2 text-sm font-body hover:bg-gray-50 transition-colors" @click="collectionsMenuOpen = false">T-Shirts</NuxtLink>
                <NuxtLink to="/products?category=tracksuits" class="block px-4 py-2 text-sm font-body hover:bg-gray-50 transition-colors" @click="collectionsMenuOpen = false">Tracksuits</NuxtLink>
                <NuxtLink to="/products?category=nba" class="block px-4 py-2 text-sm font-body hover:bg-gray-50 transition-colors" @click="collectionsMenuOpen = false">NBA</NuxtLink>
              </div>
            </Transition>
          </div>

          <!-- Search -->
          <div class="px-2 bg-white flex-grow flex items-center py-2 border-r border-slate-100">
            <input
              v-model="searchQuery"
              class="outline-none border-0 w-full placeholder:text-sm text-[13px] font-body"
              type="search"
              placeholder="What are you looking for?"
              @keydown.enter="handleSearch"
            />
            <div class="flex shrink-0">
              <button class="bg-primary px-4 py-2 text-[11px] font-body font-semibold" @click="handleSearch">Search</button>
              <button class="bg-black px-3 py-2 grid place-items-center mr-9" @click="handleSearch">
                <img src="/assets/icons/search-white.svg" width="14" height="14" alt="" aria-hidden="true" />
              </button>
            </div>
          </div>

          <button class="border-r border-slate-100 py-2 grid place-items-center px-7 hover:bg-slate-100 relative" @click="cartStore.isOpen = !cartStore.isOpen">
            <img src="/assets/icons/cart-dark.svg" width="20" height="20" alt="" aria-hidden="true" />
            <span v-if="cartStore.itemCount > 0" class="absolute -top-0.5 -right-0.5 bg-primary text-black text-[10px] font-bold w-4 h-4 rounded-full flex items-center justify-center">{{ cartStore.itemCount }}</span>
          </button>

          <div ref="accountMenuRef" class="relative flex items-center px-7 hover:bg-slate-100 cursor-pointer" @click="accountMenuOpen = !accountMenuOpen">
            <img src="/assets/icons/user.svg" class="mr-2" width="20" height="20" alt="" aria-hidden="true" />
            <img src="/assets/icons/chevron-down-dark.svg" width="6" height="4" alt="" aria-hidden="true" />

            <Transition name="fade-down">
              <div v-if="accountMenuOpen" class="absolute right-0 top-full mt-1 w-48 bg-white border border-gray-200 shadow-lg z-50 py-1">
                <template v-if="authStore.isAuthenticated">
                  <div class="px-4 py-2 border-b border-gray-100">
                    <p class="text-[11px] font-body text-gray-400">Signed in as</p>
                    <p class="text-sm font-body font-semibold truncate">{{ authStore.user?.email }}</p>
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

        <!-- Nav links row -->
        <nav class="flex items-center font-medium text-[12px] text-gray-700 pl-9 pt-1 cursor-pointer border-b border-slate-100">
          <NuxtLink
            to="/"
            class="mr-14 py-1 hover:font-bold hover:text-black"
            exact-active-class="text-black font-bold border-b-2 border-primary"
          >Home</NuxtLink>
          <div class="flex items-center mr-14 hover:font-bold hover:text-black">
            <NuxtLink to="/products">T-Shirts</NuxtLink>
            <img src="/assets/icons/chevron-down-gray.svg" class="ml-2" width="6" height="4" alt="" aria-hidden="true" />
          </div>
          <div class="flex items-center mr-14 hover:font-bold hover:text-black">
            <NuxtLink to="/products">NBA</NuxtLink>
            <img src="/assets/icons/chevron-down-gray.svg" class="ml-2" width="6" height="4" alt="" aria-hidden="true" />
          </div>
          <div class="flex items-center mr-14 hover:font-bold hover:text-black">
            <NuxtLink to="/products">Tracksuits</NuxtLink>
            <img src="/assets/icons/chevron-down-gray.svg" class="ml-2" width="6" height="4" alt="" aria-hidden="true" />
          </div>
          <NuxtLink to="/products" class="mr-14 hover:font-bold hover:text-black">Products Delivery · 1–2 days</NuxtLink>
          <NuxtLink to="/" class="mr-14 hover:font-bold hover:text-black">Contact</NuxtLink>
          <NuxtLink to="/" class="mr-14 hover:font-bold hover:text-black">Reviews</NuxtLink>
        </nav>
      </div>
    </div>

    <!-- Mobile nav -->
    <div class="md:hidden bg-white border-b border-gray-200">
      <div class="flex items-center justify-between px-5 py-3">
        <div class="flex items-center gap-6">
          <button @click="mobileMenuOpen = !mobileMenuOpen">
            <img src="/assets/icons/hamburger.svg" width="20" height="20" alt="Menu" />
          </button>
          <button @click="mobileSearchOpen = !mobileSearchOpen">
            <img src="/assets/icons/search-dark.svg" width="20" height="20" alt="Search" />
          </button>
        </div>

        <div class="flex items-center gap-6">
          <button class="relative" @click="cartStore.isOpen = !cartStore.isOpen">
            <img src="/assets/icons/cart-dark.svg" width="20" height="20" alt="" aria-hidden="true" />
            <span v-if="cartStore.itemCount > 0" class="absolute -top-1 -right-1 bg-primary text-black text-[10px] font-bold w-4 h-4 rounded-full flex items-center justify-center">{{ cartStore.itemCount }}</span>
          </button>
          <NuxtLink v-if="!authStore.isAuthenticated" to="/login">
            <img src="/assets/icons/user.svg" width="20" height="20" alt="Account" />
          </NuxtLink>
          <NuxtLink v-else to="/account">
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
        <button class="bg-primary px-3 py-1.5 font-body font-bold text-xs" @click="handleSearch">Go</button>
      </div>

      <!-- Mobile menu -->
      <div v-if="mobileMenuOpen" class="border-t border-gray-200 bg-white">
        <NuxtLink to="/" class="flex items-center px-4 py-3 text-sm font-body border-b border-gray-100" @click="mobileMenuOpen = false">Home</NuxtLink>
        <NuxtLink to="/products" class="flex items-center justify-between px-4 py-3 text-sm font-body border-b border-gray-100" @click="mobileMenuOpen = false">
          T-shirts
          <img src="/assets/icons/chevron-right-gray.svg" class="w-3 h-3" alt="" aria-hidden="true" />
        </NuxtLink>
        <NuxtLink to="/products" class="flex items-center justify-between px-4 py-3 text-sm font-body border-b border-gray-100" @click="mobileMenuOpen = false">
          NBA
          <img src="/assets/icons/chevron-right-gray.svg" class="w-3 h-3" alt="" aria-hidden="true" />
        </NuxtLink>
        <NuxtLink to="/products" class="flex items-center justify-between px-4 py-3 text-sm font-body border-b border-gray-100" @click="mobileMenuOpen = false">
          Tracksuits
          <img src="/assets/icons/chevron-right-gray.svg" class="w-3 h-3" alt="" aria-hidden="true" />
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

const cartStore = useCartStore()
const authStore = useAuthStore()
const router = useRouter()

const searchQuery = ref('')
const mobileMenuOpen = ref(false)
const mobileSearchOpen = ref(false)
const accountMenuOpen = ref(false)
const accountMenuRef = ref<HTMLElement | null>(null)
const collectionsMenuOpen = ref(false)
const collectionsMenuRef = ref<HTMLElement | null>(null)

onClickOutside(accountMenuRef, () => { accountMenuOpen.value = false })
onClickOutside(collectionsMenuRef, () => { collectionsMenuOpen.value = false })

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
.topbar {
  background-color: #111112;
}

.lang-selector {
  background-color: #1f2937;
}
@media (min-width: 768px) {
  .lang-selector {
    background-color: rgba(255, 255, 255, 0.08); 
  }
}

.fade-down-enter-active, .fade-down-leave-active {
  transition: opacity 0.15s, transform 0.15s;
}
.fade-down-enter-from, .fade-down-leave-to {
  opacity: 0;
  transform: translateY(-6px);
}
</style>