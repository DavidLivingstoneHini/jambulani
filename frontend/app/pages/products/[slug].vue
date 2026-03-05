<template>
  <div class="md:px-[120px] py-6 pb-32 max-w-7xl w-full mx-auto px-2">
    <nav v-if="product" class="w-full mb-4">
      <ol class="flex items-center text-[9px] md:text-[10px]">
        <li>
          <NuxtLink to="/" class="text-[#1256DB] hover:underline">Home</NuxtLink>
        </li>
        <li><span class="mx-2 text-gray-500">&gt;</span></li>
        <li>
          <NuxtLink
            v-if="product.league"
            :to="`/products?league=${product.league.slug}`"
            class="text-[#1256DB] hover:underline"
          >{{ product.league.name }}</NuxtLink>
          <span v-else class="text-[#1256DB]">category</span>
        </li>
        <li><span class="mx-2 text-gray-500">&gt;</span></li>
        <li class="text-gray-400">{{ product.name }}</li>
      </ol>
    </nav>

    <div v-if="pending" class="md:grid grid-cols-2 flex flex-col py-5 animate-pulse gap-10">
      <div>
        <div class="bg-gray-200 mb-3" style="width:480px; height:450px; max-width:100%;" />
        <div class="flex gap-2 mt-2">
          <div v-for="n in 6" :key="n" class="w-[70px] h-[70px] bg-gray-200 shrink-0" />
        </div>
      </div>
      <div class="space-y-4 pt-2">
        <div class="h-7 bg-gray-200 w-3/4 rounded" />
        <div class="h-10 bg-gray-200 w-1/2 rounded" />
        <div class="h-20 bg-gray-200 rounded" />
        <div class="h-9 bg-gray-200 rounded" />
        <div class="h-9 bg-gray-200 rounded" />
        <div class="h-9 bg-gray-200 rounded" />
        <div class="h-12 bg-gray-200 rounded" />
      </div>
    </div>

    <!-- Product detail -->
    <div v-else-if="product" class="md:grid grid-cols-2 flex flex-col py-5 md:gap-8">
      <div>
        <div class="relative">
          <img
            v-if="selectedImage || product.images[0]?.image"
            :src="selectedImage || product.images[0]?.image"
            :alt="product.name"
            width="480"
            height="450"
            class="block object-contain w-full"
          />
          <div v-else class="bg-gray-100 flex items-center justify-center w-full" style="height:450px;">
            <img src="/assets/icons/image-placeholder.svg" class="w-20 h-20 text-gray-300" alt="" aria-hidden="true" />
          </div>

          <div class="absolute bottom-[50px] right-[50px] flex gap-2">
            <button
              v-if="imageIndex > 0"
              class="border border-gray-200 p-3 bg-black/60 hover:bg-black/80 transition-colors"
              @click="prevImage"
            >
              <img src="/assets/icons/arrow-left-white.svg" width="8" height="8" alt="" aria-hidden="true" />
            </button>
            <button
              v-if="imageIndex + 1 < (product.images?.length ?? 0)"
              class="border border-gray-200 p-3 bg-black/60 hover:bg-black/80 transition-colors"
              @click="nextImage"
            >
              <img src="/assets/icons/arrow-right-white.svg" width="8" height="8" alt="" aria-hidden="true" />
            </button>
          </div>
        </div>

        <div class="flex mt-2">
          <img
            v-for="(img, index) in product.images"
            :key="img.id"
            :src="img.image"
            :alt="img.alt_text"
            width="70"
            height="70"
            class="block cursor-pointer mr-3 transition-opacity object-cover"
            style="width:70px; height:70px;"
            :class="selectedImage === img.image ? 'opacity-100' : 'opacity-50 hover:opacity-75'"
            @click="selectImage(img.image, index)"
          />
        </div>
      </div>

      <!-- product info -->
      <div class="md:pt-0 pt-6">

        <p class="text-xl font-bold">{{ product.name }}</p>

        <div class="mt-2 flex items-center flex-wrap">
          <small class="font-bold text-[30px] mr-3 leading-none">€{{ product.price }}</small>
          <small v-if="product.original_price" class="text-[#EE503E] line-through text-[14px] mr-4">
            €{{ product.original_price }}
          </small>
          <div v-if="product.discount_percentage > 0"
               class="bg-[#23C353] text-white text-[12px] py-1 font-semibold px-3">
            Save {{ product.discount_percentage }}%
          </div>
          <button class="flex items-center ml-auto border-gray-300 text-gray-400 border px-3 py-2">
            <img src="/assets/icons/heart.svg" width="12" height="11" alt="" aria-hidden="true" />
            <span class="ml-2 text-[11px] hidden md:inline">Add to Favorites</span>
          </button>
        </div>

        <p class="text-[#111112] text-[12px] mt-6 leading-relaxed">
          {{ showFullDesc ? product.description : truncated }}
          <button
            v-if="product.description?.length > 200 && !showFullDesc"
            class="text-[12px] font-bold hover:underline ml-0.5"
            @click="showFullDesc = true"
          >Read More</button>
          <button
            v-if="showFullDesc"
            class="text-[12px] font-bold hover:underline ml-0.5"
            @click="showFullDesc = false"
          >Read Less</button>
        </p>

        <div class="flex items-center mt-10">
          <label class="w-[130px] shrink-0 text-xs font-bold">
            Size <span class="text-red-500">*</span>
          </label>
          <div class="flex items-center flex-1 gap-2">
            <div class="relative flex-1">
              <select v-model="form.size" class="w-full text-[12px] text-gray-400 border-gray-300 border p-2 outline-none appearance-none pr-8">
                <option value="" disabled>Select a shirt size</option>
                <option v-for="size in product.available_sizes" :key="size" :value="size">{{ size }}</option>
              </select>
              <div class="pointer-events-none absolute right-4 top-1/2 -translate-y-1/2">
                <img src="/assets/icons/chevron-down.svg" class="w-2 h-2" alt="" aria-hidden="true" />
              </div>
            </div>
            <button
              class="border-gray-300 text-[#111112] border px-3 bg-[#F5F5F6] text-[12px] font-semibold py-2 whitespace-nowrap"
              @click="showSizeChart = true"
            >
              <span class="hidden md:inline">View Size Chart</span>
              <span class="md:hidden">Size Chart</span>
            </button>
          </div>
        </div>

        <div v-if="product.allow_name_customization" class="flex items-center mt-6">
          <label class="w-[130px] shrink-0 text-xs font-bold">Name</label>
          <input
            v-model="form.custom_name"
            type="text"
            class="flex-1 text-gray-400 border-gray-300 border p-2 outline-none placeholder:text-[12px] text-[12px]"
            placeholder="What name would you want in the shirt?"
            maxlength="100"
          />
        </div>

        <div v-if="product.allow_number_customization" class="flex items-center mt-6">
          <label class="w-[130px] shrink-0 text-xs font-bold">Number on Shirt</label>
          <input
            v-model="form.custom_number"
            type="text"
            class="flex-1 text-gray-400 border-gray-300 border p-2 outline-none placeholder:text-[12px] text-[12px]"
            placeholder="Enter a number between 0 and 99"
          />
        </div>

        <div v-if="product.patches?.length > 0" class="flex items-center mt-6">
          <label class="w-[130px] shrink-0 text-xs font-bold">Patch</label>
          <div class="relative flex-1">
            <select v-model="form.patch_id" class="w-full text-[12px] text-gray-400 border-gray-300 border p-2 outline-none appearance-none pr-8">
              <option :value="null">Select a patch</option>
              <option v-for="patch in product.patches" :key="patch.id" :value="patch.id">
                {{ patch.name }}<template v-if="+patch.extra_price > 0"> (+€{{ patch.extra_price }})</template>
              </option>
            </select>
            <div class="pointer-events-none absolute right-4 top-1/2 -translate-y-1/2">
                <img src="/assets/icons/chevron-down.svg" class="w-2 h-2" alt="" aria-hidden="true" />
            </div>
          </div>
        </div>

        <div class="flex items-center mt-6">
          <label class="w-[130px] shrink-0 text-xs font-bold">Quantity</label>
          <input
            v-model="form.quantity"
            type="number"
            min="1"
            class="text-gray-400 border-gray-300 border text-[12px] p-2 outline-none"
            style="width: 70px;"
          />
        </div>

        <p v-if="formError" class="text-red-500 text-[12px] mt-3">{{ formError }}</p>
        <p v-if="addedSuccess" class="text-green-600 text-[12px] mt-3">✓ Added to cart successfully!</p>

        <div
          class="flex items-stretch mt-10 w-full cursor-pointer"
          :class="{ 'opacity-50 pointer-events-none': cartStore.loading }"
          @click="handleAddToCart"
        >
          <div class="bg-primary text-black text-[15px] flex-grow font-semibold pl-5 flex items-center py-3">
            {{ cartStore.loading ? 'Adding...' : 'Add to Cart' }}
          </div>
          <div class="bg-black px-4 flex items-center justify-center">
            <img src="/assets/icons/cart.svg" width="16" height="16" alt="" aria-hidden="true" />
          </div>
        </div>

      </div>
    </div>

    <!-- 404 -->
    <div v-else-if="!pending" class="text-center py-16">
      <p class="font-bold text-xl mb-4 uppercase">Product not found</p>
      <NuxtLink to="/products" class="inline-block bg-primary text-black font-bold uppercase px-6 py-3">
        Back to Products
      </NuxtLink>
    </div>

    <Transition name="fade">
      <div
        v-if="showSizeChart"
        class="fixed inset-0 bg-black/60 z-50 flex items-center justify-center p-4"
        @click.self="showSizeChart = false"
      >
        <div class="bg-white max-w-lg w-full p-6">
          <div class="flex justify-between items-center mb-4">
            <h3 class="font-bold uppercase text-base tracking-wide">{{ product?.size_chart?.name || 'Size Chart' }}</h3>
            <button class="p-1 hover:bg-gray-100 transition-colors" @click="showSizeChart = false">
              <img src="/assets/icons/close.svg" class="w-5 h-5" alt="Close" />
            </button>
          </div>
          <template v-if="product?.size_chart">
            <img :src="product.size_chart.image" :alt="product.size_chart.name" class="w-full" />
            <p v-if="product.size_chart.description" class="mt-3 text-sm text-gray-600">
              {{ product.size_chart.description }}
            </p>
          </template>
          <p v-else class="text-sm text-gray-400 text-center py-6">No size chart available for this product.</p>
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
  const d = product.value.description
  return d?.length > 200 ? d.slice(0, 200) + '...' : d
})

watch(product, (p) => {
  if (p?.images?.length) {
    const primary = p.images.find(img => img.is_primary)
    imageIndex.value = primary ? p.images.indexOf(primary) : 0
    selectedImage.value = p.images[imageIndex.value]?.image ?? null
  }
}, { immediate: true })

function selectImage(src: string, index: number) {
  selectedImage.value = src
  imageIndex.value = index
}
function prevImage() {
  if (!product.value?.images?.length || imageIndex.value === 0) return
  imageIndex.value--
  selectedImage.value = product.value.images[imageIndex.value]?.image ?? null
}
function nextImage() {
  if (!product.value?.images?.length) return
  if (imageIndex.value + 1 >= product.value.images.length) return
  imageIndex.value++
  selectedImage.value = product.value.images[imageIndex.value]?.image ?? null
}

async function handleAddToCart() {
  formError.value = ''
  addedSuccess.value = false
  if (!form.size) { formError.value = 'Please select a size.'; return }
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
.fade-enter-from, .fade-leave-to       { opacity: 0; }
</style>