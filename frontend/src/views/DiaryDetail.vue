<script setup lang="ts">
import { onMounted, ref, computed } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useDiariesStore } from '@/stores/diaries';
import { useToast } from '@/composables/useToast';
import MainLayout from '@/layouts/MainLayout.vue';
import DiaryForm from '@/components/DiaryForm.vue';
import LoadingSpinner from '@/components/LoadingSpinner.vue';
import DeleteConfirmationModal from '@/components/DeleteConfirmationModal.vue';

const route = useRoute();
const router = useRouter();
const diariesStore = useDiariesStore();
const { showError, showSuccess } = useToast();

const isLoading = ref(true);
const isEditing = ref(false);
const isSubmitting = ref(false);
const showDeleteModal = ref(false);

const diaryId = computed(() => parseInt(route.params.id as string));

/**
 * Format date to readable string
 */
const formatDate = (dateString: string) => {
  const date = new Date(dateString);
  return date.toLocaleString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  });
};

/**
 * Load diary entry by ID
 */
const loadDiary = async () => {
  isLoading.value = true;
  try {
    await diariesStore.fetchDiary(diaryId.value);
  } catch (error: unknown) {
    const message = error instanceof Error ? error.message : 'Failed to load diary entry';
    showError(message);
    // Redirect to diaries list if not found
    if (message.includes('404') || message.toLowerCase().includes('not found')) {
      router.push('/diaries');
    }
  } finally {
    isLoading.value = false;
  }
};

/**
 * Toggle edit mode
 */
const toggleEditMode = () => {
  isEditing.value = !isEditing.value;
};

/**
 * Handle edit form submission
 */
const handleEditSubmit = async (content: string) => {
  isSubmitting.value = true;
  try {
    await diariesStore.updateDiary(diaryId.value, content);
    showSuccess('Diary entry updated successfully');
    isEditing.value = false;
    // Reload diary to get updated content
    await loadDiary();
  } catch (error: unknown) {
    const message = error instanceof Error ? error.message : 'Failed to update diary entry';
    showError(message);
  } finally {
    isSubmitting.value = false;
  }
};

/**
 * Handle edit form cancel
 */
const handleEditCancel = () => {
  isEditing.value = false;
};

/**
 * Open delete confirmation modal
 */
const openDeleteModal = () => {
  showDeleteModal.value = true;
};

/**
 * Handle delete confirmation
 */
const handleDeleteConfirm = async () => {
  try {
    await diariesStore.deleteDiary(diaryId.value);
    showSuccess('Diary entry deleted successfully');
    showDeleteModal.value = false;
    router.push('/diaries');
  } catch (error: unknown) {
    const message = error instanceof Error ? error.message : 'Failed to delete diary entry';
    showError(message);
  }
};

/**
 * Handle delete cancel
 */
const handleDeleteCancel = () => {
  showDeleteModal.value = false;
};

/**
 * Navigate back to diaries list
 */
const goBack = () => {
  router.push('/diaries');
};

onMounted(() => {
  loadDiary();
});
</script>

