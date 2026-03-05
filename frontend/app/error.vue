<template>
  <div class="min-h-screen flex items-center justify-center px-4">
    <div class="text-center">
      <p class="font-heading text-8xl text-primary mb-4">{{ error?.statusCode }}</p>
      <h1 class="font-body font-bold uppercase text-2xl mb-4">
        {{ error?.statusCode === 404 ? "Page Not Found" : "Something went wrong" }}
      </h1>
      <p class="font-body text-gray-500 mb-8 max-w-md mx-auto">
        {{ error?.message || "An unexpected error occurred." }}
      </p>
      <NuxtLink to="/" class="btn-primary inline-block">Go Home</NuxtLink>
    </div>
  </div>
</template>

<script setup lang="ts">
defineProps<{ error: { statusCode?: number; message?: string } | null }>();
</script>
