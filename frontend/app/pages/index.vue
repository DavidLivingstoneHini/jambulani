<template>
  <div>
    <!-- Hero Banner -->
    <section class="px-1 md:px-[34px] pt-8">
      <div
        class="relative overflow-hidden"
        style="height: 300px; background-color: #1a1a2e;"
      >
        <div
          v-for="(_, i) in heroSlides"
          :key="i"
          class="absolute inset-0 bg-cover bg-center bg-no-repeat transition-opacity duration-700"
          :style="`background-image: url('/assets/images/hero-banner.jpg'); opacity: ${heroIndex === i ? 1 : 0};`"
        />

        <div
          class="absolute inset-0"
          style="background: linear-gradient(to right, rgba(0,0,0,0.60) 35%, rgba(0,0,0,0.08) 100%);"
        />

        <div class="absolute inset-0 flex flex-col justify-between z-10 px-6 md:px-10 py-6 md:py-8">
          <div>
            <h1 class="font-display font-bold text-white leading-[1.1] text-[24px] md:text-[38px]">
              Your favorite customized<br>
              <span class="text-primary">Club Jerseys.</span>
            </h1>
          </div>

          <div class="flex items-center justify-between gap-3">
            <div class="flex items-center gap-1.5 md:gap-2 flex-shrink-0">
              <span
                v-for="(_, i) in heroSlides"
                :key="i"
                class="block cursor-pointer transition-all duration-300"
                :style="heroIndex === i
                  ? 'width: clamp(24px, 4vw, 80px); height:4px; background:#F9DC38; opacity:1;'
                  : 'width: clamp(24px, 4vw, 80px); height:4px; background:#ffffff; opacity:0.16;'"
                @click="heroIndex = i"
              />
            </div>

            <div class="flex items-stretch flex-shrink-0">
              <NuxtLink
                to="/products"
                class="flex items-center px-3 md:px-5 py-2 text-[11px] md:text-[12px] font-display font-semibold text-white
                       border border-white hover:bg-white/10 transition-colors whitespace-nowrap"
                style="background: rgba(0,0,0,0.45);"
              >
                Shop Now
              </NuxtLink>
              <NuxtLink
                to="/products"
                class="bg-white flex items-center justify-center px-2 md:px-3 hover:bg-gray-100 transition-colors"
              >
                <img src="/assets/icons/shopping-bag.svg" width="13" height="13" alt="" aria-hidden="true" />
              </NuxtLink>
            </div>

          </div>
        </div>

      </div>
    </section>

    <!-- Page Content -->
    <div class="px-1 md:px-[34px]">

    <!-- Trust Badges -->
    <section class="pt-8">
      <div class="grid grid-cols-2 md:grid-cols-4 gap-3">
        <div class="overflow-hidden bg-[#fdf9e0] p-5 pb-3">
          <div class="skewed bg-primary p-2 w-fit mb-4">
            <img src="/assets/icons/shipping.svg" width="17" height="17" alt="" aria-hidden="true" />
          </div>
          <p class="font-semibold text-[12px] mb-1 inline-block">Secure Shipping</p>
          <p class="text-[10px]">on all orders</p>
        </div>

        <div class="overflow-hidden bg-[#fdf9e0] p-5 pb-3">
          <div class="skewed bg-primary p-2 w-fit mb-4">
            <img src="/assets/icons/phone.svg" width="18" height="18" alt="" aria-hidden="true" />
          </div>
          <p class="font-semibold text-[12px] mb-1 inline-block">Telephone</p>
          <p class="text-[10px]">+1 (25) 01 7880</p>
        </div>

        <div class="overflow-hidden bg-[#fdf9e0] p-5 pb-3">
          <div class="skewed bg-primary p-2 w-fit mb-4">
            <img src="/assets/icons/whatsapp.svg" width="20" height="20" alt="" aria-hidden="true" />
          </div>
          <p class="font-semibold text-[12px] mb-1 inline-block">Chat WhatsApp</p>
          <p class="text-[10px]">Mon – Fri: 9:00 – 21:00 · Sat – Sun: 9:00 – 17:00</p>
        </div>

        <div class="overflow-hidden bg-[#fdf9e0] p-5 pb-3">
          <div class="skewed bg-primary p-2 w-fit mb-4">
            <img src="/assets/icons/quality-badge.svg" width="22" height="21" alt="" aria-hidden="true" />
          </div>
          <p class="font-semibold text-[12px] mb-1 inline-block">Quality Guarantee</p>
          <p class="text-[10px]">Verified Purchase Reviews</p>
        </div>

      </div>
    </section>


    <!-- Most Popular T-Shirts -->
    <section class="px-4 pt-24">
      <div class="flex items-center justify-between">
        <h2 class="section-title mb-8">MOST POPULAR T-SHIRTS</h2>
        <div class="flex gap-1">
          <button
            class="border border-gray-300 p-2 hover:bg-gray-100 transition-colors"
            aria-label="Previous"
            @click="prevPage"
          >
            <img src="/assets/icons/chevron-left.svg" class="w-3 h-3" alt="" aria-hidden="true" />
          </button>
          <button
            class="border border-gray-300 p-2 hover:bg-gray-100 transition-colors"
            aria-label="Next"
            @click="nextPage"
          >
            <img src="/assets/icons/chevron-right.svg" class="w-3 h-3" alt="" aria-hidden="true" />
          </button>
        </div>
      </div>

      <div v-if="featuredPending" class="grid grid-cols-2 md:grid-cols-3 gap-3 lg:flex lg:overflow-hidden">
        <div v-for="n in 6" :key="n" class="animate-pulse lg:w-[18%] lg:shrink-0">
          <div class="aspect-square bg-gray-200 mb-2" />
          <div class="h-3 bg-gray-200 mb-1 rounded" />
          <div class="h-3 w-2/3 bg-gray-200 rounded" />
        </div>
      </div>

      <div v-else-if="visibleFeatured.length > 0" class="grid grid-cols-2 md:grid-cols-3 gap-3 lg:flex lg:overflow-hidden">
        <ProductCard
          v-for="product in visibleFeatured"
          :key="product.id"
          :product="product"
          class="lg:w-[18%] lg:shrink-0"
        />
      </div>

      <p v-else class="text-center py-10 text-gray-400 font-body text-sm">
        No featured products yet.
      </p>
    </section>


    <!-- Country Leagues -->
    <section class="px-4 pt-24">
      <h2 class="section-title mb-8">COUNTRY LEAGUES</h2>
      <div class="grid grid-cols-2 md:grid-cols-5 gap-3">
        <NuxtLink
          v-for="league in staticLeagues"
          :key="league.slug"
          :to="`/products?league=${league.slug}`"
          class="block cursor-pointer group"
        >
          <div
            class="relative overflow-hidden w-full"
            style="aspect-ratio: 1 / 1;"
          >
            <div
              class="absolute inset-0 bg-cover bg-center bg-no-repeat
                     transition-transform duration-500 group-hover:scale-105"
              :style="`background-image: url('/assets/images/leagues/${league.slug}.jpg');
                       background-color: ${league.color};`"
            />
            <div class="absolute inset-0 bg-black/20 group-hover:bg-black/35 transition-colors duration-300" />
          </div>
          <p class="text-[11px] md:text-[15px] font-display font-bold mt-2 leading-tight text-black">
            {{ league.name }}
          </p>
        </NuxtLink>
      </div>
    </section>


    <!-- Other Collections -->
    <section class="pt-24 pb-20">
        <h2 class="section-title mb-8">Other collections</h2>
      <div class="grid grid-cols-2 md:grid-cols-3 gap-4 md:gap-6">
        <NuxtLink
          v-for="col in staticCollections"
          :key="col.slug"
          :to="`/products?collection=${col.slug}`"
          class="bg-no-repeat bg-cover bg-center pt-40 block cursor-pointer"
          :style="`background-image: url('/assets/images/collections/${col.slug}.jpg'); background-color: ${col.color};`"
        >
          <div class="flex items-center justify-between bg-[#0000007d] backdrop-blur-sm">
            <small class="text-xs text-white font-medium pl-3">{{ col.name }}</small>
            <small class="bg-primary p-4">
              <img src="/assets/icons/arrow-right.svg" width="8" height="8" alt="" aria-hidden="true" />
            </small>
          </div>
        </NuxtLink>
      </div>
    </section>


    <!-- Personalization & Social Networks -->
    <section class="py-10 pb-14">
      <div class="grid md:grid-cols-2 grid-cols-1 gap-6 text-white">
        <div class="relative px-6 md:px-12 pt-52 pb-8">
          <div
            class="absolute inset-0 bg-cover bg-center bg-no-repeat"
            style="background-image: url('/assets/images/personalization.jpg'); background-color: #1a1a2e;"
          />
          <div class="absolute inset-0" style="background-color: rgba(0,0,0,0.5);" />
          <div class="relative z-10">
            <p class="uppercase text-lg font-bold mb-6">Personalization</p>
            <p class="font-light text-xs">Put a custom print on the football shirt of your choice with our Personalization service.</p>
            <p class="font-light text-xs mt-3">
              Tell us what name, what number and we put it. <b class="font-bold">FREE!!!</b>
            </p>
          </div>
        </div>

        <div class="relative px-6 md:px-12 pt-52 pb-8">
          <div
            class="absolute inset-0 bg-cover bg-center bg-no-repeat"
            style="background-image: url('/assets/images/social-networks.jpg'); background-color: #111827;"
          />
          <div class="absolute inset-0" style="background-color: rgba(0,0,0,0.5);" />
          <div class="relative z-10">
            <p class="uppercase text-lg font-bold mb-6">Social Networks</p>
            <p class="font-light text-xs">Share your shirts with us with the #CamisetasFutbolSpanish</p>
            <div class="flex items-center mt-3">
              <a href="#" aria-label="Facebook" class="bg-white py-2 px-3 mr-2 hover:opacity-80 transition-opacity">
                <img src="/assets/icons/facebook.svg" width="9" height="18" alt="Facebook" />
              </a>
              <a href="#" aria-label="Twitter" class="bg-white py-2.5 px-2 mr-2 hover:opacity-80 transition-opacity">
                <img src="/assets/icons/twitter.svg" width="18" height="18" alt="Twitter" />
              </a>
              <a href="#" aria-label="Instagram" class="bg-white py-2 px-2 mr-2 hover:opacity-80 transition-opacity">
                <img src="/assets/icons/instagram.svg" width="18" height="18" alt="Instagram" />
              </a>
            </div>
          </div>
        </div>

      </div>
    </section>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { ProductList } from '~/app/types'

const { apiFetch } = useApi()

const heroSlides = [0, 1, 2, 3, 4]
const heroIndex = ref(0)

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

const staticLeagues = [
  { slug: 'champions-league',     name: 'Champions League',    color: '#0d47a1' },
  { slug: 'europa-league',        name: 'Europe League',       color: '#1b5e20' },
  { slug: 'copa-america',         name: 'Copa America',        color: '#880e4f' },
  { slug: 'asian-cup',            name: 'Asian Cup',           color: '#b71c1c' },
  { slug: 'african-nations-cup',  name: 'African Nations Cup', color: '#1b5e20' },
]

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