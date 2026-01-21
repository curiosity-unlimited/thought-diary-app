<template>
  <div
    class="flex flex-col items-center justify-center min-h-[400px] p-8 text-center"
  >
    <!-- Icon -->
    <div class="mb-6">
      <svg
        xmlns="http://www.w3.org/2000/svg"
        class="h-24 w-24 text-gray-400"
        fill="none"
        viewBox="0 0 24 24"
        stroke="currentColor"
      >
        <path
          stroke-linecap="round"
          stroke-linejoin="round"
          stroke-width="2"
          d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
        />
      </svg>
    </div>

    <!-- Title -->
    <h3 class="text-2xl font-semibold text-gray-900 mb-2">
      {{ title }}
    </h3>

    <!-- Message -->
    <p class="text-gray-600 mb-6 max-w-md">
      {{ message }}
    </p>

    <!-- Optional Action Button -->
    <RouterLink
      v-if="actionText && actionTo"
      :to="actionTo"
      class="px-6 py-3 bg-indigo-600 text-white rounded-lg font-medium hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 transition-colors"
    >
      {{ actionText }}
    </RouterLink>
  </div>
</template>

<script setup lang="ts">
import { RouterLink } from 'vue-router';

interface Props {
  title: string;
  message: string;
  actionText?: string;
  actionTo?: string;
}

defineProps<Props>();
</script>
