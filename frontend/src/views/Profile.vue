<script setup lang="ts">
import { computed } from 'vue';
import { useAuthStore } from '@/stores/auth';
import MainLayout from '@/layouts/MainLayout.vue';

const authStore = useAuthStore();

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

// Compute formatted dates
const createdDate = computed(() =>
  authStore.user?.created_at ? formatDate(authStore.user.created_at) : 'N/A'
);

const updatedDate = computed(() =>
  authStore.user?.updated_at ? formatDate(authStore.user.updated_at) : 'N/A'
);
</script>

<template>
  <MainLayout>
    <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <!-- Page Header -->
      <div class="mb-8">
        <h1 class="text-3xl font-bold text-gray-900">Profile</h1>
        <p class="mt-2 text-sm text-gray-600">
          View and manage your account information
        </p>
      </div>

      <!-- Profile Card -->
      <div class="bg-white shadow rounded-lg overflow-hidden">
        <!-- Header -->
        <div class="px-6 py-4 border-b border-gray-200 bg-gray-50">
          <h2 class="text-lg font-semibold text-gray-900">
            Account Information
          </h2>
        </div>

        <!-- Content -->
        <div class="px-6 py-6 space-y-6">
          <!-- Email -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">
              Email Address
            </label>
            <div
              class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md bg-gray-50 text-gray-900"
            >
              {{ authStore.user?.email || 'N/A' }}
            </div>
          </div>

          <!-- Account Created -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">
              Account Created
            </label>
            <div
              class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md bg-gray-50 text-gray-900"
            >
              {{ createdDate }}
            </div>
          </div>

          <!-- Last Updated -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">
              Last Updated
            </label>
            <div
              class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md bg-gray-50 text-gray-900"
            >
              {{ updatedDate }}
            </div>
          </div>
        </div>

        <!-- Footer -->
        <div class="px-6 py-4 bg-gray-50 border-t border-gray-200">
          <div class="flex items-center">
            <svg
              class="h-5 w-5 text-blue-500 mr-2"
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
            <p class="text-sm text-gray-600">
              Additional profile features (password change, account deletion,
              etc.) will be added in future updates.
            </p>
          </div>
        </div>
      </div>
    </div>
  </MainLayout>
</template>
