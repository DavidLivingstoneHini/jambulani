<template>
  <div class="max-w-screen-xl mx-auto px-4 py-10">
    <nav class="text-sm font-body mb-6 text-gray-500">
      <NuxtLink to="/" class="hover:text-gray-900">Home</NuxtLink>
      <span class="mx-2">›</span>
      <span class="text-gray-900">My Account</span>
    </nav>

    <div class="grid grid-cols-1 md:grid-cols-4 gap-8">
      <!-- Sidebar nav -->
      <aside class="md:col-span-1">
        <div class="border border-gray-200 p-4">
          <div class="flex items-center gap-3 mb-5 pb-4 border-b border-gray-100">
            <div class="w-10 h-10 bg-primary flex items-center justify-center font-heading text-black text-lg">
              {{ authStore.user?.first_name?.[0]?.toUpperCase() || authStore.user?.email?.[0]?.toUpperCase() }}
            </div>
            <div class="min-w-0">
              <p class="font-display font-bold text-sm truncate">{{ authStore.user?.full_name || 'My Account' }}</p>
              <p class="text-gray-400 text-xs font-body truncate">{{ authStore.user?.email }}</p>
            </div>
          </div>
          <nav class="space-y-1">
            <button
              v-for="tab in tabs"
              :key="tab.key"
              class="w-full text-left px-3 py-2 text-sm font-body transition-colors duration-150"
              :class="activeTab === tab.key ? 'bg-primary font-semibold' : 'hover:bg-gray-50'"
              @click="activeTab = tab.key"
            >
              {{ tab.label }}
            </button>
            <button
              class="w-full text-left px-3 py-2 text-sm font-body text-red-500 hover:bg-red-50 transition-colors duration-150 mt-2 pt-3 border-t border-gray-100"
              @click="handleLogout"
            >
              Sign Out
            </button>
          </nav>
        </div>
      </aside>

      <!-- Main content -->
      <div class="md:col-span-3">
        <!-- Profile tab -->
        <div v-if="activeTab === 'profile'">
          <h2 class="font-display font-bold uppercase text-lg tracking-wider mb-6">Personal Information</h2>
          <form class="space-y-4 max-w-lg" @submit.prevent="handleUpdateProfile">
            <div v-if="profileSuccess" class="bg-green-50 border border-green-200 text-green-700 px-4 py-3 text-sm font-body">
              Profile updated successfully.
            </div>
            <div v-if="profileError" class="bg-red-50 border border-red-200 text-red-700 px-4 py-3 text-sm font-body">
              {{ profileError }}
            </div>

            <div class="grid grid-cols-2 gap-4">
              <div>
                <label class="font-display font-bold uppercase text-xs tracking-wide mb-1.5 block">First Name</label>
                <input v-model="profileForm.first_name" type="text" class="form-input" />
              </div>
              <div>
                <label class="font-display font-bold uppercase text-xs tracking-wide mb-1.5 block">Last Name</label>
                <input v-model="profileForm.last_name" type="text" class="form-input" />
              </div>
            </div>
            <div>
              <label class="font-display font-bold uppercase text-xs tracking-wide mb-1.5 block">Email</label>
              <input :value="authStore.user?.email" type="email" class="form-input bg-gray-50" disabled />
              <p class="text-xs text-gray-400 font-body mt-1">Email cannot be changed.</p>
            </div>
            <div>
              <label class="font-display font-bold uppercase text-xs tracking-wide mb-1.5 block">Phone</label>
              <input v-model="profileForm.phone" type="tel" class="form-input" placeholder="+34 000 000 000" />
            </div>

            <h3 class="font-display font-bold uppercase text-sm tracking-wider pt-2 border-t border-gray-100">Shipping Address</h3>
            <div>
              <label class="font-display font-bold uppercase text-xs tracking-wide mb-1.5 block">Address Line 1</label>
              <input v-model="profileForm.address_line1" type="text" class="form-input" />
            </div>
            <div>
              <label class="font-display font-bold uppercase text-xs tracking-wide mb-1.5 block">Address Line 2</label>
              <input v-model="profileForm.address_line2" type="text" class="form-input" />
            </div>
            <div class="grid grid-cols-2 gap-4">
              <div>
                <label class="font-display font-bold uppercase text-xs tracking-wide mb-1.5 block">City</label>
                <input v-model="profileForm.city" type="text" class="form-input" />
              </div>
              <div>
                <label class="font-display font-bold uppercase text-xs tracking-wide mb-1.5 block">Postal Code</label>
                <input v-model="profileForm.postal_code" type="text" class="form-input" />
              </div>
            </div>
            <div>
              <label class="font-display font-bold uppercase text-xs tracking-wide mb-1.5 block">Country</label>
              <input v-model="profileForm.country" type="text" class="form-input" />
            </div>

            <button type="submit" class="btn-primary px-8 py-3" :disabled="profileLoading">
              {{ profileLoading ? 'Saving...' : 'Save Changes' }}
            </button>
          </form>
        </div>

        <!-- Change password tab -->
        <div v-if="activeTab === 'password'">
          <h2 class="font-display font-bold uppercase text-lg tracking-wider mb-6">Change Password</h2>
          <form class="space-y-4 max-w-lg" @submit.prevent="handleChangePassword">
            <div v-if="pwSuccess" class="bg-green-50 border border-green-200 text-green-700 px-4 py-3 text-sm font-body">
              Password changed. You have been signed out.
            </div>
            <div v-if="pwError" class="bg-red-50 border border-red-200 text-red-700 px-4 py-3 text-sm font-body">
              {{ pwError }}
            </div>

            <div>
              <label class="font-display font-bold uppercase text-xs tracking-wide mb-1.5 block">Current Password</label>
              <input v-model="pwForm.current_password" type="password" autocomplete="current-password" class="form-input" :class="{ 'border-red-400': pwErrors.current_password }" />
              <p v-if="pwErrors.current_password" class="text-red-500 text-xs mt-1 font-body">{{ pwErrors.current_password }}</p>
            </div>
            <div>
              <label class="font-display font-bold uppercase text-xs tracking-wide mb-1.5 block">New Password</label>
              <input v-model="pwForm.new_password" type="password" autocomplete="new-password" class="form-input" :class="{ 'border-red-400': pwErrors.new_password }" />
              <p v-if="pwErrors.new_password" class="text-red-500 text-xs mt-1 font-body">{{ pwErrors.new_password }}</p>
            </div>
            <div>
              <label class="font-display font-bold uppercase text-xs tracking-wide mb-1.5 block">Confirm New Password</label>
              <input v-model="pwForm.new_password_confirm" type="password" autocomplete="new-password" class="form-input" :class="{ 'border-red-400': pwErrors.new_password_confirm }" />
              <p v-if="pwErrors.new_password_confirm" class="text-red-500 text-xs mt-1 font-body">{{ pwErrors.new_password_confirm }}</p>
            </div>

            <button type="submit" class="btn-primary px-8 py-3" :disabled="pwLoading">
              {{ pwLoading ? 'Updating...' : 'Update Password' }}
            </button>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
