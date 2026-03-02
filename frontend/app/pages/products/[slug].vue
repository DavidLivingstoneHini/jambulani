<template>
  <div class="max-w-screen-xl mx-auto px-4 py-5">

    <!-- Breadcrumb -->
    <nav v-if="product" class="flex items-center gap-1.5 text-[13px] font-body mb-5 text-gray-500">
      <NuxtLink to="/" class="text-[#0071e3] hover:underline">Home</NuxtLink>
      <span class="text-gray-400">›</span>
      <NuxtLink
        v-if="product.league"
        :to="`/products?league=${product.league.slug}`"
        class="text-[#0071e3] hover:underline"
      >{{ product.league.name }}</NuxtLink>
      <span v-if="product.league" class="text-gray-400">›</span>
      <span class="text-gray-700">{{ product.name }}</span>
    </nav>

    <!-- Skeleton loading -->
    <div v-if="pending" class="grid grid-cols-1 md:grid-cols-2 gap-10 animate-pulse">
      <div>
        <div class="aspect-square bg-gray-200 mb-3" />
        <div class="flex gap-2">
          <div v-for="n in 6" :key="n" class="w-[68px] h-[68px] bg-gray-200 shrink-0" />
        </div>
      </div>
      <div class="space-y-4 pt-2">
        <div class="h-8 bg-gray-200 w-3/4 rounded" />
        <div class="h-8 bg-gray-200 w-1/3 rounded" />
        <div class="h-20 bg-gray-200 rounded" />
        <div class="h-10 bg-gray-200 rounded" />
        <div class="h-10 bg-gray-200 rounded" />
        <div class="h-10 bg-gray-200 rounded" />
        <div class="h-12 bg-gray-200 rounded" />
      </div>
    </div>

    <!-- Product detail -->
    <div v-else-if="product" class="grid grid-cols-1 md:grid-cols-2 gap-10">

      <!-- ── LEFT: Images ── -->
      <div>
        <!-- Main image -->
        <div class="relative overflow-hidden bg-gray-100 mb-2" style="aspect-ratio:1/1;">
          <img
            v-if="selectedImage || product.images[0]?.image"
            :src="selectedImage || product.images[0]?.image"
            :alt="product.name"
            class="w-full h-full object-cover"
          />
          <div v-else class="w-full h-full flex items-center justify-center">
            <svg class="w-20 h-20 text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
            </svg>
          </div>

          <!-- Arrow nav (only when >1 image) -->
          <template v-if="product.images.length > 1">
            <button
              class="absolute left-2 top-1/2 -translate-y-1/2 bg-black/50 text-white p-2 hover:bg-black/75 transition-colors"
              @click="prevImage"
            >
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
              </svg>
            </button>
            <button
              class="absolute right-2 top-1/2 -translate-y-1/2 bg-black/50 text-white p-2 hover:bg-black/75 transition-colors"
              @click="nextImage"
            >
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
              </svg>
            </button>
          </template>

          <!-- Small down-arrow indicator (bottom-centre, like design) -->
          <div class="absolute bottom-2 left-1/2 -translate-x-1/2">
            <svg class="w-4 h-4 text-white/70" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
            </svg>
          </div>
        </div>

        <!-- Thumbnail strip -->
        <div class="flex gap-2 overflow-x-auto pb-1">
          <button
            v-for="img in product.images"
            :key="img.id"
            class="w-[68px] h-[68px] shrink-0 border-2 overflow-hidden transition-colors"
            :class="selectedImage === img.image
              ? 'border-gray-900'
              : 'border-gray-200 hover:border-gray-400'"
            @click="selectedImage = img.image"
          >
            <img :src="img.image" :alt="img.alt_text" class="w-full h-full object-cover" />
          </button>
        </div>
      </div>


      <!-- ── RIGHT: Product info ── -->
      <div class="pt-1">

        <!-- Name -->
        <h1 class="font-display font-bold text-[26px] md:text-[30px] uppercase leading-tight text-gray-900 mb-3">
          {{ product.name }}
        </h1>

        <!-- Price row -->
        <div class="flex items-center gap-3 flex-wrap mb-5">
          <span class="font-display font-bold text-[34px] text-gray-900 leading-none">€{{ product.price }}</span>
          <span v-if="product.original_price" class="text-red-500 line-through text-[17px] font-body">€{{ product.original_price }}</span>
          <span v-if="product.discount_percentage > 0" class="bg-green-500 text-white text-[12px] font-bold px-2 py-0.5 uppercase font-display">
            Save {{ product.discount_percentage }}%
          </span>
          <button class="ml-auto flex items-center gap-1.5 text-gray-400 hover:text-gray-700 transition-colors text-[13px] font-body">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
            </svg>
            Add to Favorites
          </button>
        </div>

        <!-- Description -->
        <div class="mb-6">
          <p class="font-body text-gray-600 text-[13px] leading-[1.65]">
            {{ showFullDesc ? product.description : truncated }}
          </p>
          <button
            v-if="product.description.length > 200"
            class="text-[13px] text-gray-900 font-body font-semibold mt-1 hover:underline"
            @click="showFullDesc = !showFullDesc"
          >{{ showFullDesc ? 'Read Less' : 'Read More' }}</button>
        </div>

        <!-- Divider -->
        <div class="border-t border-gray-200 mb-5" />

        <!-- Size field -->
        <div class="mb-4">
          <div class="flex items-center justify-between mb-1.5">
            <label class="font-display font-bold uppercase text-[13px] text-gray-800">
              Size <span class="text-red-500">*</span>
            </label>
            <button
              v-if="product.size_chart"
              class="border border-gray-900 px-3 py-1 text-[11px] font-display font-bold uppercase hover:bg-gray-100 transition-colors"
              @click="showSizeChart = true"
            >View Size Chart</button>
          </div>
          <div class="relative">
            <select v-model="form.size" class="form-select pr-8">
              <option value="" disabled>Select a shirt size</option>
              <option v-for="size in product.available_sizes" :key="size" :value="size">{{ size }}</option>
            </select>
            <div class="absolute right-3 top-1/2 -translate-y-1/2 pointer-events-none">
              <svg class="w-3 h-3 text-gray-500" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" clip-rule="evenodd" />
              </svg>
            </div>
          </div>
        </div>

        <!-- Name customisation -->
        <div v-if="product.allow_name_customization" class="mb-4">
          <label class="font-display font-bold uppercase text-[13px] text-gray-800 mb-1.5 block">Name</label>
          <input
            v-model="form.custom_name"
            type="text"
            placeholder="What name would you want in the shirt?"
            class="form-input"
            maxlength="100"
          />
        </div>

        <!-- Number customisation -->
        <div v-if="product.allow_number_customization" class="mb-4">
          <label class="font-display font-bold uppercase text-[13px] text-gray-800 mb-1.5 block">Number on Shirt</label>
          <input
            v-model="form.custom_number"
            type="number"
            placeholder="Enter a number between 0 and 99"
            class="form-input"
            min="0"
            max="99"
          />
        </div>

        <!-- Patch -->
        <div v-if="product.patches.length > 0" class="mb-4">
          <label class="font-display font-bold uppercase text-[13px] text-gray-800 mb-1.5 block">Patch</label>
          <div class="relative">
            <select v-model="form.patch_id" class="form-select pr-8">
              <option :value="null">Select a patch</option>
              <option v-for="patch in product.patches" :key="patch.id" :value="patch.id">
                {{ patch.name }}<template v-if="+patch.extra_price > 0"> (+€{{ patch.extra_price }})</template>
              </option>
            </select>
            <div class="absolute right-3 top-1/2 -translate-y-1/2 pointer-events-none">
              <svg class="w-3 h-3 text-gray-500" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" clip-rule="evenodd" />
              </svg>
            </div>
          </div>
        </div>

        <!-- Quantity -->
        <div class="mb-6">
          <label class="font-display font-bold uppercase text-[13px] text-gray-800 mb-1.5 block">Quantity</label>
          <div class="flex items-center border border-gray-300 w-[108px]">
            <button
              class="w-8 h-9 flex items-center justify-center text-gray-600 hover:bg-gray-100 transition-colors text-lg leading-none"
              @click="form.quantity = Math.max(1, form.quantity - 1)"
            >−</button>
            <span class="flex-1 text-center font-body text-[13px] border-x border-gray-300 h-9 flex items-center justify-center">
              {{ form.quantity }}
            </span>
            <button
              class="w-8 h-9 flex items-center justify-center text-gray-600 hover:bg-gray-100 transition-colors text-lg leading-none"
              @click="form.quantity++"
            >+</button>
          </div>
        </div>

        <!-- Feedback messages -->
        <p v-if="formError" class="text-red-500 text-[13px] font-body mb-3">{{ formError }}</p>
        <p v-if="addedSuccess" class="text-green-600 text-[13px] font-body mb-3">✓ Added to cart successfully!</p>

        <!-- Add to Cart button — yellow with cart icon on right -->
        <button
          class="w-full flex items-center justify-between bg-primary hover:bg-primary-600 transition-colors py-4 px-6 cursor-pointer disabled:opacity-60"
          :disabled="cartStore.loading"
          @click="handleAddToCart"
        >
          <span class="font-display font-bold uppercase text-[15px] tracking-wider text-black">
            {{ cartStore.loading ? 'Adding...' : 'Add to Cart' }}
          </span>
          <div class="bg-black p-2 ml-4">
            <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 11-4 0 2 2 0 014 0z" />
            </svg>
          </div>
        </button>

      </div>
    </div>

    <!-- 404 -->
    <div v-else-if="!pending" class="text-center py-16">
      <p class="font-display font-bold text-xl mb-4 uppercase">Product not found</p>
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
            <h3 class="font-display font-bold uppercase text-base tracking-wide">{{ product.size_chart.name }}</h3>
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
  () => apiFetch<ProductDetail>(`/products/${route.params.slug}/`).catch(() => null)
)

