<template>
  <div class="max-w-screen-xl mx-auto px-4 py-8">
    <nav class="text-sm font-body mb-6 text-gray-500">
      <NuxtLink to="/" class="hover:text-gray-900">Home</NuxtLink>
      <span class="mx-2">›</span>
      <span class="text-gray-900">Products</span>
    </nav>

    <div class="flex flex-col md:flex-row gap-8">
      <aside class="w-full md:w-56 shrink-0">
        <div class="border border-gray-200 p-4">
          <h3 class="font-body font-bold uppercase text-sm tracking-wider mb-4">Filters</h3>

          <!-- Search Input -->
          <div class="mb-4">
            <label class="font-body font-semibold text-xs uppercase tracking-wide text-gray-600 mb-2 block">
              Search
            </label>
            <div class="relative">
              <input
                v-model="filters.search"
                type="text"
                placeholder="Search products..."
                class="form-input text-xs pr-8"
                @input="debouncedSearch"
              />
              <svg
                v-if="filters.search"
                class="absolute right-2 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400 cursor-pointer hover:text-gray-600"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
                @click="clearSearch"
              >
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </div>
          </div>

          <div class="mb-4">
            <label class="font-body font-semibold text-xs uppercase tracking-wide text-gray-600 mb-2 block">
              League
            </label>
            <select v-model="filters.league" class="form-select text-xs" @change="applyFilters">
              <option value="">All Leagues</option>
              <option v-if="leagues && leagues.length" v-for="l in leagues" :key="l.id" :value="l.slug">{{ l.name }}</option>
            </select>
          </div>

          <div class="mb-4">
            <label class="font-body font-semibold text-xs uppercase tracking-wide text-gray-600 mb-2 block">
              Category
            </label>
            <select v-model="filters.category" class="form-select text-xs" @change="applyFilters">
              <option value="">All Categories</option>
              <option v-if="categories && categories.length" v-for="c in categories" :key="c.id" :value="c.slug">{{ c.name }}</option>
            </select>
          </div>

          <div class="mb-4" v-if="collections && collections.length">
            <label class="font-body font-semibold text-xs uppercase tracking-wide text-gray-600 mb-2 block">
              Collection
            </label>
            <select v-model="filters.collection" class="form-select text-xs" @change="applyFilters">
              <option value="">All Collections</option>
              <option v-if="collections && collections.length" v-for="c in collections" :key="c.id" :value="c.slug">{{ c.name }}</option>
            </select>
          </div>

          <!-- Price Range -->
          <div class="mb-4">
            <label class="font-body font-semibold text-xs uppercase tracking-wide text-gray-600 mb-2 block">
              Price Range (€)
            </label>
            <div class="flex gap-2">
              <input
                v-model.number="filters.min_price"
                type="number"
                placeholder="Min"
                min="0"
                class="form-input text-xs w-1/2"
                @change="applyFilters"
              />
              <input
                v-model.number="filters.max_price"
                type="number"
                placeholder="Max"
                min="0"
                class="form-input text-xs w-1/2"
                @change="applyFilters"
              />
            </div>
          </div>

          <button class="w-full btn-dark text-xs py-2" @click="clearFilters">Clear Filters</button>
        </div>
      </aside>

      <!-- Main Content -->
      <div class="flex-1">
        <div v-if="hasActiveFilters" class="flex flex-wrap items-center gap-2 mb-4">
          <span class="text-xs text-gray-500 font-body">Active filters:</span>
          
          <span
            v-if="filters.search"
            class="inline-flex items-center gap-1 bg-gray-100 px-2 py-1 text-xs rounded"
          >
            Search: "{{ filters.search }}"
            <button @click="removeFilter('search')" class="text-gray-500 hover:text-gray-700">×</button>
          </span>
          
          <span
            v-if="filters.league && selectedLeagueName"
            class="inline-flex items-center gap-1 bg-gray-100 px-2 py-1 text-xs rounded"
          >
            League: {{ selectedLeagueName }}
            <button @click="removeFilter('league')" class="text-gray-500 hover:text-gray-700">×</button>
          </span>
          
          <span
            v-if="filters.category && selectedCategoryName"
            class="inline-flex items-center gap-1 bg-gray-100 px-2 py-1 text-xs rounded"
          >
            Category: {{ selectedCategoryName }}
            <button @click="removeFilter('category')" class="text-gray-500 hover:text-gray-700">×</button>
          </span>
          
          <span
            v-if="filters.collection && selectedCollectionName"
            class="inline-flex items-center gap-1 bg-gray-100 px-2 py-1 text-xs rounded"
          >
            Collection: {{ selectedCollectionName }}
            <button @click="removeFilter('collection')" class="text-gray-500 hover:text-gray-700">×</button>
          </span>
          
          <span
            v-if="filters.min_price || filters.max_price"
            class="inline-flex items-center gap-1 bg-gray-100 px-2 py-1 text-xs rounded"
          >
            Price: {{ filters.min_price || '0' }} - {{ filters.max_price || '∞' }} €
            <button @click="removeFilter('price')" class="text-gray-500 hover:text-gray-700">×</button>
          </span>
          
          <button
            class="text-xs text-gray-500 underline hover:text-gray-700"
            @click="clearFilters"
          >
            Clear all
          </button>
        </div>

        <div class="flex items-center justify-between mb-6">
          <p class="text-sm text-gray-500 font-body">
            <span v-if="!pending && totalCount !== null">{{ totalCount }} product{{ totalCount !== 1 ? 's' : '' }} found</span>
            <span v-else-if="pending" class="text-gray-400">Loading products...</span>
            <span v-if="filters.search && !pending && totalCount !== null" class="text-xs ml-2 text-gray-400">
              for "{{ filters.search }}"
            </span>
          </p>
          <select v-model="ordering" class="form-select text-sm w-48" @change="applyFilters">
            <option value="-created_at">Newest First</option>
            <option value="price">Price: Low to High</option>
            <option value="-price">Price: High to Low</option>
            <option value="name">Name A–Z</option>
            <option value="-name">Name Z–A</option>
          </select>
        </div>

        <div v-if="pending" class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
          <div v-for="n in 8" :key="n" class="animate-pulse">
            <div class="aspect-square bg-gray-200 mb-2" />
            <div class="h-4 bg-gray-200 mb-1 rounded" />
            <div class="h-4 w-1/2 bg-gray-200 rounded" />
          </div>
        </div>

        <!-- Empty State -->
        <div v-else-if="!products || products.length === 0" class="text-center py-16 text-gray-400">
          <svg class="w-16 h-16 mx-auto mb-4 opacity-30" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5"
              d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
          </svg>
          <p class="font-body font-semibold uppercase text-sm tracking-wide">No products found</p>
          <p class="text-xs mt-1">Try adjusting your search or filters</p>
          <button class="mt-4 text-sm underline font-body hover:text-gray-600" @click="clearFilters">
            Clear all filters
          </button>
        </div>

        <div v-else class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
          <ProductCard
            v-for="product in products"
            :key="product?.id || Math.random()"
            :product="product"
          />
        </div>

        <!-- Pagination -->
        <div v-if="!pending && totalPages > 1" class="flex items-center justify-center gap-2 mt-8">
          <button
            :disabled="currentPage === 1"
            class="border border-gray-300 px-3 py-2 text-sm font-body disabled:opacity-40 hover:bg-gray-100 transition-colors"
            @click="goToPage(currentPage - 1)"
          >
            ← Prev
          </button>
          <button
            v-for="p in visiblePages"
            :key="p"
            class="border px-3 py-2 text-sm font-body transition-colors"
            :class="p === currentPage ? 'bg-primary border-primary font-bold' : 'border-gray-300 hover:bg-gray-100'"
            @click="goToPage(p)"
          >
            {{ p }}
          </button>
          <button
            :disabled="currentPage === totalPages"
            class="border border-gray-300 px-3 py-2 text-sm font-body disabled:opacity-40 hover:bg-gray-100 transition-colors"
            @click="goToPage(currentPage + 1)"
          >
            Next →
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { ProductList, League, Collection, Category, PaginatedResponse } from '~/app/types'
import { useDebounceFn } from '@vueuse/core'

