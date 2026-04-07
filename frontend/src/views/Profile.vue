<script setup lang="ts">
import { computed } from 'vue';
import { useI18n } from 'vue-i18n';
import { useAuthStore } from '@/stores/auth';
import MainLayout from '@/layouts/MainLayout.vue';
import { formatDateTime } from '@/utils/dateFormatter';

const authStore = useAuthStore();
const { t } = useI18n();

// Compute formatted dates using locale-aware formatter
const createdDate = computed(() =>
  authStore.user?.created_at ? formatDateTime(authStore.user.created_at) : t('common.na')
);

const updatedDate = computed(() =>
  authStore.user?.updated_at ? formatDateTime(authStore.user.updated_at) : t('common.na')
);
</script>

<template>
  <MainLayout>
    <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <!-- Page Header -->
      <div class="mb-8">
        <h1 class="text-3xl font-bold text-gray-900 dark:text-gray-100">{{ $t('profile.title') }}</h1>
        <p class="mt-2 text-sm text-gray-600 dark:text-gray-400">
          {{ $t('profile.subtitle') }}
        </p>
      </div>

      <!-- Profile Card -->
      <div class="bg-white dark:bg-gray-800 shadow rounded-lg overflow-hidden">
        <!-- Header -->
        <div class="px-6 py-4 border-b border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-700">
          <h2 class="text-lg font-semibold text-gray-900 dark:text-gray-100">
            {{ $t('profile.accountInfo') }}
          </h2>
        </div>

        <!-- Content -->
        <div class="px-6 py-6 space-y-6">
          <!-- Email -->
          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
              {{ $t('profile.emailAddress') }}
            </label>
            <div
              class="mt-1 block w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md bg-gray-50 dark:bg-gray-700 text-gray-900 dark:text-gray-100"
            >
              {{ authStore.user?.email || $t('common.na') }}
            </div>
          </div>

          <!-- Account Created -->
          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
              {{ $t('profile.accountCreated') }}
            </label>
            <div
              class="mt-1 block w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md bg-gray-50 dark:bg-gray-700 text-gray-900 dark:text-gray-100"
            >
              {{ createdDate }}
            </div>
          </div>

          <!-- Last Updated -->
          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
              {{ $t('profile.lastUpdated') }}
            </label>
            <div
              class="mt-1 block w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md bg-gray-50 dark:bg-gray-700 text-gray-900 dark:text-gray-100"
            >
              {{ updatedDate }}
            </div>
          </div>
        </div>

        <!-- Footer -->
        <div class="px-6 py-4 bg-gray-50 dark:bg-gray-700 border-t border-gray-200 dark:border-gray-600">
          <div class="flex items-center">
            <svg
              class="h-5 w-5 text-blue-500 dark:text-blue-400 mr-2"
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
              />
            </svg>
            <p class="text-sm text-gray-600 dark:text-gray-400">
              {{ $t('profile.futureFeatures') }}
            </p>
          </div>
        </div>
      </div>
    </div>
  </MainLayout>
</template>
