<template>
  <form class="space-y-4" @submit.prevent="handleSubmit">
    <!-- Textarea for Content -->
    <div>
      <label for="content" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
        {{ $t('diary.contentLabel') }}
      </label>
      <textarea
        id="content"
        v-model="contentValue"
        :class="[
          'w-full px-4 py-3 rounded-lg border focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-colors resize-none bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 placeholder-gray-400 dark:placeholder-gray-500',
          errorMessage
            ? 'border-red-500 focus:ring-red-500'
            : 'border-gray-300 dark:border-gray-600',
        ]"
        :rows="rows"
        :placeholder="$t('diary.contentPlaceholder')"
        :disabled="isSubmitting"
        @input="handleInput"
      ></textarea>

      <!-- Character Counter -->
      <div class="flex justify-between items-center mt-2">
        <p v-if="errorMessage" class="text-sm text-red-600 dark:text-red-400" role="alert">
          {{ errorMessage }}
        </p>
        <span v-else class="text-sm text-gray-500 dark:text-gray-400"></span>
        <span
          :class="[
            'text-sm font-medium',
            contentValue.length > MAX_LENGTH
              ? 'text-red-600 dark:text-red-400'
              : contentValue.length > MAX_LENGTH * 0.9
                ? 'text-yellow-600 dark:text-yellow-400'
                : 'text-gray-500 dark:text-gray-400',
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
        class="px-4 py-2 text-gray-700 dark:text-gray-300 bg-gray-100 dark:bg-gray-700 hover:bg-gray-200 dark:hover:bg-gray-600 rounded-lg font-medium transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
        :disabled="isSubmitting"
        @click="$emit('cancel')"
      >
        {{ $t('common.cancel') }}
      </button>
      <button
        type="submit"
        :disabled="!isValid || isSubmitting"
        class="px-6 py-2 bg-indigo-600 text-white rounded-lg font-medium hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 dark:focus:ring-offset-gray-800 disabled:opacity-50 disabled:cursor-not-allowed transition-colors flex items-center gap-2"
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
          isSubmitting ? $t('common.saving') : diary ? $t('common.update') : $t('common.create')
        }}</span>
      </button>
    </div>
  </form>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue';
import { useI18n } from 'vue-i18n';
import type { DiaryEntry } from '@/types';

interface Props {
  diary?: DiaryEntry;
  isSubmitting?: boolean;
}

const props = withDefaults(defineProps<Props>(), {
  diary: undefined,
  isSubmitting: false,
});

const { t } = useI18n();

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
    return t('validation.contentMin', { min: MIN_LENGTH });
  }
  if (contentValue.value.length > MAX_LENGTH) {
    return t('validation.contentMax', { max: MAX_LENGTH });
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
