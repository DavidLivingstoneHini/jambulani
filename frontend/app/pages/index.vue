<template>
  <div>

    <!-- ════════════════════════════════════════
         HERO BANNER
         Background image: put hero-banner.jpg in ~/assets/images/
    ════════════════════════════════════════ -->
    <section class="relative overflow-hidden bg-gray-900" style="height: 340px;">
      <!-- Background image (add hero-banner.jpg to assets/images/) -->
      <div
        class="absolute inset-0 bg-cover bg-center bg-no-repeat"
        style="background-image: url('/assets/images/hero-banner.jpg'); background-color: #1a1a2e;"
      />
      <!-- Dark overlay for text legibility -->
      <div class="absolute inset-0 bg-black/40" />

      <!-- Text content — left-aligned, vertically centred -->
      <div class="relative z-10 h-full flex items-center">
        <div class="max-w-screen-xl mx-auto px-6 md:px-10 w-full">
          <h1 class="font-display font-bold text-white text-[28px] md:text-[52px] leading-[1.05] uppercase">
            Your favorite customized<br>
            <span class="text-primary">Club Jerseys.</span>
          </h1>
          <NuxtLink
            to="/products"
            class="btn-primary inline-block mt-5 text-sm px-5 py-2.5"
          >Shop Now</NuxtLink>
        </div>
      </div>

      <!-- Slide dots — bottom centre -->
      <div class="absolute bottom-4 left-1/2 -translate-x-1/2 flex items-center gap-1.5 z-10">
        <span class="block w-7 h-1.5 bg-primary" />
        <span class="block w-2.5 h-1.5 bg-white/40" />
        <span class="block w-2.5 h-1.5 bg-white/40" />
      </div>
    </section>


    <!-- ════════════════════════════════════════
         TRUST BADGES (4 columns)
    ════════════════════════════════════════ -->
    <section class="bg-[#f9f9f4] border-b border-gray-200">
      <div class="max-w-screen-xl mx-auto px-4">
        <div class="grid grid-cols-2 md:grid-cols-4 divide-x divide-gray-200">
          <div
            v-for="badge in trustBadges"
            :key="badge.label"
            class="flex items-center gap-3 px-5 py-4"
          >
            <div class="bg-primary p-2 shrink-0">
              <svg class="w-5 h-5 text-black" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" :d="badge.icon" />
              </svg>
            </div>
            <div>
              <p class="font-display font-bold uppercase text-[12px] tracking-wide text-gray-900 leading-tight">{{ badge.label }}</p>
              <p class="text-gray-500 text-[11px] font-body leading-tight mt-0.5">{{ badge.sub }}</p>
            </div>
          </div>
        </div>
      </div>
    </section>


    <!-- ════════════════════════════════════════
         REWARDS floating tab (left side)
    ════════════════════════════════════════ -->
    <div class="fixed left-0 top-1/2 -translate-y-1/2 z-40">
      <div class="bg-primary text-black flex items-center gap-1.5 shadow-lg cursor-pointer hover:bg-primary-600 transition-colors py-2.5 px-2.5">
        <svg class="w-3.5 h-3.5 shrink-0" fill="currentColor" viewBox="0 0 20 20">
          <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
        </svg>
        <span class="font-display font-bold text-[11px] uppercase tracking-wider writing-vertical">Rewards</span>
      </div>
    </div>


    <!-- ════════════════════════════════════════
         MOST POPULAR T-SHIRTS (dynamic, seeded)
    ════════════════════════════════════════ -->
    <section class="max-w-screen-xl mx-auto px-4 pt-10 pb-6">
      <div class="flex items-center justify-between mb-5">
        <h2 class="section-title mb-0">Most Popular T-Shirts</h2>
        <div class="flex gap-0.5">
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

      <!-- Skeleton -->
      <div v-if="featuredPending" class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3">
        <div v-for="n in 6" :key="n" class="animate-pulse">
          <div class="aspect-square bg-gray-200 mb-2" />
          <div class="h-3 bg-gray-200 mb-1.5 rounded" />
          <div class="h-3 w-2/3 bg-gray-200 rounded" />
          <div class="h-3 w-1/2 bg-gray-200 mt-1 rounded" />
        </div>
      </div>

      <!-- Products grid — 6 per row on desktop -->
      <div v-else-if="visibleFeatured.length > 0" class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3">
        <ProductCard
          v-for="product in visibleFeatured"
          :key="product.id"
          :product="product"
        />
      </div>

      <div v-else class="text-center py-10 text-gray-400 font-body text-sm">
        No featured products yet. Run <code class="bg-gray-100 px-1">python manage.py seed_data</code> to seed the database.
      </div>
    </section>


    <!-- ════════════════════════════════════════
         COUNTRY LEAGUES  (STATIC — 5 items)
         Place your league images in assets/images/leagues/
         Filenames: champions-league.jpg, europa-league.jpg,
                    copa-america.jpg, asian-cup.jpg, african-nations-cup.jpg
    ════════════════════════════════════════ -->
    <section class="max-w-screen-xl mx-auto px-4 pt-8 pb-6">
      <h2 class="section-title">Country Leagues</h2>
      <div class="grid grid-cols-2 md:grid-cols-5 gap-3">
        <NuxtLink
          v-for="league in staticLeagues"
          :key="league.slug"
          :to="`/products?league=${league.slug}`"
          class="relative aspect-square overflow-hidden group cursor-pointer block"
        >
          <!-- Background image — falls back to gradient if image missing -->
          <div
            class="absolute inset-0 bg-cover bg-center bg-no-repeat transition-transform duration-500 group-hover:scale-105"
            :style="`background-image: url('/assets/images/leagues/${league.slug}.jpg'); background-color: ${league.fallbackColor};`"
          />
          <!-- Slight dark veil always present, darker on hover -->
          <div class="absolute inset-0 bg-black/20 group-hover:bg-black/35 transition-colors duration-300" />
          <!-- Label at bottom centre -->
          <div class="absolute bottom-0 inset-x-0 pb-3 flex justify-center z-10">
            <span class="text-white font-display font-bold text-[11px] md:text-[13px] uppercase text-center px-2 leading-tight drop-shadow">
              {{ league.name }}
            </span>
          </div>
        </NuxtLink>
      </div>
    </section>


    <!-- ════════════════════════════════════════
         OTHER COLLECTIONS  (STATIC — 6 items 2×3)
         Place images in assets/images/collections/
         Filenames: kids.jpg, large-sizes.jpg, goalkeeper.jpg,
                    authentic-pro-player.jpg, shorts.jpg, socks.jpg
    ════════════════════════════════════════ -->
    <section class="max-w-screen-xl mx-auto px-4 pt-8 pb-6">
      <h2 class="section-title">Other Collections</h2>
      <div class="grid grid-cols-2 md:grid-cols-3 gap-3">
        <NuxtLink
          v-for="col in staticCollections"
          :key="col.slug"
          :to="`/products?collection=${col.slug}`"
          class="relative overflow-hidden group cursor-pointer block"
          style="padding-top: 56.25%;"  <!-- 16:9 aspect ratio -->
        >
          <!-- Background image -->
          <div
            class="absolute inset-0 bg-cover bg-center bg-no-repeat transition-transform duration-500 group-hover:scale-105"
            :style="`background-image: url('/assets/images/collections/${col.slug}.jpg'); background-color: ${col.fallbackColor};`"
          />
          <!-- Gradient overlay — bottom-heavy so text is legible -->
          <div class="absolute inset-0 bg-gradient-to-t from-black/70 via-black/10 to-transparent" />
          <!-- Bottom row: name + arrow -->
          <div class="absolute bottom-0 inset-x-0 flex items-center justify-between px-3 pb-2.5 z-10">
            <span class="text-white font-display font-bold text-[13px] md:text-[15px] uppercase drop-shadow">
              {{ col.name }}
            </span>
            <div class="bg-primary w-6 h-6 flex items-center justify-center shrink-0 group-hover:bg-primary-600 transition-colors">
              <svg class="w-3.5 h-3.5 text-black" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M9 5l7 7-7 7" />
              </svg>
            </div>
          </div>
        </NuxtLink>
      </div>
    </section>


    <!-- ════════════════════════════════════════
         PERSONALIZATION + SOCIAL NETWORKS
         Place images in assets/images/:
           personalization-bg.jpg  (jersey close-up / red Arsenal type)
           social-bg.jpg           (fans / crowd)
    ════════════════════════════════════════ -->
    <section class="max-w-screen-xl mx-auto px-4 pt-8 pb-10">
      <div class="grid grid-cols-1 md:grid-cols-2 gap-3">

        <!-- Personalization -->
        <div
          class="relative overflow-hidden text-white"
          style="min-height: 220px;"
        >
          <div
            class="absolute inset-0 bg-cover bg-center bg-no-repeat"
            style="background-image: url('/assets/images/personalization-bg.jpg'); background-color: #1a1a2e;"
          />
          <div class="absolute inset-0 bg-black/55" />
          <div class="relative z-10 p-8 md:p-10 flex flex-col justify-end h-full" style="min-height: 220px;">
            <h3 class="font-display font-bold uppercase text-[20px] md:text-[24px] tracking-wide mb-2">Personalization</h3>
            <p class="font-body text-gray-300 text-[13px] leading-relaxed mb-3 max-w-xs">
              Put a custom print on the football shirt of your choice with our Personalization services.
            </p>
            <p class="font-display font-bold text-primary text-[13px] uppercase tracking-wide">
              "Tell us what name, what number and we put it. FREE!!"
            </p>
          </div>
        </div>

        <!-- Social Networks -->
        <div
          class="relative overflow-hidden text-white"
          style="min-height: 220px;"
        >
          <div
            class="absolute inset-0 bg-cover bg-center bg-no-repeat"
            style="background-image: url('/assets/images/social-bg.jpg'); background-color: #111827;"
          />
          <div class="absolute inset-0 bg-black/55" />
          <div class="relative z-10 p-8 md:p-10 flex flex-col justify-end h-full" style="min-height: 220px;">
            <h3 class="font-display font-bold uppercase text-[20px] md:text-[24px] tracking-wide mb-2">Social Networks</h3>
            <p class="font-body text-gray-300 text-[13px] leading-relaxed mb-4 max-w-xs">
              Share your shirts with us with the #CamisetasFutbolSpanish
            </p>
            <div class="flex gap-2">
              <a href="#" aria-label="Facebook" class="bg-[#1877f2] p-2.5 hover:brightness-110 transition-all">
                <svg class="w-4 h-4 text-white" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M18 2h-3a5 5 0 00-5 5v3H7v4h3v8h4v-8h3l1-4h-4V7a1 1 0 011-1h3z" />
                </svg>
              </a>
              <a href="#" aria-label="Twitter" class="bg-[#1da1f2] p-2.5 hover:brightness-110 transition-all">
                <svg class="w-4 h-4 text-white" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M23 3a10.9 10.9 0 01-3.14 1.53 4.48 4.48 0 00-7.86 3v1A10.66 10.66 0 013 4s-4 9 5 13a11.64 11.64 0 01-7 2c9 5 20 0 20-11.5a4.5 4.5 0 00-.08-.83A7.72 7.72 0 0023 3z" />
                </svg>
              </a>
              <a href="#" aria-label="Instagram" class="p-2.5 hover:brightness-110 transition-all" style="background: linear-gradient(45deg,#f09433,#e6683c,#dc2743,#cc2366,#bc1888)">
                <svg class="w-4 h-4 text-white" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
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

