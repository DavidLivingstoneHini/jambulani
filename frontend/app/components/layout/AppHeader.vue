<template>
  <header class="sticky top-0 z-50 bg-white shadow-sm">

    <!-- Announcement bar -->
    <div class="topbar flex items-center justify-between p-0 w-full">

      <!-- Language selector -->
      <div class="lang-selector flex items-center cursor-pointer select-none px-5 py-2 md:px-12 shrink-0 z-10">
        <svg class="w-3.5 h-3.5 text-white/80" fill="currentColor" viewBox="0 0 20 20">
          <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM4.332 8.027a6.012 6.012 0 011.912-2.706C6.512 5.73 6.5 5.862 6.5 6c0 1.105.8 2 2 2 .26 0 .52-.052.76-.164A7.01 7.01 0 019.5 8c0 1.664-.805 3.126-2.037 4.016a4 4 0 01-.63-2.366 4.007 4.007 0 01-.501-1.623zM10 16a5.99 5.99 0 01-3.377-1.038A4.006 4.006 0 0110 12c1.007 0 1.918.373 2.614.985A5.99 5.99 0 0110 16z" clip-rule="evenodd" />
        </svg>
        <span class="text-white uppercase mx-2 text-[10px] font-normal">EN</span>
        <svg width="6" height="4" viewBox="0 0 6 4" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M3.36728 3.60241C3.16932 3.81671 2.83068 3.81671 2.63272 3.60241L0.311188 1.08928C0.0153625 0.769035 0.242499 0.25 0.678465 0.25L5.32154 0.25C5.7575 0.25 5.98464 0.769036 5.68881 1.08928L3.36728 3.60241Z" fill="white" />
        </svg>
      </div>

      <div class="flex-1 overflow-hidden">
        <p class="text-white text-center uppercase text-[10px] font-normal">
          SALES BEGIN · FREE SHIPPING ON ALL ORDERS
        </p>
      </div>

      <!-- WhatsApp CTA -->
      <a
        href="https://wa.me/"
        target="_blank"
        class="whatsapp-btn bg-green-500 text-white flex items-center justify-center py-2 px-6 md:px-12 cursor-pointer shrink-0 relative md:relative hover:bg-green-600 transition-colors"
      >
        <svg width="15" height="15" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M14.582 11.9842C14.3338 11.8602 13.1099 11.2601 12.8818 11.178C12.6537 11.095 12.4879 11.054 12.3221 11.3021C12.1563 11.5491 11.6791 12.1082 11.5334 12.2733C11.3887 12.4383 11.243 12.4583 10.9948 12.3343C10.2613 12.0436 9.58432 11.628 8.99417 11.106C8.44988 10.6052 7.98325 10.0268 7.60952 9.38964C7.46483 9.14158 7.59445 9.00755 7.71905 8.88452C7.83058 8.7735 7.96824 8.59546 8.09184 8.45043C8.1942 8.32522 8.27811 8.18612 8.34103 8.03733C8.37414 7.96896 8.38956 7.89343 8.38587 7.81762C8.38219 7.7418 8.35952 7.66811 8.31993 7.60324C8.25763 7.47921 7.76025 6.25993 7.55325 5.76382C7.35128 5.28172 7.1463 5.34673 6.99256 5.33873C6.84787 5.33173 6.68207 5.32973 6.51628 5.32973C6.39016 5.33323 6.26613 5.36267 6.15199 5.4162C6.03786 5.46974 5.93609 5.54621 5.85309 5.6408C5.57177 5.90599 5.34901 6.22661 5.19902 6.58222C5.04903 6.93783 4.97509 7.32064 4.98191 7.70626C5.0626 8.6407 5.41567 9.53135 5.99779 10.2688C7.06483 11.8612 8.52957 13.15 10.2482 14.0087C10.7118 14.2069 11.1853 14.3812 11.667 14.5308C12.1748 14.6842 12.7116 14.7175 13.2345 14.6278C13.5809 14.558 13.9089 14.4174 14.1979 14.2149C14.4869 14.0124 14.7306 13.7525 14.9136 13.4515C15.0768 13.0814 15.1271 12.6717 15.0583 12.2733C14.997 12.1693 14.8312 12.1082 14.582 11.9842ZM17.086 2.90318C15.3778 1.20315 13.1071 0.178983 10.6967 0.0213433C8.28639 -0.136297 5.90062 0.583338 3.9836 2.04627C2.06658 3.5092 0.748953 5.61573 0.276019 7.97369C-0.196916 10.3316 0.207076 12.7803 1.41278 14.8639L0 20L5.27934 18.6227C6.7395 19.4141 8.37558 19.8288 10.0382 19.829H10.0422C12.0117 19.828 13.9368 19.2459 15.5742 18.1563C17.2115 17.0667 18.4877 15.5185 19.2415 13.7072C19.9953 11.8959 20.1928 9.90288 19.8092 7.9799C19.4255 6.05692 18.4779 4.29028 17.086 2.90317V2.90318ZM14.4403 16.8953C13.1221 17.7178 11.5979 18.1542 10.0422 18.1546H10.0382C8.55597 18.1545 7.10107 17.7575 5.82596 17.0053L5.52351 16.8273L2.39047 17.6455L3.22649 14.6048L3.03055 14.2927C2.16092 12.9123 1.72205 11.3061 1.76943 9.67735C1.81681 8.0486 2.34832 6.47042 3.29674 5.14236C4.24517 3.81429 5.56791 2.796 7.09771 2.21624C8.62752 1.63649 10.2957 1.5213 11.8912 1.88525C13.4868 2.2492 14.9381 3.07594 16.0617 4.26093C17.1852 5.44593 17.9305 6.93595 18.2034 8.54258C18.4762 10.1492 18.2643 11.8003 17.5945 13.2871C16.9247 14.7738 15.827 16.0295 14.4403 16.8953Z" fill="white"/>
        </svg>
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

          <!-- All Collections dropdown -->
          <div ref="collectionsMenuRef" class="relative flex items-center border-r border-slate-100 px-8 py-2 shrink-0 cursor-pointer hover:bg-slate-50" @click="collectionsMenuOpen = !collectionsMenuOpen">
            <span class="text-[12px] mr-2">All Collections</span>
            <svg width="6" height="4" viewBox="0 0 6 4" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M3.36728 3.60241C3.16932 3.81671 2.83068 3.81671 2.63272 3.60241L0.311188 1.08928C0.0153625 0.769035 0.242499 0.25 0.678465 0.25L5.32154 0.25C5.7575 0.25 5.98464 0.769036 5.68881 1.08928L3.36728 3.60241Z" fill="#111112" />
            </svg>
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
      <button class="bg-primary px-4 py-2 text-[11px] font-body font-semibold" @click="handleSearch">
        Search
      </button>
      <button class="bg-black px-3 py-2 grid place-items-center mr-9" @click="handleSearch">
        <svg width="14" height="14" viewBox="0 0 14 14" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path fill-rule="evenodd" clip-rule="evenodd" d="M11.2907 10.3433C12.2088 9.24903 12.7616 7.83803 12.7616 6.2979C12.7616 2.81967 9.94191 5.9873e-07 6.46368 0C2.98544 1.52039e-07 0.165771 2.81967 0.165771 6.2979C0.165771 9.77614 2.98544 12.5958 6.46368 12.5958C7.83398 12.5958 9.10207 12.1582 10.1358 11.415L12.7208 14L13.8341 12.8867L11.2907 10.3433ZM11.1871 6.2979C11.1871 8.90658 9.07235 11.0213 6.46368 11.0213C3.855 11.0213 1.74025 8.90658 1.74025 6.2979C1.74025 3.68923 3.855 1.57448 6.46368 1.57448C9.07235 1.57448 11.1871 3.68923 11.1871 6.2979Z" fill="white" />
        </svg>
      </button>
    </div>
  </div>

          <button class="border-r border-slate-100 py-2 grid place-items-center px-7 hover:bg-slate-100 relative" @click="cartStore.isOpen = !cartStore.isOpen">
            <svg width="20" height="20" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M6 16C4.9 16 4.01 16.9 4.01 18C4.01 19.1 4.9 20 6 20C7.1 20 8 19.1 8 18C8 16.9 7.1 16 6 16ZM0 0V2H2L5.6 9.59L4.25 12.04C4.09 12.32 4 12.65 4 13C4 14.1 4.9 15 6 15H18V13H6.42C6.28 13 6.17 12.89 6.17 12.75L6.2 12.63L7.1 11H14.55C15.3 11 15.96 10.59 16.3 9.97L19.88 3.48C19.96 3.34 20 3.17 20 3C20 2.45 19.55 2 19 2H4.21L3.27 0H0ZM16 16C14.9 16 14.01 16.9 14.01 18C14.01 19.1 14.9 20 16 20C17.1 20 18 19.1 18 18C18 16.9 17.1 16 16 16Z" fill="#111112" />
            </svg>
            <span v-if="cartStore.itemCount > 0" class="absolute -top-0.5 -right-0.5 bg-primary text-black text-[10px] font-bold w-4 h-4 rounded-full flex items-center justify-center">{{ cartStore.itemCount }}</span>
          </button>

          <div ref="accountMenuRef" class="relative flex items-center px-7 hover:bg-slate-100 cursor-pointer" @click="accountMenuOpen = !accountMenuOpen">
            <svg class="mr-2" width="20" height="20" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M10 0C4.48 0 0 4.48 0 10C0 15.52 4.48 20 10 20C15.52 20 20 15.52 20 10C20 4.48 15.52 0 10 0ZM10 3C11.66 3 13 4.34 13 6C13 7.66 11.66 9 10 9C8.34 9 7 7.66 7 6C7 4.34 8.34 3 10 3ZM10 17.2C7.5 17.2 5.29 15.92 4 13.98C4.03 11.99 8 10.9 10 10.9C11.99 10.9 15.97 11.99 16 13.98C14.71 15.92 12.5 17.2 10 17.2Z" fill="#111112" />
            </svg>
            <svg width="6" height="4" viewBox="0 0 6 4" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M3.36728 3.60241C3.16932 3.81671 2.83068 3.81671 2.63272 3.60241L0.311188 1.08928C0.0153625 0.769035 0.242499 0.25 0.678465 0.25L5.32154 0.25C5.7575 0.25 5.98464 0.769036 5.68881 1.08928L3.36728 3.60241Z" fill="#111112" />
            </svg>

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

        <!-- Nav links row -->
        <nav class="flex items-center font-medium text-[12px] text-gray-700 pl-9 pt-1 cursor-pointer border-b border-slate-100">
          <NuxtLink
            to="/"
            class="mr-14 py-1 hover:font-bold hover:text-black"
            exact-active-class="text-black font-bold border-b-2 border-primary"
          >Home</NuxtLink>
          <div class="flex items-center mr-14 hover:font-bold hover:text-black">
            <NuxtLink to="/products">T-Shirts</NuxtLink>
            <svg class="ml-2" width="6" height="4" viewBox="0 0 6 4" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M3.36728 3.60241C3.16932 3.81671 2.83068 3.81671 2.63272 3.60241L0.311188 1.08928C0.0153625 0.769035 0.242499 0.25 0.678465 0.25L5.32154 0.25C5.7575 0.25 5.98464 0.769036 5.68881 1.08928L3.36728 3.60241Z" fill="gray" />
            </svg>
          </div>
          <div class="flex items-center mr-14 hover:font-bold hover:text-black">
            <NuxtLink to="/products">NBA</NuxtLink>
            <svg class="ml-2" width="6" height="4" viewBox="0 0 6 4" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M3.36728 3.60241C3.16932 3.81671 2.83068 3.81671 2.63272 3.60241L0.311188 1.08928C0.0153625 0.769035 0.242499 0.25 0.678465 0.25L5.32154 0.25C5.7575 0.25 5.98464 0.769036 5.68881 1.08928L3.36728 3.60241Z" fill="gray" />
            </svg>
          </div>
          <div class="flex items-center mr-14 hover:font-bold hover:text-black">
            <NuxtLink to="/products">Tracksuits</NuxtLink>
            <svg class="ml-2" width="6" height="4" viewBox="0 0 6 4" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M3.36728 3.60241C3.16932 3.81671 2.83068 3.81671 2.63272 3.60241L0.311188 1.08928C0.0153625 0.769035 0.242499 0.25 0.678465 0.25L5.32154 0.25C5.7575 0.25 5.98464 0.769036 5.68881 1.08928L3.36728 3.60241Z" fill="gray" />
            </svg>
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
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M4 17H20M4 12H20M4 7H20" stroke="#000000" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" />
            </svg>
          </button>
          <button @click="mobileSearchOpen = !mobileSearchOpen">
            <svg width="20" height="20" viewBox="0 0 14 14" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path fill-rule="evenodd" clip-rule="evenodd" d="M11.2907 10.3433C12.2088 9.24903 12.7616 7.83803 12.7616 6.2979C12.7616 2.81967 9.94191 5.9873e-07 6.46368 0C2.98544 1.52039e-07 0.165771 2.81967 0.165771 6.2979C0.165771 9.77614 2.98544 12.5958 6.46368 12.5958C7.83398 12.5958 9.10207 12.1582 10.1358 11.415L12.7208 14L13.8341 12.8867L11.2907 10.3433ZM11.1871 6.2979C11.1871 8.90658 9.07235 11.0213 6.46368 11.0213C3.855 11.0213 1.74025 8.90658 1.74025 6.2979C1.74025 3.68923 3.855 1.57448 6.46368 1.57448C9.07235 1.57448 11.1871 3.68923 11.1871 6.2979Z" fill="black" />
            </svg>
          </button>
        </div>

        <div class="flex items-center gap-6">
          <button class="relative" @click="cartStore.isOpen = !cartStore.isOpen">
            <svg width="20" height="20" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M6 16C4.9 16 4.01 16.9 4.01 18C4.01 19.1 4.9 20 6 20C7.1 20 8 19.1 8 18C8 16.9 7.1 16 6 16ZM0 0V2H2L5.6 9.59L4.25 12.04C4.09 12.32 4 12.65 4 13C4 14.1 4.9 15 6 15H18V13H6.42C6.28 13 6.17 12.89 6.17 12.75L6.2 12.63L7.1 11H14.55C15.3 11 15.96 10.59 16.3 9.97L19.88 3.48C19.96 3.34 20 3.17 20 3C20 2.45 19.55 2 19 2H4.21L3.27 0H0ZM16 16C14.9 16 14.01 16.9 14.01 18C14.01 19.1 14.9 20 16 20C17.1 20 18 19.1 18 18C18 16.9 17.1 16 16 16Z" fill="#111112" />
            </svg>
            <span v-if="cartStore.itemCount > 0" class="absolute -top-1 -right-1 bg-primary text-black text-[10px] font-bold w-4 h-4 rounded-full flex items-center justify-center">{{ cartStore.itemCount }}</span>
          </button>
          <NuxtLink v-if="!authStore.isAuthenticated" to="/login">
            <svg width="20" height="20" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M10 0C4.48 0 0 4.48 0 10C0 15.52 4.48 20 10 20C15.52 20 20 15.52 20 10C20 4.48 15.52 0 10 0ZM10 3C11.66 3 13 4.34 13 6C13 7.66 11.66 9 10 9C8.34 9 7 7.66 7 6C7 4.34 8.34 3 10 3ZM10 17.2C7.5 17.2 5.29 15.92 4 13.98C4.03 11.99 8 10.9 10 10.9C11.99 10.9 15.97 11.99 16 13.98C14.71 15.92 12.5 17.2 10 17.2Z" fill="#111112" />
            </svg>
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
const cartStore = useCartStore()
const authStore = useAuthStore()
const router = useRouter()
const route = useRoute()

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
    // Navigate to products page with search query
    router.push({
      path: '/products',
      query: { search: q }
    })
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



/* Dropdown transition */
.fade-down-enter-active, .fade-down-leave-active {
  transition: opacity 0.15s, transform 0.15s;
}
.fade-down-enter-from, .fade-down-leave-to {
  opacity: 0;
  transform: translateY(-6px);
}
</style>