definePageMeta({
  ssr: false
})

const { apiFetch } = useApi()
const route = useRoute()
const router = useRouter()

// State
const products = ref<ProductList[]>([])
const totalCount = ref<number | null>(null)
const pending = ref(false)
const currentPage = ref(1)
const ordering = ref('-created_at')
const leagues = ref<League[]>([])
const categories = ref<Category[]>([])
const collections = ref<Collection[]>([])

const filters = reactive({
  search: (route.query.search as string) || '',
  league: (route.query.league as string) || '',
  category: (route.query.category as string) || '',
  collection: (route.query.collection as string) || '',
  min_price: (route.query.min_price as string) || '',
  max_price: (route.query.max_price as string) || '',
})

onMounted(async () => {
  try {
    const [leaguesData, categoriesData, collectionsData] = await Promise.all([
      apiFetch<League[]>('/leagues/').catch(() => []),
      apiFetch<Category[]>('/categories/').catch(() => []),
      apiFetch<Collection[]>('/collections/').catch(() => [])
    ])
    leagues.value = leaguesData || []
    categories.value = categoriesData || []
    collections.value = collectionsData || []
  } catch (error) {
    console.error('Failed to fetch filter options:', error)
  }
  
  await fetchProducts()
})

// Computed properties
const hasActiveFilters = computed(() => {
  return !!(filters.search || filters.league || filters.category || filters.collection || filters.min_price || filters.max_price)
})

const selectedLeagueName = computed(() => {
  if (!filters.league || !leagues.value || !leagues.value.length) return ''
  const league = leagues.value.find(l => l && l.slug === filters.league)
  return league?.name || filters.league
})

