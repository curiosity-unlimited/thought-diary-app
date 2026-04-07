<script setup lang="ts">
import { onMounted, ref, watch } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useI18n } from 'vue-i18n';
import { useDiariesStore } from '@/stores/diaries';
import { useToast } from '@/composables/useToast';
import MainLayout from '@/layouts/MainLayout.vue';
import DiaryCard from '@/components/DiaryCard.vue';
import DiaryForm from '@/components/DiaryForm.vue';
import Pagination from '@/components/Pagination.vue';
import LoadingSpinner from '@/components/LoadingSpinner.vue';
import EmptyState from '@/components/EmptyState.vue';

const route = useRoute();
const router = useRouter();
const diariesStore = useDiariesStore();
const { showError, showSuccess } = useToast();
const { t } = useI18n();

const isLoading = ref(true);
const showCreateForm = ref(false);
const isSubmitting = ref(false);

/**
 * Load diaries for the specified page
 */
const loadDiaries = async (page: number = 1) => {
  isLoading.value = true;
  try {
    await diariesStore.fetchDiaries(page);
  } catch (error: unknown) {
    const message =
      error instanceof Error ? error.message : t('diary.failedToLoad', 'Failed to load diary entries');
    showError(message);
  } finally {
    isLoading.value = false;
  }
};

/**
 * Handle page change from pagination component
 */
const handlePageChange = (page: number) => {
  router.push({ query: { ...route.query, page: page.toString() } });
};

/**
 * Handle create diary form submission
 */
const handleCreateSubmit = async (content: string) => {
  isSubmitting.value = true;
  try {
    await diariesStore.createDiary(content);
    showSuccess(t('success.diaryCreated'));
    showCreateForm.value = false;
    // Reload first page to show new entry
    await loadDiaries(1);
    router.push({ query: {} }); // Clear query params
  } catch (error: unknown) {
    const message =
      error instanceof Error ? error.message : t('diary.failedToCreate', 'Failed to create diary entry');
    showError(message);
  } finally {
    isSubmitting.value = false;
  }
};

/**
 * Handle create form cancel
 */
const handleCreateCancel = () => {
  showCreateForm.value = false;

  const { create: _create, ...queryWithoutCreate } = route.query;
  router.push({ query: queryWithoutCreate });
};

/**
 * Handle edit action from DiaryCard
 */
const handleEdit = (diaryId: number) => {
  router.push(`/diaries/${diaryId}`);
};

/**
 * Handle delete action from DiaryCard
 */
const handleDelete = async (diaryId: number) => {
  try {
    await diariesStore.deleteDiary(diaryId);
    showSuccess(t('success.diaryDeleted'));
    // Reload current page
    const currentPage = parseInt(route.query.page as string) || 1;
    await loadDiaries(currentPage);
  } catch (error: unknown) {
    const message =
      error instanceof Error ? error.message : t('diary.failedToDelete', 'Failed to delete diary entry');
    showError(message);
  }
};

// Watch for page changes in query params
watch(
  () => route.query.page,
  (newPage) => {
    const page = parseInt(newPage as string) || 1;
    loadDiaries(page);
  }
);

// Watch for create query param
watch(
  () => route.query.create,
  (create) => {
    showCreateForm.value = create === 'true';
  },
  { immediate: true }
);

onMounted(() => {
  const page = parseInt(route.query.page as string) || 1;
  loadDiaries(page);
});
</script>

<template>
  <MainLayout>
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <!-- Page Header -->
      <div class="mb-8">
        <div class="flex items-center justify-between">
          <div>
            <h1 class="text-3xl font-bold text-gray-900 dark:text-gray-100">{{ $t('diary.myDiaries') }}</h1>
            <p class="mt-2 text-sm text-gray-600 dark:text-gray-400">
              {{ $t('diary.myDiariesSubtitle') }}
            </p>
          </div>
          <button
            v-if="!showCreateForm"
            class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 transition-colors"
            @click="showCreateForm = true"
          >
            <svg
              class="-ml-1 mr-2 h-5 w-5"
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M12 4v16m8-8H4"
              />
            </svg>
            {{ $t('diary.createNewEntry') }}
          </button>
        </div>
      </div>

      <!-- Create Form -->
      <div v-if="showCreateForm" class="mb-8">
        <div class="bg-white dark:bg-gray-800 shadow rounded-lg p-6">
          <h2 class="text-xl font-semibold text-gray-900 dark:text-gray-100 mb-4">
            {{ $t('diary.createNewEntry') }}
          </h2>
          <DiaryForm
            :is-submitting="isSubmitting"
            @submit="handleCreateSubmit"
            @cancel="handleCreateCancel"
          />
        </div>
      </div>

      <!-- Loading State -->
      <LoadingSpinner
        v-if="isLoading"
        size="lg"
        :message="$t('loading.loadingDiaryEntries')"
        class="my-12"
      />

      <!-- Empty State -->
      <EmptyState
        v-else-if="!diariesStore.entries || diariesStore.entries.length === 0"
        :title="$t('diary.noEntriesFoundTitle')"
        :message="$t('diary.noEntriesMessage')"
        :action-text="$t('diary.createEntry')"
        @action="showCreateForm = true"
      />

      <!-- Diary List -->
      <div v-else>
        <div class="space-y-4 mb-8">
          <DiaryCard
            v-for="diary in diariesStore.entries"
            :key="diary.id"
            :diary="diary"
            @edit="handleEdit(diary.id)"
            @delete="handleDelete(diary.id)"
          />
        </div>

        <!-- Pagination -->
        <div
          v-if="diariesStore.pagination && diariesStore.pagination.pages > 1"
          class="flex justify-center"
        >
          <Pagination
            :pagination="diariesStore.pagination"
            @page-change="handlePageChange"
          />
        </div>
      </div>
    </div>
  </MainLayout>
</template>