definePageMeta({ middleware: 'auth' })

const authStore = useAuthStore()
const router = useRouter()

const tabs = [
  { key: 'profile', label: 'Personal Information' },
  { key: 'password', label: 'Change Password' },
]
const activeTab = ref('profile')

// ── Profile form ──────────────────────────────────────────────────
const profileForm = reactive({
  first_name: authStore.user?.first_name || '',
  last_name: authStore.user?.last_name || '',
  phone: authStore.user?.phone || '',
  address_line1: authStore.user?.address_line1 || '',
  address_line2: authStore.user?.address_line2 || '',
  city: authStore.user?.city || '',
  postal_code: authStore.user?.postal_code || '',
  country: authStore.user?.country || '',
})
const profileLoading = ref(false)
const profileSuccess = ref(false)
const profileError = ref('')

async function handleUpdateProfile() {
  profileLoading.value = true
  profileSuccess.value = false
  profileError.value = ''
  try {
    await authStore.updateProfile({ ...profileForm })
    profileSuccess.value = true
    setTimeout(() => (profileSuccess.value = false), 4000)
  } catch (e: unknown) {
    profileError.value = ((e as Record<string, Record<string, string>>)?.data?.detail) ?? 'Failed to update profile.'
  } finally {
    profileLoading.value = false
  }
}

// ── Password form ─────────────────────────────────────────────────
const pwForm = reactive({ current_password: '', new_password: '', new_password_confirm: '' })
const pwErrors = reactive<Record<string, string>>({})
const pwLoading = ref(false)
const pwSuccess = ref(false)
const pwError = ref('')

async function handleChangePassword() {
  Object.keys(pwErrors).forEach(k => delete ( pwErrors as Record<string, string>)[k])
  pwError.value = ''
  pwLoading.value = true
  try {
    await authStore.changePassword({ ...pwForm })
    pwSuccess.value = true
    setTimeout(() => router.push('/login'), 2000)
  } catch (e: unknown) {
    const data = (e as Record<string, unknown>)?.data as Record<string, unknown> | undefined
    if (data) {
      Object.entries(data).forEach(([k, v]) => {
        ( pwErrors as Record<string, string>)[k] = Array.isArray(v) ? (v as string[])[0] : String(v)
      })
    }
    if (Object.keys(pwErrors).length === 0) pwError.value = 'Failed to change password.'
  } finally {
    pwLoading.value = false
  }
}

// ── Logout ────────────────────────────────────────────────────────
async function handleLogout() {
  await authStore.logout()
  router.push('/')
}

useHead({ title: 'My Account — Jambulani' })
</script>
