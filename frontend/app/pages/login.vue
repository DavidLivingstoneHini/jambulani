<template>
  <div class="min-h-[70vh] flex items-center justify-center px-4 py-16">
    <div class="w-full max-w-md">
      <!-- Header -->
      <div class="text-center mb-8">
        <NuxtLink to="/" class="inline-block mb-6">
          <div class="bg-primary px-4 py-2 inline-block">
            <span class="font-heading text-black text-2xl">JAMBULANI</span>
          </div>
        </NuxtLink>
        <h1 class="font-display font-bold uppercase text-2xl tracking-wider">Sign In</h1>
        <p class="text-gray-500 text-sm font-body mt-1">
          New here?
          <NuxtLink to="/register" class="text-gray-900 font-semibold underline">Create an account</NuxtLink>
        </p>
      </div>

      <!-- Form -->
      <form class="space-y-4" @submit.prevent="handleLogin">
        <!-- Global error -->
        <div v-if="serverError" class="bg-red-50 border border-red-200 text-red-700 px-4 py-3 text-sm font-body">
          {{ serverError }}
        </div>

        <div>
          <label class="font-display font-bold uppercase text-xs tracking-wide mb-1.5 block">
            Email Address
          </label>
          <input
            v-model="form.email"
            type="email"
            autocomplete="email"
            required
            class="form-input"
            :class="{ 'border-red-400': errors.email }"
            placeholder="you@example.com"
          />
          <p v-if="errors.email" class="text-red-500 text-xs mt-1 font-body">{{ errors.email }}</p>
        </div>

        <div>
          <label class="font-display font-bold uppercase text-xs tracking-wide mb-1.5 block">
            Password
          </label>
          <div class="relative">
            <input
              v-model="form.password"
              :type="showPassword ? 'text' : 'password'"
              autocomplete="current-password"
              required
              class="form-input pr-10"
              :class="{ 'border-red-400': errors.password }"
              placeholder="••••••••"
            />
            <button
              type="button"
              class="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600"
              tabindex="-1"
              @click="showPassword = !showPassword"
            >
              <svg v-if="!showPassword" class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
              </svg>
              <svg v-else class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88l-3.29-3.29m7.532 7.532l3.29 3.29M3 3l3.59 3.59m0 0A9.953 9.953 0 0112 5c4.478 0 8.268 2.943 9.543 7a10.025 10.025 0 01-4.132 5.411m0 0L21 21" />
              </svg>
            </button>
          </div>
          <p v-if="errors.password" class="text-red-500 text-xs mt-1 font-body">{{ errors.password }}</p>
        </div>

        <button
          type="submit"
          class="btn-primary w-full py-3.5 text-base flex items-center justify-center gap-2"
          :disabled="authStore.loading"
        >
          <svg v-if="authStore.loading" class="animate-spin w-4 h-4" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" />
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
          </svg>
          {{ authStore.loading ? 'Signing in...' : 'Sign In' }}
        </button>
      </form>

      <p class="text-center text-xs text-gray-400 font-body mt-6">
        By signing in, you agree to our
        <NuxtLink to="/" class="underline">Terms of Service</NuxtLink> and
        <NuxtLink to="/" class="underline">Privacy Policy</NuxtLink>.
      </p>
    </div>
  </div>
</template>

<script setup lang="ts">
definePageMeta({ middleware: 'auth' })

const authStore = useAuthStore()
const router = useRouter()
const route = useRoute()

const form = reactive({ email: '', password: '' })
const errors = reactive<Record<string, string>>({})
const serverError = ref('')
const showPassword = ref(false)

async function handleLogin() {
  Object.keys(errors).forEach(k => delete (errors as any)[k])
  serverError.value = ''

  // Basic client-side validation
  if (!form.email) { errors.email = 'Email is required.'; return }
  if (!form.password) { errors.password = 'Password is required.'; return }

  try {
    await authStore.login({ email: form.email, password: form.password })
    const redirect = route.query.redirect as string
    router.push(redirect && redirect.startsWith('/') ? redirect : '/')
  } catch (e: any) {
    const data = e?.data
    if (data?.email) { errors.email = Array.isArray(data.email) ? data.email[0] : data.email }
    else if (data?.detail) { serverError.value = data.detail }
    else if (data?.non_field_errors) { serverError.value = data.non_field_errors[0] }
    else { serverError.value = 'Login failed. Please try again.' }
  }
}

useHead({ title: 'Sign In — Jambulani' })
</script>
