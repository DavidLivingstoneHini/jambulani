<template>
  <div class="min-h-[70vh] flex items-center justify-center px-4 py-16">
    <div class="w-full max-w-lg">
      <div class="text-center mb-8">
        <NuxtLink to="/" class="inline-block mb-6">
          <div class="bg-primary px-4 py-2 inline-block">
            <span class="font-heading text-black text-2xl">JAMBULANI</span>
          </div>
        </NuxtLink>
        <h1 class="font-display font-bold uppercase text-2xl tracking-wider">Create Account</h1>
        <p class="text-gray-500 text-sm font-body mt-1">
          Already have an account?
          <NuxtLink to="/login" class="text-gray-900 font-semibold underline">Sign in</NuxtLink>
        </p>
      </div>

      <form class="space-y-4" @submit.prevent="handleRegister">
        <div v-if="serverError" class="bg-red-50 border border-red-200 text-red-700 px-4 py-3 text-sm font-body">
          {{ serverError }}
        </div>

        <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <div>
            <label class="font-display font-bold uppercase text-xs tracking-wide mb-1.5 block">First Name</label>
            <input v-model="form.first_name" type="text" autocomplete="given-name" class="form-input" placeholder="John" :class="{ 'border-red-400': errors.first_name }" />
            <p v-if="errors.first_name" class="text-red-500 text-xs mt-1 font-body">{{ errors.first_name }}</p>
          </div>
          <div>
            <label class="font-display font-bold uppercase text-xs tracking-wide mb-1.5 block">Last Name</label>
            <input v-model="form.last_name" type="text" autocomplete="family-name" class="form-input" placeholder="Doe" :class="{ 'border-red-400': errors.last_name }" />
            <p v-if="errors.last_name" class="text-red-500 text-xs mt-1 font-body">{{ errors.last_name }}</p>
          </div>
        </div>

        <div>
          <label class="font-display font-bold uppercase text-xs tracking-wide mb-1.5 block">Email Address</label>
          <input v-model="form.email" type="email" autocomplete="email" required class="form-input" placeholder="you@example.com" :class="{ 'border-red-400': errors.email }" />
          <p v-if="errors.email" class="text-red-500 text-xs mt-1 font-body">{{ errors.email }}</p>
        </div>

        <div>
          <label class="font-display font-bold uppercase text-xs tracking-wide mb-1.5 block">Password</label>
          <div class="relative">
            <input v-model="form.password" :type="showPassword ? 'text' : 'password'" autocomplete="new-password" required class="form-input pr-10" placeholder="Min. 8 characters" :class="{ 'border-red-400': errors.password }" />
            <button type="button" class="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600" tabindex="-1" @click="showPassword = !showPassword">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0zM2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
              </svg>
            </button>
          </div>
          <!-- Password strength indicator -->
          <div class="flex gap-1 mt-2">
            <div v-for="i in 4" :key="i" class="h-1 flex-1 rounded transition-colors duration-300" :class="passwordStrengthColor(i)" />
          </div>
          <p v-if="errors.password" class="text-red-500 text-xs mt-1 font-body">{{ errors.password }}</p>
        </div>

        <div>
          <label class="font-display font-bold uppercase text-xs tracking-wide mb-1.5 block">Confirm Password</label>
          <input v-model="form.password_confirm" :type="showPassword ? 'text' : 'password'" autocomplete="new-password" required class="form-input" placeholder="Repeat password" :class="{ 'border-red-400': errors.password_confirm }" />
          <p v-if="errors.password_confirm" class="text-red-500 text-xs mt-1 font-body">{{ errors.password_confirm }}</p>
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
          {{ authStore.loading ? 'Creating account...' : 'Create Account' }}
        </button>
      </form>

      <p class="text-center text-xs text-gray-400 font-body mt-6">
        By creating an account, you agree to our
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

const form = reactive({
  email: '',
  first_name: '',
  last_name: '',
  password: '',
  password_confirm: '',
})
const errors = reactive<Record<string, string>>({})
const serverError = ref('')
const showPassword = ref(false)

// Simple password strength: 1=weak, 4=strong
const passwordStrength = computed(() => {
  const p = form.password
  if (!p) return 0
  let score = 0
  if (p.length >= 8) score++
  if (p.length >= 12) score++
  if (/[A-Z]/.test(p) && /[0-9]/.test(p)) score++
  if (/[^A-Za-z0-9]/.test(p)) score++
  return score
})

function passwordStrengthColor(bar: number) {
  if (bar > passwordStrength.value) return 'bg-gray-200'
  const colors = ['bg-red-400', 'bg-orange-400', 'bg-yellow-400', 'bg-green-500']
  return colors[passwordStrength.value - 1] || 'bg-gray-200'
}

async function handleRegister() {
  Object.keys(errors).forEach(k => delete (errors as any)[k])
  serverError.value = ''

  if (form.password !== form.password_confirm) {
    errors.password_confirm = 'Passwords do not match.'
    return
  }

  try {
    await authStore.register({ ...form })
    router.push('/')
  } catch (e: any) {
    const data = e?.data
    if (data && typeof data === 'object') {
      Object.entries(data).forEach(([key, val]) => {
        if (key in form || key === 'password_confirm') {
          (errors as any)[key] = Array.isArray(val) ? (val as string[])[0] : String(val)
        } else if (key === 'detail' || key === 'non_field_errors') {
          serverError.value = Array.isArray(val) ? (val as string[])[0] : String(val)
        }
      })
    }
    if (!serverError.value && Object.keys(errors).length === 0) {
      serverError.value = 'Registration failed. Please try again.'
    }
  }
}

useHead({ title: 'Create Account — Jambulani' })
</script>
