<template>
  <div
    class="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow duration-200"
  >
    <!-- Date and Actions Header -->
    <div class="flex justify-between items-start mb-4">
      <time
        :datetime="diary.created_at"
        class="text-sm text-gray-500 font-medium"
      >
        {{ formatDate(diary.created_at) }}
      </time>
      <div class="flex gap-2">
        <button
          class="p-2 text-indigo-600 hover:bg-indigo-50 rounded-md transition-colors"
          aria-label="Edit diary entry"
          @click="$emit('edit', diary.id)"
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            class="h-5 w-5"
            viewBox="0 0 20 20"
            fill="currentColor"
          >
            <path
              d="M13.586 3.586a2 2 0 112.828 2.828l-.793.793-2.828-2.828.793-.793zM11.379 5.793L3 14.172V17h2.828l8.38-8.379-2.83-2.828z"
            />
          </svg>
        </button>
        <button
          class="p-2 text-red-600 hover:bg-red-50 rounded-md transition-colors"
          aria-label="Delete diary entry"
          @click="$emit('delete', diary.id)"
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            class="h-5 w-5"
            viewBox="0 0 20 20"
            fill="currentColor"
          >
            <path
              fill-rule="evenodd"
              d="M9 2a1 1 0 00-.894.553L7.382 4H4a1 1 0 000 2v10a2 2 0 002 2h8a2 2 0 002-2V6a1 1 0 100-2h-3.382l-.724-1.447A1 1 0 0011 2H9zM7 8a1 1 0 012 0v6a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v6a1 1 0 102 0V8a1 1 0 00-1-1z"
              clip-rule="evenodd"
            />
          </svg>
        </button>
      </div>
    </div>

    <!-- Content with Sentiment Highlighting -->
    <!-- Note: v-html is safe here as the backend sanitizes and analyzes the content -->
    <!-- eslint-disable vue/no-v-html -->
    <div
      v-if="!isExpanded && isLongContent"
      class="prose prose-sm max-w-none mb-4"
    >
      <div
        class="diary-content text-gray-700 leading-relaxed"
        v-html="truncatedContent"
      ></div>
      <button
        class="text-indigo-600 hover:text-indigo-800 font-medium text-sm mt-2"
        @click="isExpanded = true"
      >
        Read more
      </button>
    </div>
    <div
      v-else
      class="diary-content prose prose-sm max-w-none text-gray-700 leading-relaxed mb-4"
      v-html="diary.analyzed_content || diary.content"
    ></div>
    <!-- eslint-enable vue/no-v-html -->

    <!-- Sentiment Counts -->
    <div class="flex gap-4 pt-4 border-t border-gray-200">
      <div class="flex items-center gap-2">
        <svg
          xmlns="http://www.w3.org/2000/svg"
          class="h-5 w-5 text-green-600"
          viewBox="0 0 20 20"
          fill="currentColor"
        >
          <path
            fill-rule="evenodd"
            d="M10 18a8 8 0 100-16 8 8 0 000 16zM7 9a1 1 0 100-2 1 1 0 000 2zm7-1a1 1 0 11-2 0 1 1 0 012 0zm-3.5 4a.5.5 0 01.5-.5h.01a.5.5 0 01.5.5v.01a.5.5 0 01-.5.5H11a.5.5 0 01-.5-.5V12zm-2.5.5a.5.5 0 00-.5-.5h-.01a.5.5 0 00-.5.5v.01c0 .276.224.5.5.5H8.5a.5.5 0 00.5-.5V12z"
            clip-rule="evenodd"
          />
        </svg>
        <span class="text-sm font-medium text-gray-700">
          {{ diary.positive_count }} positive
        </span>
      </div>
      <div class="flex items-center gap-2">
        <svg
          xmlns="http://www.w3.org/2000/svg"
          class="h-5 w-5 text-red-600"
          viewBox="0 0 20 20"
          fill="currentColor"
        >
          <path
            fill-rule="evenodd"
            d="M10 18a8 8 0 100-16 8 8 0 000 16zM7 9a1 1 0 100-2 1 1 0 000 2zm7-1a1 1 0 11-2 0 1 1 0 012 0zm-3.5 5.5a.5.5 0 01-.5.5h-.01a.5.5 0 01-.5-.5v-.01a.5.5 0 01.5-.5H10a.5.5 0 01.5.5v.01zm2.5-.5a.5.5 0 00.5.5h.01a.5.5 0 00.5-.5v-.01a.5.5 0 00-.5-.5H13a.5.5 0 00-.5.5v.01z"
            clip-rule="evenodd"
          />
        </svg>
        <span class="text-sm font-medium text-gray-700">
          {{ diary.negative_count }} negative
        </span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';
import type { DiaryEntry } from '@/types';

interface Props {
  diary: DiaryEntry;
}

const props = defineProps<Props>();

defineEmits<{
  edit: [id: number];
  delete: [id: number];
}>();

const isExpanded = ref(false);
const MAX_LENGTH = 300;

const isLongContent = computed(() => {
  const content = props.diary.analyzed_content || props.diary.content;
  return content.length > MAX_LENGTH;
});

const truncatedContent = computed(() => {
  const content = props.diary.analyzed_content || props.diary.content;
  if (content.length <= MAX_LENGTH) {
    return content;
  }
  return content.substring(0, MAX_LENGTH) + '...';
});

/**
 * Format date to readable format
 * @param dateString - ISO date string
 * @returns Formatted date string
 */
const formatDate = (dateString: string): string => {
  const date = new Date(dateString);
  return date.toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  });
};
</script>

<style scoped>
:deep(.diary-content .positive) {
  background-color: #10b981;
  color: white;
  padding: 2px 4px;
  border-radius: 3px;
}

:deep(.diary-content .negative) {
  background-color: #ef4444;
  color: white;
  padding: 2px 4px;
  border-radius: 3px;
}
</style>
