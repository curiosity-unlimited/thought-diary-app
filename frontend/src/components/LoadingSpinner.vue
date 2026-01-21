<template>
  <div
    class="flex flex-col items-center justify-center"
    :class="containerClass"
    role="status"
    :aria-label="message || 'Loading'"
  >
    <!-- Spinner -->
    <svg
      :class="spinnerSizeClass"
      class="animate-spin text-indigo-600"
      xmlns="http://www.w3.org/2000/svg"
      fill="none"
      viewBox="0 0 24 24"
    >
      <circle
        class="opacity-25"
        cx="12"
        cy="12"
        r="10"
        stroke="currentColor"
        stroke-width="4"
      ></circle>
      <path
        class="opacity-75"
        fill="currentColor"
        d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
      ></path>
    </svg>

    <!-- Optional Message -->
    <p
      v-if="message"
      :class="messageSizeClass"
      class="text-gray-600 font-medium"
    >
      {{ message }}
    </p>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';

interface Props {
  size?: 'sm' | 'md' | 'lg';
  message?: string;
  centered?: boolean;
}

const props = withDefaults(defineProps<Props>(), {
  size: 'md',
  message: undefined,
  centered: true,
});

/**
 * Compute spinner size class based on prop
 */
const spinnerSizeClass = computed(() => {
  switch (props.size) {
    case 'sm':
      return 'h-6 w-6';
    case 'md':
      return 'h-10 w-10';
    case 'lg':
      return 'h-16 w-16';
    default:
      return 'h-10 w-10';
  }
});

/**
 * Compute message size class based on spinner size
 */
const messageSizeClass = computed(() => {
  switch (props.size) {
    case 'sm':
      return 'text-sm mt-2';
    case 'md':
      return 'text-base mt-3';
    case 'lg':
      return 'text-lg mt-4';
    default:
      return 'text-base mt-3';
  }
});

/**
 * Compute container class for centering
 */
const containerClass = computed(() => {
  return props.centered ? 'min-h-[200px] p-8' : 'p-4';
});
</script>
