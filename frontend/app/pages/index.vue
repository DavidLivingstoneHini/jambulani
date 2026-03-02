<template>
  <div>
    <!-- Hero Banner -->
    <section class="relative bg-black overflow-hidden">
      <div class="relative h-64 md:h-96 w-full">
        <div class="absolute inset-0 bg-gradient-to-r from-gray-900 via-gray-800 to-gray-900 flex items-center justify-center overflow-hidden">
          <div class="flex items-end gap-4 md:gap-8 px-8 pb-8 opacity-60">
            <div class="w-24 md:w-40 h-28 md:h-48 bg-red-700 rounded transform rotate-3" />
            <div class="w-28 md:w-48 h-32 md:h-56 bg-white rounded transform -rotate-1 shadow-2xl" />
            <div class="w-24 md:w-40 h-28 md:h-48 bg-blue-900 rounded transform -rotate-3" />
          </div>
        </div>
        <div class="absolute inset-0 flex items-center">
          <div class="px-8 md:px-16">
            <h1 class="font-display font-bold text-white text-2xl md:text-5xl leading-tight uppercase">
              Your favorite customized
              <span class="text-primary block">Club Jerseys.</span>
            </h1>
            <NuxtLink to="/products" class="btn-primary inline-block mt-4 text-sm">
              Shop Now →
            </NuxtLink>
          </div>
        </div>
        <div class="absolute bottom-4 left-1/2 -translate-x-1/2 flex gap-2">
          <span class="w-8 h-1 bg-primary" />
          <span class="w-2 h-1 bg-white/40" />
          <span class="w-2 h-1 bg-white/40" />
        </div>
      </div>
    </section>

    <!-- Trust Badges -->
    <section class="bg-gray-50 border-b border-gray-200">
      <div class="max-w-screen-xl mx-auto px-4">
        <div class="grid grid-cols-2 md:grid-cols-4 divide-x divide-gray-200">
          <div v-for="badge in trustBadges" :key="badge.label" class="flex items-center gap-3 p-4">
            <div class="bg-primary p-2 shrink-0">
              <svg class="w-5 h-5 text-black" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" :d="badge.icon" />
              </svg>
            </div>
            <div>
              <p class="font-display font-bold uppercase text-xs tracking-wide">{{ badge.label }}</p>
              <p class="text-gray-500 text-xs font-body">{{ badge.sub }}</p>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Most Popular T-Shirts -->
    <section class="max-w-screen-xl mx-auto px-4 py-10">
      <div class="flex items-center justify-between mb-6">
        <h2 class="section-title mb-0">Most Popular T-Shirts</h2>
        <div class="flex gap-1">
          <button class="border border-gray-300 p-2 hover:bg-gray-100 transition-colors" @click="prevPage">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
            </svg>
          </button>
          <button class="border border-gray-300 p-2 hover:bg-gray-100 transition-colors" @click="nextPage">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
            </svg>
          </button>
        </div>
      </div>

      <div v-if="featuredPending" class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4">
        <div v-for="n in 6" :key="n" class="animate-pulse">
          <div class="aspect-square bg-gray-200 mb-2" />
          <div class="h-4 bg-gray-200 mb-1" />
          <div class="h-4 w-1/2 bg-gray-200" />
        </div>
      </div>
      <div v-else-if="visibleFeatured.length" class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4">
        <ProductProductCard v-for="product in visibleFeatured" :key="product.id" :product="product" />
      </div>
      <div v-else class="text-center py-10 text-gray-400 font-body text-sm">
        No featured products yet. Add some from the admin!
      </div>
    </section>

    <!-- Country Leagues -->
    <section class="max-w-screen-xl mx-auto px-4 py-6">
      <h2 class="section-title">Country Leagues</h2>
      <div v-if="leaguesPending" class="grid grid-cols-2 md:grid-cols-5 gap-4">
        <div v-for="n in 5" :key="n" class="animate-pulse aspect-square bg-gray-200" />
      </div>
      <div v-else class="grid grid-cols-2 md:grid-cols-5 gap-4">
        <NuxtLink
          v-for="league in leagues"
          :key="league.id"
          :to="`/products?league=${league.slug}`"
          class="relative aspect-square overflow-hidden group cursor-pointer flex items-center justify-center"
          :style="leagueStyle(league.slug)"
        >
          <span class="text-white font-display font-bold text-center text-sm uppercase px-2 leading-tight z-10">
            {{ league.name }}
          </span>
          <div class="absolute inset-0 bg-black/0 group-hover:bg-black/20 transition-colors duration-300" />
        </NuxtLink>
      </div>
    </section>

    <!-- Other Collections -->
    <section class="max-w-screen-xl mx-auto px-4 py-6">
      <h2 class="section-title">Other Collections</h2>
      <div v-if="collectionsPending" class="grid grid-cols-2 md:grid-cols-3 gap-4">
        <div v-for="n in 6" :key="n" class="animate-pulse aspect-video bg-gray-200" />
      </div>
      <div v-else-if="collections.length" class="grid grid-cols-2 md:grid-cols-3 gap-4">
        <NuxtLink
          v-for="collection in collections"
          :key="collection.id"
          :to="`/products?collection=${collection.slug}`"
          class="relative overflow-hidden group cursor-pointer bg-gray-800"
        >
          <div class="aspect-video relative flex items-end">
            <div class="p-3 z-10 relative">
              <span class="text-white font-display font-bold text-base uppercase">{{ collection.name }}</span>
            </div>
            <div class="absolute bottom-3 right-3 bg-primary p-1 group-hover:bg-primary-600 transition-colors">
              <svg class="w-4 h-4 text-black" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
              </svg>
            </div>
          </div>
        </NuxtLink>
      </div>
    </section>

    <!-- Personalization + Social -->
    <section class="max-w-screen-xl mx-auto px-4 py-6">
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div class="bg-gray-800 text-white p-8">
          <h3 class="font-display font-bold uppercase text-xl md:text-2xl mb-3">Personalization</h3>
          <p class="font-body text-gray-300 text-sm mb-4 max-w-xs">
            Put a custom print on the football shirt of your choice with our Personalization services.
          </p>
          <p class="font-display font-bold text-primary text-sm uppercase">
            "Tell us what name, what number and we put it. FREE!!"
          </p>
        </div>
        <div class="bg-gray-700 text-white p-8">
          <h3 class="font-display font-bold uppercase text-xl md:text-2xl mb-3">Social Networks</h3>
          <p class="font-body text-gray-300 text-sm mb-4 max-w-xs">
            Share your shirts with us with the #CamisetasFutbolSpanish
          </p>
          <div class="flex gap-2">
            <a href="#" class="bg-blue-600 p-2 hover:bg-blue-700 transition-colors">
              <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 24 24"><path d="M18 2h-3a5 5 0 00-5 5v3H7v4h3v8h4v-8h3l1-4h-4V7a1 1 0 011-1h3z" /></svg>
            </a>
            <a href="#" class="bg-sky-500 p-2 hover:bg-sky-600 transition-colors">
              <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 24 24"><path d="M23 3a10.9 10.9 0 01-3.14 1.53 4.48 4.48 0 00-7.86 3v1A10.66 10.66 0 013 4s-4 9 5 13a11.64 11.64 0 01-7 2c9 5 20 0 20-11.5a4.5 4.5 0 00-.08-.83A7.72 7.72 0 0023 3z" /></svg>
            </a>
            <a href="#" class="bg-gradient-to-br from-purple-600 via-pink-500 to-orange-400 p-2 hover:opacity-90 transition-opacity">
              <svg class="w-4 h-4 text-white" fill="currentColor" viewBox="0 0 24 24"><rect x="2" y="2" width="20" height="20" rx="5" ry="5" /></svg>
            </a>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
