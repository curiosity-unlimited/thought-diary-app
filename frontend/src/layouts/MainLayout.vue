<script setup lang="ts">
/**
 * MainLayout Component
 * Primary layout for authenticated pages with navbar and content area
 */
import Navbar from '@/components/Navbar.vue';
</script>

<template>
  <div class="min-h-screen flex flex-col bg-gray-50 dark:bg-gray-900">
    <!-- Navigation Bar -->
    <Navbar />

    <!-- Main Content Area -->
    <main class="flex-1">
      <slot />
    </main>

    <!-- Optional Footer -->
    <footer class="bg-white dark:bg-gray-800 border-t border-gray-200 dark:border-gray-700">
      <div class="mx-auto max-w-7xl px-4 py-4 sm:px-6 lg:px-8">
        <p class="text-center text-sm text-gray-500 dark:text-gray-400">
          {{ $t('common.copyright', { year: new Date().getFullYear() }) }}
        </p>
      </div>
    </footer>
  </div>
</template>

<style scoped>
/* Additional layout styles if needed */
</style>
