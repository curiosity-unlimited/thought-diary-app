<script setup lang="ts">
import { useRoute } from 'vue-router';

// Diary detail page - Protected route (will be implemented in Step 9)
const route = useRoute();
const diaryId = route.params.id;
</script>

<template>
  <div class="min-h-screen bg-gray-50">
    <div class="max-w-4xl mx-auto px-4 py-8">
      <h1 class="text-3xl font-bold text-gray-900 mb-6">
        Diary Entry #{{ diaryId }}
      </h1>
      <p class="text-gray-600">
        Diary detail view will be implemented in Step 9
      </p>
      <div class="mt-6">
        <router-link to="/diaries" class="text-blue-600 hover:text-blue-800">
          ← Back to Diaries
        </router-link>
      </div>
    </div>
  </div>
</template>
