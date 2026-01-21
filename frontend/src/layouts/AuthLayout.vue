<script setup lang="ts">
/**
 * AuthLayout Component
 * Layout for authentication pages (login, register) with centered card design
 */
</script>

<template>
  <div
    class="min-h-screen flex items-center justify-center bg-gradient-to-br from-indigo-500 via-purple-500 to-pink-500 px-4 sm:px-6 lg:px-8"
  >
    <div class="w-full max-w-md">
      <!-- Logo and App Name -->
      <div class="text-center mb-8">
        <router-link
          to="/"
          class="inline-flex items-center justify-center text-white hover:text-gray-100 transition-colors"
        >
          <svg
            class="h-12 w-12 mb-2"
            fill="currentColor"
            viewBox="0 0 24 24"
            xmlns="http://www.w3.org/2000/svg"
            aria-hidden="true"
          >
            <path
              d="M11.25 4.533A9.707 9.707 0 006 3a9.735 9.735 0 00-3.25.555.75.75 0 00-.5.707v14.25a.75.75 0 001 .707A8.237 8.237 0 016 18.75c1.995 0 3.823.707 5.25 1.886V4.533zM12.75 20.636A8.214 8.214 0 0118 18.75c.966 0 1.89.166 2.75.47a.75.75 0 001-.708V4.262a.75.75 0 00-.5-.707A9.735 9.735 0 0018 3a9.707 9.707 0 00-5.25 1.533v16.103z"
            />
          </svg>
        </router-link>
        <h1 class="text-3xl font-bold text-white">Thought Diary</h1>
        <p class="mt-2 text-indigo-100">Track and analyze your thoughts</p>
      </div>

      <!-- Card Container -->
      <div class="bg-white rounded-lg shadow-2xl overflow-hidden">
        <div class="px-6 py-8 sm:px-10">
          <!-- Content Slot -->
          <slot />
        </div>
      </div>

      <!-- Additional Info -->
      <div class="mt-6 text-center">
        <p class="text-sm text-white">
          <router-link
            to="/about"
            class="font-medium hover:text-gray-100 underline"
          >
            Learn more about Thought Diary
          </router-link>
        </p>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* Custom styles for authentication layout */
</style>
