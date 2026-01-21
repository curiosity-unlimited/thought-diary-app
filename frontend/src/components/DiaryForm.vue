<template>
  <form class="space-y-4" @submit.prevent="handleSubmit">
    <!-- Textarea for Content -->
    <div>
      <label for="content" class="block text-sm font-medium text-gray-700 mb-2">
        What's on your mind?
      </label>
      <textarea
        id="content"
        v-model="contentValue"
        :class="[
          'w-full px-4 py-3 rounded-lg border focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-colors resize-none',
          errorMessage
            ? 'border-red-500 focus:ring-red-500'
            : 'border-gray-300',
        ]"
        :rows="rows"
        placeholder="Share your thoughts here..."
        :disabled="isSubmitting"
        @input="handleInput"
      ></textarea>

      <!-- Character Counter -->
      <div class="flex justify-between items-center mt-2">
        <p v-if="errorMessage" class="text-sm text-red-600" role="alert">
          {{ errorMessage }}
        </p>
        <span v-else class="text-sm text-gray-500"></span>
        <span
          :class="[
            'text-sm font-medium',
            contentValue.length > MAX_LENGTH
              ? 'text-red-600'
              : contentValue.length > MAX_LENGTH * 0.9
                ? 'text-yellow-600'
                : 'text-gray-500',
          ]"
        >
          {{ contentValue.length }} / {{ MAX_LENGTH }}
        </span>
      </div>
    </div>

    <!-- Action Buttons -->
    <div class="flex gap-3 justify-end">
      <button
        type="button"
        class="px-4 py-2 text-gray-700 bg-gray-100 hover:bg-gray-200 rounded-lg font-medium transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
        :disabled="isSubmitting"
        @click="$emit('cancel')"
      >
        Cancel
      </button>
      <button
        type="submit"
        :disabled="!isValid || isSubmitting"
        class="px-6 py-2 bg-indigo-600 text-white rounded-lg font-medium hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition-colors flex items-center gap-2"
      >
        <svg
          v-if="isSubmitting"
          class="animate-spin h-5 w-5 text-white"
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
        <span>{{
          isSubmitting ? 'Saving...' : diary ? 'Update' : 'Create'
        }}</span>
      </button>
    </div>
  </form>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue';
import type { DiaryEntry } from '@/types';

interface Props {
  diary?: DiaryEntry;
  isSubmitting?: boolean;
}

const props = withDefaults(defineProps<Props>(), {
  diary: undefined,
  isSubmitting: false,
});

const emit = defineEmits<{
  submit: [content: string];
  cancel: [];
}>();

const MIN_LENGTH = 10;
const MAX_LENGTH = 5000;
const MIN_ROWS = 5;
const MAX_ROWS = 20;

const contentValue = ref(props.diary?.content || '');
const rows = ref(MIN_ROWS);

/**
 * Validate content and return error message
 */
const errorMessage = computed(() => {
  if (contentValue.value.length === 0) {
    return '';
  }
  if (contentValue.value.length < MIN_LENGTH) {
    return `Content must be at least ${MIN_LENGTH} characters`;
  }
  if (contentValue.value.length > MAX_LENGTH) {
    return `Content must not exceed ${MAX_LENGTH} characters`;
  }
  return '';
});

/**
 * Check if form is valid
 */
const isValid = computed(() => {
  return (
    contentValue.value.length >= MIN_LENGTH &&
    contentValue.value.length <= MAX_LENGTH
  );
});

/**
 * Handle textarea input and auto-resize
 */
const handleInput = (event: Event) => {
  const target = event.target as HTMLTextAreaElement;

  // Auto-resize textarea
  const lineCount = (target.value.match(/\n/g) || []).length + 1;
  rows.value = Math.min(Math.max(lineCount, MIN_ROWS), MAX_ROWS);
};

/**
 * Handle form submission
 */
const handleSubmit = () => {
  if (isValid.value && !props.isSubmitting) {
    emit('submit', contentValue.value);
  }
};

/**
 * Watch for diary prop changes (edit mode)
 */
watch(
  () => props.diary?.content,
  (newContent) => {
    if (newContent !== undefined) {
      contentValue.value = newContent;
    }
  }
);
</script>