<template>
  <MainLayout>
    <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <!-- Loading State -->
      <LoadingSpinner
        v-if="isLoading"
        size="lg"
        message="Loading diary entry..."
        class="my-12"
      />

      <!-- Diary Content -->
      <div v-else-if="diariesStore.currentDiary">
        <!-- Back Button -->
        <div class="mb-6">
          <button
            class="inline-flex items-center text-sm text-gray-600 hover:text-gray-900"
            @click="goBack"
          >
            <svg
              class="mr-2 h-4 w-4"
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M10 19l-7-7m0 0l7-7m-7 7h18"
              />
            </svg>
            Back to Diaries
          </button>
        </div>

        <!-- View Mode -->
        <div v-if="!isEditing" class="bg-white shadow rounded-lg overflow-hidden">
          <!-- Header -->
          <div class="px-6 py-4 border-b border-gray-200">
            <div class="flex items-start justify-between">
              <div>
                <h1 class="text-2xl font-bold text-gray-900 mb-2">
                  Diary Entry
                </h1>
                <p class="text-sm text-gray-500">
                  {{ formatDate(diariesStore.currentDiary.created_at) }}
                </p>
              </div>
              <div class="flex space-x-2">
                <button
                  class="inline-flex items-center px-3 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
                  @click="toggleEditMode"
                >
                  <svg
                    class="-ml-0.5 mr-2 h-4 w-4"
                    xmlns="http://www.w3.org/2000/svg"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke="currentColor"
                  >
                    <path
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      stroke-width="2"
                      d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"
                    />
                  </svg>
                  Edit
                </button>
                <button
                  class="inline-flex items-center px-3 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-red-600 hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500"
                  @click="openDeleteModal"
                >
                  <svg
                    class="-ml-0.5 mr-2 h-4 w-4"
                    xmlns="http://www.w3.org/2000/svg"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke="currentColor"
                  >
                    <path
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      stroke-width="2"
                      d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"
                    />
                  </svg>
                  Delete
                </button>
              </div>
            </div>
          </div>

          <!-- Content with Sentiment Highlighting -->
          <div class="px-6 py-6">
            <!-- Note: analyzed_content is sanitized by backend AI service -->
            <div
              class="prose max-w-none text-gray-900 leading-relaxed"
              v-html="diariesStore.currentDiary.analyzed_content"
            ></div>
          </div>

          <!-- Footer with Sentiment Counts -->
          <div class="px-6 py-4 bg-gray-50 border-t border-gray-200">
            <div class="flex items-center space-x-6 text-sm">
              <div class="flex items-center">
                <svg
                  class="h-5 w-5 text-green-500 mr-1"
                  xmlns="http://www.w3.org/2000/svg"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M14 10h4.764a2 2 0 011.789 2.894l-3.5 7A2 2 0 0115.263 21h-4.017c-.163 0-.326-.02-.485-.06L7 20m7-10V5a2 2 0 00-2-2h-.095c-.5 0-.905.405-.905.905 0 .714-.211 1.412-.608 2.006L7 11v9m7-10h-2M7 20H5a2 2 0 01-2-2v-6a2 2 0 012-2h2.5"
                  />
                </svg>
                <span class="text-gray-700">
                  <span class="font-medium">{{
                    diariesStore.currentDiary.positive_count
                  }}</span>
                  positive
                </span>
              </div>
              <div class="flex items-center">
                <svg
                  class="h-5 w-5 text-red-500 mr-1"
                  xmlns="http://www.w3.org/2000/svg"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M10 14H5.236a2 2 0 01-1.789-2.894l3.5-7A2 2 0 018.736 3h4.018a2 2 0 01.485.06l3.76.94m-7 10v5a2 2 0 002 2h.096c.5 0 .905-.405.905-.904 0-.715.211-1.413.608-2.008L17 13V4m-7 10h2m5-10h2a2 2 0 012 2v6a2 2 0 01-2 2h-2.5"
                  />
                </svg>
                <span class="text-gray-700">
                  <span class="font-medium">{{
                    diariesStore.currentDiary.negative_count
                  }}</span>
                  negative
                </span>
              </div>
            </div>
          </div>
        </div>

        <!-- Edit Mode -->
        <div v-else class="bg-white shadow rounded-lg p-6">
          <h2 class="text-xl font-semibold text-gray-900 mb-4">Edit Entry</h2>
          <DiaryForm
            :diary="diariesStore.currentDiary"
            :is-submitting="isSubmitting"
            @submit="handleEditSubmit"
            @cancel="handleEditCancel"
          />
        </div>

        <!-- Delete Confirmation Modal -->
        <DeleteConfirmationModal
          v-if="showDeleteModal"
          :is-open="showDeleteModal"
          :diary-id="diaryId"
          :diary-preview="diariesStore.currentDiary.content"
          @confirm="handleDeleteConfirm"
          @cancel="handleDeleteCancel"
        />
      </div>

      <!-- Not Found State -->
      <div v-else class="text-center py-12">
        <p class="text-gray-500 mb-4">Diary entry not found</p>
        <button
          class="text-indigo-600 hover:text-indigo-800 font-medium"
          @click="goBack"
        >
          ← Back to Diaries
        </button>
      </div>
    </div>
  </MainLayout>
</template>

<style scoped>
/* Sentiment highlighting styles */
:deep(.positive) {
  background-color: #10b981;
  color: white;
  padding: 0.125rem 0.25rem;
  border-radius: 0.25rem;
}

:deep(.negative) {
  background-color: #ef4444;
  color: white;
  padding: 0.125rem 0.25rem;
  border-radius: 0.25rem;
}
</style>