// ── Featured products (dynamic, seeded) ───────────────────────────
const { data: featuredData, pending: featuredPending } = await useAsyncData(
  'featured-products',
  () => apiFetch<ProductList[]>('/products/featured/').catch(() => [] as ProductList[])
)
const featuredProducts = computed<ProductList[]>(() => featuredData.value ?? [])

const featuredOffset = ref(0)
const itemsPerPage = 6
const visibleFeatured = computed(() =>
  featuredProducts.value.slice(featuredOffset.value, featuredOffset.value + itemsPerPage)
)
function prevPage() {
  if (featuredOffset.value > 0) featuredOffset.value -= itemsPerPage
}
function nextPage() {
  if (featuredOffset.value + itemsPerPage < featuredProducts.value.length) featuredOffset.value += itemsPerPage
}

// ── STATIC leagues (exactly 5 to match design) ────────────────────
// Images go in: public/assets/images/leagues/{slug}.jpg
const staticLeagues = [
  { slug: 'champions-league',   name: 'Champions League',    fallbackColor: '#0d47a1' },
  { slug: 'europa-league',      name: 'Europe League',       fallbackColor: '#1b5e20' },
  { slug: 'copa-america',       name: 'Copa America',        fallbackColor: '#880e4f' },
  { slug: 'asian-cup',          name: 'Asian Cup',           fallbackColor: '#b71c1c' },
  { slug: 'african-nations-cup',name: 'African Nations Cup', fallbackColor: '#1b5e20' },
]

