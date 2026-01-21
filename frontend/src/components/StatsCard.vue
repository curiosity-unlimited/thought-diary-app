<template>
  <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
    <!-- Total Entries -->
    <div
      class="bg-gradient-to-br from-blue-500 to-blue-600 rounded-lg p-6 text-white shadow-md hover:shadow-lg transition-shadow"
    >
      <div class="flex items-center justify-between mb-2">
        <svg
          xmlns="http://www.w3.org/2000/svg"
          class="h-8 w-8 opacity-80"
          viewBox="0 0 20 20"
          fill="currentColor"
        >
          <path d="M9 2a1 1 0 000 2h2a1 1 0 100-2H9z" />
          <path
            fill-rule="evenodd"
            d="M4 5a2 2 0 012-2 3 3 0 003 3h2a3 3 0 003-3 2 2 0 012 2v11a2 2 0 01-2 2H6a2 2 0 01-2-2V5zm3 4a1 1 0 000 2h.01a1 1 0 100-2H7zm3 0a1 1 0 000 2h3a1 1 0 100-2h-3zm-3 4a1 1 0 100 2h.01a1 1 0 100-2H7zm3 0a1 1 0 100 2h3a1 1 0 100-2h-3z"
            clip-rule="evenodd"
          />
        </svg>
      </div>
      <div class="text-3xl font-bold mb-1">{{ stats.total }}</div>
      <div class="text-sm font-medium opacity-90">Total Entries</div>
    </div>

    <!-- Positive Entries -->
    <div
      class="bg-gradient-to-br from-green-500 to-green-600 rounded-lg p-6 text-white shadow-md hover:shadow-lg transition-shadow"
    >
      <div class="flex items-center justify-between mb-2">
        <svg
          xmlns="http://www.w3.org/2000/svg"
          class="h-8 w-8 opacity-80"
          viewBox="0 0 20 20"
          fill="currentColor"
        >
          <path
            fill-rule="evenodd"
            d="M10 18a8 8 0 100-16 8 8 0 000 16zM7 9a1 1 0 100-2 1 1 0 000 2zm7-1a1 1 0 11-2 0 1 1 0 012 0zm-.464 5.535a1 1 0 10-1.415-1.414 3 3 0 01-4.242 0 1 1 0 00-1.415 1.414 5 5 0 007.072 0z"
            clip-rule="evenodd"
          />
        </svg>
      </div>
      <div class="text-3xl font-bold mb-1">{{ stats.positive }}</div>
      <div class="text-sm font-medium opacity-90">Positive Entries</div>
    </div>

    <!-- Negative Entries -->
    <div
      class="bg-gradient-to-br from-red-500 to-red-600 rounded-lg p-6 text-white shadow-md hover:shadow-lg transition-shadow"
    >
      <div class="flex items-center justify-between mb-2">
        <svg
          xmlns="http://www.w3.org/2000/svg"
          class="h-8 w-8 opacity-80"
          viewBox="0 0 20 20"
          fill="currentColor"
        >
          <path
            fill-rule="evenodd"
            d="M10 18a8 8 0 100-16 8 8 0 000 16zM7 9a1 1 0 100-2 1 1 0 000 2zm7-1a1 1 0 11-2 0 1 1 0 012 0zm-7.536 5.879a1 1 0 001.415 0 3 3 0 014.242 0 1 1 0 001.415-1.415 5 5 0 00-7.072 0 1 1 0 000 1.415z"
            clip-rule="evenodd"
          />
        </svg>
      </div>
      <div class="text-3xl font-bold mb-1">{{ stats.negative }}</div>
      <div class="text-sm font-medium opacity-90">Negative Entries</div>
    </div>

    <!-- Neutral Entries -->
    <div
      class="bg-gradient-to-br from-gray-500 to-gray-600 rounded-lg p-6 text-white shadow-md hover:shadow-lg transition-shadow"
    >
      <div class="flex items-center justify-between mb-2">
        <svg
          xmlns="http://www.w3.org/2000/svg"
          class="h-8 w-8 opacity-80"
          viewBox="0 0 20 20"
          fill="currentColor"
        >
          <path
            fill-rule="evenodd"
            d="M10 18a8 8 0 100-16 8 8 0 000 16zM7 9a1 1 0 100-2 1 1 0 000 2zm7-1a1 1 0 11-2 0 1 1 0 012 0zm-3 6a1 1 0 011-1h.01a1 1 0 110 2H11a1 1 0 01-1-1z"
            clip-rule="evenodd"
          />
        </svg>
      </div>
      <div class="text-3xl font-bold mb-1">{{ stats.neutral }}</div>
      <div class="text-sm font-medium opacity-90">Neutral Entries</div>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { DiaryStats } from '@/types';

interface Props {
  stats: DiaryStats;
}

defineProps<Props>();
</script>
