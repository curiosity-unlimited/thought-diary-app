<script setup lang="ts">
import { onMounted, ref, computed } from 'vue';
import { useRouter } from 'vue-router';
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

const isLoading = ref(true);

// Get recent entries (first 5) from the store
const recentEntries = computed(() => diariesStore.entries.slice(0, 5));

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
      error instanceof Error ? error.message : 'Failed to load dashboard data';
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
      error instanceof Error ? error.message : 'Failed to delete diary entry';
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
        <h1 class="text-3xl font-bold text-gray-900">Dashboard</h1>
        <p class="mt-2 text-sm text-gray-600">
          Your thought diary overview and recent entries
        </p>
      </div>

      <!-- Loading State -->
      <LoadingSpinner
        v-if="isLoading"
        size="lg"
        message="Loading dashboard..."
        class="my-12"
      />

      <!-- Dashboard Content -->
      <div v-else>
        <!-- Statistics Cards -->
        <div class="mb-8">
          <StatsCard :stats="diariesStore.stats" />
        </div>

        <!-- Recent Entries Section -->
        <div class="mb-8">
          <div class="flex items-center justify-between mb-4">
            <h2 class="text-2xl font-semibold text-gray-900">Recent Entries</h2>
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
              Create Entry
            </button>
          </div>

          <!-- Empty State -->
          <EmptyState
            v-if="recentEntries.length === 0"
            title="No diary entries yet"
            message="Start your thought diary journey by creating your first entry."
            action-text="Create Entry"
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
                class="text-indigo-600 hover:text-indigo-800 font-medium inline-flex items-center"
              >
                View All Entries
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