import type { ProductList, League, Collection } from '~/app/types'

const { apiFetch } = useApi()

const { data: featuredData, pending: featuredPending } = await useAsyncData(
  'featured-products',
  () => apiFetch<ProductList[]>('/products/featured/')
)
const featuredProducts = computed(() => featuredData.value || [])

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

const { data: leaguesData, pending: leaguesPending } = await useAsyncData(
  'leagues',
  () => apiFetch<League[]>('/leagues/')
)
const leagues = computed(() => leaguesData.value || [])

const { data: collectionsData, pending: collectionsPending } = await useAsyncData(
  'collections',
  () => apiFetch<Collection[]>('/collections/')
)
const collections = computed(() => collectionsData.value || [])

const leagueGradients: Record<string, string> = {
  'champions-league': 'background: linear-gradient(135deg, #1a237e, #0d47a1)',
  'europa-league': 'background: linear-gradient(135deg, #1b5e20, #2e7d32)',
  'copa-america': 'background: linear-gradient(135deg, #880e4f, #ad1457)',
  'asian-cup': 'background: linear-gradient(135deg, #e65100, #f57c00)',
  'african-nations-cup': 'background: linear-gradient(135deg, #1b5e20, #558b2f)',
  'england-premier-league': 'background: linear-gradient(135deg, #4a148c, #7b1fa2)',
  'la-liga': 'background: linear-gradient(135deg, #b71c1c, #c62828)',
  'serie-a': 'background: linear-gradient(135deg, #0d47a1, #1565c0)',
  'bundesliga': 'background: linear-gradient(135deg, #b71c1c, #f57f17)',
  'ligue-1': 'background: linear-gradient(135deg, #0d47a1, #1a237e)',
}

function leagueStyle(slug: string): string {
  return leagueGradients[slug] || 'background: linear-gradient(135deg, #1a1a1a, #2a2a2a)'
}

const trustBadges = [
  { label: 'Secure Shipping', sub: 'on all orders', icon: 'M5 8h14M5 8a2 2 0 110-4h14a2 2 0 110 4M5 8v10a2 2 0 002 2h10a2 2 0 002-2V8m-9 4h4' },
  { label: 'Telephone', sub: '+1 (25) 01 7880', icon: 'M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z' },
  { label: 'Chat WhatsApp', sub: 'Mon–Fri 9:00–17:00', icon: 'M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z' },
  { label: 'Quality Guarantee', sub: 'Verified Purchase Reviews', icon: 'M9 12l2 2 4-4M7.835 4.697a3.42 3.42 0 001.946-.806 3.42 3.42 0 014.438 0 3.42 3.42 0 001.946.806 3.42 3.42 0 013.138 3.138 3.42 3.42 0 00.806 1.946 3.42 3.42 0 010 4.438 3.42 3.42 0 00-.806 1.946 3.42 3.42 0 01-3.138 3.138 3.42 3.42 0 00-1.946.806 3.42 3.42 0 01-4.438 0 3.42 3.42 0 00-1.946-.806 3.42 3.42 0 01-3.138-3.138 3.42 3.42 0 00-.806-1.946 3.42 3.42 0 010-4.438 3.42 3.42 0 00.806-1.946 3.42 3.42 0 013.138-3.138z' },
]

useHead({ title: 'Jambulani — Your Favorite Customized Club Jerseys' })
</script>
