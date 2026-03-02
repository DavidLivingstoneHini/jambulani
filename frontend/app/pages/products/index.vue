<template>
  <div class="max-w-screen-xl mx-auto px-4 py-8">
    <nav class="text-sm font-body mb-6 text-gray-500">
      <NuxtLink to="/" class="hover:text-gray-900">Home</NuxtLink>
      <span class="mx-2">›</span>
      <span class="text-gray-900">Products</span>
    </nav>

    <div class="flex flex-col md:flex-row gap-8">
      <!-- Sidebar -->
      <aside class="w-full md:w-56 shrink-0">
        <div class="border border-gray-200 p-4">
          <h3 class="font-display font-bold uppercase text-sm tracking-wider mb-4">Filters</h3>

          <div class="mb-4">
            <label class="font-display font-semibold text-xs uppercase tracking-wide text-gray-600 mb-2 block">Search</label>
            <input v-model="filters.search" type="text" placeholder="Search products..." class="form-input text-xs" @input="debouncedFetch" />
          </div>

          <div class="mb-4">
            <label class="font-display font-semibold text-xs uppercase tracking-wide text-gray-600 mb-2 block">League</label>
            <select v-model="filters.league" class="form-select text-xs" @change="fetchProducts">
              <option value="">All Leagues</option>
              <option v-for="l in leagues" :key="l.id" :value="l.slug">{{ l.name }}</option>
            </select>
          </div>

          <div class="mb-4">
            <label class="font-display font-semibold text-xs uppercase tracking-wide text-gray-600 mb-2 block">Price Range</label>
            <div class="flex gap-2">
              <input v-model.number="filters.min_price" type="number" placeholder="Min" class="form-input text-xs w-1/2" @change="fetchProducts" />
              <input v-model.number="filters.max_price" type="number" placeholder="Max" class="form-input text-xs w-1/2" @change="fetchProducts" />
            </div>
          </div>

          <button class="w-full btn-dark text-xs py-2" @click="clearFilters">Clear Filters</button>
        </div>
      </aside>

      <!-- Grid -->
      <div class="flex-1">
        <div class="flex items-center justify-between mb-6">
          <p class="text-sm text-gray-500 font-body">
            <span v-if="!pending">{{ totalCount }} products</span>
          </p>
          <select v-model="ordering" class="form-select text-sm w-48" @change="fetchProducts">
            <option value="-created_at">Newest First</option>
            <option value="price">Price: Low to High</option>
            <option value="-price">Price: High to Low</option>
            <option value="name">Name A–Z</option>
          </select>
        </div>

        <div v-if="pending" class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
          <div v-for="n in 8" :key="n" class="animate-pulse">
            <div class="aspect-square bg-gray-200 mb-2" />
            <div class="h-4 bg-gray-200 mb-1" />
            <div class="h-4 w-1/2 bg-gray-200" />
          </div>
        </div>

        <div v-else-if="products.length === 0" class="text-center py-16 text-gray-400">
          <p class="font-display font-semibold uppercase text-sm tracking-wide">No products found</p>
          <button class="mt-4 text-sm underline font-body" @click="clearFilters">Clear filters</button>
        </div>

        <div v-else class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
          <ProductProductCard v-for="product in products" :key="product.id" :product="product" />
        </div>

        <!-- Pagination -->
        <div v-if="totalPages > 1" class="flex items-center justify-center gap-2 mt-8">
          <button
            :disabled="currentPage === 1"
            class="border border-gray-300 px-3 py-2 text-sm font-body disabled:opacity-40 hover:bg-gray-100 transition-colors"
            @click="goToPage(currentPage - 1)"
          >← Prev</button>
          <button
            v-for="p in visiblePages"
            :key="p"
            class="border px-3 py-2 text-sm font-body transition-colors"
            :class="p === currentPage ? 'bg-primary border-primary font-bold' : 'border-gray-300 hover:bg-gray-100'"
            @click="goToPage(p)"
          >{{ p }}</button>
          <button
            :disabled="currentPage === totalPages"
            class="border border-gray-300 px-3 py-2 text-sm font-body disabled:opacity-40 hover:bg-gray-100 transition-colors"
            @click="goToPage(currentPage + 1)"
          >Next →</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { ProductList, League, PaginatedResponse } from '~/app/types'

const { apiFetch } = useApi()
const route = useRoute()

const products = ref<ProductList[]>([])
const totalCount = ref(0)
const pending = ref(false)
const currentPage = ref(1)
const ordering = ref('-created_at')

const filters = reactive({
  search: (route.query.search as string) || '',
  league: (route.query.league as string) || '',
  collection: (route.query.collection as string) || '',
  min_price: '' as string | number,
  max_price: '' as string | number,
})

const totalPages = computed(() => Math.ceil(totalCount.value / 12))
const visiblePages = computed(() => {
  const pages: number[] = []
  const start = Math.max(1, currentPage.value - 2)
  const end = Math.min(totalPages.value, currentPage.value + 2)
  for (let i = start; i <= end; i++) pages.push(i)
  return pages
})

const { data: leaguesData } = await useAsyncData('leagues-filter', () => apiFetch<League[]>('/leagues/'))
const leagues = computed(() => leaguesData.value || [])

async function fetchProducts() {
  pending.value = true
  const params = new URLSearchParams()
  if (filters.search) params.set('search', filters.search)
  if (filters.league) params.set('league', filters.league)
  if (filters.collection) params.set('collection', filters.collection)
  if (filters.min_price) params.set('min_price', String(filters.min_price))
  if (filters.max_price) params.set('max_price', String(filters.max_price))
  params.set('ordering', ordering.value)
  params.set('page', String(currentPage.value))

  try {
    const data = await apiFetch<PaginatedResponse<ProductList>>(`/products/?${params.toString()}`)
    products.value = data.results
    totalCount.value = data.count
  } catch (e) {
    console.error(e)
  } finally {
    pending.value = false
  }
}

function clearFilters() {
  filters.search = ''
  filters.league = ''
  filters.collection = ''
  filters.min_price = ''
  filters.max_price = ''
  currentPage.value = 1
  fetchProducts()
}

function goToPage(page: number) {
  currentPage.value = page
  window.scrollTo({ top: 0, behavior: 'smooth' })
  fetchProducts()
}

let debounceTimer: ReturnType<typeof setTimeout>
function debouncedFetch() {
  clearTimeout(debounceTimer)
  debounceTimer = setTimeout(() => {
    currentPage.value = 1
    fetchProducts()
  }, 400)
}

onMounted(() => fetchProducts())

useHead({ title: 'Products — Jambulani' })
</script>
