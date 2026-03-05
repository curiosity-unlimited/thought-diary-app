<script setup lang="ts">
// 404 Not Found page
</script>

<template>
  <div class="min-h-screen bg-gray-50 dark:bg-gray-900 flex items-center justify-center">
    <div class="max-w-md w-full text-center">
      <div class="text-9xl font-bold text-gray-300 dark:text-gray-700 mb-4">404</div>
      <h1 class="text-3xl font-bold text-gray-900 dark:text-gray-100 mb-4">Page Not Found</h1>
      <p class="text-gray-600 dark:text-gray-400 mb-8">
        The page you're looking for doesn't exist or has been moved.
      </p>
      <router-link
        to="/"
        class="inline-block bg-blue-600 text-white px-6 py-3 rounded-lg font-semibold hover:bg-blue-700 transition"
      >
        Go to Home
      </router-link>
    </div>
  </div>
</template>