// ── STATIC collections (exactly 6 to match design — 2 rows × 3) ──
// Images go in: public/assets/images/collections/{slug}.jpg
const staticCollections = [
  { slug: 'kids',               name: 'Kids',                fallbackColor: '#1565c0' },
  { slug: 'large-sizes',        name: 'Large sizes',         fallbackColor: '#2e7d32' },
  { slug: 'goalkeeper',         name: 'Goalkeeper',          fallbackColor: '#212121' },
  { slug: 'authentic-pro-player',name:'Authentic / Pro Player',fallbackColor:'#4a148c'},
  { slug: 'shorts',             name: 'Shorts',              fallbackColor: '#b71c1c' },
  { slug: 'socks',              name: 'Socks',               fallbackColor: '#e65100' },
]

// ── Trust badges ──────────────────────────────────────────────────
const trustBadges = [
  {
    label: 'Secure Shipping',
    sub: 'on all orders',
    icon: 'M5 8h14M5 8a2 2 0 110-4h14a2 2 0 110 4M5 8v10a2 2 0 002 2h10a2 2 0 002-2V8m-9 4h4',
  },
  {
    label: 'Telephone',
    sub: '+1 (25) 01 7880',
    icon: 'M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z',
  },
  {
    label: 'Chat WhatsApp',
    sub: 'Mon–Fri 9:00–17:00 · Sat–S 9:00–17:00',
    icon: 'M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z',
  },
  {
    label: 'Quality Guarantee',
    sub: 'Verified Purchase Reviews',
    icon: 'M9 12l2 2 4-4M7.835 4.697a3.42 3.42 0 001.946-.806 3.42 3.42 0 014.438 0 3.42 3.42 0 001.946.806 3.42 3.42 0 013.138 3.138 3.42 3.42 0 00.806 1.946 3.42 3.42 0 010 4.438 3.42 3.42 0 00-.806 1.946 3.42 3.42 0 01-3.138 3.138 3.42 3.42 0 00-1.946.806 3.42 3.42 0 01-4.438 0 3.42 3.42 0 00-1.946-.806 3.42 3.42 0 01-3.138-3.138 3.42 3.42 0 00-.806-1.946 3.42 3.42 0 010-4.438 3.42 3.42 0 00.806-1.946 3.42 3.42 0 013.138-3.138z',
  },
]

useHead({ title: 'Jambulani — Your Favorite Customized Club Jerseys' })
</script>
