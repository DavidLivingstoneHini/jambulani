<template>
  <div class="max-w-screen-xl mx-auto px-4 py-6">
    <nav v-if="product" class="text-sm font-body mb-6 text-gray-500">
      <NuxtLink to="/" class="hover:text-gray-900">Home</NuxtLink>
      <span class="mx-2">›</span>
      <NuxtLink
        v-if="product.league"
        :to="`/products?league=${product.league.slug}`"
        class="hover:text-gray-900"
      >{{ product.league.name }}</NuxtLink>
      <span v-if="product.league" class="mx-2">›</span>
      <span class="text-gray-900 line-clamp-1">{{ product.name }}</span>
    </nav>

    <!-- Skeleton -->
    <div v-if="pending" class="grid grid-cols-1 md:grid-cols-2 gap-10 animate-pulse">
      <div>
        <div class="aspect-square bg-gray-200 mb-4" />
        <div class="flex gap-2">
          <div v-for="n in 5" :key="n" class="w-16 h-16 bg-gray-200" />
        </div>
      </div>
      <div class="space-y-4">
        <div class="h-8 bg-gray-200 w-3/4" />
        <div class="h-6 bg-gray-200 w-1/3" />
        <div class="h-24 bg-gray-200" />
        <div class="h-10 bg-gray-200" />
        <div class="h-10 bg-gray-200" />
        <div class="h-12 bg-gray-200" />
      </div>
    </div>

    <div v-else-if="product" class="grid grid-cols-1 md:grid-cols-2 gap-10">
      <!-- Images -->
      <div>
        <div class="relative aspect-square bg-gray-100 overflow-hidden mb-3">
          <img
            :src="selectedImage || product.images[0]?.image || ''"
            :alt="product.name"
            class="w-full h-full object-cover"
          />
          <template v-if="product.images.length > 1">
            <button
              class="absolute left-2 top-1/2 -translate-y-1/2 bg-black/50 text-white p-2 hover:bg-black/70 transition-colors"
              @click="prevImage"
            >
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
              </svg>
            </button>
            <button
              class="absolute right-2 top-1/2 -translate-y-1/2 bg-black/50 text-white p-2 hover:bg-black/70 transition-colors"
              @click="nextImage"
            >
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
              </svg>
            </button>
          </template>
        </div>
        <div class="flex gap-2 overflow-x-auto pb-1">
          <button
            v-for="img in product.images"
            :key="img.id"
            class="w-16 h-16 shrink-0 border-2 overflow-hidden transition-colors"
            :class="selectedImage === img.image ? 'border-gray-900' : 'border-transparent hover:border-gray-300'"
            @click="selectedImage = img.image"
          >
            <img :src="img.image" :alt="img.alt_text" class="w-full h-full object-cover" />
          </button>
        </div>
      </div>

      <!-- Info -->
      <div>
        <h1 class="font-display font-bold text-2xl md:text-3xl uppercase leading-tight mb-3">
          {{ product.name }}
        </h1>

        <div class="flex items-center gap-3 mb-5">
          <span class="font-display font-bold text-3xl">€{{ product.price }}</span>
          <span v-if="product.original_price" class="price-original text-lg">€{{ product.original_price }}</span>
          <span v-if="product.discount_percentage > 0" class="badge-save">Save {{ product.discount_percentage }}%</span>
          <button class="ml-auto flex items-center gap-1.5 text-gray-400 hover:text-red-500 transition-colors">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
            </svg>
            <span class="text-sm font-body">Add to Favorites</span>
          </button>
        </div>

        <div class="mb-6">
          <p class="font-body text-gray-600 text-sm leading-relaxed">
            {{ showFullDesc ? product.description : truncated }}
          </p>
          <button
            v-if="product.description.length > 200"
            class="text-sm text-gray-900 font-body underline mt-1"
            @click="showFullDesc = !showFullDesc"
          >
            {{ showFullDesc ? 'Read Less' : 'Read More' }}
          </button>
        </div>

        <!-- Size -->
        <div class="mb-4">
          <div class="flex items-center justify-between mb-2">
            <label class="font-display font-bold uppercase text-sm">
              Size <span class="text-red-500">*</span>
            </label>
            <button
              v-if="product.size_chart"
              class="border border-gray-900 px-3 py-1 text-xs font-display font-bold uppercase hover:bg-gray-100 transition-colors"
              @click="showSizeChart = true"
            >Size Chart</button>
          </div>
          <select v-model="form.size" class="form-select" required>
            <option value="" disabled>Select a shirt size</option>
            <option v-for="size in product.available_sizes" :key="size" :value="size">{{ size }}</option>
          </select>
        </div>

        <!-- Name -->
        <div v-if="product.allow_name_customization" class="mb-4">
          <label class="font-display font-bold uppercase text-sm mb-2 block">Name</label>
          <input v-model="form.custom_name" type="text" placeholder="What name would you want in the shirt?" class="form-input" maxlength="100" />
        </div>

        <!-- Number -->
        <div v-if="product.allow_number_customization" class="mb-4">
          <label class="font-display font-bold uppercase text-sm mb-2 block">Number on Shirt</label>
          <input v-model="form.custom_number" type="number" placeholder="Enter a number between 0 and 99" class="form-input" min="0" max="99" />
        </div>

        <!-- Patch -->
        <div v-if="product.patches.length > 0" class="mb-4">
          <label class="font-display font-bold uppercase text-sm mb-2 block">Patch</label>
          <select v-model="form.patch_id" class="form-select">
            <option :value="null">Select a patch</option>
            <option v-for="patch in product.patches" :key="patch.id" :value="patch.id">
              {{ patch.name }}<span v-if="+patch.extra_price > 0"> (+€{{ patch.extra_price }})</span>
            </option>
          </select>
        </div>

        <!-- Quantity -->
        <div class="mb-6">
          <label class="font-display font-bold uppercase text-sm mb-2 block">Quantity</label>
          <div class="flex items-center border border-gray-300 w-fit">
            <button class="px-3 py-2 text-gray-500 hover:bg-gray-100 transition-colors" @click="form.quantity = Math.max(1, form.quantity - 1)">−</button>
            <span class="px-5 py-2 font-body text-sm border-x border-gray-300">{{ form.quantity }}</span>
            <button class="px-3 py-2 text-gray-500 hover:bg-gray-100 transition-colors" @click="form.quantity++">+</button>
          </div>
        </div>

        <p v-if="formError" class="text-red-500 text-sm font-body mb-3">{{ formError }}</p>
        <p v-if="addedSuccess" class="text-green-600 text-sm font-body mb-3">✓ Added to cart!</p>

        <button
          class="btn-primary w-full flex items-center justify-center gap-3 py-4 text-base"
          :disabled="cartStore.loading"
          @click="handleAddToCart"
        >
          <span>{{ cartStore.loading ? 'Adding...' : 'Add to Cart' }}</span>
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 11-4 0 2 2 0 014 0z" />
          </svg>
        </button>
      </div>
    </div>

    <!-- 404 -->
    <div v-else-if="!pending" class="text-center py-16">
      <p class="font-display font-bold text-xl mb-4">Product not found</p>
      <NuxtLink to="/products" class="btn-primary inline-block">Back to Products</NuxtLink>
    </div>

    <!-- Size Chart Modal -->
    <Transition name="fade">
      <div
        v-if="showSizeChart && product?.size_chart"
        class="fixed inset-0 bg-black/60 z-50 flex items-center justify-center p-4"
        @click.self="showSizeChart = false"
      >
        <div class="bg-white max-w-lg w-full p-6">
          <div class="flex justify-between items-center mb-4">
            <h3 class="font-display font-bold uppercase text-lg">{{ product.size_chart.name }}</h3>
            <button class="p-1 hover:bg-gray-100 transition-colors" @click="showSizeChart = false">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
          <img :src="product.size_chart.image" :alt="product.size_chart.name" class="w-full" />
          <p v-if="product.size_chart.description" class="mt-3 text-sm font-body text-gray-600">
            {{ product.size_chart.description }}
          </p>
        </div>
      </div>
    </Transition>
  </div>