const truncated = computed(() => {
  if (!product.value) return ''
  const desc = product.value.description
  return desc.length > 200 ? desc.slice(0, 200) + '...' : desc
})

watch(product, (p) => {
  if (p?.images.length) {
    const primary = p.images.find(img => img.is_primary)
    selectedImage.value = primary?.image ?? p.images[0]?.image ?? null
    imageIndex.value = primary ? p.images.indexOf(primary) : 0
  }
}, { immediate: true })

function prevImage() {
  if (!product.value?.images.length) return
  imageIndex.value = (imageIndex.value - 1 + product.value.images.length) % product.value.images.length
  selectedImage.value = product.value.images[imageIndex.value]?.image ?? null
}
function nextImage() {
  if (!product.value?.images.length) return
  imageIndex.value = (imageIndex.value + 1) % product.value.images.length
  selectedImage.value = product.value.images[imageIndex.value]?.image ?? null
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
    setTimeout(() => { addedSuccess.value = false }, 3000)
  } catch (e: unknown) {
    const err = e as Record<string, Record<string, string>>
    formError.value = err?.data?.detail ?? 'Failed to add to cart. Please try again.'
  }
}

useHead({
  title: () => product.value ? `${product.value.name} — Jambulani` : 'Product — Jambulani',
})
</script>

<style scoped>
.fade-enter-active, .fade-leave-active { transition: opacity 0.2s; }
.fade-enter-from, .fade-leave-to { opacity: 0; }
</style>
