<script setup lang="ts">
import { onMounted, ref, computed } from 'vue';
import { useRouter } from 'vue-router';
import { useI18n } from 'vue-i18n';
import { useDiariesStore } from '@/stores/diaries';
import { useToast } from '@/composables/useToast';
import MainLayout from '@/layouts/MainLayout.vue';
import StatsCard from '@/components/StatsCard.vue';
import DiaryCard from '@/components/DiaryCard.vue';
import LoadingSpinner from '@/components/LoadingSpinner.vue';
import EmptyState from '@/components/EmptyState.vue';

const router = useRouter();
const diariesStore = useDiariesStore();
const { showError } = useToast();
const { t } = useI18n();

const isLoading = ref(true);

// Get recent entries (first 5) from the store
const recentEntries = computed(() => (diariesStore.entries || []).slice(0, 5));

/**
 * Load dashboard data on component mount
 * Fetches statistics and recent diary entries
 */
const loadDashboardData = async () => {
  isLoading.value = true;
  try {
    // Load stats and recent entries in parallel
    await Promise.all([
      diariesStore.fetchStats(),
      diariesStore.fetchDiaries(1, 5), // First page, 5 items
    ]);
  } catch (error: unknown) {
    const message =
      error instanceof Error ? error.message : t('diary.failedToLoadDashboard', 'Failed to load dashboard data');
    showError(message);
  } finally {
    isLoading.value = false;
  }
};

/**
 * Navigate to create diary page
 */
const createEntry = () => {
  router.push('/diaries?create=true');
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
    // Reload dashboard data after deletion
    await loadDashboardData();
  } catch (error: unknown) {
    const message =
      error instanceof Error ? error.message : t('diary.failedToDelete', 'Failed to delete diary entry');
    showError(message);
  }
};

onMounted(() => {
  loadDashboardData();
});
</script>

<template>
  <MainLayout>
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <!-- Page Header -->
      <div class="mb-8">
        <h1 class="text-3xl font-bold text-gray-900 dark:text-gray-100">{{ $t('diary.dashboard') }}</h1>
        <p class="mt-2 text-sm text-gray-600 dark:text-gray-400">
          {{ $t('diary.dashboardSubtitle') }}
        </p>
      </div>

      <!-- Loading State -->
      <LoadingSpinner
        v-if="isLoading"
        size="lg"
        :message="$t('loading.loadingDashboard')"
        class="my-12"
      />

      <!-- Dashboard Content -->
      <div v-else>
        <!-- Statistics Cards -->
        <div v-if="diariesStore.stats" class="mb-8">
          <StatsCard :stats="diariesStore.stats" />
        </div>

        <!-- Recent Entries Section -->
        <div class="mb-8">
          <div class="flex items-center justify-between mb-4">
            <h2 class="text-2xl font-semibold text-gray-900 dark:text-gray-100">{{ $t('diary.recentEntries') }}</h2>
            <button
              class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 transition-colors"
              @click="createEntry"
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
              {{ $t('diary.createEntry') }}
            </button>
          </div>

          <!-- Empty State -->
          <EmptyState
            v-if="recentEntries.length === 0"
            :title="$t('diary.noEntriesTitle')"
            :message="$t('diary.noEntriesMessage')"
            :action-text="$t('diary.createEntry')"
            @action="createEntry"
          />

          <!-- Recent Diary Cards -->
          <div v-else class="space-y-4">
            <DiaryCard
              v-for="diary in recentEntries"
              :key="diary.id"
              :diary="diary"
              @edit="handleEdit(diary.id)"
              @delete="handleDelete(diary.id)"
            />

            <!-- View All Link -->
            <div class="text-center pt-4">
              <router-link
                to="/diaries"
                class="text-indigo-600 dark:text-indigo-400 hover:text-indigo-800 dark:hover:text-indigo-300 font-medium inline-flex items-center"
              >
                {{ $t('diary.viewAllEntries') }}
                <svg
                  class="ml-1 h-5 w-5"
                  xmlns="http://www.w3.org/2000/svg"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M9 5l7 7-7 7"
                  />
                </svg>
              </router-link>
            </div>
          </div>
        </div>
      </div>
    </div>
  </MainLayout>
</template>