const selectedCategoryName = computed(() => {
  if (!filters.category || !categories.value || !categories.value.length) return ''
  const category = categories.value.find(c => c && c.slug === filters.category)
  return category?.name || filters.category
})

const selectedCollectionName = computed(() => {
  if (!filters.collection || !collections.value || !collections.value.length) return ''
  const collection = collections.value.find(c => c && c.slug === filters.collection)
  return collection?.name || filters.collection
})

const totalPages = computed(() => {
  if (!totalCount.value) return 1
  return Math.ceil(totalCount.value / 12)
})

const visiblePages = computed(() => {
  const pages: number[] = []
  const total = totalPages.value
  const current = currentPage.value
  
  if (!total || total <= 1) return pages
  
  const start = Math.max(1, current - 2)
  const end = Math.min(total, current + 2)
  
  for (let i = start; i <= end; i++) {
    pages.push(i)
  }
  return pages
})

// Helper function to remove individual filters
const removeFilter = (filterType: string) => {
  switch (filterType) {
    case 'search':
      filters.search = ''
      break
    case 'league':
      filters.league = ''
      break
    case 'category':
      filters.category = ''
      break
    case 'collection':
      filters.collection = ''
      break
    case 'price':
      filters.min_price = ''
      filters.max_price = ''
      break
  }
  currentPage.value = 1
  fetchProducts()
}

const updateUrl = () => {
  const query: Record<string, string> = {}
  
  if (filters.search) query.search = filters.search
  if (filters.league) query.league = filters.league
  if (filters.category) query.category = filters.category
  if (filters.collection) query.collection = filters.collection
  if (filters.min_price) query.min_price = String(filters.min_price)
  if (filters.max_price) query.max_price = String(filters.max_price)
  if (ordering.value !== '-created_at') query.sort = ordering.value
  if (currentPage.value > 1) query.page = String(currentPage.value)

  const currentQuery = JSON.stringify(route.query)
  const newQuery = JSON.stringify(query)
  
  if (currentQuery !== newQuery) {
    router.replace({ query })
  }
}

// Fetch products with current filters
async function fetchProducts() {
  pending.value = true
  
  const params = new URLSearchParams()
  
  if (filters.search) params.set('search', filters.search)
  if (filters.league) params.set('league', filters.league)
  if (filters.category) params.set('category', filters.category)
  if (filters.collection) params.set('collection', filters.collection)
  if (filters.min_price) params.set('min_price', String(filters.min_price))
  if (filters.max_price) params.set('max_price', String(filters.max_price))
  if (ordering.value) params.set('ordering', ordering.value)
  params.set('page', String(currentPage.value))

  try {
    console.log('Fetching products with params:', params.toString())
    const data = await apiFetch<PaginatedResponse<ProductList>>(`/products/?${params.toString()}`)
    console.log('Products response:', data)
    
    if (!data) {
      throw new Error('No data received from server')
    }
    
    products.value = data.results || []
    totalCount.value = data.count || 0
    
    console.log(`Loaded ${products.value.length} products out of ${totalCount.value} total`)
    
    updateUrl()
  } catch (error: any) {
    console.error('Failed to fetch products:', error)
    products.value = []
    totalCount.value = 0
  } finally {
    pending.value = false
  }
}

// Debounced search
const debouncedSearch = useDebounceFn(() => {
  currentPage.value = 1
  fetchProducts()
}, 400)

const applyFilters = () => {
  currentPage.value = 1
  fetchProducts()
}

const clearSearch = () => {
  filters.search = ''
  currentPage.value = 1
  fetchProducts()
}

const clearFilters = () => {
  filters.search = ''
  filters.league = ''
  filters.category = ''
  filters.collection = ''
  filters.min_price = ''
  filters.max_price = ''
  ordering.value = '-created_at'
  currentPage.value = 1
  fetchProducts()
}

const goToPage = (page: number) => {
  if (page < 1 || page > totalPages.value) return
  currentPage.value = page
  window.scrollTo({ top: 0, behavior: 'smooth' })
  fetchProducts()
}

// Watch route changes
watch(
  () => route.query,
  (newQuery) => {
    const shouldUpdate = 
      newQuery.search !== filters.search ||
      newQuery.league !== filters.league ||
      newQuery.category !== filters.category ||
      newQuery.collection !== filters.collection ||
      newQuery.min_price !== filters.min_price ||
      newQuery.max_price !== filters.max_price
    
    if (shouldUpdate) {
      filters.search = (newQuery.search as string) || ''
      filters.league = (newQuery.league as string) || ''
      filters.category = (newQuery.category as string) || ''
      filters.collection = (newQuery.collection as string) || ''
      filters.min_price = (newQuery.min_price as string) || ''
      filters.max_price = (newQuery.max_price as string) || ''
      currentPage.value = Number(newQuery.page) || 1
      fetchProducts()
    }
  },
  { deep: true }
)

useHead({
  title: 'Products — Jambulani'
})
</script>
