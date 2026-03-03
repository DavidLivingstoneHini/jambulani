<template>
  <div>

    <!-- ══════════════════════════════════════════
         HERO BANNER
         Place your image at: public/assets/images/hero-banner.jpg
    ══════════════════════════════════════════ -->
    <section
      class="relative overflow-hidden bg-gray-900"
      style="height: 340px;"
    >
      <div
        class="absolute inset-0 bg-cover bg-center bg-no-repeat"
        style="background-image: url('/assets/images/hero-banner.jpg'); background-color: #1a1a2e;"
      />
      <div class="absolute inset-0 bg-black/35" />

      <div class="relative z-10 h-full flex items-center">
        <div class="max-w-screen-xl mx-auto px-6 md:px-10 w-full">
          <h1 class="font-display font-bold text-white text-[30px] md:text-[52px] leading-[1.05] uppercase drop-shadow-lg">
            Your favorite customized<br>
            <span class="text-primary">Club Jerseys.</span>
          </h1>
          <NuxtLink
            to="/products"
            class="inline-block mt-5 bg-primary text-black font-display font-bold uppercase
                   tracking-wider px-5 py-2.5 text-[13px] hover:bg-primary-600 transition-colors shadow"
          >
            Shop Now
          </NuxtLink>
        </div>
      </div>

      <!-- Slide dots bottom-left -->
      <div class="absolute bottom-4 left-6 md:left-10 flex items-center gap-1.5 z-10">
        <span class="block w-7 h-1.5 bg-primary" />
        <span class="block w-2.5 h-1.5 bg-white/40 cursor-pointer" />
        <span class="block w-2.5 h-1.5 bg-white/40 cursor-pointer" />
      </div>
    </section>


    <!-- ══════════════════════════════════════════
         TRUST BADGES — 4 columns
    ══════════════════════════════════════════ -->
    <section class="bg-[#fafaf5] border-y border-gray-200">
      <div class="max-w-screen-xl mx-auto">
        <div class="grid grid-cols-2 md:grid-cols-4 divide-x divide-gray-200">

          <div class="flex items-center gap-3 px-5 py-5">
            <div class="bg-primary p-2.5 shrink-0">
              <svg class="w-5 h-5 text-black" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M5 8h14M5 8a2 2 0 110-4h14a2 2 0 110 4M5 8v10a2 2 0 002 2h10a2 2 0 002-2V8m-9 4h4" />
              </svg>
            </div>
            <div>
              <p class="font-display font-bold uppercase text-[12px] tracking-wide text-gray-900 leading-tight">Secure Shipping</p>
              <p class="text-gray-500 text-[11px] font-body mt-0.5">on all orders</p>
            </div>
          </div>

          <div class="flex items-center gap-3 px-5 py-5">
            <div class="bg-primary p-2.5 shrink-0">
              <svg class="w-5 h-5 text-black" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042
                     11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2
                     0 01-2 2h-1C9.716 21 3 14.284 3 6V5z" />
              </svg>
            </div>
            <div>
              <p class="font-display font-bold uppercase text-[12px] tracking-wide text-gray-900 leading-tight">Telephone</p>
              <p class="text-gray-500 text-[11px] font-body mt-0.5">+1 (25) 01 7880</p>
            </div>
          </div>

          <div class="flex items-center gap-3 px-5 py-5">
            <div class="bg-primary p-2.5 shrink-0">
              <svg class="w-5 h-5 text-black" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0
                     01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
              </svg>
            </div>
            <div>
              <p class="font-display font-bold uppercase text-[12px] tracking-wide text-gray-900 leading-tight">Chat WhatsApp</p>
              <p class="text-gray-500 text-[11px] font-body mt-0.5">Mon–Fri 9:00–17:00 · Sat–S 9:00–17:00</p>
            </div>
          </div>

          <div class="flex items-center gap-3 px-5 py-5">
            <div class="bg-primary p-2.5 shrink-0">
              <svg class="w-5 h-5 text-black" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M9 12l2 2 4-4M7.835 4.697a3.42 3.42 0 001.946-.806 3.42 3.42 0 014.438 0 3.42 3.42 0
                     001.946.806 3.42 3.42 0 013.138 3.138 3.42 3.42 0 00.806 1.946 3.42 3.42 0 010 4.438 3.42
                     3.42 0 00-.806 1.946 3.42 3.42 0 01-3.138 3.138 3.42 3.42 0 00-1.946.806 3.42 3.42 0
                     01-4.438 0 3.42 3.42 0 00-1.946-.806 3.42 3.42 0 01-3.138-3.138 3.42 3.42 0 00-.806-1.946
                     3.42 3.42 0 010-4.438 3.42 3.42 0 00.806-1.946 3.42 3.42 0 013.138-3.138z" />
              </svg>
            </div>
            <div>
              <p class="font-display font-bold uppercase text-[12px] tracking-wide text-gray-900 leading-tight">Quality Guarantee</p>
              <p class="text-gray-500 text-[11px] font-body mt-0.5">Verified Purchase Reviews</p>
            </div>
          </div>

        </div>
      </div>
    </section>


    <!-- ══════════════════════════════════════════
         MOST POPULAR T-SHIRTS
    ══════════════════════════════════════════ -->
    <section class="max-w-screen-xl mx-auto px-4 pt-10 pb-6">
      <div class="flex items-center justify-between mb-5">
        <h2 class="section-title mb-0">MOST POPULAR T-SHIRTS</h2>
        <div class="flex gap-0">
          <button
            class="border border-gray-300 p-2 hover:bg-gray-100 transition-colors"
            aria-label="Previous"
            @click="prevPage"
          >
            <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
            </svg>
          </button>
          <button
            class="border border-gray-300 p-2 hover:bg-gray-100 transition-colors"
            aria-label="Next"
            @click="nextPage"
          >
            <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
            </svg>
          </button>
        </div>
      </div>

      <div v-if="featuredPending" class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3">
        <div v-for="n in 6" :key="n" class="animate-pulse">
          <div class="aspect-square bg-gray-200 mb-2" />
          <div class="h-3 bg-gray-200 mb-1 rounded" />
          <div class="h-3 w-2/3 bg-gray-200 rounded" />
        </div>
      </div>

      <div v-else-if="visibleFeatured.length > 0" class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3">
        <ProductCard
          v-for="product in visibleFeatured"
          :key="product.id"
          :product="product"
        />
      </div>

      <p v-else class="text-center py-10 text-gray-400 font-body text-sm">
        No featured products yet — run
        <code class="bg-gray-100 px-1 text-xs">python manage.py seed_data</code>
      </p>
    </section>


    <!-- ══════════════════════════════════════════
         COUNTRY LEAGUES — 5 static squares
         Images → public/assets/images/leagues/{slug}.jpg
    ══════════════════════════════════════════ -->
    <section class="max-w-screen-xl mx-auto px-4 pt-8 pb-6">
      <h2 class="section-title">COUNTRY LEAGUES</h2>
      <div class="grid grid-cols-2 md:grid-cols-5 gap-3">
        <NuxtLink
          v-for="league in staticLeagues"
          :key="league.slug"
          :to="`/products?league=${league.slug}`"
          class="relative overflow-hidden block cursor-pointer group"
          style="aspect-ratio: 1 / 1;"
        >
          <div
            class="absolute inset-0 bg-cover bg-center bg-no-repeat
                   transition-transform duration-500 group-hover:scale-105"
            :style="`background-image: url('/assets/images/leagues/${league.slug}.jpg');
                     background-color: ${league.color};`"
          />
          <div class="absolute inset-0 bg-black/20 group-hover:bg-black/35 transition-colors duration-300" />
          <span
            class="absolute bottom-0 inset-x-0 pb-2.5 text-center text-white font-display
                   font-bold text-[11px] md:text-[12px] uppercase leading-tight drop-shadow px-1 z-10"
          >
            {{ league.name }}
          </span>
        </NuxtLink>
      </div>
    </section>


    <!-- ══════════════════════════════════════════
         OTHER COLLECTIONS — 6 static 16:9 cards
         Images → public/assets/images/collections/{slug}.jpg
    ══════════════════════════════════════════ -->
    <section class="max-w-screen-xl mx-auto px-4 pt-8 pb-6">
      <h2 class="section-title">OTHER COLLECTIONS</h2>
      <div class="grid grid-cols-2 md:grid-cols-3 gap-3">
        <NuxtLink
          v-for="col in staticCollections"
          :key="col.slug"
          :to="`/products?collection=${col.slug}`"
          class="relative overflow-hidden block cursor-pointer group"
          style="aspect-ratio: 16 / 9;"
        >
          <div
            class="absolute inset-0 bg-cover bg-center bg-no-repeat
                   transition-transform duration-500 group-hover:scale-105"
            :style="`background-image: url('/assets/images/collections/${col.slug}.jpg');
                     background-color: ${col.color};`"
          />
          <div class="absolute inset-0 bg-gradient-to-t from-black/75 via-black/15 to-transparent" />
          <div class="absolute bottom-0 inset-x-0 flex items-center justify-between px-3 pb-2.5 z-10">
            <span class="text-white font-display font-bold text-[12px] md:text-[14px] uppercase leading-tight drop-shadow">
              {{ col.name }}
            </span>
            <div class="bg-primary w-5 h-5 flex items-center justify-center shrink-0
                        group-hover:bg-primary-600 transition-colors">
              <svg class="w-3 h-3 text-black" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M9 5l7 7-7 7" />
              </svg>
            </div>
          </div>
        </NuxtLink>
      </div>
    </section>


    <!-- ══════════════════════════════════════════
         PERSONALIZATION + SOCIAL NETWORKS
         Images → public/assets/images/personalization-bg.jpg
                  public/assets/images/social-bg.jpg
    ══════════════════════════════════════════ -->
    <section class="max-w-screen-xl mx-auto px-4 pt-8 pb-10">
      <div class="grid grid-cols-1 md:grid-cols-2 gap-3">

        <div
          class="relative overflow-hidden bg-cover bg-center"
          style="min-height:220px; background-image:url('/assets/images/personalization-bg.jpg');
                 background-color:#1a1a2e;"
        >
          <div class="absolute inset-0 bg-black/55" />
          <div class="relative z-10 p-8 md:p-10 flex flex-col justify-end" style="min-height:220px;">
            <h3 class="font-display font-bold uppercase text-[20px] md:text-[22px] tracking-wide mb-2 text-white">
              PERSONALIZATION
            </h3>
            <p class="font-body text-gray-300 text-[13px] leading-relaxed mb-3 max-w-xs">
              Put a custom print on the football shirt of your choice with our Personalization services.
            </p>
            <p class="font-display font-bold text-primary text-[12px] uppercase tracking-wide">
              "Tell us what name, what number and we put it. FREE!!"
            </p>
          </div>
        </div>

        <div
          class="relative overflow-hidden bg-cover bg-center"
          style="min-height:220px; background-image:url('/assets/images/social-bg.jpg');
                 background-color:#111827;"
        >
          <div class="absolute inset-0 bg-black/55" />
          <div class="relative z-10 p-8 md:p-10 flex flex-col justify-end" style="min-height:220px;">
            <h3 class="font-display font-bold uppercase text-[20px] md:text-[22px] tracking-wide mb-2 text-white">
              SOCIAL NETWORKS
            </h3>
            <p class="font-body text-gray-300 text-[13px] leading-relaxed mb-4 max-w-xs">
              Share your shirts with us with the #CamisetasFutbolSpanish
            </p>
            <div class="flex gap-2">
              <a href="#" aria-label="Facebook"
                 class="p-2.5 hover:brightness-110 transition-all bg-[#1877f2]">
                <svg class="w-4 h-4 text-white" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M18 2h-3a5 5 0 00-5 5v3H7v4h3v8h4v-8h3l1-4h-4V7a1 1 0 011-1h3z" />
                </svg>
              </a>
              <a href="#" aria-label="Twitter"
                 class="p-2.5 hover:brightness-110 transition-all bg-[#1da1f2]">
                <svg class="w-4 h-4 text-white" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M23 3a10.9 10.9 0 01-3.14 1.53 4.48 4.48 0 00-7.86 3v1A10.66
                           10.66 0 013 4s-4 9 5 13a11.64 11.64 0 01-7 2c9 5 20 0 20-11.5a4.5
                           4.5 0 00-.08-.83A7.72 7.72 0 0023 3z" />
                </svg>
              </a>
              <a href="#" aria-label="Instagram"
                 class="p-2.5 hover:brightness-110 transition-all"
                 style="background:linear-gradient(45deg,#f09433,#e6683c,#dc2743,#cc2366,#bc1888)">
                <svg class="w-4 h-4 text-white" fill="none" stroke="currentColor"
                     stroke-width="2" viewBox="0 0 24 24">
                  <rect x="2" y="2" width="20" height="20" rx="5" ry="5" />
                  <circle cx="12" cy="12" r="4" />
                  <circle cx="17.5" cy="6.5" r="1" fill="white" stroke="none" />
                </svg>
              </a>
            </div>
          </div>
        </div>

      </div>
    </section>

  </div>
</template>

<script setup lang="ts">
import type { ProductList } from '~/app/types'

const { apiFetch } = useApi()

const { data: featuredData, pending: featuredPending } = await useAsyncData(
  'featured-products',
  () => apiFetch<ProductList[]>('/products/featured/').catch(() => [] as ProductList[])
)
const featuredProducts = computed<ProductList[]>(() => featuredData.value ?? [])

const featuredOffset = ref(0)
const ITEMS_PER_PAGE = 6
const visibleFeatured = computed(() =>
  featuredProducts.value.slice(featuredOffset.value, featuredOffset.value + ITEMS_PER_PAGE)
)
function prevPage() {
  if (featuredOffset.value > 0) featuredOffset.value -= ITEMS_PER_PAGE
}
function nextPage() {
  if (featuredOffset.value + ITEMS_PER_PAGE < featuredProducts.value.length)
    featuredOffset.value += ITEMS_PER_PAGE
}

// Static leagues — images in public/assets/images/leagues/{slug}.jpg
const staticLeagues = [
  { slug: 'champions-league',     name: 'Champions League',    color: '#0d47a1' },
  { slug: 'europa-league',        name: 'Europe League',       color: '#1b5e20' },
  { slug: 'copa-america',         name: 'Copa America',        color: '#880e4f' },
  { slug: 'asian-cup',            name: 'Asian Cup',           color: '#b71c1c' },
  { slug: 'african-nations-cup',  name: 'African Nations Cup', color: '#1b5e20' },
]

// Static collections — images in public/assets/images/collections/{slug}.jpg
const staticCollections = [
  { slug: 'kids',                 name: 'Kids',                  color: '#1565c0' },
  { slug: 'large-sizes',          name: 'Large sizes',           color: '#2e7d32' },
  { slug: 'goalkeeper',           name: 'Goalkeeper',            color: '#212121' },
  { slug: 'authentic-pro-player', name: 'Authentic / Pro Player',color: '#4a148c' },
  { slug: 'shorts',               name: 'Shorts',                color: '#b71c1c' },
  { slug: 'socks',                name: 'Socks',                 color: '#e65100' },
]

useHead({ title: 'Jambulani — Your Favorite Customized Club Jerseys' })
</script>