</template>

<script setup lang="ts">
import type { ProductDetail } from '~/app/types'

const route = useRoute()
const cartStore = useCartStore()
const { apiFetch } = useApi()

const selectedImage = ref<string | null>(null)
const imageIndex = ref(0)
const showFullDesc = ref(false)
const showSizeChart = ref(false)
const formError = ref('')
const addedSuccess = ref(false)

const form = reactive({
  size: '',
  custom_name: '',
  custom_number: '',
  patch_id: null as number | null,
  quantity: 1,
})

const { data: product, pending } = await useAsyncData(
  `product-${route.params.slug}`,
  () => apiFetch<ProductDetail>(`/products/${route.params.slug}/`)
)

const truncated = computed(() => {
  if (!product.value) return ''
  return product.value.description.length > 200
    ? product.value.description.slice(0, 200) + '...'
    : product.value.description
})

watch(product, (p) => {
  if (p?.images.length) {
    const primary = p.images.find(img => img.is_primary)
    selectedImage.value = primary?.image || p.images[0]?.image || null
  }
}, { immediate: true })

function prevImage() {
  if (!product.value?.images.length) return
  imageIndex.value = (imageIndex.value - 1 + product.value.images.length) % product.value.images.length
  selectedImage.value = product.value.images[imageIndex.value].image
}
function nextImage() {
  if (!product.value?.images.length) return
  imageIndex.value = (imageIndex.value + 1) % product.value.images.length
  selectedImage.value = product.value.images[imageIndex.value].image
}

async function handleAddToCart() {
  formError.value = ''
  addedSuccess.value = false
  if (!form.size) {
    formError.value = 'Please select a size.'
    return
  }
  if (!product.value) return
  try {
    await cartStore.addItem({
      product_id: product.value.id,
      size: form.size,
      quantity: form.quantity,
      custom_name: form.custom_name,
      custom_number: form.custom_number,
      patch_id: form.patch_id,
    })
    addedSuccess.value = true
    setTimeout(() => (addedSuccess.value = false), 3000)
  } catch (e: any) {
    formError.value = e?.data?.detail || 'Failed to add to cart. Please try again.'
  }
}

useHead({
  title: computed(() => product.value ? `${product.value.name} — Jambulani` : 'Product — Jambulani'),
})
</script>

<style scoped>
.fade-enter-active, .fade-leave-active { transition: opacity 0.2s; }
.fade-enter-from, .fade-leave-to { opacity: 0; }
</style>
