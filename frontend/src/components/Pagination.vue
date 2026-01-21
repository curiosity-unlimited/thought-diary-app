<template>
  <nav
    class="flex items-center justify-center gap-2 mt-8"
    role="navigation"
    aria-label="Pagination"
  >
    <!-- Previous Button -->
    <button
      :disabled="pagination.page === 1"
      class="px-3 py-2 rounded-md text-sm font-medium transition-colors disabled:opacity-50 disabled:cursor-not-allowed bg-white border border-gray-300 text-gray-700 hover:bg-gray-50 disabled:hover:bg-white"
      aria-label="Previous page"
      @click="changePage(pagination.page - 1)"
    >
      <svg
        xmlns="http://www.w3.org/2000/svg"
        class="h-5 w-5"
        viewBox="0 0 20 20"
        fill="currentColor"
      >
        <path
          fill-rule="evenodd"
          d="M12.707 5.293a1 1 0 010 1.414L9.414 10l3.293 3.293a1 1 0 01-1.414 1.414l-4-4a1 1 0 010-1.414l4-4a1 1 0 011.414 0z"
          clip-rule="evenodd"
        />
      </svg>
    </button>

    <!-- Page Numbers -->
    <div class="hidden sm:flex gap-2">
      <button
        v-for="page in visiblePages"
        :key="page"
        :disabled="typeof page !== 'number'"
        :class="[
          'px-4 py-2 rounded-md text-sm font-medium transition-colors',
          page === pagination.page
            ? 'bg-indigo-600 text-white'
            : typeof page === 'number'
              ? 'bg-white border border-gray-300 text-gray-700 hover:bg-gray-50'
              : 'bg-white text-gray-400 cursor-default',
        ]"
        :aria-label="typeof page === 'number' ? `Page ${page}` : 'More pages'"
        :aria-current="page === pagination.page ? 'page' : undefined"
        @click="typeof page === 'number' ? changePage(page) : null"
      >
        {{ page }}
      </button>
    </div>

    <!-- Mobile: Current Page Indicator -->
    <div class="sm:hidden px-4 py-2 text-sm font-medium text-gray-700">
      {{ pagination.page }} / {{ pagination.pages }}
    </div>

    <!-- Next Button -->
    <button
      :disabled="pagination.page === pagination.pages"
      class="px-3 py-2 rounded-md text-sm font-medium transition-colors disabled:opacity-50 disabled:cursor-not-allowed bg-white border border-gray-300 text-gray-700 hover:bg-gray-50 disabled:hover:bg-white"
      aria-label="Next page"
      @click="changePage(pagination.page + 1)"
    >
      <svg
        xmlns="http://www.w3.org/2000/svg"
        class="h-5 w-5"
        viewBox="0 0 20 20"
        fill="currentColor"
      >
        <path
          fill-rule="evenodd"
          d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z"
          clip-rule="evenodd"
        />
      </svg>
    </button>
  </nav>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import type { PaginationInfo } from '@/types';

interface Props {
  pagination: PaginationInfo;
}

const props = defineProps<Props>();

const emit = defineEmits<{
  pageChange: [page: number];
}>();

/**
 * Calculate visible page numbers with ellipsis
 */
const visiblePages = computed(() => {
  const { page, pages } = props.pagination;
  const delta = 2; // Number of pages to show on each side of current page
  const pages_array: (number | string)[] = [];

  // Always show first page
  if (pages >= 1) {
    pages_array.push(1);
  }

  // Add ellipsis after first page if needed
  if (page > delta + 2) {
    pages_array.push('...');
  }

  // Add pages around current page
  const start = Math.max(2, page - delta);
  const end = Math.min(pages - 1, page + delta);

  for (let i = start; i <= end; i++) {
    pages_array.push(i);
  }

  // Add ellipsis before last page if needed
  if (page < pages - delta - 1) {
    pages_array.push('...');
  }

  // Always show last page
  if (pages > 1) {
    pages_array.push(pages);
  }

  return pages_array;
});

/**
 * Change page and emit event
 */
const changePage = (page: number) => {
  if (page >= 1 && page <= props.pagination.pages) {
    emit('pageChange', page);
  }
};
</script>
